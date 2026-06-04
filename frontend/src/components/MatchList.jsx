import { useState, useEffect } from 'react'
import axios from 'axios'
import Standings from './Standings'

const TEAM_LOGOS = {
  "서울": "https://www.kleague.com/assets/images/emblem/emblem_K09.png",
  "수원": "https://www.kleague.com/assets/images/emblem/emblem_K02.png",
  "인천": "https://www.kleague.com/assets/images/emblem/emblem_K18.png",
  "대구": "https://www.kleague.com/assets/images/emblem/emblem_K17.png",
  "대전": "https://www.kleague.com/assets/images/emblem/emblem_K10.png",
  "광주": "https://www.kleague.com/assets/images/emblem/emblem_K22.png",
  "전북": "https://www.kleague.com/assets/images/emblem/emblem_K05.png",
  "전남": "https://www.kleague.com/assets/images/emblem/emblem_K07.png",
  "포항": "https://www.kleague.com/assets/images/emblem/emblem_K03.png",
  "울산": "https://www.kleague.com/assets/images/emblem/emblem_K01.png",
  "제주": "https://www.kleague.com/assets/images/emblem/emblem_K04.png",
  "부산": "https://www.kleague.com/assets/images/emblem/emblem_K06.png",
  "파주": "https://www.kleague.com/assets/images/emblem/emblem_K40.png",
  "수원FC": "https://www.kleague.com/assets/images/emblem/emblem_K29.png",
  "충남아산": "https://www.kleague.com/assets/images/emblem/emblem_K34.png",
  "대구FC": "https://www.kleague.com/assets/images/emblem/emblem_K17.png",
  "안양": "https://www.kleague.com/assets/images/emblem/emblem_K27.png",
  "성남": "https://www.kleague.com/assets/images/emblem/emblem_K08.png",
  "용인": "https://www.kleague.com/assets/images/emblem/emblem_K42.png",
  "김포": "https://www.kleague.com/assets/images/emblem/emblem_K36.png",
  "김해": "https://www.kleague.com/assets/images/emblem/emblem_K41.png",
  "천안": "https://www.kleague.com/assets/images/emblem/emblem_K38.png",
  "화성": "https://www.kleague.com/assets/images/emblem/emblem_K39.png",
  "서울E": "https://www.kleague.com/assets/images/emblem/emblem_K31.png",
  "강원": "https://www.kleague.com/assets/images/emblem/emblem_K21.png",
  "강원FC": "https://www.kleague.com/assets/images/emblem/emblem_K21.png",
  "부천": "https://www.kleague.com/assets/images/emblem/emblem_K26.png",
  "경남": "https://www.kleague.com/assets/images/emblem/emblem_K20.png",
  "김천": "https://www.kleague.com/assets/images/emblem/emblem_K35.png",
  "청주": "https://www.kleague.com/assets/images/emblem/emblem_K37.png",
  "충북청주": "https://www.kleague.com/assets/images/emblem/emblem_K37.png",
  "안산": "https://www.kleague.com/assets/images/emblem/emblem_K32.png",
  "이천": "https://www.kleague.com/assets/images/emblem/emblem_K25.png",
  "여수": "https://www.kleague.com/assets/images/emblem/emblem_K26.png",
  "시흥": "https://www.kleague.com/assets/images/emblem/emblem_K24.png",
}

const STATUS_LABEL = {
  'Ended': '종료',
  'Scheduled': '예정',
  'Live': '진행중',
  FT: '종료',
  '1H': '전반',
  HT: '하프타임',
  '2H': '후반',
  NS: '예정',
  PST: '연기',
  CANC: '취소',
}

const TEAM_COLORS = {
  "서울": "#00D9A3",
  "수원": "#4169E1",
  "인천": "#FF6B6B",
  "대구": "#FF1493",
  "대전": "#FFD700",
  "광주": "#FF0000",
  "전북": "#32CD32",
  "전남": "#00CED1",
  "포항": "#FF8C00",
  "울산": "#4B0082",
  "제주": "#20B2AA",
  "부산": "#DC143C",
  "파주": "#6495ED",
  "수원FC": "#4169E1",
  "충남아산": "#FFB6C1",
  "대구FC": "#FF1493",
  "안양": "#F0E68C",
  "성남": "#FF69B4",
  "용인": "#9932CC",
  "김포": "#8B4513",
  "김해": "#2F4F4F",
  "천안": "#FF4500",
  "화성": "#228B22",
  "시흥": "#1E90FF",
  "이천": "#DAA520",
  "여수": "#00BFFF",
  "서울E": "#00D9A3",
}

function getTeamColor(teamName) {
  return TEAM_COLORS[teamName] || "#999999"
}

export default function MatchList({ onSelect }) {
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [season, setSeason] = useState(2021)
  const [league, setLeague] = useState(10001)
  const [search, setSearch] = useState('')

  useEffect(() => {
    setLoading(true)
    setError(null)
    setMatches([])
    axios.get(`http://localhost:8000/api/fixtures?year=${season}&league=${league}&limit=500`)
      .then(r => {
        if (r.data?.error) {
          setError(r.data.error)
          if (r.data.cached?.length) setMatches(r.data.cached)
        } else {
          setMatches(r.data)
        }
      })
      .catch(err => {
        const msg = err.response?.data?.error || err.response?.data?.detail
        setError(msg || '백엔드 서버에 연결할 수 없습니다. python api_server.py 실행 확인')
      })
      .finally(() => setLoading(false))
  }, [season, league])

  const filtered = matches.filter(m =>
    m.home_team.toLowerCase().includes(search.toLowerCase()) ||
    m.away_team.toLowerCase().includes(search.toLowerCase())
  )

  const grouped = filtered.reduce((acc, m) => {
    const date = m.date
    if (!acc[date]) acc[date] = []
    acc[date].push(m)
    return acc
  }, {})

  return (
    <div className="match-list">
      <div className="filters">
        <div className="filter-group">
          <label>리그</label>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              className={`league-btn ${league === 10001 ? 'active' : ''}`}
              onClick={() => setLeague(10001)}
              style={{
                padding: '8px 16px',
                borderRadius: '6px',
                border: league === 10001 ? '2px solid #00D9A3' : '2px solid #ddd',
                background: league === 10001 ? '#00D9A3' : '#fff',
                color: league === 10001 ? '#fff' : '#333',
                fontWeight: 'bold',
                cursor: 'pointer'
              }}
            >
              K리그 1
            </button>
            <button
              className={`league-btn ${league === 10002 ? 'active' : ''}`}
              onClick={() => setLeague(10002)}
              style={{
                padding: '8px 16px',
                borderRadius: '6px',
                border: league === 10002 ? '2px solid #6C3FB8' : '2px solid #ddd',
                background: league === 10002 ? '#6C3FB8' : '#fff',
                color: league === 10002 ? '#fff' : '#333',
                fontWeight: 'bold',
                cursor: 'pointer'
              }}
            >
              K리그 2
            </button>
          </div>
        </div>
        <div className="filter-group">
          <label>시즌</label>
          <select value={season} onChange={e => setSeason(Number(e.target.value))}>
            <option value={2021}>2021</option>
          </select>
        </div>
        <div className="filter-group search">
          <label>팀 검색</label>
          <input
            placeholder="팀명 입력..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
      </div>

      {loading && <div className="state-msg">데이터 불러오는 중...</div>}
      {/* Error UI removed */}

      {!loading && !error && Object.keys(grouped).length === 0 && (
        <div className="state-msg">경기 데이터가 없습니다.</div>
      )}

      {Object.entries(grouped).map(([date, dayMatches]) => (
        <div key={date} className="day-group">
          <div className="day-header">{date}</div>
          <div className="day-matches">
            {dayMatches.map(m => (
              <div key={m.fixture_id} className="match-card" onClick={() => onSelect({
                ...m,
                home_logo: m.home_logo || TEAM_LOGOS[m.home_team],
                away_logo: m.away_logo || TEAM_LOGOS[m.away_team]
              })}>
                <div className="match-teams">
                  <div className="team home">
                    {m.home_logo || TEAM_LOGOS[m.home_team] ? (
                      <img src={m.home_logo || TEAM_LOGOS[m.home_team]} alt={m.home_team} onError={e => e.target.style.display='none'} />
                    ) : (
                      <div className="team-avatar" style={{background: getTeamColor(m.home_team)}}>{m.home_team.charAt(0)}</div>
                    )}
                    <span>{m.home_team}</span>
                  </div>
                  <div className="score-block">
                    <div className={`status-badge ${m.status}`}>
                      {STATUS_LABEL[m.status] || m.status}
                    </div>
                    <div className="score">
                      {m.home_score ?? '-'} : {m.away_score ?? '-'}
                    </div>
                  </div>
                  <div className="team away">
                    {m.away_logo || TEAM_LOGOS[m.away_team] ? (
                      <img src={m.away_logo || TEAM_LOGOS[m.away_team]} alt={m.away_team} onError={e => e.target.style.display='none'} />
                    ) : (
                      <div className="team-avatar" style={{background: getTeamColor(m.away_team)}}>{m.away_team.charAt(0)}</div>
                    )}
                    <span>{m.away_team}</span>
                  </div>
                </div>
                <div className="match-footer">
                  <span>전술 분석 보기 →</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      <Standings season={season} league={league} />
    </div>
  )
}
