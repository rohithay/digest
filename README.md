# AI Ethics Publication Analyzer
A tool for analyzing responsible AI publications to identify key themes, trends, and summaries. It's designed to help researchers and practitioners stay current with the evolving field of AI ethics.

## Features
- **Content Collection**: Automatically scrapes content from leading AI ethics publications
- **Theme Detection**: Uses AI to identify key themes in publications
- **Trend Analysis**: Tracks the evolution of themes over time
- **Interactive Dashboard**: Explore themes and publications

## Project Structure
* `config/` - Configuration files for sources and themes
* `data/` - Directory for raw and processed data
* `src/` - Source code with scrapers and analyzers
* `notebooks/` - For Jupyter notebooks (placeholder)
* `app/` - For the Streamlit dashboard (placeholder)
* `logs/` - For application logs
* `output/` - For analysis results


## Usage

### Running the Full Pipeline

```bash
cd src
python main.py --all
```

This will:
1. Scrape articles from configured sources
2. Analyze themes
3. Export results

### Running Individual Components

```bash
# Just scrape new data
python main.py --scrape

# Just analyze themes
python main.py --analyze

# Just export results
python main.py --export
```

## Configuration

### Adding Publications

Edit `config/sources.yaml` to add new publications.

### Modifying Themes

Edit `config/themes.yaml` to modify the themes.
