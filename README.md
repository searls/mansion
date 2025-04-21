# Vibe-sourced code example

This is the code that Copilot Agent wrote with GPT 4.1 for me and is featured on [this here screencast](https://youtu.be/O0Vfmfqqan4).

## Running the Project

This project uses [Poetry](https://python-poetry.org/) for dependency management and execution.

### Install dependencies

```
poetry install
```

### Run the main script

You can run the main script with Poetry using:

```
poetry run python main.py <query>
```

Replace `<query>` with your search term (e.g., 新宿).

### Example

```
poetry run python main.py 新宿
```

This will execute all scrapers and store results in your configured Postgres database.

---

For development, you can also use `poetry shell` to spawn a subshell with the environment activated:

```
poetry shell
python main.py <query>
```
