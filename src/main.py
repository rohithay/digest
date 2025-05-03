import argparse
import logging
import os
import yaml
import json
import pandas as pd
from datetime import datetime

# Import project modules
from scrapers.web_scraper import WebScraper
from analyzers.theme_detector import ThemeDetector

def setup_logging():
    """Set up logging configuration"""
    log_dir = "../logs"
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"analysis_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="AI Ethics Publication Analyzer")
    
    parser.add_argument("--scrape", action="store_true", help="Scrape new data")
    parser.add_argument("--analyze", action="store_true", help="Analyze themes")
    parser.add_argument("--export", action="store_true", help="Export results")
    parser.add_argument("--all", action="store_true", help="Run full pipeline")
    
    parser.add_argument("--config", type=str, default="../config/sources.yaml",
                       help="Path to configuration file")
    parser.add_argument("--themes", type=str, default="../config/themes.yaml",
                       help="Path to themes configuration")
    
    return parser.parse_args()

def main():
    """Main execution function"""
    # Set up logging
    logger = setup_logging()
    logger.info("Starting AI Ethics Publication Analyzer")
    
    # Parse arguments
    args = parse_args()
    
    # Set up output directory
    output_dir = "../output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Run pipeline based on arguments
    if args.all or args.scrape:
        logger.info("Scraping publications")
        scraper = WebScraper(config_path=args.config)
        articles = scraper.scrape_all()
        logger.info(f"Scraped {sum(len(pub_articles) for pub_articles in articles.values())} articles")
    
    if args.all or args.analyze:
        logger.info("Analyzing themes")
        detector = ThemeDetector(theme_config_path=args.themes)
        
        # Load articles if not already scraped
        if not args.scrape and not args.all:
            articles_list = detector.load_articles()
        else:
            # Flatten articles dictionary
            articles_list = []
            for pub_articles in articles.values():
                articles_list.extend(pub_articles)
        
        # Detect themes
        theme_results = detector.detect_themes(articles_list)
        
        # Get top themes
        top_themes = detector.get_top_themes(theme_results)
        
        # Save results
        theme_results.to_csv(os.path.join(output_dir, "theme_results.csv"), index=False)
        top_themes.to_csv(os.path.join(output_dir, "top_themes.csv"), index=False)
        
        logger.info(f"Analyzed themes for {len(theme_results)} articles")
    
    if args.all or args.export:
        logger.info("Exporting results")
        
        # Load data if not already loaded
        if not args.analyze and not args.all:
            try:
                theme_results = pd.read_csv(os.path.join(output_dir, "theme_results.csv"))
                top_themes = pd.read_csv(os.path.join(output_dir, "top_themes.csv"))
            except FileNotFoundError:
                logger.error("Analysis results not found. Run analysis first.")
                return
        
        # Generate comprehensive report
        timestamp = datetime.now().strftime("%Y-%m-%d")
        report = f"# AI Ethics Publication Analysis\n\n"
        report += f"Generated on: {timestamp}\n\n"
        
        # Add themes overview
        report += "## Key Themes Identified\n\n"
        
        # Count articles per theme
        theme_counts = {}
        for _, row in top_themes.iterrows():
            theme = row["top_theme_1"]
            if theme not in theme_counts:
                theme_counts[theme] = 0
            theme_counts[theme] += 1
        
        # Sort themes by count
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        
        for theme, count in sorted_themes:
            report += f"### {theme} ({count} articles)\n\n"
            
            # Get articles for this theme
            theme_articles = top_themes[top_themes["top_theme_1"] == theme]
            
            for _, article in theme_articles.iterrows():
                report += f"- **{article['title']}** ({article['publication']})\n"
                report += f"  [Read more]({article['url']})\n\n"
        
        # Write report
        with open(os.path.join(output_dir, f"ai_ethics_report_{timestamp}.md"), 'w') as file:
            file.write(report)
            
        logger.info("Export complete")
    
    logger.info("Analysis complete")

if __name__ == "__main__":
    main()
