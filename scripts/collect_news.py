#!/usr/bin/env python3
"""
News collection module - Collects news from RSS feeds without using AI APIs
This can be safely run by anyone without incurring costs
"""

import feedparser
import json
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any


class NewsCollector:
    """Collects news from Korean news sources without API usage"""
    
    def __init__(self):
        self.sources = {
            # Working RSS feeds for Korean news
            'yonhap': {
                'all_news': 'https://en.yna.co.kr/RSS/news.xml',
            },
            'google_news_kr': {
                'top_stories': 'https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko',
                'business': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR:ko',
                'technology': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR:ko',
                'entertainment': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR:ko',
                'sports': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR:ko',
            }
        }
        self.output_dir = Path('news_data')
        self.output_dir.mkdir(exist_ok=True)
    
    def collect_rss_feed(self, url: str) -> List[Dict[str, Any]]:
        """Collect news from a single RSS feed"""
        try:
            feed = feedparser.parse(url)
            
            # Check for HTTP errors
            if hasattr(feed, 'status'):
                if feed.status >= 400:
                    print(f"  HTTP Error {feed.status} for {url}")
                    return []
                    
            # Check if feed has entries
            if not hasattr(feed, 'entries') or len(feed.entries) == 0:
                print(f"  No entries found in feed: {url}")
                return []
            
            articles = []
            
            for entry in feed.entries[:10]:  # Limit to 10 articles per feed
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('description', ''),
                    'published': entry.get('published', ''),
                    'source': feed.feed.get('title', '') if hasattr(feed, 'feed') else '',
                }
                articles.append(article)
            
            return articles
        except Exception as e:
            print(f"  Exception collecting from {url}: {e}")
            return []
    
    def collect_all_news(self) -> Dict[str, List[Dict[str, Any]]]:
        """Collect news from all configured sources"""
        all_news = {}
        
        for source, categories in self.sources.items():
            all_news[source] = {}
            for category, url in categories.items():
                print(f"Collecting {category} news from {source}...")
                articles = self.collect_rss_feed(url)
                all_news[source][category] = articles
                print(f"  Collected {len(articles)} articles")
        
        return all_news
    
    def save_news_data(self, news_data: Dict[str, Any]) -> str:
        """Save collected news to JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.output_dir / f'news_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        print(f"\nNews data saved to: {filename}")
        return str(filename)
    
    def run(self) -> str:
        """Main collection process"""
        print("Starting news collection...")
        print("=" * 50)
        
        news_data = self.collect_all_news()
        
        # Add metadata
        metadata = {
            'collected_at': datetime.now().isoformat(),
            'total_articles': sum(
                len(articles) 
                for source in news_data.values() 
                for articles in source.values()
            )
        }
        
        final_data = {
            'metadata': metadata,
            'news': news_data
        }
        
        filename = self.save_news_data(final_data)
        
        print("\nCollection complete!")
        print(f"Total articles collected: {metadata['total_articles']}")
        
        return filename


def main():
    """Run news collection"""
    collector = NewsCollector()
    collector.run()


if __name__ == '__main__':
    main()