# AI Ethics Publication Analyzer
A tool for analyzing responsible AI publications to identify key themes, trends, and summaries. It's designed to help researchers and practitioners stay current with the evolving field of AI ethics.

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
2. Install dependencies
3. Run the full pipeline with `python main.py --all`
4. Launch the dashboard with `streamlit run app.py`

## Usage

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

## Configuration

### Adding Publications

Edit `config/sources.yaml` to add new publications.

### Modifying Themes

Edit `config/themes.yaml` to modify the themes.
