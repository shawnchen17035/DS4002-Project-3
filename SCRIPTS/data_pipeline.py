"""DS4002 Project 3 | Shawn Chen and Zichen Luo, The Pink Panthers.

Prepare a reproducible review queue, validate selected DVM-CAR image files,
and export only human-approved matched triplets with model-disjoint splits.
Use from 01_data_cleaning.ipynb. No model fitting or inferred review approvals.
"""
from pathlib import Path
from collections import Counter
from io import BytesIO
import hashlib
import json
import platform
import shutil
import zipfile
import importlib.metadata

import numpy as np
import pandas as pd
from PIL import Image, ImageOps
import matplotlib.pyplot as plt

CLASSES = ('Sedan', 'SUV', 'Pickup')
VIEWS = ('Front', 'Side', 'Rear')
CLASS_IDS = {name: i for i, name in enumerate(CLASSES)}
ANGLE_MAP = {0: 'Front', 90: 'Side', 270: 'Side', 180: 'Rear'}
REVIEW_COLUMNS = ['Image_ID', 'Decision', 'Reason', 'Reviewer', 'Reviewed_at']


def save_json(value, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2, default=str) + '\n')


def read_table(path, required):
    """Keep IDs as strings; strip source whitespace without imputing labels."""
    df = pd.read_csv(path, dtype='string')
    df.columns = df.columns.str.strip()
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f'{path}: missing columns {sorted(missing)}')
    for col in df.columns:
        df[col] = df[col].str.strip().replace('', pd.NA)
    return df


def prepare(ad_path, image_path, work, max_listings_per_model=10,
            alternatives_per_view=3, seed=4002, audit_path=None):
    """Clean metadata and select deterministic listings for a feasible visual audit.

    max_listings_per_model=0 selects every eligible listing. This is a workload
    parameter, not a learned threshold. Multiple body styles in one generic model
    are sampled separately, then kept in the same split during finalization.
    """
    work = Path(work)
    (work / 'DATA').mkdir(parents=True, exist_ok=True)
    (work / 'OUTPUT').mkdir(exist_ok=True)
    ads = read_table(ad_path, ['Adv_ID', 'Genmodel_ID', 'Bodytype'])
    images = read_table(image_path, ['Genmodel_ID', 'Image_ID', 'Image_name',
                                     'Predicted_viewpoint', 'Quality_check'])
    stages = []
    def log(stage, n, unit):
        stages.append({'Stage': stage, 'Count': int(n), 'Unit': unit})
    log('Raw advertisement rows', len(ads), 'rows')
    log('Raw image rows', len(images), 'rows')
    # Save missingness before excluding records; downstream analyses use labels only.
    for name, df in [('ad', ads), ('image', images)]:
        pd.DataFrame({'Feature': df.columns, 'Missing_count': df.isna().sum().values,
                      'Missing_percent': df.isna().mean().mul(100).values}).to_csv(
            work / 'OUTPUT' / f'{name}_missing_values.csv', index=False)
    ads = ads.drop_duplicates().dropna(subset=['Adv_ID', 'Genmodel_ID', 'Bodytype'])
    images = images.drop_duplicates().dropna(subset=['Genmodel_ID','Image_ID','Image_name'])
    # Remaining repeated identifiers are ambiguous, so exclude all their records.
    bad_ads = ads.Adv_ID.duplicated(keep=False)
    log('Ambiguous advertisement rows excluded', bad_ads.sum(), 'rows')
    ads = ads.loc[~bad_ads].copy()
    bad_images = images.Image_ID.duplicated(keep=False) | images.Image_name.duplicated(keep=False)
    log('Ambiguous image rows excluded', bad_images.sum(), 'rows')
    images = images.loc[~bad_images].copy()
    # Format checks prevent a malformed filename/ID from silently joining a listing.
    valid_id = images.Image_ID.str.fullmatch(r'\d+_\d+\$\$\d+\$\$\d+', na=False)
    images = images.loc[valid_id].copy()
    parts = images.Image_name.str.split('$$', regex=False)
    images = images.loc[parts.str.len().eq(7)].copy()
    parts = images.Image_name.str.split('$$', regex=False)
    images['Adv_ID'] = images.Image_ID.str.rsplit('$$', n=1).str[0]
    expected_ad = parts.str[4] + '$$' + parts.str[5]
    expected_index = parts.str[6].str.extract(r'^image_(\d+)\.jpg$', expand=False)
    valid_file = (expected_ad.eq(images.Adv_ID) & parts.str[4].eq(images.Genmodel_ID)
                  & expected_index.eq(images.Image_ID.str.rsplit('$$', n=1).str[-1])
                  & ~images.Image_name.str.contains(r'[/\\]', regex=True, na=True))
    log('Filename/ID mismatches excluded', (~valid_file.fillna(False)).sum(), 'rows')
    images = images.loc[valid_file.fillna(False)].copy()
    images['Predicted_viewpoint'] = pd.to_numeric(images.Predicted_viewpoint, errors='coerce')
    images['View'] = images.Predicted_viewpoint.map(ANGLE_MAP)
    # P=source pass; N=source failure; unassessed values stay subject to our review.
    images = images.loc[images.View.notna() & ~images.Quality_check.str.upper().eq('N').fillna(False)].copy()
    ads['Body_type'] = ads.Bodytype.str.casefold().map({'saloon': 'Sedan', 'suv': 'SUV', 'pickup': 'Pickup'})
    ads = ads.loc[ads.Body_type.notna()].copy()
    cols = ['Adv_ID', 'Genmodel_ID', 'Bodytype', 'Body_type']
    cols += [c for c in ['Maker', 'Genmodel', 'Color', 'Reg_year'] if c in ads]
    merged = images.merge(ads[cols], on=['Adv_ID','Genmodel_ID'], how='inner', validate='many_to_one')
    merged['Relative_path'] = merged.Image_name.map(lambda n: '/'.join(n.split('$$')[:4] + [n]))
    # Coverage counts describe candidates, never visual approvals.
    for metric, key in [('listing', 'Adv_ID'), ('model', 'Genmodel_ID')]:
        tab = merged.groupby(['Body_type','View'])[key].nunique().unstack(fill_value=0)
        tab.reindex(index=CLASSES, columns=VIEWS, fill_value=0).to_csv(work/'OUTPUT'/f'{metric}_counts_by_view.csv')
    covered = merged.groupby('Adv_ID').View.nunique()
    candidates = merged.loc[merged.Adv_ID.isin(covered[covered.eq(3)].index)].copy()
    listing_cols = [c for c in cols if c in candidates]
    listings = candidates[listing_cols].drop_duplicates('Adv_ID').sort_values('Adv_ID')
    summary = listings.groupby('Body_type').agg(Listings=('Adv_ID','nunique'), Models=('Genmodel_ID','nunique')).reindex(CLASSES, fill_value=0)
    summary.to_csv(work/'OUTPUT'/'candidate_matched_summary.csv')
    candidates.to_csv(work/'DATA'/'candidate_images.csv', index=False)
    log('Eligible matched listings before visual cleaning', len(listings), 'listings')
    # Hash ranks make queue selection reproducible across input row ordering.
    rank = lambda s: hashlib.sha256(f'{seed}:{s}'.encode()).hexdigest()
    listings['Selection_rank'] = listings.Adv_ID.map(rank)
    listings = listings.sort_values(['Body_type','Genmodel_ID','Selection_rank'])
    chosen = listings if max_listings_per_model == 0 else listings.groupby(
        ['Body_type','Genmodel_ID'], sort=False).head(max_listings_per_model)
    selected_ids = set(chosen.Adv_ID)
    # Include earlier audit listings when they remain eligible; no prior approvals inferred.
    if audit_path and Path(audit_path).exists():
        audit = read_table(audit_path, ['Adv_ID'])
        selected_ids |= set(audit.Adv_ID.dropna()) & set(listings.Adv_ID)
    pool = candidates.loc[candidates.Adv_ID.isin(selected_ids)].copy()
    # Prioritize source-passed images, then original numeric image index.
    pool['Source_priority'] = (~pool.Quality_check.str.upper().eq('P').fillna(False)).astype(int)
    pool['Image_index'] = pool.Image_ID.str.rsplit('$$', n=1).str[-1].astype(int)
    queue = pool.sort_values(['Body_type','Genmodel_ID','Adv_ID','View','Source_priority','Image_index','Image_ID'])
    queue = queue.groupby(['Adv_ID','View'], sort=False).head(alternatives_per_view).copy()
    queue['Alternative_rank'] = queue.groupby(['Adv_ID','View']).cumcount() + 1
    queue.drop(columns=['Source_priority','Image_index']).to_csv(work/'DATA'/'review_queue.csv', index=False)
    pd.DataFrame(stages).to_csv(work/'OUTPUT'/'metadata_cleaning_counts.csv', index=False)
    config = dict(seed=seed, max_listings_per_model=max_listings_per_model,
                  alternatives_per_view=alternatives_per_view,
                  ad_file=str(ad_path), image_file=str(image_path),
                  selected_listings=len(selected_ids), candidate_listings=len(listings),
                  audit_file=str(audit_path) if audit_path and Path(audit_path).exists() else None,
                  source_sha256={str(Path(f).name): hashlib.sha256(Path(f).read_bytes()).hexdigest()
                                 for f in [ad_path,image_path]})
    save_json(config, work/'OUTPUT'/'preparation_config.json')
    versions = {'python': platform.python_version(), 'platform': platform.platform()}
    for p in ['pandas','numpy','Pillow','matplotlib','ipywidgets']:
        try: versions[p] = importlib.metadata.version(p)
        except importlib.metadata.PackageNotFoundError: versions[p] = 'not installed'
    save_json(versions, work/'OUTPUT'/'cleaning_environment.json')
    write_candidate_plots(work)
    return queue.drop(columns=['Source_priority','Image_index']), summary


def extract_queue(queue, archive_path, work):
    """Extract just queued files, checking readability and hashing decoded pixels.

    Accepts the full source ZIP or a previously reduced ZIP. Duplicate basenames
    in the archive are ambiguous and rejected. Never extract arbitrary ZIP paths.
    """
    work = Path(work)
    image_dir = work/'review_images'
    image_dir.mkdir(parents=True, exist_ok=True)
    wanted = set(queue.Image_name)
    records = []
    with zipfile.ZipFile(archive_path) as z:
        lookup = {}
        for info in z.infolist():
            name = info.filename.rsplit('/', 1)[-1]
            if name in wanted and not info.is_dir():
                lookup.setdefault(name, []).append(info)
        for row in queue.itertuples(index=False):
            record = {'Image_ID': row.Image_ID, 'Technical_ok': False,
                      'Technical_reason': '', 'Pixel_sha256': '', 'Width': 0, 'Height': 0}
            matches = lookup.get(row.Image_name, [])
            if len(matches) != 1:
                record['Technical_reason'] = 'missing_file' if not matches else 'ambiguous_archive_filename'
            else:
                try:
                    raw = z.read(matches[0])
                    with Image.open(BytesIO(raw)) as im:
                        im.load()
                        im = ImageOps.exif_transpose(im).convert('RGB')
                        record.update(Width=im.width, Height=im.height)
                        record['Pixel_sha256'] = hashlib.sha256(
                            f'{im.size}'.encode() + im.tobytes()).hexdigest()
                        record['Technical_ok'] = im.size == (300, 300)
                        if not record['Technical_ok']: record['Technical_reason'] = 'unexpected_dimensions'
                    if record['Technical_ok']: (image_dir/row.Image_name).write_bytes(raw)
                except Exception as exc:
                    record['Technical_reason'] = f'unreadable:{type(exc).__name__}'
            records.append(record)
    tech = pd.DataFrame(records)
    tech.to_csv(work/'DATA'/'technical_checks.csv', index=False)
    return tech


def load_reviews(work):
    path = Path(work)/'DATA'/'review_decisions.csv'
    return pd.read_csv(path, dtype=str).fillna('') if path.exists() else pd.DataFrame(columns=REVIEW_COLUMNS)


def review_ui(queue, work, reviewer='Shawn Chen'):
    """Display one listing and its alternatives. Every save checkpoints to disk.

    Accept only a complete exterior, correct category, correct cardinal view,
    closed hood/trunk, and the same actual vehicle across the three views.
    Angled, partial, wrong-identity, or uncertain images must be rejected.
    """
    import ipywidgets as w
    from IPython.display import display, clear_output
    from datetime import datetime, timezone
    work = Path(work)
    tech = pd.read_csv(work/'DATA'/'technical_checks.csv', dtype={'Image_ID': str})
    good_ids = set(tech.loc[tech.Technical_ok.astype(str).str.lower().eq('true'), 'Image_ID'])
    q = queue.loc[queue.Image_ID.isin(good_ids)].copy()
    listing_ids = sorted(q.Adv_ID.unique())
    if not listing_ids: raise ValueError('No readable queued images found.')
    reviews = load_reviews(work)
    recorded = set(reviews.Image_ID)
    pending = [a for a in listing_ids if not set(q.loc[q.Adv_ID.eq(a), 'Image_ID']).issubset(recorded)]
    state = {'i': listing_ids.index(pending[0]) if pending else 0}
    output, status = w.Output(), w.HTML()
    prev, save, nxt = w.Button(description='Previous'), w.Button(description='Save decisions', button_style='success'), w.Button(description='Next')
    jump = w.Text(description='Listing ID', placeholder='e.g. 7_11$$1708')
    controls = {}
    def render():
        nonlocal controls
        controls = {}
        with output:
            clear_output(wait=True)
            adv = listing_ids[state['i']]
            rows = q.loc[q.Adv_ID.eq(adv)]
            saved = load_reviews(work).set_index('Image_ID')
            first = rows.iloc[0]
            maker = first.get('Maker', '')
            model = first.get('Genmodel', '')
            display(w.HTML(f'<h3>{state["i"]+1}/{len(listing_ids)} — {first.Body_type}: {maker} {model} — {adv}</h3><p>Approve exactly one image per view, checking that all three show the same vehicle. Reject unsuitable alternatives; leave uncertainty pending.</p>'))
            columns = []
            for view in VIEWS:
                cards = [w.HTML(f'<b>{view}</b>')]
                for row in rows.loc[rows.View.eq(view)].itertuples(index=False):
                    dropdown = w.Dropdown(options=[('Pending','pending'),('Accept','accept'),('Reject','reject')], layout=w.Layout(width='220px'))
                    note = w.Text(placeholder='Reason (required for rejection)', layout=w.Layout(width='260px'))
                    if row.Image_ID in saved.index:
                        dropdown.value = saved.loc[row.Image_ID,'Decision']
                        note.value = saved.loc[row.Image_ID,'Reason']
                    controls[row.Image_ID] = (dropdown, note)
                    cards += [w.Image(value=(work/'review_images'/row.Image_name).read_bytes(),format='jpg',width=260), w.HTML(row.Image_ID), dropdown, note]
                if len(cards)==1: cards.append(w.HTML('No readable alternative. Listing cannot qualify.'))
                columns.append(w.VBox(cards))
            display(w.HBox(columns))
    def save_current(_):
        existing = load_reviews(work)
        updates = []
        for image_id, (decision, reason) in controls.items():
            if decision.value == 'reject' and not reason.value.strip():
                status.value = 'Add a reason for every rejection before saving.'; return
            if decision.value != 'pending':
                updates.append(dict(Image_ID=image_id, Decision=decision.value,
                                    Reason=reason.value.strip(), Reviewer=reviewer,
                                    Reviewed_at=datetime.now(timezone.utc).isoformat()))
        # More than one accepted photo for a view is usually an accidental click.
        accepted = {r['Image_ID'] for r in updates if r['Decision']=='accept'}
        counts = queue.loc[queue.Image_ID.isin(accepted)].groupby('View').size()
        if (counts > 1).any():
            status.value = 'Accept only one image per view.'; return
        existing = existing.loc[~existing.Image_ID.isin(controls)]
        result = pd.concat([existing,pd.DataFrame(updates,columns=REVIEW_COLUMNS)],ignore_index=True)
        path = work/'DATA'/'review_decisions.csv'
        temp = path.with_suffix('.tmp')
        result.to_csv(temp,index=False); temp.replace(path)
        status.value = f'Saved {len(updates)} decisions. Use Next to continue.'
    def navigate(delta):
        def go(_):
            state['i'] = max(0,min(len(listing_ids)-1,state['i']+delta)); render()
            status.value = 'Navigation does not save. Save decisions before leaving a listing.'
        return go
    def do_jump(change):
        target = change['new'].strip()
        if target in listing_ids: state['i'] = listing_ids.index(target); render()
    prev.on_click(navigate(-1)); nxt.on_click(navigate(1)); save.on_click(save_current)
    jump.observe(do_jump,names='value')
    display(w.VBox([w.HBox([prev,save,nxt]),jump,status,output])); render()


def assign_splits(manifest, seed=4002):
    """Assign complete generic models, approximately 70/15/15 by model count.

    Multi-body models receive one shared split. Primary body stratum is the
    most common retained listing body type (alphabetical tie breaking).
    """
    listings = manifest.drop_duplicates('Adv_ID')
    counts = listings.groupby(['Genmodel_ID','Body_type']).size().rename('N').reset_index()
    primary = counts.sort_values(['Genmodel_ID','N','Body_type'], ascending=[True,False,True]).drop_duplicates('Genmodel_ID')
    assignments = []
    for body, group in primary.groupby('Body_type', sort=True):
        models = sorted(group.Genmodel_ID, key=lambda m: hashlib.sha256(f'{seed}:{m}'.encode()).hexdigest())
        n = len(models)
        if n < 3: raise ValueError(f'{body}: only {n} model groups after cleaning; need >=3 for all splits. Review additional models.')
        nval, ntest = max(1,round(.15*n)), max(1,round(.15*n))
        ntrain = n-nval-ntest
        for i, model in enumerate(models):
            split = 'train' if i<ntrain else ('validation' if i<ntrain+nval else 'test')
            assignments.append({'Genmodel_ID':model,'Split':split,'Primary_body_stratum':body})
    result = manifest.merge(pd.DataFrame(assignments),on='Genmodel_ID',validate='many_to_one')
    if result.groupby('Genmodel_ID').Split.nunique().max() != 1: raise AssertionError('Model leakage')
    for split in ['train','validation','test']:
        if set(result.loc[result.Split.eq(split),'Body_type']) != set(CLASSES):
            raise ValueError(f'{split} lacks a class. Review more generic models before training.')
    return result, pd.DataFrame(assignments)


def finalize(work, seed=4002):
    """Export human-approved triplets. Stop on pending review or class loss.

    Whole listings with duplicate decoded pixels in any other listing or across
    their own views are excluded conservatively, before model splitting.
    """
    work = Path(work)
    queue = pd.read_csv(work/'DATA'/'review_queue.csv',dtype=str).fillna('')
    tech = pd.read_csv(work/'DATA'/'technical_checks.csv',dtype=str).fillna('')
    decisions = load_reviews(work)
    if decisions.Image_ID.duplicated().any(): raise ValueError('Repeated review decisions; resolve them first.')
    if not set(decisions.Decision).issubset({'accept','reject'}): raise ValueError('Invalid review decision.')
    rows = queue.merge(tech,on='Image_ID',validate='one_to_one').merge(decisions,on='Image_ID',how='left',validate='one_to_one')
    good = rows.Technical_ok.str.lower().eq('true')
    pending = rows.loc[good & rows.Decision.isna()]
    if len(pending):
        pending.to_csv(work/'DATA'/'pending_reviews.csv',index=False)
        raise ValueError(f'{len(pending)} readable images still need decisions. Finish the review queue before exporting.')
    accepted = rows.loc[good & rows.Decision.eq('accept')].copy()
    perview = accepted.groupby(['Adv_ID','View']).size()
    if (perview>1).any(): raise ValueError('Accept exactly one alternative per listing/view.')
    complete_ids = accepted.groupby('Adv_ID').View.nunique()
    complete_ids = set(complete_ids[complete_ids.eq(3)].index)
    triplets = accepted.loc[accepted.Adv_ID.isin(complete_ids)].copy()
    # Detect duplicates among all accepted photos, including incomplete listings.
    duplicates = accepted.Pixel_sha256.duplicated(keep=False)
    duplicate_ids = set(accepted.loc[duplicates,'Adv_ID'])
    triplets = triplets.loc[~triplets.Adv_ID.isin(duplicate_ids)].copy()
    excluded = queue[['Adv_ID','Body_type','Genmodel_ID']].drop_duplicates('Adv_ID')
    excluded['Reason'] = excluded.Adv_ID.map(lambda a: 'duplicate_pixels' if a in duplicate_ids else 'no_approved_triplet')
    excluded = excluded.loc[~excluded.Adv_ID.isin(triplets.Adv_ID)]
    excluded.to_csv(work/'DATA'/'excluded_listings.csv',index=False)
    if triplets.empty: raise ValueError('No approved unique triplets remain.')
    manifest, assignments = assign_splits(triplets,seed)
    manifest['Class_id'] = manifest.Body_type.map(CLASS_IDS)
    manifest['Path'] = 'images/' + manifest.Image_name
    columns = ['Adv_ID','Genmodel_ID','Body_type','Class_id','View','Image_ID','Image_name',
               'Predicted_viewpoint','Quality_check','Relative_path','Path','Pixel_sha256',
               'Width','Height','Reviewer','Reviewed_at','Split']
    manifest = manifest[columns].sort_values(['Split','Body_type','Genmodel_ID','Adv_ID','View'])
    assert manifest.groupby('Adv_ID').size().eq(3).all()
    assert manifest.groupby('Adv_ID').Split.nunique().eq(1).all()
    assert manifest.groupby('Pixel_sha256').Split.nunique().eq(1).all()
    processed = work/'DATA'/'processed'; processed.mkdir(exist_ok=True)
    manifest.to_csv(processed/'clean_manifest.csv',index=False)
    assignments.to_csv(processed/'model_split_assignments.csv',index=False)
    for split in ['train','validation','test']:
        manifest.loc[manifest.Split.eq(split)].to_csv(processed/f'{split}_manifest.csv',index=False)
    summary = manifest.groupby(['Split','Body_type']).agg(Images=('Image_ID','size'),Listings=('Adv_ID','nunique'),Models=('Genmodel_ID','nunique'))
    summary.to_csv(work/'OUTPUT'/'clean_split_summary.csv')
    save_json({'seed':seed,'class_to_id':CLASS_IDS,'split_unit':'Genmodel_ID',
               'target_model_proportions':{'train':.7,'validation':.15,'test':.15},
               'images':len(manifest),'listings':manifest.Adv_ID.nunique(),
               'models':manifest.Genmodel_ID.nunique(),
               'duplicate_policy':'exclude all affected listings; exact decoded RGB pixels',
               'remaining_limitations':['near duplicates not automatically detected','source body labels and generic model groups may be imperfect','small held-out pickup model count']},work/'OUTPUT'/'handoff_summary.json')
    # Ship only selected photos. Zichen can train without downloading the full ZIP.
    bundle = work/'zichen_training_data.zip'
    with zipfile.ZipFile(bundle,'w',compression=zipfile.ZIP_STORED) as z:
        for f in sorted(processed.glob('*.csv')): z.write(f,'DATA/'+f.name)
        for row in manifest.itertuples(index=False):
            z.write(work/'review_images'/row.Image_name,row.Path)
        for f in ['review_decisions.csv','excluded_listings.csv','technical_checks.csv']:
            z.write(work/'DATA'/f,'AUDIT/'+f)
        z.write(work/'OUTPUT'/'handoff_summary.json','OUTPUT/handoff_summary.json')
        z.write(work/'OUTPUT'/'clean_split_summary.csv','OUTPUT/clean_split_summary.csv')
        z.writestr('DATA_LICENSE.txt','DVM-CAR by J. Huang, B. Chen, L. Luo, S. Yue, I. Ounis. https://deepvisualmarketing.github.io\nCC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/\nChanges: selected, visually reviewed, filtered and grouped into model-disjoint splits.\n')
    return manifest, summary, bundle


def write_candidate_plots(work):
    """Plot metadata candidates before image/visual checks; preserve MI2 separately."""
    out = Path(work)/'OUTPUT'
    table = pd.read_csv(out/'listing_counts_by_view.csv',index_col=0).reindex(CLASSES)
    ax = table[list(VIEWS)].plot.bar(figsize=(8,4),rot=0,color=['#517caa','#db8c53','#6f9e73'])
    ax.set(xlabel='Body type',ylabel='Candidate listings',title='Metadata coverage after source-failure filtering')
    ax.figure.tight_layout();ax.figure.savefig(out/'candidate_viewpoint_coverage.png',dpi=180);plt.close(ax.figure)
    summary = pd.read_csv(out/'candidate_matched_summary.csv',index_col=0).reindex(CLASSES)
    ax = summary.Models.plot.bar(figsize=(6,4),rot=0,color=['#517caa','#db8c53','#6f9e73'])
    ax.set(xlabel='Body type',ylabel='Generic models',title='Models with three-view metadata candidates')
    for i,v in enumerate(summary.Models): ax.text(i,v,str(v),ha='center',va='bottom')
    ax.set_ylim(0,max(summary.Models)*1.15)
    ax.figure.tight_layout();ax.figure.savefig(out/'candidate_matched_model_coverage.png',dpi=180);plt.close(ax.figure)
