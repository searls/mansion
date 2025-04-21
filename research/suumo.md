---

# 2025-04-21: Important Suumo Scraper Findings

## Region and Search Flow
- Suumo's search is region-scoped: every query (e.g., 静岡) must be mapped to a specific region (e.g., 中部/東海 for 静岡, 関東 for 東京).
- The region is not determined by the query string alone; the user must select a region before searching.
- The URL parameters `ar` (area/region) and `bs` (listing type: 010=new, 011=used) are required for direct search URLs, but the correct region code must be chosen for the query to work.
- To robustly scrape, the scraper should:
  1. Visit both new and used entry points: https://suumo.jp/ms/shinchiku/ and https://suumo.jp/ms/chuko/
  2. Determine the correct region for the query (e.g., 静岡→中部/東海). This may require a mapping or external lookup if not hardcoded.
  3. Click into the region, then enter the query into the キーワード ([name=fw]) field and submit.
- Hardcoding region codes in the URL is fragile and will not work for all queries (e.g., 静岡 with 関東 will not return 静岡 listings).
- If region mapping cannot be done with a static dictionary, consider using an LLM or external API to resolve the region for a given query.

## Actionable Guidance
- Do not attempt to construct listing URLs directly for arbitrary queries.
- Always start from the new/used entry points, select the correct region, and then search.
- Maintain a mapping of common prefectures/cities to their Suumo region, and update as needed.
- Document this process for future maintainers.

## Suumo Region Codes Mapping

| ar code | Region    | Example Prefectures |
|---------|-----------|---------------------|
| 010     | 北海道    | 北海道              |
| 020     | 東北      | 青森, 岩手, 宮城, 秋田, 山形, 福島 |
| 030     | 関東      | 東京, 神奈川, 千葉, 埼玉, 茨城, 栃木, 群馬 |
| 040     | 甲信越    | 山梨, 長野, 新潟    |
| 050     | 東海      | 静岡, 愛知, 岐阜, 三重 |
| 060     | 関西      | 大阪, 兵庫, 京都, 滋賀, 奈良, 和歌山 |
| 070     | 四国      | 徳島, 香川, 愛媛, 高知 |
| 080     | 中国      | 鳥取, 島根, 岡山, 広島, 山口 |
| 090     | 九州      | 福岡, 佐賀, 長崎, 熊本, 大分, 宮崎, 鹿児島, 沖縄 |

- Use this mapping to route queries to the correct region code (`ar`) for Suumo searches.
- Example: 静岡 → 東海 → ar=050
- This dictionary can be used to automate region selection for most queries without LLMs.
