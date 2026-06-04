import { useState, useEffect } from 'react'
import axios from 'axios'

// 프로덕션 환경에서는 VITE_API_URL을 사용하고, 로컬에서는 localhost로 폴백
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

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

export default function Standings({ season, league }) {
  const [standings, setStandings] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!league) return

    setLoading(true)
    setError(null)

    axios
      .get(`${apiUrl}/api/standings?year=${season}&league=${league}`)
      .then(r => setStandings(r.data))
      .catch(err => setError(err.response?.data?.error || '순위 데이터 로드 실패'))
      .finally(() => setLoading(false))
  }, [season, league])

  if (loading) return <div className="standings-loading">순위표 불러오는 중...</div>
  // Error UI removed to hide messages
  if (!standings.length) return <div className="standings-empty">순위 데이터가 없습니다.</div>

  return (
    <div className="standings">
      <table>
        <thead>
          <tr>
            <th>순위</th>
            <th>팀</th>
            <th>경</th>
            <th>승</th>
            <th>무</th>
            <th>패</th>
            <th>득</th>
            <th>실</th>
            <th>득차</th>
            <th>승점</th>
          </tr>
        </thead>
        <tbody>
          {standings.map((team, idx) => (
            <tr key={team.team} className={idx < 3 ? 'top-3' : ''}>
              <td className="rank">{idx + 1}</td>
              <td className="team-name">
                {TEAM_LOGOS[team.team] && <img src={TEAM_LOGOS[team.team]} alt={team.team} className="team-logo-small" onError={e => e.target.style.display='none'} />}
                <span>{team.team}</span>
              </td>
              <td>{team.played}</td>
              <td className="wins">{team.wins}</td>
              <td className="draws">{team.draws}</td>
              <td className="losses">{team.losses}</td>
              <td>{team.gf}</td>
              <td>{team.ga}</td>
              <td className={team.gd >= 0 ? 'positive' : 'negative'}>{team.gd >= 0 ? '+' : ''}{team.gd}</td>
              <td className="points"><strong>{team.pts}</strong></td>
            </tr>
          ))}
        </tbody>
      </table>

      <style>{`
        .standings {
          margin-top: 40px;
          padding: 20px;
          background: #f9f9f9;
          border-radius: 8px;
        }

        .standings table {
          width: 100%;
          border-collapse: collapse;
          font-size: 14px;
        }

        .standings thead {
          background: #333;
          color: white;
        }

        .standings th {
          padding: 12px 8px;
          text-align: center;
          font-weight: bold;
          border-bottom: 2px solid #ddd;
        }

        .standings td {
          padding: 10px 8px;
          text-align: center;
          border-bottom: 1px solid #eee;
        }

        .standings tr.top-3 {
          background: #f0f8ff;
        }

        .standings tr:hover {
          background: #f5f5f5;
        }

        .standings .rank {
          font-weight: bold;
          width: 40px;
        }

        .standings .team-name {
          text-align: left;
          display: flex;
          align-items: center;
          gap: 8px;
          font-weight: 500;
        }

        .standings .team-logo-small {
          width: 24px;
          height: 24px;
          object-fit: contain;
        }

        .standings .wins {
          color: #27ae60;
          font-weight: bold;
        }

        .standings .draws {
          color: #f39c12;
        }

        .standings .losses {
          color: #e74c3c;
        }

        .standings .positive {
          color: #27ae60;
        }

        .standings .negative {
          color: #e74c3c;
        }

        .standings .points {
          background: #ecf0f1;
          padding: 8px;
          border-radius: 4px;
        }

        .standings-loading,
        .standings-error,
        .standings-empty {
          padding: 20px;
          text-align: center;
          color: #666;
        }
      `}</style>
    </div>
  )
}
