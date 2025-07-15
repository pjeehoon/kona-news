# KONA - Korean Open News by AI

🤖 Open-source AI-powered Korean news generation platform

## 소개 (Introduction)

KONA는 AI 기술을 활용하여 한국 뉴스를 자동으로 수집, 분석, 생성하는 오픈소스 플랫폼입니다. 투명하고 사실적인 뉴스 콘텐츠를 제공하며, 최소한의 광고로 지속 가능한 운영을 목표로 합니다.

KONA is an open-source platform that automatically collects, analyzes, and generates Korean news using AI technology. It aims to provide transparent and factual news content while maintaining sustainability with minimal advertising.

## 주요 기능 (Key Features)

- 🔍 **다중 소스 뉴스 수집**: Naver, Daum 등 주요 한국 뉴스 소스에서 자동 수집
- 🤖 **AI 기반 기사 생성**: Claude API와 GPT-4를 활용한 고품질 뉴스 작성
- ✅ **교차 검증 시스템**: 여러 소스를 통한 사실 확인 및 신뢰도 향상
- 📱 **반응형 웹 디자인**: 모든 기기에서 최적화된 읽기 경험
- 🌏 **오픈소스**: 투명한 개발 과정과 커뮤니티 기여 환영

## 기술 스택 (Tech Stack)

- **Backend**: Python 3.10+
- **AI Models**: Claude API, GPT-4 API
- **Web Scraping**: BeautifulSoup, Requests
- **Template Engine**: Jinja2
- **Frontend**: HTML/CSS, JavaScript
- **CI/CD**: GitHub Actions
- **Hosting**: Cloudflare Pages

## 시작하기 (Getting Started)

### 요구사항 (Requirements)

- Python 3.10 이상
- Claude API 키 또는 GPT-4 API 키
- GitHub 계정
- Cloudflare 계정 (배포용)

### 설치 (Installation)

```bash
# 저장소 클론
git clone https://github.com/pjeehoon/kona-news.git
cd kona-news

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에 API 키 추가
```

### 사용법 (Usage)

```bash
# 뉴스 수집
python scripts/collect_news.py

# 기사 생성
python scripts/generate_articles.py

# 테스트 실행
pytest
```

## 개발 로드맵 (Development Roadmap)

### Phase 1: MVP (1-2주)
- [x] 프로젝트 구조 설정
- [ ] 기본 뉴스 수집 모듈
- [ ] Claude API 통합
- [ ] 간단한 HTML 템플릿
- [ ] GitHub Actions 자동화

### Phase 2: 핵심 기능 (3-4주)
- [ ] 다중 소스 뉴스 수집
- [ ] 고급 연구 모듈
- [ ] 반응형 웹 디자인
- [ ] 카테고리별 뉴스 분류

### Phase 3: 커뮤니티 (5-6주)
- [ ] 기여자 가이드라인
- [ ] 이슈 템플릿
- [ ] PR 검증 시스템
- [ ] API 사용량 모니터링

### Phase 4: 고급 기능 (7-8주)
- [ ] 다중 AI 모델 지원
- [ ] 독자 맞춤 설정
- [ ] 뉴스 아카이브 시스템
- [ ] 통계 대시보드

## 기여하기 (Contributing)

KONA는 오픈소스 프로젝트로 모든 기여를 환영합니다! 자세한 내용은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참조해주세요.

## 라이선스 (License)

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조해주세요.

## 연락처 (Contact)

- 프로젝트 관리자: [@pjeehoon](https://github.com/pjeehoon)
- 이슈 트래커: [GitHub Issues](https://github.com/pjeehoon/kona-news/issues)

---

**KONA** - AI로 만드는 투명한 한국 뉴스 플랫폼 🇰🇷