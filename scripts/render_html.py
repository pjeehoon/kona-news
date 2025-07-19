#!/usr/bin/env python3
"""
Render HTML pages from generated articles using Jinja2 templates.
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

def load_articles(articles_dir="generated_articles"):
    """Load all generated articles from JSON files."""
    articles = []
    articles_path = Path(articles_dir)
    
    if not articles_path.exists():
        print(f"Articles directory '{articles_dir}' not found.")
        return articles
    
    for json_file in articles_path.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                article = json.load(f)
                articles.append(article)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    # Sort articles by date (newest first)
    articles.sort(key=lambda x: x.get('published_date', ''), reverse=True)
    return articles

def setup_jinja_env():
    """Set up Jinja2 environment with templates directory."""
    templates_dir = Path("templates")
    if not templates_dir.exists():
        templates_dir.mkdir(parents=True)
        create_default_templates(templates_dir)
    
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    return env

def create_default_templates(templates_dir):
    """Create default templates if they don't exist."""
    # Create base template
    base_template = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}KONA - Korean Open News by AI{% endblock %}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <header>
        <h1>KONA</h1>
        <p>Korean Open News by AI</p>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2024 KONA. Open source AI-powered news.</p>
    </footer>
</body>
</html>'''
    
    # Create index template
    index_template = '''{% extends "base.html" %}

{% block title %}KONA - AI로 만드는 투명한 뉴스{% endblock %}

{% block content %}
<h2>최신 뉴스</h2>
<div class="articles">
    {% for article in articles %}
    <article>
        <h3><a href="/articles/{{ article.id }}.html">{{ article.title }}</a></h3>
        <p class="meta">{{ article.published_date }} | {{ article.category }}</p>
        <p>{{ article.summary }}</p>
    </article>
    {% endfor %}
</div>
{% endblock %}'''
    
    # Create article template
    article_template = '''{% extends "base.html" %}

{% block title %}{{ article.title }} - KONA{% endblock %}

{% block content %}
<article class="full-article">
    <h2>{{ article.title }}</h2>
    <p class="meta">{{ article.published_date }} | {{ article.category }}</p>
    
    <div class="content">
        {{ article.content | safe }}
    </div>
    
    {% if article.sources %}
    <div class="sources">
        <h3>출처</h3>
        <ul>
            {% for source in article.sources %}
            <li><a href="{{ source.url }}" target="_blank">{{ source.title }}</a></li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}
</article>

<a href="/">← 목록으로 돌아가기</a>
{% endblock %}'''
    
    # Write templates
    (templates_dir / "base.html").write_text(base_template, encoding='utf-8')
    (templates_dir / "index.html").write_text(index_template, encoding='utf-8')
    (templates_dir / "article.html").write_text(article_template, encoding='utf-8')
    print("Created default templates")

def create_default_css():
    """Create default CSS file."""
    css_content = '''/* KONA Default Styles */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
}

header {
    text-align: center;
    margin-bottom: 40px;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

header h1 {
    color: #0066cc;
    margin: 0;
}

header p {
    color: #666;
    margin: 5px 0 0 0;
}

main {
    background-color: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.articles article {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid #eee;
}

.articles article:last-child {
    border-bottom: none;
}

h2, h3 {
    color: #333;
}

a {
    color: #0066cc;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.meta {
    color: #666;
    font-size: 0.9em;
}

.sources {
    margin-top: 40px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
}

footer {
    text-align: center;
    margin-top: 40px;
    color: #666;
    font-size: 0.9em;
}'''
    
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    (static_dir / "style.css").write_text(css_content, encoding='utf-8')
    print("Created default CSS")

def render_pages(articles):
    """Render HTML pages from articles."""
    env = setup_jinja_env()
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Create static directory in output
    output_static = output_dir / "static"
    output_static.mkdir(exist_ok=True)
    
    # Copy CSS file
    if not Path("static/style.css").exists():
        create_default_css()
    
    css_source = Path("static/style.css")
    if css_source.exists():
        (output_static / "style.css").write_text(
            css_source.read_text(encoding='utf-8'),
            encoding='utf-8'
        )
    
    # Render index page
    index_template = env.get_template("index.html")
    index_html = index_template.render(articles=articles)
    (output_dir / "index.html").write_text(index_html, encoding='utf-8')
    print(f"Generated index.html")
    
    # Create articles directory
    articles_dir = output_dir / "articles"
    articles_dir.mkdir(exist_ok=True)
    
    # Render individual article pages
    article_template = env.get_template("article.html")
    for article in articles:
        if 'id' in article:
            article_html = article_template.render(article=article)
            article_file = articles_dir / f"{article['id']}.html"
            article_file.write_text(article_html, encoding='utf-8')
            print(f"Generated {article['id']}.html")
    
    print(f"\nSuccessfully rendered {len(articles)} articles to {output_dir}")

def main():
    """Main function."""
    print("Starting HTML rendering...")
    
    # Load articles
    articles = load_articles()
    
    if not articles:
        print("No articles found to render.")
        return 0
    
    print(f"Found {len(articles)} articles to render")
    
    # Render pages
    try:
        render_pages(articles)
        return 0
    except Exception as e:
        print(f"Error during rendering: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())