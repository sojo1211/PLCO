import { useState, useEffect } from 'react'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

/* ── 포메이션 데이터 ── */
const FORMATION_POSITIONS = {
  '4-3-3': [
    {x:50,y:8,pos:'GK'},
    {x:14,y:26,pos:'LB'},{x:37,y:25,pos:'CB'},{x:63,y:25,pos:'CB'},{x:86,y:26,pos:'RB'},
    {x:24,y:51,pos:'CM'},{x:50,y:48,pos:'CM'},{x:76,y:51,pos:'CM'},
    {x:14,y:75,pos:'LW'},{x:50,y:80,pos:'ST'},{x:86,y:75,pos:'RW'},
  ],
  '4-4-2': [
    {x:50,y:8,pos:'GK'},
    {x:14,y:26,pos:'LB'},{x:37,y:25,pos:'CB'},{x:63,y:25,pos:'CB'},{x:86,y:26,pos:'RB'},
    {x:14,y:52,pos:'LM'},{x:38,y:51,pos:'CM'},{x:62,y:51,pos:'CM'},{x:86,y:52,pos:'RM'},
    {x:36,y:79,pos:'ST'},{x:64,y:79,pos:'ST'},
  ],
  '4-2-3-1': [
    {x:50,y:8,pos:'GK'},
    {x:14,y:24,pos:'LB'},{x:37,y:23,pos:'CB'},{x:63,y:23,pos:'CB'},{x:86,y:24,pos:'RB'},
    {x:35,y:43,pos:'DM'},{x:65,y:43,pos:'DM'},
    {x:14,y:64,pos:'LW'},{x:50,y:62,pos:'AM'},{x:86,y:64,pos:'RW'},
    {x:50,y:81,pos:'ST'},
  ],
  '3-4-3': [
    {x:50,y:8,pos:'GK'},
    {x:25,y:25,pos:'CB'},{x:50,y:23,pos:'CB'},{x:75,y:25,pos:'CB'},
    {x:9,y:52,pos:'LWB'},{x:35,y:50,pos:'CM'},{x:65,y:50,pos:'CM'},{x:91,y:52,pos:'RWB'},
    {x:18,y:76,pos:'LW'},{x:50,y:81,pos:'ST'},{x:82,y:76,pos:'RW'},
  ],
  '3-5-2': [
    {x:50,y:8,pos:'GK'},
    {x:25,y:25,pos:'CB'},{x:50,y:23,pos:'CB'},{x:75,y:25,pos:'CB'},
    {x:8,y:52,pos:'LWB'},{x:30,y:50,pos:'CM'},{x:50,y:48,pos:'CM'},{x:70,y:50,pos:'CM'},{x:92,y:52,pos:'RWB'},
    {x:36,y:80,pos:'ST'},{x:64,y:80,pos:'ST'},
  ],
  '4-1-4-1': [
    {x:50,y:8,pos:'GK'},
    {x:14,y:23,pos:'LB'},{x:37,y:22,pos:'CB'},{x:63,y:22,pos:'CB'},{x:86,y:23,pos:'RB'},
    {x:50,y:38,pos:'DM'},
    {x:12,y:58,pos:'LM'},{x:35,y:56,pos:'CM'},{x:65,y:56,pos:'CM'},{x:88,y:58,pos:'RM'},
    {x:50,y:80,pos:'ST'},
  ],
}

const TACTIC_MATCHUP = {
  '고압박형': {beats:'점유율형', losesto:'카운터형', color:'#ef4444', desc:'빠른 압박으로 점유율팀 패스 차단'},
  '점유율형': {beats:'저블록형', losesto:'고압박형', color:'#3b82f6', desc:'볼 지배력으로 저블록 수비 소진'},
  '저블록형': {beats:'카운터형', losesto:'점유율형', color:'#8b5cf6', desc:'수비 블록으로 역습 공간 차단'},
  '카운터형': {beats:'고압박형', losesto:'저블록형', color:'#f59e0b', desc:'넓어진 공간 역이용 빠른 역습'},
}

/* ── 유니폼 SVG 아이콘 ── */
function JerseyIcon({ number, isGK = false, color = '#e8f0ff', size = 54 }) {
  const bg = isGK ? '#ec4899' : color
  const numColor = isGK ? '#fff' : '#19181D'
  return (
    <svg viewBox="0 0 60 68" width={size} height={size * 1.13} style={{filter:'drop-shadow(0 2px 4px rgba(0,0,0,0.4))'}}>
      <path d="M9,14 L0,33 L16,38 L16,65 L44,65 L44,38 L60,33 L51,14 L42,21 C42,21 37,26 30,26 C23,26 18,21 18,21 Z"
        fill={bg} stroke="rgba(255,255,255,0.25)" strokeWidth="1.5" />
      <text x="30" y="49" textAnchor="middle" dominantBaseline="middle"
        fill={numColor} fontSize="21" fontWeight="900" fontFamily="'Pretendard',Arial,sans-serif">
        {number}
      </text>
    </svg>
  )
}

/* ── K리그 방송 스타일 포메이션 ── */
function FormationPitch({ formation = '4-3-3', teamName = '우리팀', teamColor = '#dbeafe', players = [], subs = [], flipped = false }) {
  const positions = FORMATION_POSITIONS[formation] || FORMATION_POSITIONS['4-3-3']
  return (
    <div className="broadcast-wrap">
      {/* 좌측 팀 패널 */}
      <div className="broadcast-panel">
        <div className="broadcast-team-name">{teamName}</div>
        <div className="broadcast-formation">{formation}</div>
        {subs.length > 0 && (
          <div className="broadcast-subs">
            <div className="broadcast-subs-label">교체명단</div>
            {subs.map((s, i) => (
              <div key={i} className="broadcast-sub-row">
                <span className="bsr-num">{s.number}</span>
                <span className="bsr-name">{s.name}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 피치 */}
      <div className="broadcast-field">
        <div className="bf-center-line" />
        <div className="bf-center-circle" />
        <div className="bf-penalty-top" />
        <div className="bf-penalty-bot" />
        <div className="bf-goal-top" />
        <div className="bf-goal-bot" />
        {positions.map((pos, i) => {
          const p = players[i]
          const isGK = pos.pos === 'GK'
          const xPct = flipped ? (100 - pos.x) : pos.x
          const yPct = flipped ? pos.y : (100 - pos.y)
          return (
            <div key={i} className="bf-player" style={{left:`${xPct}%`, top:`${yPct}%`}}>
              <JerseyIcon number={p?.number ?? (i + 1)} isGK={isGK} color={teamColor} size={48} />
              <div className="bf-name">{p?.name ?? pos.pos}</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

function TacticalWheel() {
  const entries = Object.entries(TACTIC_MATCHUP)
  const cx = 120, cy = 120, r = 82
  return (
    <div className="tactical-wheel-wrap">
      <svg width="240" height="240" viewBox="0 0 240 240">
        <defs>
          <marker id="arr" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto">
            <polygon points="0,0 7,3.5 0,7" fill="rgba(255,255,255,0.7)" />
          </marker>
        </defs>
        {entries.map(([tactic, data], i) => {
          const fromA = (i * 90 - 90) * Math.PI / 180
          const toIdx = entries.findIndex(([t]) => t === data.beats)
          const toA = (toIdx * 90 - 90) * Math.PI / 180
          const x1 = cx + (r - 18) * Math.cos(fromA), y1 = cy + (r - 18) * Math.sin(fromA)
          const x2 = cx + (r - 18) * Math.cos(toA), y2 = cy + (r - 18) * Math.sin(toA)
          const mx = (x1+x2)/2 + (y2-y1)*0.28, my = (y1+y2)/2 - (x2-x1)*0.28
          return <path key={tactic} d={`M${x1},${y1} Q${mx},${my} ${x2},${y2}`}
            stroke="rgba(255,255,255,0.45)" strokeWidth="1.5" fill="none" markerEnd="url(#arr)" />
        })}
        {entries.map(([tactic, data], i) => {
          const angle = (i * 90 - 90) * Math.PI / 180
          const x = cx + r * Math.cos(angle), y = cy + r * Math.sin(angle)
          return (
            <g key={tactic}>
              <circle cx={x} cy={y} r={26} fill={data.color} fillOpacity={0.92} />
              <text x={x} y={y+4} textAnchor="middle" fill="white" fontSize="9.5" fontWeight="800">{tactic}</text>
            </g>
          )
        })}
        <circle cx={cx} cy={cy} r={24} fill="#19181D" />
        <text x={cx} y={cy-3} textAnchor="middle" fill="#8b95a1" fontSize="9" fontWeight="700">전술</text>
        <text x={cx} y={cy+9} textAnchor="middle" fill="#8b95a1" fontSize="9" fontWeight="700">상성</text>
      </svg>
    </div>
  )
}

/* ── 상수 ── */
const SCORE_STATES = [
  { value: -1, label: '뒤짐', emoji: '😰' },
  { value:  0, label: '동점', emoji: '😐' },
  { value:  1, label: '리드', emoji: '😊' },
]
const TACTICAL_COLORS = { '고압박형':'#ef4444', '점유율형':'#3b82f6', '카운터형':'#f59e0b', '저블록형':'#8b5cf6' }

function getInitials(name) {
  if (!name) return '?'
  const p = name.trim().split(' ')
  return p.length >= 2 ? (p[0][0] + p[p.length-1][0]).toUpperCase() : name.slice(0,2).toUpperCase()
}

/* ── 선수 아바타 ── */
function PlayerAvatar({ player, selected, onClick, jerseyNumber }) {
  const prob = player.goal_after_prob
  const isHot = prob >= 30
  const lastName = player.player.split(' ').slice(-1)[0]
  const shortTeam = player.team?.split(' ')[0]
  return (
    <div className={`player-avatar-card ${selected ? 'selected' : ''}`} onClick={() => onClick(player)}>
      <div className="pav-photo">
        {getInitials(player.player)}
        {isHot && <span className="pav-hot">🔥</span>}
        {jerseyNumber && <span className="pav-number">{jerseyNumber}</span>}
      </div>
      <div className="pav-info">
        <div className="pav-name">{lastName}</div>
        <div className="pav-team">{shortTeam}</div>
      </div>
      <div className={`pav-prob ${prob >= 30 ? 'high' : prob >= 20 ? 'mid' : ''}`}>{prob}%</div>
    </div>
  )
}

/* ── 메인 컴포넌트 ── */
export default function BacktestingPage() {
  const [activeAnalysisTab, setActiveAnalysisTab] = useState('technical')
  const [players, setPlayers] = useState([])
  const [jerseyNumbers, setJerseyNumbers] = useState({})
  const [selectedPlayer, setSelectedPlayer] = useState(null)
  const [minute, setMinute] = useState(67)
  const [scoreState, setScoreState] = useState(-1)
  const [simResult, setSimResult] = useState(null)
  const [simLoading, setSimLoading] = useState(false)
  const [teamFilter, setTeamFilter] = useState('전체')

  const [summary, setSummary] = useState(null)
  const [substData, setSubstData] = useState(null)
  const [timelineData, setTimelineData] = useState(null)
  const [mlClusters, setMlClusters] = useState(null)
  const [dataLoading, setDataLoading] = useState(true)
  const [rosterLoading, setRosterLoading] = useState(false)
  const [rosterPlayers, setRosterPlayers] = useState([])
  const [myFormation, setMyFormation] = useState('4-3-3')
  const [oppFormation, setOppFormation] = useState('4-4-2')
  const [myTactic, setMyTactic] = useState('고압박형')
  const [oppTactic, setOppTactic] = useState('카운터형')
  const [matchupData, setMatchupData] = useState([])
  const [tacticSubPlayer, setTacticSubPlayer] = useState(null)
  const [tacticMinute, setTacticMinute] = useState(67)
  const [tacticSimResult, setTacticSimResult] = useState(null)

  useEffect(() => {
    setDataLoading(true)
    Promise.all([
      axios.get('http://localhost:8000/api/backtest/summary'),
      axios.get('http://localhost:8000/api/backtest/substitution'),
      axios.get('http://localhost:8000/api/backtest/timeline'),
      axios.get('http://localhost:8000/api/ml/players'),
      axios.get('http://localhost:8000/api/ml/clusters'),
    ]).then(([s, sub, tl, pl, cl]) => {
      setSummary(s.data)
      setSubstData(Object.entries(sub.data).map(([label, d]) => ({ label, ...d })))
      setTimelineData(Object.entries(tl.data).map(([label, d]) => ({ label, ...d })))
      const sorted = [...pl.data].sort((a, b) => b.goal_after_prob - a.goal_after_prob)
      setPlayers(sorted)
      if (sorted.length > 0) setSelectedPlayer(sorted[0])
      setMlClusters(cl.data)
    }).finally(() => setDataLoading(false))

    axios.get('http://localhost:8000/api/players/jersey-numbers')
      .then(r => setJerseyNumbers(r.data))
      .catch(() => {})

    axios.get('http://localhost:8000/api/tactics/matchup')
      .then(r => setMatchupData(r.data))
      .catch(() => {})
  }, [])

  // 전술 선택 + 선수 투입 → 통합 승률 계산
  useEffect(() => {
    if (!tacticSubPlayer) return
    axios.get('http://localhost:8000/api/ml/simulate', {
      params: { player_in: tacticSubPlayer.player, minute: tacticMinute, score_state: 0 }
    }).then(r => setTacticSimResult(r.data)).catch(() => {})
  }, [tacticSubPlayer, tacticMinute])

  // 팀 필터 변경 시 전체 선수단 가져오기
  useEffect(() => {
    if (teamFilter === '전체') { setRosterPlayers([]); return }
    setRosterLoading(true)
    axios.get('http://localhost:8000/api/teams/roster', { params: { team: teamFilter } })
      .then(r => {
        const roster = (r.data.players || []).map(p => ({
          player: p.name,
          team: teamFilter,
          sub_count: 0,
          goal_after_prob: 0,
          avg_minute: 0,
          jersey: p.number,
          pos: p.pos,
          fromRoster: true,
        }))
        setRosterPlayers(roster)
        if (roster.length > 0) setJerseyNumbers(prev => {
          const next = { ...prev }
          roster.forEach(p => { if (p.jersey) next[p.player] = p.jersey })
          return next
        })
      })
      .catch(() => setRosterPlayers([]))
      .finally(() => setRosterLoading(false))
  }, [teamFilter])

  useEffect(() => {
    if (!selectedPlayer) return
    setSimLoading(true)
    axios.get('http://localhost:8000/api/ml/simulate', {
      params: { player_in: selectedPlayer.player, minute, score_state: scoreState }
    }).then(r => setSimResult(r.data)).finally(() => setSimLoading(false))
  }, [selectedPlayer, minute, scoreState])

  if (dataLoading) return <div className="bt-loading"><div className="spinner" /><p>전력분석관 데이터 로딩 중...</p></div>

  const teams = ['전체', ...new Set(players.map(p => p.team))]

  // 팀 필터 적용: ML데이터 + 선수단 병합 (중복 제거)
  const mlFiltered = teamFilter === '전체' ? players : players.filter(p => p.team === teamFilter)
  const mlNames = new Set(mlFiltered.map(p => p.player))
  const rosterOnly = rosterPlayers.filter(p => !mlNames.has(p.player))
  const filteredPlayers = [...mlFiltered, ...rosterOnly]

  const ANALYSIS_TABS = [
    { id: 'technical',  label: '⚽ 기술 데이터',   desc: '점유율 · 슈팅 · xG · 세트피스' },
    { id: 'tactical',   label: '🧠 전술 데이터',   desc: 'PPDA · 수비 라인 · 팀 유형' },
    { id: 'physical',   label: '💪 피지컬 데이터', desc: '교체 타이밍 · 체력 패턴' },
    { id: 'opposition', label: '🔍 상대 분석',     desc: '핵심 선수 · 약점 파악' },
  ]

  return (
    <div className="bt-page">

      {/* 요약 배너 */}
      {summary && (
        <>
          <div className="bt-summary-grid">
            <SummaryCard label="분석 경기" value={summary.total_fixtures} unit="경기" color="#00c4a1" />
            <SummaryCard label="총 이벤트" value={summary.total_events?.toLocaleString?.()} unit="건" color="#3b82f6" />
            <SummaryCard label="경기당 평균 득점" value={summary.avg_goals_per_game} unit="골" color="#f59e0b" />
            <SummaryCard label="경기당 평균 교체" value={summary.avg_substs_per_game} unit="회" color="#8b5cf6" />
          </div>
          <div className="bt-season-bar">
            <span className="bt-season-source">📦 출처: {summary.source}</span>
            <div className="bt-season-chips">
              {Object.entries(summary.by_season || {}).map(([yr, cnt]) => (
                <span key={yr} className="bt-season-chip">
                  <b>{yr}</b> {cnt}경기
                </span>
              ))}
            </div>
          </div>
        </>
      )}

      {/* 전력분석관 탭 */}
      <div className="analyst-tab-bar">
        {ANALYSIS_TABS.map(t => (
          <button key={t.id} className={`analyst-tab ${activeAnalysisTab === t.id ? 'active' : ''}`}
            onClick={() => setActiveAnalysisTab(t.id)}>
            <span className="analyst-tab-title">{t.label}</span>
            <span className="analyst-tab-desc">{t.desc}</span>
          </button>
        ))}
      </div>

      {/* ── 기술 데이터 탭 ── */}
      {activeAnalysisTab === 'technical' && (
        <div className="analysis-section">
          <div className="analysis-intro">
            <span className="analysis-category-badge">Technical Data</span>
            <p>전력분석관이 공격 효율성을 파악하는 핵심 지표 — 슈팅 · 점유율 · xG · 세트피스</p>
          </div>

          {/* xG 추정 + 슈팅 분석 */}
          <div className="tech-grid">
            <div className="bt-card tech-card">
              <div className="bt-card-header">
                <h3>xG 추정 (Expected Goals)</h3>
                <span className="bt-badge">득점 질 분석</span>
              </div>
              <p className="bt-desc">슈팅 수 대비 실제 득점으로 결정력 평가 — xG 대비 실제 득점이 낮으면 결정력 부족</p>
              {summary && (
                <div className="xg-display">
                  <div className="xg-item">
                    <span>경기당 평균 슈팅</span>
                    <b>데이터 수집 중</b>
                    <small>통계 API 연동 후 표시</small>
                  </div>
                  <div className="xg-item highlight">
                    <span>경기당 평균 득점</span>
                    <b style={{ color: '#00c4a1', fontSize: 32 }}>{summary.avg_goals_per_game}</b>
                    <small>골 / 경기</small>
                  </div>
                  <div className="xg-item">
                    <span>xG 공식</span>
                    <b style={{ fontSize: 14 }}>xG = P(goal | shot_features)</b>
                    <small>슈팅 위치 · 상황 · 수비수 위치 포함</small>
                  </div>
                </div>
              )}
            </div>

            <div className="bt-card tech-card">
              <div className="bt-card-header">
                <h3>세트피스 위협도</h3>
                <span className="bt-badge">코너킥 · 프리킥</span>
              </div>
              <p className="bt-desc">코너킥 효율 = 팀별 득점 기여율 → 세트피스 수비 집중도 파라미터 산출</p>
              <div className="setpiece-formula">
                <div className="formula-box">
                  <span>세트피스 위협도</span>
                  <code>코너킥 수 × (득점 / 코너킥)</code>
                </div>
                <div className="formula-box">
                  <span>SETPIECE_FOCUS 파라미터</span>
                  <code>위협도 높음 → 0.8~1.0</code>
                </div>
              </div>
            </div>
          </div>

          {/* 시간대별 득점 */}
          {timelineData && (
            <div className="bt-card">
              <div className="bt-card-header">
                <h3>시간대별 득점 분포</h3>
                <span className="bt-badge">기술 데이터 · 체력 패턴</span>
              </div>
              <p className="bt-desc">어느 시간대에 득점이 집중되는가 — 압박 타이밍과 체력 관리 전략의 근거</p>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={timelineData} margin={{ top:10, right:20, left:0, bottom:0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e8eaf0" />
                  <XAxis dataKey="label" tick={{ fontSize:11, fill:'#8b95a1' }} />
                  <YAxis tick={{ fontSize:12, fill:'#8b95a1' }} />
                  <Tooltip formatter={(v,_,p) => [`${v}골 (${p.payload.pct}%)`, '득점']} contentStyle={{ borderRadius:8, border:'1px solid #e8eaf0', fontSize:13 }} />
                  <Bar dataKey="goals" radius={[4,4,0,0]}>
                    {timelineData.map((e,i) => <Cell key={i} fill={e.pct>15?'#ef4444':e.pct>10?'#f59e0b':'#00c4a1'} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <div className="timeline-insight">
                <div className="ti-item red">🔴 0~15분 — 초반 압박에 취약한 팀 → 킥오프 직후 고압박 전술 유효</div>
                <div className="ti-item yellow">🟡 44~47분 — 인저리타임 집중 실점 → 후반 수비 집중 경보</div>
                <div className="ti-item green">🟢 75~90분 — 체력 저하 구간 → 우리팀 역습 집중 타이밍</div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── 전술 데이터 탭 ── */}
      {activeAnalysisTab === 'tactical' && (
        <div className="analysis-section">
          <div className="analysis-intro">
            <span className="analysis-category-badge tactical">Tactical Data</span>
            <p>팀 전체 움직임과 포메이션 — PPDA · 수비 라인 · 압박 강도 · 전술 유형 분류</p>
          </div>

          {/* PPDA 설명 카드 */}
          <div className="bt-card">
            <div className="bt-card-header">
              <h3>PPDA — 압박 강도 지표</h3>
              <span className="bt-badge">전술 데이터</span>
            </div>
            <p className="bt-desc">Passes Per Defensive Action — 상대가 패스 1번 할 때 우리의 수비 행동 횟수. 낮을수록 강한 압박</p>
            <div className="ppda-formula">
              <div className="ppda-box">
                <div className="ppda-title">PPDA 계산식</div>
                <code>PPDA = 상대 공격 3분의 2 지역 패스 수 / 우리팀 수비 행동 수</code>
                <div className="ppda-scale">
                  <span style={{color:'#00c4a1'}}>낮음(6~8)</span>
                  <span>→ 강한 압박</span>
                  <span>·</span>
                  <span>높음(12+)</span>
                  <span>→</span>
                  <span style={{color:'#ef4444'}}>저블록 수비</span>
                </div>
              </div>
              <div className="ppda-params">
                <div className="param-row"><span>PRESS_INTENSITY</span><b>파울 × 4 + 슈팅 × 1.5</b></div>
                <div className="param-row"><span>DEFENSIVE_LINE</span><b>점유율 × 0.9</b></div>
                <div className="param-row"><span>OFFSIDE_TRAP</span><b>오프사이드 빈도 × 0.15</b></div>
              </div>
            </div>
          </div>

          {/* K-means 팀 전술 유형 */}
          {mlClusters && Object.keys(mlClusters).length > 0 && (
            <div className="bt-card">
              <div className="bt-card-header">
                <h3>🎯 팀 전술 유형 자동 분류</h3>
                <span className="bt-badge">K-means 비지도학습</span>
              </div>
              <p className="bt-desc">전력분석관의 "플레이 스타일 파악" 자동화 — K리그 이벤트 패턴으로 4가지 전술 유형 분류</p>
              <div className="bt-type-legend">
                {Object.entries(TACTICAL_COLORS).map(([type, color]) => (
                  <div key={type} className="bt-legend-item">
                    <div className="bt-legend-dot" style={{ background: color }} />
                    <span>{type}</span>
                    <span className="bt-legend-count">{Object.values(mlClusters).filter(t => t.tactical_type === type).length}팀</span>
                  </div>
                ))}
              </div>
              <div className="tactical-type-grid">
                {['고압박형','점유율형','카운터형','저블록형'].map(type => {
                  const teamsOfType = Object.entries(mlClusters).filter(([,d]) => d.tactical_type === type)
                  return (
                    <div key={type} className="tactical-type-card" style={{ borderColor: TACTICAL_COLORS[type] }}>
                      <div className="ttc-header" style={{ background: TACTICAL_COLORS[type]+'22', color: TACTICAL_COLORS[type] }}>
                        {type}
                      </div>
                      <div className="ttc-teams">
                        {teamsOfType.map(([team]) => (
                          <span key={team} className="ttc-team">{team.split(' ')[0]}</span>
                        ))}
                        {teamsOfType.length === 0 && <span className="ttc-team" style={{color:'#b0b8c4'}}>없음</span>}
                      </div>
                      <div className="ttc-desc">
                        {{
                          '고압박형': '파울 多, 상대진영 슈팅 多',
                          '점유율형': '점유율 高, 코너킥 多',
                          '카운터형': '오프사이드 多, 빠른 역습',
                          '저블록형': '자진영 파울 多, 수비형 교체'
                        }[type]}
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          )}

          {/* 교체 타이밍 분석 */}
          {substData && (
            <div className="bt-card">
              <div className="bt-card-header">
                <h3>교체 타이밍별 득점·실점 확률</h3>
                <span className="bt-badge">전술 데이터</span>
              </div>
              <p className="bt-desc">PDF 설계 수치 백테스팅 — "45~55분 교체 → 득점 확률 +12%" 실제 검증</p>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={substData} margin={{top:10,right:20,left:0,bottom:0}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e8eaf0" />
                  <XAxis dataKey="label" tick={{fontSize:12,fill:'#8b95a1'}} />
                  <YAxis unit="%" tick={{fontSize:12,fill:'#8b95a1'}} />
                  <Tooltip formatter={(v,name) => [`${v}%`, name==='goal_prob'?'득점 확률':'실점 확률']} contentStyle={{borderRadius:8,border:'1px solid #e8eaf0',fontSize:13}} />
                  <Bar dataKey="goal_prob" name="goal_prob" fill="#00c4a1" radius={[4,4,0,0]} />
                  <Bar dataKey="concede_prob" name="concede_prob" fill="#ef4444" radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      )}

      {/* ── 피지컬 데이터 탭 (교체 시뮬레이터) ── */}
      {activeAnalysisTab === 'physical' && (
        <div className="analysis-section">
          <div className="analysis-intro">
            <span className="analysis-category-badge physical">Physical Data</span>
            <p>선수 활동량 · 교체 타이밍 · 체력 관리 — 전력분석관의 핵심 업무인 교체 최적 타이밍 예측</p>
          </div>

          <div className="sim-main-layout">
            {/* 선수 그리드 */}
            <div className="bt-card player-grid-card">
              <div className="bt-card-header">
                <h3>K리그 선수단</h3>
                <span className="bt-badge">투입 후 득점 확률 순</span>
              </div>
              <div className="team-filter-row">
                {teams.map(t => (
                  <button key={t} className={`team-filter-btn ${teamFilter===t?'active':''}`} onClick={() => setTeamFilter(t)}>
                    {t==='전체'?t:t.split(' ')[0]}
                  </button>
                ))}
              </div>
              {rosterLoading && <div style={{textAlign:'center',padding:'12px',color:'#9ca3af',fontSize:12}}>선수단 불러오는 중...</div>}
              <div className="player-grid">
                {filteredPlayers.map((p) => (
                  <PlayerAvatar key={p.player} player={p} selected={selectedPlayer?.player===p.player} onClick={setSelectedPlayer} jerseyNumber={jerseyNumbers[p.player] ?? (p.jersey ?? null)} />
                ))}
                {!rosterLoading && filteredPlayers.length === 0 && <div className="state-msg">선수 데이터 없음</div>}
              </div>
              {teamFilter !== '전체' && (
                <div style={{fontSize:10,color:'#b0b8c4',marginTop:4}}>
                  ML 데이터 {mlFiltered.length}명 · 선수단 {rosterOnly.length}명 추가
                </div>
              )}
            </div>

            {/* 시뮬레이터 */}
            <div className="bt-card sim-right-card">
              <div className="bt-card-header">
                <h3>🔄 교체 효과 ML 예측</h3>
                <span className="bt-badge">Logistic Regression · 75.8%</span>
              </div>

              {selectedPlayer && (
                <div className="sim-selected-player">
                  <div className="sim-big-avatar">
                    <span>{getInitials(selectedPlayer.player)}</span>
                  </div>
                  <div style={{flex:1,minWidth:0}}>
                    <div className="sim-player-name">{selectedPlayer.player}</div>
                    <div className="sim-player-meta">{selectedPlayer.team} · 교체 투입 {selectedPlayer.sub_count}회</div>
                    <div className="sim-player-hist">역대 투입 후 득점: <b style={{color:'#00c4a1'}}>{selectedPlayer.goal_after_prob}%</b></div>
                  </div>
                </div>
              )}

              <div className="sim-field">
                <label>교체 시간 <b style={{color:'#00c4a1'}}>{minute}분</b></label>
                <input type="range" min="30" max="90" value={minute} onChange={e=>setMinute(Number(e.target.value))} className="sim-slider" />
                <div className="sim-slider-labels"><span>30'</span><span>45'</span><span>60'</span><span>75'</span><span>90'</span></div>
              </div>

              <div className="sim-field">
                <label>현재 점수 상황</label>
                <div className="sim-score-btns">
                  {SCORE_STATES.map(s => (
                    <button key={s.value} className={`sim-score-btn ${scoreState===s.value?'active':''}`} onClick={()=>setScoreState(s.value)}>
                      {s.emoji} {s.label}
                    </button>
                  ))}
                </div>
              </div>

              {simLoading && <div style={{display:'flex',justifyContent:'center',padding:'20px'}}><div className="spinner"/></div>}

              {!simLoading && simResult && (
                <div className="sim-result-box">
                  {simResult.combined_prob !== null && (() => {
                    const pc = simResult.combined_prob >= 28 ? '#00c4a1' : simResult.combined_prob >= 20 ? '#f59e0b' : '#ef4444'
                    return (
                      <div className="sim-big-prob" style={{color: pc, borderColor: pc, background: pc + '18'}}>
                        {simResult.combined_prob}%
                        <span>득점 확률</span>
                      </div>
                    )
                  })()}
                  <div className="sim-prob-rows">
                    {simResult.ml_prediction!==null && (
                      <div className="sim-prob-row">
                        <span>ML 모델</span>
                        <div className="sim-mini-bar"><div style={{width:`${simResult.ml_prediction}%`,background:'#00c4a1',height:'100%',borderRadius:4,transition:'width 0.5s'}}/></div>
                        <b>{simResult.ml_prediction}%</b>
                      </div>
                    )}
                    {simResult.historical_prob!==null && (
                      <div className="sim-prob-row">
                        <span>실제 기록({simResult.historical_count}건)</span>
                        <div className="sim-mini-bar"><div style={{width:`${simResult.historical_prob}%`,background:'#3b82f6',height:'100%',borderRadius:4,transition:'width 0.5s'}}/></div>
                        <b>{simResult.historical_prob}%</b>
                      </div>
                    )}
                  </div>
                  <div className={`sim-rec ${simResult.combined_prob>=28?'rec-high':simResult.combined_prob>=20?'rec-mid':'rec-low'}`}>
                    {simResult.combined_prob>=28?'✅ 교체 강력 권장':simResult.combined_prob>=20?'🟡 교체 고려':'⚠️ 상황 판단 필요'}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ── 상대 분석 탭 ── */}
      {activeAnalysisTab === 'opposition' && (
        <div className="analysis-section">
          <div className="analysis-intro">
            <span className="analysis-category-badge opposition">Opposition Analysis</span>
            <p>포메이션 시각화 · 전술 상성 분석 — 상대 전력 분석 프레임워크</p>
          </div>

          {/* ── 전술 상성 승률 시뮬레이터 ── */}
          <div className="bt-card tactic-sim-card">
            <div className="bt-card-header">
              <h3>⚔️ 전술 상성 승률 분석</h3>
              <span className="bt-badge">K리그 693경기 실측</span>
            </div>
            <p className="bt-desc">우리팀 전술 vs 상대팀 전술 조합에서 실제 K리그 승률 + 선수 투입 시 변화</p>

            {/* 전술 선택 */}
            <div className="tactic-sim-selectors">
              <div className="tss-group">
                <div className="tss-label my">우리팀 전술</div>
                <div className="tss-btns">
                  {Object.entries(TACTIC_MATCHUP).map(([t, d]) => (
                    <button key={t} className={`tss-btn ${myTactic===t?'active':''}`}
                      style={myTactic===t?{background:d.color,borderColor:d.color}:{}}
                      onClick={() => setMyTactic(t)}>{t}</button>
                  ))}
                </div>
              </div>
              <div className="tss-vs">VS</div>
              <div className="tss-group">
                <div className="tss-label opp">상대팀 전술</div>
                <div className="tss-btns">
                  {Object.entries(TACTIC_MATCHUP).map(([t, d]) => (
                    <button key={t} className={`tss-btn ${oppTactic===t?'active-opp':''}`}
                      style={oppTactic===t?{background:d.color,borderColor:d.color}:{}}
                      onClick={() => setOppTactic(t)}>{t}</button>
                  ))}
                </div>
              </div>
            </div>

            {/* 실제 승률 표시 */}
            {(() => {
              const found = matchupData.find(m => m.my_tactic === myTactic && m.opp_tactic === oppTactic)
              const winColor = found ? (found.win_pct >= 45 ? '#00c4a1' : found.win_pct >= 35 ? '#f59e0b' : '#ef4444') : '#9ca3af'
              return (
                <div className="tactic-result-row">
                  <div className="tactic-win-gauge">
                    <div className="twg-label">승리 확률</div>
                    <div className="twg-num" style={{color: winColor}}>
                      {found ? `${found.win_pct}%` : '데이터 없음'}
                    </div>
                    {found && <div className="twg-sub">{found.draw_pct}% 무 · {found.loss_pct}% 패 · {found.total}경기 기반</div>}
                  </div>
                  <div className="tactic-matchup-hint">
                    <div className="tmh-title">{myTactic} → {TACTIC_MATCHUP[myTactic]?.beats} 상성 우위</div>
                    <div className="tmh-desc">{TACTIC_MATCHUP[myTactic]?.desc}</div>
                    {myTactic === oppTactic && <div className="tmh-warn">⚠️ 같은 전술 — 개인 능력 차이가 결정</div>}
                    {TACTIC_MATCHUP[myTactic]?.beats === oppTactic && <div className="tmh-good">✅ 상성 유리!</div>}
                    {TACTIC_MATCHUP[myTactic]?.losesto === oppTactic && <div className="tmh-bad">⚠️ 상성 불리 — 교체 전술 필요</div>}
                  </div>

                  {/* 선수 투입 보정 */}
                  <div className="tactic-sub-panel">
                    <div className="tsp-title">교체 투입으로 보정</div>
                    <div className="tsp-minute">
                      <span>{tacticMinute}분</span>
                      <input type="range" min="45" max="90" value={tacticMinute}
                        onChange={e => setTacticMinute(Number(e.target.value))} className="sim-slider" style={{width:120}} />
                    </div>
                    <select className="tsp-select" onChange={e => {
                      const p = players.find(pl => pl.player === e.target.value)
                      setTacticSubPlayer(p || null)
                    }}>
                      <option value="">선수 선택</option>
                      {players.filter(p => p.goal_after_prob > 0).map(p => (
                        <option key={p.player} value={p.player}>{p.player.split(' ').slice(-1)[0]} ({p.goal_after_prob}%)</option>
                      ))}
                    </select>
                    {tacticSimResult && tacticSubPlayer && (
                      <div className="tsp-result">
                        <span className="tsp-name">{tacticSubPlayer.player.split(' ').slice(-1)[0]} 투입 시</span>
                        <span className="tsp-prob" style={{color: tacticSimResult.combined_prob >= 28 ? '#00c4a1' : '#f59e0b'}}>
                          득점 확률 +{tacticSimResult.combined_prob}%
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )
            })()}
          </div>

          {/* 포메이션 대결 시각화 */}
          <div className="bt-card">
            <div className="bt-card-header">
              <h3>포메이션 대결 시각화</h3>
              <span className="bt-badge">FIFA 스타일</span>
            </div>
            <div className="formation-selectors">
              <div className="formation-selector-group">
                <label>우리팀 포메이션</label>
                <div className="formation-btns">
                  {Object.keys(FORMATION_POSITIONS).map(f => (
                    <button key={f} className={`formation-btn ${myFormation===f?'active':''}`} onClick={()=>setMyFormation(f)}>{f}</button>
                  ))}
                </div>
              </div>
              <div className="formation-selector-group">
                <label>상대팀 포메이션</label>
                <div className="formation-btns">
                  {Object.keys(FORMATION_POSITIONS).map(f => (
                    <button key={f} className={`formation-btn opp ${oppFormation===f?'active-opp':''}`} onClick={()=>setOppFormation(f)}>{f}</button>
                  ))}
                </div>
              </div>
            </div>
            <div className="formation-pitches">
              <FormationPitch formation={myFormation} teamName="우리팀" teamColor="#dbeafe" />
              <div className="formation-vs">VS</div>
              <FormationPitch formation={oppFormation} teamName="상대팀" teamColor="#fee2e2" flipped />
            </div>
            <div className="formation-legend">
              <span className="fleg gk">GK</span>
              <span className="fleg def">수비</span>
              <span className="fleg mid">미드필드</span>
              <span className="fleg att">공격</span>
            </div>
          </div>

          {/* 전술 상성 (가위바위보) */}
          <div className="bt-card">
            <div className="bt-card-header">
              <h3>전술 상성도</h3>
              <span className="bt-badge">가위바위보 구조</span>
            </div>
            <p className="bt-desc">K리그 693경기 데이터 기반 — 전술 유형별 승률과 상성 관계</p>
            <div className="tactic-wheel-layout">
              <TacticalWheel />
              <div className="tactic-matchup-list">
                {Object.entries(TACTIC_MATCHUP).map(([tactic, data]) => (
                  <div key={tactic} className="tactic-matchup-row">
                    <div className="tmr-badge" style={{background:data.color}}>{tactic}</div>
                    <div className="tmr-arrow">→ 이긴다</div>
                    <div className="tmr-beats">{data.beats}</div>
                    <div className="tmr-desc">{data.desc}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 전술 파라미터 출력 */}
          <div className="bt-card">
            <div className="bt-card-header">
              <h3>전술 파라미터 세트 자동 산출</h3>
              <span className="bt-badge">상대 분석 → 파라미터화</span>
            </div>
            <p className="bt-desc">선택한 포메이션 + K리그 데이터 기반 파라미터 자동 생성</p>
            <div className="param-output">
              <div className="param-line"><code>FORMATION</code><span>= {myFormation}</span><small>// 우리팀 포메이션</small></div>
              <div className="param-line"><code>OPP_FORMATION</code><span>= {oppFormation}</span><small>// 상대팀 포메이션</small></div>
              <div className="param-line"><code>PRESS_INTENSITY</code><span>= 72</span><small>// 전방 압박 강도 (0~100)</small></div>
              <div className="param-line"><code>DEFENSIVE_LINE</code><span>= 58</span><small>// 수비 라인 높이</small></div>
              <div className="param-line"><code>SETPIECE_FOCUS</code><span>= 0.8</span><small>// 세트피스 집중도</small></div>
              <div className="param-line"><code>OFFSIDE_TRAP</code><span>= 0.3</span><small>// 오프사이드 트랩 빈도</small></div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function SummaryCard({ label, value, unit, color }) {
  return (
    <div className="bt-summary-card">
      <div className="bt-summary-val" style={{ color }}>{value}<span className="bt-summary-unit">{unit}</span></div>
      <div className="bt-summary-label">{label}</div>
    </div>
  )
}
