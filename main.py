#!/usr/bin/env python3
# coding: utf-8

import csv
import os
import shutil
import urllib.request
import zipfile

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
        metadata_filename = 'mt_town_pref' + pref_num + '.metadata.csv'

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
                csv2markdowntable(csv_filename)
                update_list.append(csv_filename)

    print(update_list)
    deinit()

def init():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
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

def csv2markdowntable(csv_file_path):
    output_file = csv_file_path.replace(".csv", ".md")
    csv_dict = csv.DictReader(open(TMP_DIR + csv_file_path, encoding="UTF-8"),delimiter=',')
    list_of_rows = [dict_row for dict_row in csv_dict]
    headers = list(list_of_rows[0].keys())

    md_string = " | "
    for header in headers:
        md_string += header+" |"

    md_string += "\n |"
    for i in range(len(headers)):
        md_string += "--- | "

    md_string += "\n"
    for row in list_of_rows:
        md_string += " | "
        for header in headers:
            md_string += row[header]+" | "
        md_string += "\n"

    file = open(DATA_DIR + output_file, "w", encoding="UTF-8")
    file.write(md_string)
    file.close()

def deinit():
    shutil.rmtree(TMP_DIR)

if __name__ == '__main__':
    main()
