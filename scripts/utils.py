#!/usr/bin/env python3
"""
Utility functions for KONA project
"""

import os
import time
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
def setup_logging(name: str = "kona") -> logging.Logger:
    """Set up logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(name)


class APIKeyManager:
    """Manage API keys for different services"""
    
    def __init__(self):
        self.claude_key = os.getenv('CLAUDE_API_KEY')
        self.gpt4_key = os.getenv('GPT4_API_KEY')
        self.active_model = os.getenv('AI_MODEL', 'claude').lower()
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    def get_active_key(self) -> Optional[str]:
        """Get the API key for the active model"""
        if self.active_model == 'claude':
            return self.claude_key
        elif self.active_model in ['gpt4', 'gpt-4.1-nano']:
            return self.gpt4_key
        return None
    
    def has_valid_key(self) -> bool:
        """Check if a valid API key exists"""
        return self.get_active_key() is not None


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, calls_per_minute: int = 10):
        self.calls_per_minute = calls_per_minute
        self.calls = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        # Remove calls older than 1 minute
        self.calls = [call_time for call_time in self.calls if now - call_time < 60]
        
        if len(self.calls) >= self.calls_per_minute:
            # Wait until the oldest call is more than 1 minute old
            sleep_time = 60 - (now - self.calls[0]) + 1
            if sleep_time > 0:
                logging.info(f"Rate limit reached. Waiting {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
        
        self.calls.append(now)


def clean_text(text: str) -> str:
    """Clean text for processing"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Remove HTML tags if any
    import re
    text = re.sub(r'<[^>]+>', '', text)
    
    return text.strip()


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    
    # Find the last complete sentence within the limit
    sentences = text[:max_length].split('.')
    if len(sentences) > 1:
        return '.'.join(sentences[:-1]) + '.'
    
    # If no sentence boundary, truncate at word boundary
    words = text[:max_length].split()
    return ' '.join(words[:-1]) + '...'


def load_latest_news_data() -> Optional[Dict[str, Any]]:
    """Load the most recent news data file"""
    import json
    
    news_dir = Path("news_data")
    if not news_dir.exists():
        return None
    
    # Find the most recent news file
    news_files = sorted(news_dir.glob("news_*.json"), reverse=True)
    if not news_files:
        return None
    
    latest_file = news_files[0]
    logging.info(f"Loading news data from: {latest_file}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading news data: {e}")
        return None


def save_generated_article(article: Dict[str, Any], output_dir: Path = Path("generated_articles")) -> str:
    """Save a generated article to file"""
    import json
    
    output_dir.mkdir(exist_ok=True)
    
    # Create filename from title and timestamp
    safe_title = "".join(c for c in article['title'] if c.isalnum() or c in (' ', '-', '_'))[:50]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = output_dir / f"{safe_title}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    
    return str(filename)