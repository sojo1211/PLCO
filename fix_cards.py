"""
MatchDetail.jsx에서 중복 구 카드 섹션 제거 스크립트
- 새 다크테마 카드(01~04)는 유지
- 뒤에 남은 구 라이트테마 카드(과제 1~4) 잔재 제거
"""
import os

file_path = r"C:\Users\sungj\OneDrive\Desktop\플코 진\match_intelligence\frontend\src\components\MatchDetail.jsx"

with open(file_path, "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

print(f"총 줄 수: {len(lines)}")

# "실시간 전술 HUD 분석 프로세스 이미지 섹션" 주석이 두 번 나오는 위치 찾기
MARKER = "실시간 전술 HUD 분석 프로세스 이미지 섹션"
marker_positions = [i for i, l in enumerate(lines) if MARKER in l]
print(f"HUD 주석 위치(줄번호): {[p+1 for p in marker_positions]}")

if len(marker_positions) >= 2:
    # 첫 번째(가짜, 구 카드 사이에 낀 것)부터 두 번째(진짜) 직전까지 삭제
    del_from = marker_positions[0]
    del_to   = marker_positions[1]   # 이 줄은 유지
    removed  = del_to - del_from
    print(f"삭제 범위: {del_from+1}줄 ~ {del_to}줄 ({removed}줄 제거)")
    
    new_lines = lines[:del_from] + lines[del_to:]
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("✅ 중복 구 카드 제거 완료!")
    print(f"   파일 크기: {len(lines)}줄 → {len(new_lines)}줄")

elif len(marker_positions) == 1:
    print("이미 정리된 상태 – 작업 불필요")

else:
    # 주석이 없으면 다른 방법으로 구 카드 탐색
    print("HUD 주석을 찾을 수 없음. 구 카드 잔재 직접 탐색...")
    for i, l in enumerate(lines):
        if "과제 1. 교체 직후 전술 변화" in l or \
           ("f8fafc" in l and "justifyContent: 'space-between'" in l and i > 1700):
            print(f"  잔재 발견 줄 {i+1}: {l[:80].strip()}")
