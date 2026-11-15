"""Synthetic checks for the cleaning contract, without real image downloads.
Run: python -m unittest discover -s SCRIPTS/tests -v
"""
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import pandas as pd
from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1]/'data_pipeline.py'
spec = importlib.util.spec_from_file_location('pipeline', SCRIPT)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class CleaningContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        ads, images = [], []
        archive = self.root/'images.zip'
        # Four model groups in each class, one listing per model, three unique views.
        with zipfile.ZipFile(archive,'w') as z:
            for c, body in enumerate(['Saloon','SUV','Pickup']):
                for model in range(4):
                    gid = f'{c+1}_{model+1}'; adv = f'{gid}$$1'
                    ads.append(dict(Adv_ID=adv,Genmodel_ID=gid,Bodytype=body))
                    for i, angle in enumerate([0,90,180]):
                        name=f'Brand$$Model$$2020$$Red$${gid}$$1$$image_{i}.jpg'
                        images.append(dict(Genmodel_ID=gid,Image_ID=f'{adv}$${i}',Image_name=name,Predicted_viewpoint=angle,Quality_check='P'))
                        file=self.root/'photo.jpg'
                        Image.new('RGB',(300,300),(c*70+20,model*50+10,i*70+20)).save(file,quality=100,subsampling=0)
                        z.write(file,'nested/'+name)
            # A source-rejected image and a non-cardinal angle cannot enter queue.
        pd.DataFrame(ads).to_csv(self.root/'ad.csv',index=False)
        pd.DataFrame(images).to_csv(self.root/'image.csv',index=False)
        self.work=self.root/'work'
        self.queue,_=p.prepare(self.root/'ad.csv',self.root/'image.csv',self.work,max_listings_per_model=0)
        self.tech=p.extract_queue(self.queue,archive,self.work)

    def tearDown(self): self.temp.cleanup()

    def approve(self):
        pd.DataFrame([dict(Image_ID=i,Decision='accept',Reason='',Reviewer='Unit test',Reviewed_at='2026-11-14T00:00:00Z') for i in self.queue.Image_ID]).to_csv(self.work/'DATA/review_decisions.csv',index=False)

    def test_pending_review_blocks_export(self):
        with self.assertRaisesRegex(ValueError,'still need decisions'):
            p.finalize(self.work)
        self.assertFalse((self.work/'zichen_training_data.zip').exists())

    def test_clean_export_has_matched_model_disjoint_splits(self):
        self.approve();m,summary,bundle=p.finalize(self.work)
        self.assertEqual(len(m),36)
        self.assertTrue(m.groupby('Adv_ID').size().eq(3).all())
        self.assertTrue(m.groupby('Genmodel_ID').Split.nunique().eq(1).all())
        self.assertTrue(m.Pixel_sha256.is_unique)
        for split in ['train','validation','test']:
            self.assertEqual(set(m.loc[m.Split.eq(split),'Body_type']),set(p.CLASSES))
        with zipfile.ZipFile(bundle) as z:
            self.assertIn('DATA/clean_manifest.csv',z.namelist())
            self.assertEqual(sum(n.startswith('images/') for n in z.namelist()),36)

    def test_duplicate_pixels_exclude_every_affected_listing(self):
        self.approve()
        tech=self.tech.copy()
        # Identical pixels in two distinct Sedan listings: exclude both whole triplets.
        i0=0;i1=3
        ids=set(self.queue.iloc[[i0,i1]].Adv_ID)
        tech.loc[i1,'Pixel_sha256']=tech.loc[i0,'Pixel_sha256']
        tech.to_csv(self.work/'DATA/technical_checks.csv',index=False)
        # Only two Sedan groups would remain; no model split may be fabricated.
        with self.assertRaisesRegex(ValueError,'need >=3'):
            p.finalize(self.work)
        excluded=pd.read_csv(self.work/'DATA/excluded_listings.csv')
        self.assertTrue(ids.issubset(set(excluded.Adv_ID)))

    def test_incomplete_listing_is_excluded(self):
        self.approve()
        d=p.load_reviews(self.work);adv=self.queue.iloc[0].Adv_ID
        d.loc[d.Image_ID.eq(self.queue.iloc[0].Image_ID),['Decision','Reason']]=['reject','wrong_view']
        d.to_csv(self.work/'DATA/review_decisions.csv',index=False)
        m,_,_=p.finalize(self.work)
        self.assertNotIn(adv,set(m.Adv_ID))
        self.assertEqual(len(m),33)

    def test_sample_is_stable_under_input_order(self):
        ad=pd.read_csv(self.root/'ad.csv').sample(frac=1,random_state=9)
        im=pd.read_csv(self.root/'image.csv').sample(frac=1,random_state=9)
        ad.to_csv(self.root/'ad2.csv',index=False);im.to_csv(self.root/'im2.csv',index=False)
        q,_=p.prepare(self.root/'ad2.csv',self.root/'im2.csv',self.root/'work2',max_listings_per_model=0)
        self.assertEqual(q.Image_ID.tolist(),self.queue.Image_ID.tolist())

    def test_notebook_shared_implementation_matches_module(self):
        nb=json.loads((SCRIPT.parent/'01_data_cleaning.ipynb').read_text())
        self.assertEqual(''.join(nb['cells'][4]['source']),SCRIPT.read_text())


if __name__=='__main__': unittest.main()
