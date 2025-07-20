# digest
A tool for analyzing responsible AI publications to identify key themes, trends, and summaries. It's designed to help researchers and practitioners stay current with the evolving field of AI ethics.

## Getting Started
1. Clone the repository
2. Install dependencies
3. Run the full pipeline with `python main.py --all`
4. Launch the dashboard with `streamlit run app.py`

## Use

### Running the Full Pipeline

```bash
cd src
python main.py --all
```

### Running Individual Components

```bash
# Just scrape new data
python main.py --scrape

# Just analyze themes
python main.py --analyze

# Just export results
python main.py --export
```

## Contribute

### Adding Publications

Edit `config/sources.yaml` to add new publications.

### Modifying Themes

Edit `config/themes.yaml` to modify the themes.
