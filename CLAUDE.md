# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KONA (Korean Open News by AI) is an open-source AI-powered news generation platform focused on Korean news. The project aims to create transparent, factual news content using AI while maintaining minimal advertising for sustainability.

## Technology Stack

- **Backend**: Python 3.10+
- **AI Integration**: Claude API, GPT-4 API (optional)
- **Web Scraping**: BeautifulSoup, Requests
- **Template Engine**: Jinja2
- **Frontend**: HTML/CSS, JavaScript
- **Infrastructure**: GitHub Actions (CI/CD), Cloudflare Pages (hosting)
- **Testing**: Pytest

## Project Structure

```
kona-news/
├── .github/
│   └── workflows/      # GitHub Actions automation
├── scripts/            # Python scripts for news collection and AI generation
├── docs/              # Documentation
├── tests/             # Test files (Pytest)
├── templates/         # Jinja2 HTML templates
├── static/            # CSS, JavaScript files
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Key Commands

Once the project is set up, use these commands:

```bash
# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run news collection script
python scripts/collect_news.py

# Generate news articles
python scripts/generate_articles.py

# Build and deploy (via GitHub Actions)
# Triggered automatically on push to main branch
```

# Run python code automatically
to run a code for yourself, run conda run -n kona python xxx.py


## Architecture Overview

1. **News Collection Module** (`scripts/collect_news.py`): Fetches RSS feeds from Korean news sources (Naver, Daum)
2. **Research Module** (`scripts/research.py`): Cross-validates news from multiple sources
3. **AI Generation Module** (`scripts/generate_articles.py`): Uses Claude/GPT-4 API to generate articles
4. **Template Rendering** (`scripts/render_html.py`): Uses Jinja2 to create HTML pages
5. **GitHub Actions Workflows** (`.github/workflows/`): Automates daily news generation and deployment

## Development Phases

The project follows a 4-phase development plan:
- **Phase 1**: MVP with basic news collection and Claude API integration
- **Phase 2**: Multi-source collection and responsive design
- **Phase 3**: Community features and contributor guidelines
- **Phase 4**: Advanced features including multiple AI models and customization

## API Configuration

Store API keys as GitHub Secrets:
- `CLAUDE_API_KEY`: For Claude API access
- `GPT4_API_KEY`: For GPT-4 API access (optional)
- `CLOUDFLARE_API_TOKEN`: For deployment to Cloudflare Pages

## Important Notes

- The project is currently in planning phase with no code implementation yet
- Focus on creating transparent, factual news content
- Maintain minimal advertising (single Google AdSense banner)
- All contributions should follow the open-source model
- Target audience is Korean readers interested in AI-generated news
- To run python code, use conda -n kona xxx
