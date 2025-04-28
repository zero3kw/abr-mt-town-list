#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import pandas as pd

# --- Configuration ---
ORGANIZATION = "zero3kw"
REPOSITORY = "abr-mt-town-list-stg"

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, 'data')
PAGE_ROOT = os.path.join(ROOT_DIR, 'docs', 'data')  # Output root: docs/data

# Ensure output root exists
os.makedirs(PAGE_ROOT, exist_ok=True)

# Load and concatenate all CSV files
df_list = []
for csv_path in glob.glob(os.path.join(SRC_DIR, 'mt_town_pref*.csv')):
    df = pd.read_csv(csv_path, dtype=str, na_filter=False)
    df_list.append(df)
all_df = pd.concat(df_list, ignore_index=True)

# Generate Markdown pages, one per lg_code
for lg, grp in all_df.groupby('lg_code'):
    # Subdirectory based on first two digits of lg_code
    prefix = lg[:2]
    out_dir = os.path.join(PAGE_ROOT, prefix)
    os.makedirs(out_dir, exist_ok=True)

    # Output file path
    page_path = os.path.join(out_dir, f"{lg}.md")

    # Page title components
    pref = grp['pref'].iloc[0]
    city = grp['city'].iloc[0]
    ward = grp['ward'].iloc[0] if 'ward' in grp.columns else ''
    title_text = f"{pref}{city}{ward} ({lg})"

    # YAML front-matter and header
    lines = [
        '---',
        'layout: list',
        f'title: "{title_text}"',
        '---',
        '',
        f'# {title_text}',
        '',
        '| 大字・町名 | 丁目名 | 小字名 | ヨミガナ | 英字 | 町字ID | 住居表示フラグ | 起番フラグ | 誤データ指摘 |',
        '|:---|:---|:---|:---|:---|:---|:---|:---|:---|'
    ]

    # Add table rows
    for _, row in grp.iterrows():
        oaza = row['oaza_cho']
        chome = row['chome']
        koaza = row['koaza']
        yomigana = f"{row['oaza_cho_kana']} {row['chome_kana']} {row['koaza_kana']}"
        english = f"{row['oaza_cho_roma']}{row['chome_number']}{row['koaza_roma']}"
        machiaza_id = row['machiaza_id']
        rsdt_addr_flg = row['rsdt_addr_flg']
        wake_num_flg = row['wake_num_flg']

        issue_title = (
            f"【データ指摘】{title_text} {oaza} {chome} {koaza} {yomigana} {english} ({machiaza_id})"
        )
        issue_body = (
            "以下の項目について誤りがあればチェックしてください。%0A%0A"
            "- [ ] 大字・町名%0A"
            "- [ ] 丁目名%0A"
            "- [ ] 小字名%0A"
            "- [ ] ヨミガナ%0A"
            "- [ ] 英字%0A"
            "- [ ] 町字ID%0A"
            "- [ ] 住居表示フラグ%0A"
            "- [ ] 起番フラグ%0A%0A"
            "# 指摘時のデータ%0A"
            f"| 大字・町名 | 丁目名 | 小字名 | ヨミガナ | 英字 | 町字ID | 住居表示フラグ | 起番フラグ |%0A"
            f"| {oaza} | {chome} | {koaza} | {yomigana} | {english} | {machiaza_id} | {rsdt_addr_flg} | {wake_num_flg} |%0A%0A"
            "# 具体的な内容%0A"
             "具体的な内容を記入してください。%0A%0A"
        )
        labels = f"データ指摘,{pref}{city}{ward}{oaza}{chome}{koaza}"
        issue_link = (
            f"[📝](https://github.com/{ORGANIZATION}/{REPOSITORY}/issues/new?"
            f"title={issue_title}"
            f"&body={issue_body}"
            f"&labels={labels})"
        )

        line = '| ' + ' | '.join([
            oaza, chome, koaza, yomigana, english,
            machiaza_id, rsdt_addr_flg, wake_num_flg, issue_link
        ]) + ' |'
        lines.append(line)

    # Footer lines
    lines.extend([
        '',
        '---',
        '',
        '- 出典：[「アドレス・ベース・レジストリ（町字マスター データセット）』（デジタル庁）]'
        '(https://www.digital.go.jp/policies/base_registry_address/) を加工して作成'
    ])

    # Write to file
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

print(f"build_pages.py complete: generated {len(all_df['lg_code'].unique())} pages under docs/data")
