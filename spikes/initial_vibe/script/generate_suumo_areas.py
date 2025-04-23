#!/usr/bin/env python3
"""
Generate JSON of AR code → region → all wards/cities/towns/villages
Uses MediaWiki API:Categorymembers to fetch pages in each prefecture’s category.
"""
import requests
import json
import os

# AR code → (region name, list of prefecture-category titles)
regions = {
    "010": ("北海道", ["Category:北海道の市町村"]),
    "020": ("東北", [
        "Category:青森県の市町村", "Category:岩手県の市町村", "Category:宮城県の市町村",
        "Category:秋田県の市町村", "Category:山形県の市町村", "Category:福島県の市町村"
    ]),
    "030": ("関東", [
        "Category:茨城県の市町村", "Category:栃木県の市町村", "Category:群馬県の市町村",
        "Category:埼玉県の市町村", "Category:千葉県の市町村", "Category:東京都の市町村",
        "Category:神奈川県の市町村"
    ]),
    "040": ("甲信越", [
        "Category:山梨県の市町村", "Category:長野県の市町村", "Category:新潟県の市町村"
    ]),
    "050": ("東海", [
        "Category:静岡県の市町村", "Category:愛知県の市町村", "Category:岐阜県の市町村", "Category:三重県の市町村"
    ]),
    "060": ("関西", [
        "Category:大阪府の市町村", "Category:兵庫県の市町村", "Category:京都府の市町村",
        "Category:滋賀県の市町村", "Category:奈良県の市町村", "Category:和歌山県の市町村"
    ]),
    "070": ("四国", [
        "Category:徳島県の市町村", "Category:香川県の市町村", "Category:愛媛県の市町村", "Category:高知県の市町村"
    ]),
    "080": ("中国", [
        "Category:鳥取県の市町村", "Category:島根県の市町村", "Category:岡山県の市町村",
        "Category:広島県の市町村", "Category:山口県の市町村"
    ]),
    "090": ("九州", [
        "Category:福岡県の市町村", "Category:佐賀県の市町村", "Category:長崎県の市町村",
        "Category:熊本県の市町村", "Category:大分県の市町村", "Category:宮崎県の市町村",
        "Category:鹿児島県の市町村", "Category:沖縄県の市町村"
    ]),
}

API_ENDPOINT = "https://ja.wikipedia.org/w/api.php"
session = requests.Session()

def fetch_category_members(cat_title):
    members = []
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": cat_title,
        "cmlimit": "max",
        "format": "json"
    }
    while True:
        resp = session.get(API_ENDPOINT, params=params).json()
        for page in resp["query"]["categorymembers"]:
            members.append(page["title"])
        if "continue" in resp:
            params.update(resp["continue"])
        else:
            break
    return members

def clean_name(name):
    # Remove 'Category:' prefix
    if name.startswith("Category:"):
        name = name[len("Category:"):]
    # Remove parentheticals (e.g., '伊達市 (福島県)' -> '伊達市')
    import re
    name = re.sub(r"\s*\(.*?\)", "", name)
    # Remove suffixes like '一覧' (list), '章', '旗', '別' if present at the end
    name = re.sub(r"[の]?(市町村|区市町村|市町村旗|市町村章|市町村別|区市町村旗|区市町村章|旗|章|別|一覧)$", "", name)
    return name.strip()

output = {}
for code, (region_name, cat_list) in regions.items():
    names = []
    for cat in cat_list:
        names.extend(fetch_category_members(cat))
    # Clean names
    cleaned = [clean_name(n) for n in names]
    # dedupe and sort
    unique_names = sorted(set(cleaned))
    output[code] = {
        "region": region_name,
        "keywords": unique_names
    }

# Write to research/suumo_areas.json
output_path = os.path.join(os.path.dirname(__file__), '../research/suumo_areas.json')
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Generated {output_path} with {len(output)} regions")
