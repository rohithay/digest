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

## Getting Started
1. Clone the repository
2. Install dependencies (BeautifulSoup, PyTorch, Transformers, Streamlit, etc.)
3. Run the full pipeline with python main.py --all
4. Launch the dashboard with streamlit run app.py

## How It Works
1. The scraper collects articles from configured sources
2. The theme detector analyzes content using NLP techniques
3. The summarizer creates concise summaries of key articles
4. Results are organized into a structured database
5. The dashboard provides interactive exploration of findings

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
