#!/usr/bin/env python3
# coding: utf-8

import glob

import pref

target_file = open('./docs/index.md', mode='w', encoding="UTF-8")
target_file.write('# 町字リスト一覧ポータル \n\n')
target_file.write('## 都道府県\n')

pref_table='''
|[北海道](#北海道)|[青森県](#青森県)|[岩手県](#岩手県)|[宮城県](#宮城県)|[秋田県](#秋田県)|[山形県](#山形県)|[福島県](#福島県)|
|[茨城県](#茨城県)|[栃木県](#栃木県)|[群馬県](#群馬県)|[埼玉県](#埼玉県)|[千葉県](#千葉県)|[東京都](#東京都)|[神奈川県](#神奈川県)|
|[新潟県](#新潟県)|[富山県](#富山県)|[石川県](#石川県)|[福井県](#福井県)|[山梨県](#山梨県)|[長野県](#長野県)|[岐阜県](#岐阜県)|
|[静岡県](#静岡県)|[愛知県](#愛知県)|[三重県](#三重県)|[滋賀県](#滋賀県)|[京都府](#京都府)|[大阪府](#大阪府)|[兵庫県](#兵庫県)|
|[奈良県](#奈良県)|[和歌山県](#和歌山県)|[鳥取県](#鳥取県)|[島根県](#島根県)|[岡山県](#岡山県)|[広島県](#広島県)|[山口県](#山口県)|
|[徳島県](#徳島県)|[香川県](#香川県)|[愛媛県](#愛媛県)|[高知県](#高知県)|[福岡県](#福岡県)|[佐賀県](#佐賀県)|[長崎県](#長崎県)|
|[熊本県](#熊本県)|[大分県](#大分県)|[宮崎県](#宮崎県)|[鹿児島県](#鹿児島県)|[沖縄県](#沖縄県)| | |
'''

target_file.write(pref_table)

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