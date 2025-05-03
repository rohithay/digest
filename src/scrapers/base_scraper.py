import requests
from bs4 import BeautifulSoup
import logging
import time
import os
import yaml
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseScraper(ABC):
    """Base class for all scrapers"""
    
    def __init__(self, config_path: str = "../config/sources.yaml"):
        """Initialize the scraper with configuration"""
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Load configuration
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
            
        # Create output directory if it doesn't exist
        os.makedirs("../data/raw", exist_ok=True)
        
    @abstractmethod
    def scrape_publication(self, publication: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scrape content from a publication defined in the config"""
        pass
    
    def scrape_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Scrape all publications defined in the config"""
        results = {}
        
        for publication in self.config.get("publications", []):
            self.logger.info(f"Scraping {publication['name']}")
            
            try:
                articles = self.scrape_publication(publication)
                results[publication["name"]] = articles
                
                # Save raw results
                self._save_raw_data(publication["name"], articles)
                
                # Rate limiting
                time.sleep(2)
            except Exception as e:
                self.logger.error(f"Error scraping {publication['name']}: {str(e)}")
        
        return results
    
    def _save_raw_data(self, publication_name: str, articles: List[Dict[str, Any]]) -> None:
        """Save raw scraped data to disk"""
        # Create sanitized filename
        filename = publication_name.lower().replace(" ", "_")
        
        # Save to file
        output_path = f"../data/raw/{filename}.yaml"
        with open(output_path, 'w') as file:
            yaml.dump(articles, file)
            
        self.logger.info(f"Saved {len(articles)} articles from {publication_name}")
