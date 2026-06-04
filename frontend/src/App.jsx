import { useState } from 'react'
import MatchList from './components/MatchList'
import MatchDetail from './components/MatchDetail'
import './App.css'

export default function App() {
  const [selectedMatch, setSelectedMatch] = useState(null)

  const goToMatch = (match) => {
    setSelectedMatch(match)
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-badge">플코</span>
            <div className="logo-text">
              <h1>기록 기반 팀별 작전 분석 전술</h1>
              <p>Match Intelligence · K리그 전술 파라미터 분석 시스템</p>
            </div>
          </div>
          <nav className="header-nav">
            <button className="nav-btn active">
              경기 분석
            </button>
          </nav>
        </div>
      </header>

      <main className="main">
        {selectedMatch ? (
          <MatchDetail
            match={selectedMatch}
            onBack={() => setSelectedMatch(null)}
          />
        ) : (
          <>
            <div className="page-title">
              <h2>경기 분석</h2>
              <p>K리그 경기 데이터를 기반으로 전술 파라미터를 자동 산출합니다</p>
            </div>
            <MatchList onSelect={goToMatch} />
          </>
        )}
      </main>
    </div>
  )
}
