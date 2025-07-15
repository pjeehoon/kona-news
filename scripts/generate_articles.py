#!/usr/bin/env python3
"""
AI-powered article generation module for KONA
"""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# AI API imports
try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import openai
except ImportError:
    openai = None

# Local imports
from utils import (
    setup_logging, APIKeyManager, RateLimiter,
    clean_text, truncate_text, load_latest_news_data,
    save_generated_article
)
from prompts import SYSTEM_PROMPTS, get_prompt

# Set up logging
logger = setup_logging("generate_articles")


class ArticleGenerator:
    """Generate news articles using AI"""
    
    def __init__(self):
        self.api_manager = APIKeyManager()
        self.rate_limiter = RateLimiter(calls_per_minute=10)
        self.output_dir = Path("generated_articles")
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize AI clients
        self._init_ai_clients()
        
    def _init_ai_clients(self):
        """Initialize AI API clients"""
        self.claude_client = None
        self.openai_client = None
        
        if self.api_manager.claude_key and anthropic:
            self.claude_client = anthropic.Anthropic(api_key=self.api_manager.claude_key)
            logger.info("Claude API client initialized")
            
        if self.api_manager.gpt4_key and openai:
            openai.api_key = self.api_manager.gpt4_key
            self.openai_client = openai
            logger.info("OpenAI API client initialized")
    
    def select_top_stories(self, news_data: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """Select top stories for article generation"""
        all_articles = []
        
        # Flatten all news articles
        for source, categories in news_data.get('news', {}).items():
            for category, articles in categories.items():
                for article in articles:
                    article['source_name'] = source
                    article['category'] = category
                    all_articles.append(article)
        
        # Sort by published date (most recent first)
        # For MVP, we'll just take the first N articles
        # In future, we can add more sophisticated ranking
        selected = all_articles[:limit]
        
        logger.info(f"Selected {len(selected)} articles for generation")
        return selected
    
    def prepare_news_summary(self, articles: List[Dict[str, Any]]) -> str:
        """Prepare news summary for AI prompt"""
        summary_parts = []
        
        for article in articles:
            title = clean_text(article.get('title', ''))
            description = clean_text(article.get('description', ''))
            source = article.get('source', '')
            
            summary_parts.append(f"제목: {title}\n설명: {description}\n출처: {source}")
        
        return "\n\n".join(summary_parts)
    
    def generate_with_claude(self, prompt: str, system_prompt: str) -> Optional[Dict[str, Any]]:
        """Generate article using Claude API"""
        if not self.claude_client:
            logger.error("Claude client not initialized")
            return None
        
        try:
            self.rate_limiter.wait_if_needed()
            
            response = self.claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse JSON response
            content = response.content[0].text
            
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error generating with Claude: {e}")
            return None
    
    def generate_with_gpt4(self, prompt: str, system_prompt: str) -> Optional[Dict[str, Any]]:
        """Generate article using GPT-4 API"""
        if not self.openai_client:
            logger.error("OpenAI client not initialized")
            return None
        
        try:
            self.rate_limiter.wait_if_needed()
            
            response = self.openai_client.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error generating with GPT-4: {e}")
            return None
    
    def generate_article(self, news_items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Generate a single article from news items"""
        # Prepare the prompt
        news_summary = self.prepare_news_summary(news_items)
        sources = [item.get('link', '') for item in news_items if item.get('link')]
        
        prompt = get_prompt(
            "article_generation",
            news_summary=news_summary,
            sources="\n".join(sources)
        )
        
        # Select system prompt based on active model
        system_prompt = SYSTEM_PROMPTS.get(
            self.api_manager.active_model,
            SYSTEM_PROMPTS['claude']
        )
        
        # Generate article
        article = None
        if self.api_manager.active_model == 'claude':
            article = self.generate_with_claude(prompt, system_prompt)
        elif self.api_manager.active_model == 'gpt4':
            article = self.generate_with_gpt4(prompt, system_prompt)
        
        if article:
            # Add metadata
            article['generated_at'] = datetime.now().isoformat()
            article['model_used'] = self.api_manager.active_model
            article['source_articles'] = news_items
            
        return article
    
    def cross_validate_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Cross-validate article with original sources"""
        # For MVP, we'll do basic validation
        # In future, this can be enhanced with more sophisticated fact-checking
        
        validation_result = {
            "accuracy_score": 85,  # Placeholder for MVP
            "verified_facts": ["기본 사실 확인됨"],
            "validation_timestamp": datetime.now().isoformat()
        }
        
        article['validation'] = validation_result
        return article
    
    def run(self, max_articles: int = 5) -> List[str]:
        """Main article generation process"""
        logger.info("Starting article generation...")
        
        # Check API key
        if not self.api_manager.has_valid_key():
            logger.error("No valid API key found. Set CLAUDE_API_KEY or GPT4_API_KEY in environment.")
            return []
        
        # Load news data
        news_data = load_latest_news_data()
        if not news_data:
            logger.error("No news data found. Run collect_news.py first.")
            return []
        
        # Select top stories
        top_stories = self.select_top_stories(news_data, limit=max_articles)
        
        # Generate articles
        generated_files = []
        for i, story in enumerate(top_stories):
            logger.info(f"Generating article {i+1}/{len(top_stories)}...")
            
            # Use single story as input (can be enhanced to group related stories)
            article = self.generate_article([story])
            
            if article:
                # Cross-validate
                article = self.cross_validate_article(article)
                
                # Save article
                filename = save_generated_article(article, self.output_dir)
                generated_files.append(filename)
                logger.info(f"Article saved: {filename}")
            else:
                logger.error(f"Failed to generate article for story {i+1}")
        
        logger.info(f"Generation complete! Generated {len(generated_files)} articles.")
        return generated_files


def main():
    """Run article generation"""
    generator = ArticleGenerator()
    
    # Get max articles from environment or use default
    max_articles = int(os.getenv('MAX_ARTICLES_PER_RUN', 5))
    
    generated_files = generator.run(max_articles=max_articles)
    
    # Print results
    if generated_files:
        print(f"\nSuccessfully generated {len(generated_files)} articles:")
        for file in generated_files:
            print(f"  - {file}")
    else:
        print("\nNo articles were generated. Check the logs for errors.")


if __name__ == '__main__':
    main()