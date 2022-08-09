#!/usr/bin/env python3
# coding: utf-8

import glob

import pref

target_file = open('./docs/index.md', mode='w', encoding="UTF-8")
target_file.write('# 町字リスト一覧ポータル \n\n')
target_file.write('## 都道府県\n\n')

for i in range(1, 48):
    pref_name = pref.obj[i]
    target_file.write('- [' + pref_name + '](#' + pref_name + ')\n')

target_file.write('\n---\n')
target_file.write('\n## 市区町村 \n')

for i in range(1, 48):
    pref_name = pref.obj[i]
    target_file.write('\n### ' + pref_name + '\n\n')
    files = glob.glob('./docs/data/' + str(i).zfill(2) + '/*')
    files.sort()
    for filepath in files:
        #print(filepath)
        f = open(filepath, mode='r', encoding="UTF-8")
        title = f.readline().replace('\n','')
        md_string = '- [' + title.replace('# ', '') + '](' + filepath.replace('./docs/','./') + ')\n'
        target_file.write(md_string)

target_file.write('\n---\n')
target_file.write('\n- 出典：[「アドレス・ベース・レジストリ（町字マスター データセット）」（デジタル庁）](https://www.digital.go.jp/policies/base_registry_address/) を加工して作成')

target_file.close()