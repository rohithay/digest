import requests
from bs4 import BeautifulSoup
import logging
import time
from typing import List, Dict, Any
from datetime import datetime
from urllib.parse import urljoin
import hashlib

from .base_scraper import BaseScraper

class WebScraper(BaseScraper):
    """Scraper for generic websites"""
    
    def __init__(self, config_path: str = "../config/sources.yaml"):
        super().__init__(config_path)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def scrape_publication(self, publication: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scrape content from a publication website"""
        url = publication["url"]
        articles = []
        
        try:
            # Fetch main page
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find article links - this is a generic approach and may need customization per site
            article_links = self._extract_article_links(soup, url)
            
            # Process each article
            for link in article_links[:10]:  # Limit to 10 articles for demonstration
                article_data = self._scrape_article(link, publication)
                if article_data:
                    articles.append(article_data)
                    
                # Rate limiting
                time.sleep(1)
                
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            
        return articles
    
    def _extract_article_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract article links from the main page"""
        links = []
        
        # Look for common article containers
        article_elements = soup.select("article a, .post a, .blog-post a, .entry a")
        if not article_elements:
            # Try more generic approach
            article_elements = soup.select("a[href*='blog'], a[href*='article'], a[href*='post']")
            
        # Extract links
        for element in article_elements:
            if 'href' in element.attrs:
                # Resolve relative URLs
                full_url = urljoin(base_url, element['href'])
                if full_url not in links:
                    links.append(full_url)
                    
        return links
    
    def _scrape_article(self, url: str, publication: Dict[str, Any]) -> Dict[str, Any]:
        """Scrape a single article"""
        try:
            # Fetch article
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract article data
            title = self._extract_title(soup)
            date = self._extract_date(soup)
            author = self._extract_author(soup)
            content = self._extract_content(soup)
            
            # Generate unique ID
            article_id = hashlib.md5(url.encode()).hexdigest()
            
            return {
                "id": article_id,
                "url": url,
                "title": title,
                "date": date,
                "author": author,
                "content": content,
                "publication": publication["name"],
                "tags": publication.get("tags", [])
            }
            
        except Exception as e:
            self.logger.error(f"Error scraping article {url}: {str(e)}")
            return None
            
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title"""
        title_element = soup.find('h1')
        if title_element:
            return title_element.get_text().strip()
        return "Unknown Title"
    
    def _extract_date(self, soup: BeautifulSoup) -> str:
        """Extract article date"""
        # Try common date elements
        date_element = soup.select_one('time, .date, .published, meta[property="article:published_time"]')
        if date_element:
            if date_element.name == 'meta':
                return date_element.get('content', '')
            return date_element.get_text().strip()
        return "Unknown Date"
    
    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extract article author"""
        # Try common author elements
        author_element = soup.select_one('.author, .byline, meta[name="author"]')
        if author_element:
            if author_element.name == 'meta':
                return author_element.get('content', '')
            return author_element.get_text().strip()
        return "Unknown Author"
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract article content"""
        # Try common content containers
        content_element = soup.select_one('article, .post-content, .entry-content, .content')
        if content_element:
            # Remove unwanted elements
            for elem in content_element.select('script, style, nav, .comments, .related, .share'):
                elem.decompose()
                
            return content_element.get_text().strip()
        return "Content not found"
