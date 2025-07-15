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
            'naver': {
                'breaking': 'https://news.naver.com/section/rss?sid=001',
                'politics': 'https://news.naver.com/section/rss?sid=100',
                'economy': 'https://news.naver.com/section/rss?sid=101',
                'society': 'https://news.naver.com/section/rss?sid=102',
                'tech': 'https://news.naver.com/section/rss?sid=105',
            }
        }
        self.output_dir = Path('news_data')
        self.output_dir.mkdir(exist_ok=True)
    
    def collect_rss_feed(self, url: str) -> List[Dict[str, Any]]:
        """Collect news from a single RSS feed"""
        try:
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries[:10]:  # Limit to 10 articles per feed
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('description', ''),
                    'published': entry.get('published', ''),
                    'source': feed.feed.get('title', ''),
                }
                articles.append(article)
            
            return articles
        except Exception as e:
            print(f"Error collecting from {url}: {e}")
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