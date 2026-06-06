import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import math

# 한글 폰트 설정 (Windows 기본 맑은 고딕)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 저장될 폴더 경로 설정
OUTPUT_DIR = r"c:\Users\sungj\OneDrive\Desktop\플코 2\frontend\public\artifacts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 축구장 그리기 함수
def draw_pitch(ax):
    ax.plot([0, 0, 105, 105, 0], [0, 68, 68, 0, 0], color='black', linewidth=2)
    ax.plot([52.5, 52.5], [0, 68], color='black', linewidth=2)
    ax.plot([0, 16.5, 16.5, 0], [13.84, 13.84, 54.16, 54.16], color='black')
    ax.plot([105, 88.5, 88.5, 105], [13.84, 13.84, 54.16, 54.16], color='black')
    ax.plot([0, 5.5, 5.5, 0], [24.84, 24.84, 43.16, 43.16], color='black')
    ax.plot([105, 99.5, 99.5, 105], [24.84, 24.84, 43.16, 43.16], color='black')
    circle = plt.Circle((52.5, 34), 9.15, color='black', fill=False)
    ax.add_patch(circle)
    ax.set_xlim(-5, 110)
    ax.set_ylim(-5, 73)
    ax.axis('off')

# 1. 공간 생산 지수 (Space Creation) - Pitch Control / Heatmap
def plot_space_creation():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    draw_pitch(ax)
    
    # 가상의 중원 및 측면 공간 점유 데이터
    np.random.seed(1)
    x = np.random.normal(52.5, 15, 300)
    y = np.concatenate([np.random.normal(15, 5, 150), np.random.normal(53, 5, 150)])
    x = np.clip(x, 10, 95)
    
    sns.kdeplot(x=x, y=y, cmap="Greens", fill=True, alpha=0.7, ax=ax, levels=12)
    plt.title("전술 분석 01: 공간 창출 지수 (중원 및 측면 공간 장악력)", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "tactical_space.png"), dpi=300, bbox_inches='tight')
    plt.close()

# 2. 역습 지수 (Counter Attack Threat) - Quiver Vectors
def plot_counter_threat():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    draw_pitch(ax)
    
    # 역습 패스 및 스프린트 벡터
    np.random.seed(2)
    start_x = np.random.uniform(20, 40, 10)
    start_y = np.random.uniform(10, 58, 10)
    end_x = start_x + np.random.uniform(40, 50, 10)
    end_y = start_y + np.random.uniform(-10, 10, 10)
    
    for sx, sy, ex, ey in zip(start_x, start_y, end_x, end_y):
        ax.annotate("", xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle="->", color="red", lw=3, alpha=0.9))
        ax.scatter(sx, sy, color='blue', s=40, zorder=5)
        
    plt.title("전술 분석 02: 역습 전개 및 스프린트 벡터 분석", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "tactical_counter.png"), dpi=300, bbox_inches='tight')
    plt.close()

# 3. 세트피스도 (Setpiece Vulnerability) - Penalty Box Density
def plot_setpiece():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    draw_pitch(ax)
    
    # 코너킥 시 페널티 박스(우측) 안의 선수 밀집도
    np.random.seed(3)
    x = np.random.normal(95, 3, 200)
    y = np.random.normal(34, 6, 200)
    x = np.clip(x, 88.5, 105)
    
    sns.kdeplot(x=x, y=y, cmap="Reds", fill=True, alpha=0.85, ax=ax, levels=15)
    ax.scatter(x[:20], y[:20], color='yellow', edgecolor='black', s=60, label="수비수 밀집")
    
    plt.title("전술 분석 03: 세트피스 취약도 (페널티 박스 밀집 구역)", fontsize=16, fontweight='bold')
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "tactical_setpiece.png"), dpi=300, bbox_inches='tight')
    plt.close()

# 4. 약점x강점 매칭 (Weakness x Strength Matchup) - Radar/Polar Chart
def plot_matchup():
    labels = np.array(['빌드업 전개', '전방 압박', '공수 전환', '골 결정력', '세트피스 수비', '수비 조직력'])
    num_vars = len(labels)
    
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    # 우리팀 데이터
    values_us = [80, 65, 90, 70, 45, 85]
    values_us += values_us[:1]
    
    # 상대팀 데이터
    values_them = [60, 85, 55, 80, 75, 60]
    values_them += values_them[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    ax.plot(angles, values_us, color='blue', linewidth=2, label='우리 팀 (강점)')
    ax.fill(angles, values_us, color='blue', alpha=0.25)
    
    ax.plot(angles, values_them, color='red', linewidth=2, linestyle='dashed', label='상대 팀 (약점)')
    ax.fill(angles, values_them, color='red', alpha=0.25)
    
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12, fontweight='bold')
    
    plt.title("전술 분석 04: 양 팀 전술 상성 및 약점 매칭", fontsize=16, fontweight='bold', pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "tactical_matchup.png"), dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating Matplotlib Analysis for the 4 Tactic Cards...")
    plot_space_creation()
    plot_counter_threat()
    plot_setpiece()
    plot_matchup()
    print(f"Successfully saved 4 images to: {OUTPUT_DIR}")
