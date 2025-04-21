#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_index.py

Generate docs/index.md by reading per-prefecture markdown files under docs/data.
This Python script finds the first heading in each md file to build the index.
"""
import os
import glob

# --- Configuration ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(ROOT_DIR, 'docs')
DATA_DIR = os.path.join(DOCS_DIR, 'data')
INDEX_PATH = os.path.join(DOCS_DIR, 'index.md')

# Prefecture names list (1-indexed)
pref_names = [
    "",
    "北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県",
    "茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県",
    "新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県",
    "静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県",
    "奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県",
    "徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県",
    "熊本県","大分県","宮崎県","鹿児島県","沖縄県"
]

lines = []
# Header
lines.extend([
    '---',
    'layout: top',
    'title:',
    'description: アドレス・ベース・レジストリ(ABR)の町字リスト一覧ポータル',
    '---',
    '',
    '# 町字リスト一覧ポータル',
    '',
    '## 都道府県',
    '',
    '|[北海道](#北海道)|[青森県](#青森県)|[岩手県](#岩手県)|[宮城県](#宮城県)|[秋田県](#秋田県)|[山形県](#山形県)|[福島県](#福島県)|',
    '|[茨城県](#茨城県)|[栃木県](#栃木県)|[群馬県](#群馬県)|[埼玉県](#埼玉県)|[千葉県](#千葉県)|[東京都](#東京都)|[神奈川県](#神奈川県)|',
    '|[新潟県](#新潟県)|[富山県](#富山県)|[石川県](#石川県)|[福井県](#福井県)|[山梨県](#山梨県)|[長野県](#長野県)|[岐阜県](#岐阜県)|',
    '|[静岡県](#静岡県)|[愛知県](#愛知県)|[三重県](#三重県)|[滋賀県](#滋賀県)|[京都府](#京都府)|[大阪府](#大阪府)|[兵庫県](#兵庫県)|',
    '|[奈良県](#奈良県)|[和歌山県](#和歌山県)|[鳥取県](#鳥取県)|[島根県](#島根県)|[岡山県](#岡山県)|[広島県](#広島県)|[山口県](#山口県)|',
    '|[徳島県](#徳島県)|[香川県](#香川県)|[愛媛県](#愛媛県)|[高知県](#高知県)|[福岡県](#福岡県)|[佐賀県](#佐賀県)|[長崎県](#長崎県)|',
    '|[熊本県](#熊本県)|[大分県](#大分県)|[宮崎県](#宮崎県)|[鹿児島県](#鹿児島県)|[沖縄県](#沖縄県)| | |',
    '',
    '---',
    '',
    '## 市区町村',
    ''
])

for idx in range(1, 48):
    prefix = f"{idx:02d}"
    pref_name = pref_names[idx]
    lines.append(f'### {pref_name}\n')

    subdir = os.path.join(DATA_DIR, prefix)
    if os.path.isdir(subdir):
        md_files = sorted(glob.glob(os.path.join(subdir, '*.md')))
        for md_path in md_files:
            title = ''
            # Read first heading line
            with open(md_path, encoding='utf-8') as f:
                for line in f:
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break
            rel = os.path.relpath(md_path, DOCS_DIR)
            lines.append(f'- [{title}](./{rel})')
    lines.append('')

# Footer
lines.extend([
    '',
    '---',
    '',
    '- 出典：[「アドレス・ベース・レジストリ（町字マスター データセット）』（デジタル庁）](https://www.digital.go.jp/policies/base_registry_address/) を加工して作成'
])

# Write index.md
with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"index.md generated at {INDEX_PATH}")
