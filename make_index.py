#!/usr/bin/env python3
# coding: utf-8

import glob

target_file = open('./docs/index.md', mode='w', encoding="UTF-8")

target_file.write('# 町字一覧ポータルサイト\n\n')

files = glob.glob('./docs/data/*/*')
files.sort()
#print(files)
for filepath in files:
  #print(filepath)
  f = open(filepath, mode='r', encoding="UTF-8")
  title = f.readline().replace('\n','')
  md_string = '- [' + title.replace('# ', '') + '](' + filepath.replace('./docs/','./') + ')\n'
  target_file.write(md_string)

target_file.write('\n---\n')
target_file.write('\n- 出典：[「アドレス・ベース・レジストリ（町字マスター データセット）」（デジタル庁）](https://www.digital.go.jp/policies/base_registry_address/) を加工して作成')

target_file.close()