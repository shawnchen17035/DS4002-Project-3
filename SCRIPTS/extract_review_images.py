#!/usr/bin/env python3
"""Stage only Colab-selected DVM-CAR files from the existing Mac ZIP.

The Pink Panthers | DS4002 Project 3 | Shawn Chen, Zichen Luo.
Python standard library only. This copies bytes, not review approvals.
Default: python3 extract_review_images.py
Optional: --queue PATH --source PATH --output PATH
"""
import argparse
import csv
from pathlib import Path
import zipfile


def extract(queue, source, output):
    with Path(queue).open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        if 'Image_name' not in (reader.fieldnames or []):
            raise ValueError('Queue must contain Image_name; use the CSV exported by Colab.')
        wanted={r['Image_name'] for r in reader}
    if any('/' in n or '\\' in n for n in wanted):
        raise ValueError('Unsafe image filename in queue')
    # Index just wanted basenames, retaining ambiguity instead of picking arbitrarily.
    lookup={}
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    temp=output.with_suffix('.partial.zip')
    copied=0
    with zipfile.ZipFile(source) as src:
        for info in src.infolist():
            name=info.filename.rsplit('/',1)[-1]
            if name in wanted and not info.is_dir():lookup.setdefault(name,[]).append(info)
        with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_STORED) as dst:
            for name in sorted(wanted):
                matches=lookup.get(name,[])
                if len(matches)==1:
                    dst.writestr(name,src.read(matches[0]));copied+=1
    temp.replace(output)
    print(f'Copied {copied:,}/{len(wanted):,} selected photos to {output}')
    print(f'Size: {output.stat().st_size/1_000_000:.1f} MB')
    missing=len(wanted)-copied
    if missing:print(f'{missing} missing/ambiguous filenames were skipped; Colab will record them as failed file checks.')
    print('Upload this smaller ZIP to DS4002_Project3/input in Drive, then run Colab Cell 5.')
    return copied


def main():
    downloads=Path.home()/'Downloads'
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--queue',type=Path,default=downloads/'review_queue.csv')
    parser.add_argument('--source',type=Path,default=downloads/'resized_DVM_v2.zip')
    parser.add_argument('--output',type=Path,default=downloads/'review_images.zip')
    args=parser.parse_args()
    for path in [args.queue,args.source]:
        if not path.is_file():parser.error(f'Missing file: {path}')
    if args.output.resolve() in {args.queue.resolve(),args.source.resolve()}:
        parser.error('Output must not overwrite input files')
    extract(args.queue,args.source,args.output)


if __name__=='__main__':main()
