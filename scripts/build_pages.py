#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import pandas as pd
import urllib.parse

# --- Configuration ---
ORGANIZATION = "zero3kw"
REPOSITORY = "abr-mt-town-list-stg"

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, 'data')
PAGE_ROOT = os.path.join(ROOT_DIR, 'docs', 'data')  # Output directory for generated pages

# Ensure output directory exists
os.makedirs(PAGE_ROOT, exist_ok=True)

# --- Load and concatenate CSV files ---
df_list = []
for csv_path in glob.glob(os.path.join(SRC_DIR, 'mt_town_pref*.csv')):
    df = pd.read_csv(csv_path, dtype=str, na_filter=False)
    df_list.append(df)
all_df = pd.concat(df_list, ignore_index=True)

# --- Generate Markdown pages grouped by lg_code ---
for lg, grp in all_df.groupby('lg_code'):
    # Create subdirectory based on first two characters of lg_code
    prefix = lg[:2]
    out_dir = os.path.join(PAGE_ROOT, prefix)
    os.makedirs(out_dir, exist_ok=True)

    page_path = os.path.join(out_dir, f"{lg}.md")

    # --- Build title and headers ---
    pref = grp['pref'].iloc[0]
    city = grp['city'].iloc[0]
    ward = grp['ward'].iloc[0] if 'ward' in grp.columns else ''
    title_text = f"{pref}{city}{ward}（{lg}）"

    lines = [
        '---',
        'layout: list',
        f'title: "{title_text}"',
        '---',
        '',
        f'# {title_text}',
        '',
        '| 大字・町 | 丁目 | 小字 | ヨミガナ | 英字 | 町字ID | 住居表示フラグ | 起番フラグ | データ指摘 |',
        '|:---|:---|:---|:---|:---|:---|:---|:---|:---|'
    ]

    # --- Prepare table content and issue links ---
    for _, row in grp.iterrows():
        oaza = row['oaza_cho']
        chome = row['chome']
        koaza = row['koaza']
        yomigana = f"{row['oaza_cho_kana']} {row['chome_kana']} {row['koaza_kana']}"
        english = f"{row['oaza_cho_roma']}{row['chome_number']}{row['koaza_roma']}"
        machiaza_id = row['machiaza_id']
        rsdt_addr_flg = row['rsdt_addr_flg']
        wake_num_flg = row['wake_num_flg']

        # Construct issue title and body for GitHub issue creation link
        issue_title_raw = f"{title_text}{oaza}{chome}{koaza}({machiaza_id})"
        issue_body_raw = (
            "# 指摘項目\n\n"
            "- [ ] 大字・町\n"
            "- [ ] 丁目\n"
            "- [ ] 小字\n"
            "- [ ] ヨミガナ\n"
            "- [ ] 英字\n"
            "- [ ] 町字ID\n"
            "- [ ] 住居表示フラグ\n"
            "- [ ] 起番フラグ\n\n"
            "# 指摘時のデータ\n"
            "| 大字・町名 | 丁目名 | 小字名 | ヨミガナ | 英字 | 町字ID | 住居表示フラグ | 起番フラグ |\n"
            "|:---|:---|:---|:---|:---|:---|:---|:---|\n"
            f"| {oaza} | {chome} | {koaza} | {yomigana} | {english} | {machiaza_id} | {rsdt_addr_flg} | {wake_num_flg} |\n\n"
            "# 具体的な内容\n"
            "（ここに具体的な内容を記入してください。）\n"
        )
        labels_raw = f"データ指摘"

        # URL-encode parameters for safe inclusion in GitHub issue URL
        issue_title = urllib.parse.quote(issue_title_raw, safe='')
        issue_body = urllib.parse.quote(issue_body_raw, safe='')
        labels = urllib.parse.quote(labels_raw, safe='')

        # Generate GitHub issue creation link with pre-filled title, body, and labels
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

    # --- Footer notes ---
    lines.extend([
        '',
        '---',
        '',
        '- 出典：[「アドレス・ベース・レジストリ（町字マスター データセット）』（デジタル庁）]'
        '(https://www.digital.go.jp/policies/base_registry_address/) を加工して作成'
    ])

    # Write the assembled content to the markdown file
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

print(f"build_pages.py complete: generated {len(all_df['lg_code'].unique())} pages under docs/data")
