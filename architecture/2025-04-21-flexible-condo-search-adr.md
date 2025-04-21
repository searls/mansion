# ADR: Flexible, Extensible Condo Search Platform (2025-04-21)

## Context
We want a robust, extensible, and user-friendly platform to help our family find the ideal condo. The system should support scraping new and used listings (starting with Suumo, but extensible to other sources), store them in a normalized database, and provide a web UI for interactive, visual exploration. The UI should be usable by non-technical users (e.g., family members) and support both local and on-demand scraping.

## Decision
We will:

### 1. Data Model Improvements
- Add `created_at` and `updated_at` columns to listings for freshness and upsert logic.
- Add a `source` column to support multiple listing sources.
- Add unique constraints on (`suumo_id`, `source`).

### 2. Scraper/ETL Refactor
- Separate scraping logic from DB ingestion/upsert logic.
- Scrapers return normalized dicts/lists; ingestion layer handles upserts and timestamps.
- Implement upsert logic: update `updated_at` if exists, else insert with `created_at`.
- Define a base scraper interface; each source implements it for easy extensibility.

### 3. API & Web UI Foundation
- Build a minimal Flask/FastAPI backend with endpoints for:
  - Querying listings (with filters: region, price, area, etc.)
  - Triggering a scrape for new data
- Frontend: Use Hotwire/Turbo/Stimulus for a reactive UI.
  - Region dropdown, keyword search, results table/grid, 'fetch more' button.
  - Query results served from DB, with fallback to scrape if empty.

### 4. User Experience
- Auto-scrape fallback if no results found.
- Show freshness (last updated) for each listing.
- Mobile-friendly UI with Tailwind.

### 5. Extensibility
- Make it easy to add new sources by dropping in a new scraper class.
- For production, consider background jobs, but synchronous is fine for now.

## Consequences
- The system will be easy to extend, maintain, and use interactively.
- Adding new sources or UI features will be straightforward.
- Data will always be fresh and deduplicated.
- The platform will be accessible to both technical and non-technical users.
