#!/usr/bin/env python3
# coding: utf-8

import os
import shutil
import urllib.request
import zipfile
import pandas as pd

TMP_DIR = './tmp/'
DATA_DIR = './docs/data/'
METADATA_DIR = './metadata/'

BASE_URL = 'https://gov-csv-export-public.s3.ap-northeast-1.amazonaws.com/mt_town/pref/'
METADATA_BASE_URL = 'https://gov-csv-export-public.s3.ap-northeast-1.amazonaws.com/mt_town_meta/pref/'

def main():
    init()
    update_list = []

    for i in range(1, 48):
        pref_num = str(i).zfill(2)
        zip_filename = 'mt_town_pref' + pref_num + '.csv.zip'
        csv_filename = 'mt_town_pref' + pref_num + '.csv'
        cutted_csv_filename = 'cutted_' + csv_filename
        metadata_filename = 'mt_town_pref' + pref_num + '.metadata.csv'
        output_filename = csv_filename.replace(".csv", ".md")

        metadata_url = METADATA_BASE_URL + metadata_filename
        metadata_local_path = METADATA_DIR + metadata_filename
        metadata_tmp_path = TMP_DIR + metadata_filename

        get_data(metadata_url, metadata_tmp_path) # get metadata
        if not os.path.exists(metadata_local_path) or \
            checkupdate(metadata_tmp_path,metadata_local_path):
                shutil.copy(metadata_tmp_path,metadata_local_path)
                zip_url = BASE_URL + zip_filename
                get_data(zip_url , TMP_DIR + zip_filename) # get zipdata
                unarchive(TMP_DIR + zip_filename)
                groupby_lgcode_file(csv_filename)
                update_list.append(csv_filename)

    print(update_list)
    dispose()


def groupby_lgcode_file(csv_filename):
    df = pd.read_csv(TMP_DIR + csv_filename, dtype='object', na_filter=False)

    NEW_HEADER = [
        '都道府県名', '郡名', '市区町村名', '政令市区名', '全国地方公共団体コード',
        '大字・町名', '丁目名', '小字名', 'ヨミガナ', '英字', '町字ID', '住居表示フラグ', '起番フラグ'
        ]
    new_df = pd.DataFrame(index=[], columns=NEW_HEADER)
    new_df['都道府県名'] = df['都道府県名']
    new_df['郡名'] = df['郡名']
    new_df['市区町村名'] = df['市区町村名']
    new_df['政令市区名'] = df['政令市区名']
    new_df['全国地方公共団体コード'] = df['全国地方公共団体コード']
    new_df['大字・町名'] = df['大字・町名']
    new_df['丁目名'] = df['丁目名']
    new_df['小字名'] = df['小字名']
    new_df['ヨミガナ'] = df['大字・町名_カナ'] + \
                        df['丁目名_カナ'] + \
                        df['小字名_カナ']
    new_df['英字'] = df['大字・町名_英字'] + \
                        df['丁目名_数字'] + \
                        df['小字名_英字']
    new_df['町字ID'] = df['町字id']
    new_df['住居表示フラグ'] = df['住居表示フラグ']
    new_df['起番フラグ'] = df['起番フラグ']

    for lg_code, group_df in new_df.groupby('全国地方公共団体コード'):
        title = '# ' + \
                group_df.fillna('').mode()['都道府県名'][0] + \
                group_df.fillna('').mode()['郡名'][0] + \
                group_df.fillna('').mode()['市区町村名'][0] + \
                group_df.fillna('').mode()['政令市区名'][0] + \
                '(' + \
                group_df.fillna('').mode()['全国地方公共団体コード'][0] + \
                ')'

        title_df = pd.DataFrame([title, ' '])
        title_df.to_csv(f'{DATA_DIR}{lg_code[0:2]}/{lg_code}.md', index=False, header=False, quoting=3, encoding='utf-8')

        group_df.drop(columns=['都道府県名', '郡名', '市区町村名', '政令市区名', '全国地方公共団体コード'])\
                .to_markdown(f'{DATA_DIR}{lg_code[0:2]}/{lg_code}.md', index=False, mode='a')

def init():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    for i in range(1, 48):
        os.makedirs(DATA_DIR + str(i).zfill(2), exist_ok=True)
    os.makedirs(METADATA_DIR, exist_ok=True)

def get_data(url, filename):
    urllib.request.urlretrieve(url, filename)

def unarchive(filename):
    with zipfile.ZipFile(filename) as f:
        f.extractall(TMP_DIR)

def checkupdate(metadata_local_path, metadata_tmp_path):
    t1 = str(open(metadata_local_path).readlines()[7]).strip('\n').split(',')
    t2 = str(open(metadata_tmp_path).readlines()[7]).strip('\n').split(',')
    print(t1, t2)
    if t1 != t2:
        return True
    else:
        return False

def dispose():
    shutil.rmtree(TMP_DIR)

if __name__ == '__main__':
    main()