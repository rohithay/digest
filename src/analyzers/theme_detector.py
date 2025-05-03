import yaml
import pandas as pd
from typing import List, Dict, Any
import os
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ThemeDetector:
    """Detects themes in AI ethics publications"""
    
    def __init__(self, theme_config_path: str = "../config/themes.yaml", 
                 use_transformer: bool = False):
        """Initialize the theme detector"""
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Load theme definitions
        with open(theme_config_path, 'r') as file:
            self.theme_config = yaml.safe_load(file)
            
        self.themes = self.theme_config.get("themes", [])
        self.use_transformer = use_transformer
        
        # For TF-IDF approach
        self.logger.info("Using TF-IDF for theme detection")
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words='english'
        )
            
    def load_articles(self, data_dir: str = "../data/raw") -> List[Dict[str, Any]]:
        """Load all articles from data directory"""
        articles = []
        
        for filename in os.listdir(data_dir):
            if filename.endswith('.yaml'):
                with open(os.path.join(data_dir, filename), 'r') as file:
                    publication_articles = yaml.safe_load(file)
                    if publication_articles:
                        articles.extend(publication_articles)
                        
        self.logger.info(f"Loaded {len(articles)} articles")
        return articles
    
    def detect_themes_tfidf(self, articles: List[Dict[str, Any]]) -> pd.DataFrame:
        """Detect themes using TF-IDF and cosine similarity"""
        # Extract article texts
        texts = [article.get("content", "") for article in articles]
        
        # Transform texts to TF-IDF vectors
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        
        # Create theme descriptions
        theme_descriptions = [
            f"{theme['name']}: {theme['description']} {' '.join(theme.get('keywords', []))}"
            for theme in self.themes
        ]
        
        # Transform theme descriptions to TF-IDF vectors
        theme_vectors = self.vectorizer.transform(theme_descriptions)
        
        # Calculate cosine similarity between articles and themes
        similarity_matrix = cosine_similarity(tfidf_matrix, theme_vectors)
        
        # Create results dataframe
        results = []
        for i, article in enumerate(articles):
            # Get theme scores
            theme_scores = similarity_matrix[i]
            
            # Add to results
            article_result = {
                "id": article.get("id", f"article_{i}"),
                "title": article.get("title", "Unknown Title"),
                "publication": article.get("publication", "Unknown Publication"),
                "url": article.get("url", "")
            }
            
            # Add theme scores
            for j, theme in enumerate(self.themes):
                article_result[f"theme_{theme['name']}"] = theme_scores[j]
                
            results.append(article_result)
            
        return pd.DataFrame(results)
    
    def detect_themes(self, articles: List[Dict[str, Any]] = None) -> pd.DataFrame:
        """Detect themes in articles"""
        if articles is None:
            articles = self.load_articles()
            
        return self.detect_themes_tfidf(articles)
            
    def get_top_themes(self, df: pd.DataFrame, n_themes: int = 3) -> pd.DataFrame:
        """Get top themes for each article"""
        # Get theme columns
        theme_cols = [col for col in df.columns if col.startswith("theme_")]
        
        # Calculate top themes
        results = []
        for _, row in df.iterrows():
            article_data = {
                "id": row["id"],
                "title": row["title"],
                "publication": row["publication"],
                "url": row["url"]
            }
            
            # Get theme scores
            theme_scores = [(col.replace("theme_", ""), row[col]) for col in theme_cols]
            
            # Sort by score
            theme_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Add top themes
            for i, (theme, score) in enumerate(theme_scores[:n_themes]):
                article_data[f"top_theme_{i+1}"] = theme
                article_data[f"top_theme_{i+1}_score"] = score
                
            results.append(article_data)
            
        return pd.DataFrame(results)
