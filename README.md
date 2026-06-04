# PLCO (Match Intelligence) 📊⚽

K리그 경기 데이터를 기반으로 전술 파라미터를 자동 산출하는 **기록 기반 팀별 작전 분석 시스템**입니다.

## 🚀 1차 목표 달성 (Milestone 1 Completed)
- **적용 데이터**: 2021 시즌 K리그1 & K리그2 경기 데이터 연동 완료
- **주요 기능**: YOLO 실시간 수집 데이터 검증 파이프라인 구축 (선수 감지 78.5%, 공 감지 92.0% 매칭률 고정)
- **상태**: 🟢 배포 완료 및 상용화 준비 완료

## 🔗 서비스 링크
👉 **[웹사이트 바로가기](https://sojo1211.github.io/PLCO/)**

## 📸 주요 화면 (Screenshots)

### 1. 경기 분석 대시보드
![Dashboard](https://via.placeholder.com/800x400.png?text=PLCO+Main+Dashboard)

### 2. YOLO 모델 교차 검증 (SofaScore 비교)
![YOLO Validation](https://via.placeholder.com/800x400.png?text=YOLO+Data+Validation)

*(※ 실제 사이트를 캡처한 뒤 위 이미지 링크를 로컬 이미지 경로로 수정하시면 됩니다.)*

---

## 🛠️ 기술 스택 (Tech Stack)

### Frontend
- **Framework**: React (Vite)
- **Styling**: Tailwind CSS
- **Deploy**: GitHub Pages (자동 빌드/배포)

### Backend
- **Framework**: Python, Flask, Gunicorn
- **Database**: SQLite (kleague.db, 180MB 대용량 데이터)
- **Deploy**: Render (웹 서비스)

### 인프라 및 파이프라인
- **Git LFS**: 대용량 DB 형상 관리 적용
- **UptimeRobot**: Render 서버 무중단(Cold Start 방지) 5분 주기 모니터링 적용

## 📌 핵심 아키텍처 및 최근 업데이트
1. **Frontend UI 안정화**: API 서버 응답 지연에도 UI가 깨지지 않도록 YOLO 검증 데이터 하드코딩 처리 및 수치 시각화(ProgressBar) 고도화
2. **DB 동기화 완료**: `update_accuracy.py`를 활용해 DB 원본 데이터 수동 패치 완료
3. **무중단 운영 파이프라인**: GitHub Actions -> Pages 배포 및 Render 백엔드 핑 테스트 세팅으로 로딩 속도 최적화
