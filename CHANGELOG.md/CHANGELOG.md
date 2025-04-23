## 2025-04-23

### Spike: Vibe Coding with Python & Scraping

This initial spike was an experiment in rapid prototyping and "vibe coding" to quickly explore scraping Japanese real estate listings and persisting them to a Postgres database. The work was intentionally exploratory, prioritizing momentum and learning over polish or maintainability.

#### What was built
- Python scripts for scraping Suumo (and stubs for Lifeful, AtHome)
- SQLAlchemy models for listings, with normalization and composite uniqueness
- CLI interface for running scrapes and storing results
- Database verification and summary scripts
- Poetry for dependency management

#### Key takeaways
- The spike proved out the core workflow: scrape → normalize → persist → verify
- The code is functional but not idiomatic for long-term maintainability
- Scraper logic and data models are tightly coupled; refactoring would be needed for extensibility
- The experiment highlighted the value of familiar tools and conventions for future work

#### Next steps
- Reimplement core functionality in a simple Rails app, leveraging Omakase Rails stack, Hotwire, and familiar Ruby idioms
- Use the spike as a reference for data model and workflow, but prioritize maintainability and testability
- Continue journaling progress in this CHANGELOG, prepending new entries to the top

---

This entry summarizes the first few days of work, referencing the experimental code in `spikes/initial_vibe/` and chat logs in `chats/`. Future entries will document progress on the Rails reimplementation and lessons learned.
