# ShareIdea Docs

정적 문서형 사이트 생성/배포를 위한 저장소입니다.

## 빠른 시작

1. Python 3.10+ 설치
2. 의존성 설치
   - `python -m pip install markdown`
3. 빌드 실행
   - `python scripts/build_docs.py`

## 디렉터리 구조

```text
/
  README.md
  .nojekyll
  /site
    /docs
      /ai-presentation
        pb-tier-system.md
      index.md
    /assets
      styles.css
      site.js
    /dist
  /scripts
    build_docs.py
    deploy_pages.ps1
    deploy_pages.sh
  /templates
    base.html
  /config
    site.json
```

## 빌드 명령

```bash
python scripts/build_docs.py
```

성공 시 `site/dist/index.html`, `site/dist/ai-presentation/pb-tier-system.html`가 생성됩니다.

## 배포 방법

### 1) 수동 배포 (Windows PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/deploy_pages.ps1
```

커밋 메시지 지정:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/deploy_pages.ps1 -Message "docs: update pages"
```

### 2) 수동 배포 (macOS/Linux)

```bash
bash scripts/deploy_pages.sh
```

커밋 메시지 지정:

```bash
bash scripts/deploy_pages.sh "docs: update pages"
```

### 3) GitHub Actions 자동 배포

- `main` 브랜치 push 시 `.github/workflows/pages.yml`이 문서를 빌드해 GitHub Pages에 배포합니다.
- 기존 Pages 배포 방식이 있다면, 워크플로 상단 주석을 참고해 옵션으로만 활성화하세요.

## 새 문서 추가 규칙

1. `site/docs` 아래에 `.md` 파일 추가
2. 내부 링크는 `.md`로 작성 가능 (빌드 시 `.html` 자동 변환)
3. 새 문서를 상단 메뉴에 노출하려면 `config/site.json`의 `navigation`에 등록
4. 재빌드: `python scripts/build_docs.py`

예시:

```text
site/docs/research/weekly-note.md
```

`config/site.json`:

```json
{ "title": "Weekly Note", "path": "research/weekly-note.html" }
```

## 향후 확장(B) 로드맵 (계획)

문서 사이트 파이프라인 위에 아래 구조로 단계 확장 가능합니다.

```text
/apps
  /api      # FastAPI + SQLAlchemy + Alembic
  /web      # 대시보드 프론트엔드
/packages
  /shared   # 공통 스키마/유틸
/infra
  /docker   # 로컬 개발/배포 템플릿
```

현재 단계에서는 서버/DB/API를 생성하지 않고, 문서 파이프라인만 유지합니다.
