# ShareIdea 문서 사이트

이 사이트는 Markdown 문서를 HTML로 변환해 GitHub Pages로 배포합니다.

## 사용법

- 빌드: `python scripts/build_docs.py`
- 결과: `site/dist` 폴더
- 배포: `scripts/deploy_pages.ps1` 또는 `scripts/deploy_pages.sh`

## 새 문서 추가 절차

1. `site/docs` 아래에 새 `.md` 파일 생성
2. 내부 참조는 상대 경로 `.md` 링크로 작성
3. `config/site.json`의 `navigation`에 메뉴 추가
4. `python scripts/build_docs.py` 실행

## 주요 문서

- [PB 티어링 시스템 설계 문서](ai-presentation/pb-tier-system.md)

> 빌드 시 내부 `.md` 링크는 자동으로 `.html`로 변환됩니다.
