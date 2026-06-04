import { useState, useEffect } from 'react';
import HUDLayout from './HUDLayout';
import HUDPanel from './HUDPanel';
import TacticalPitch from './TacticalPitch';

// 프로덕션 환경에서는 VITE_API_URL을 사용하고, 로컬에서는 localhost로 폴백
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function YOLOAnalysis({ onBack }) {
  const [matchData, setMatchData] = useState(null);
  const [setpieceData, setSetpieceData] = useState(null);
  const [defensiveData, setDefensiveData] = useState(null);
  const [heatmapData, setHeatmapData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('setpiece'); // 'setpiece', 'defensive', 'heatmap'

  useEffect(() => {
    fetchAllData();
  }, []);

  async function fetchAllData() {
    try {
      const [matchRes, setpieceRes, defRes, heatmapRes] = await Promise.all([
        fetch(`${apiUrl}/api/yolo/match/1`),
        fetch(`${apiUrl}/api/yolo/match/1/setpiece`),
        fetch(`${apiUrl}/api/yolo/match/1/defensive`),
        fetch(`${apiUrl}/api/yolo/match/1/heatmap`).catch(() => ({ json: () => [] }))
      ]);

      setMatchData(await matchRes.json());
      setSetpieceData(await setpieceRes.json());
      setDefensiveData(await defRes.json());
      setHeatmapData(await heatmapRes.json());
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <HUDLayout title="INITIALIZING SYSTEM..." subtitle="Loading K-League Tactical Data">
        <div className="flex items-center justify-center h-full">
          <div className="text-axon-neon neon-text-green font-mono animate-pulse">CONNECTING TO DATABASE...</div>
        </div>
      </HUDLayout>
    );
  }

  // --- Rendering Overlays on the Pitch ---
  const renderPitchOverlays = () => {
    if (activeTab === 'setpiece' && setpieceData?.setpiece_zones) {
      return Object.entries(setpieceData.setpiece_zones).map(([zone, stat]) => {
        const [col, row] = [zone.charCodeAt(0) - 65, parseInt(zone[1])];
        const x = col * (105 / 3);
        const y = (row - 1) * (68 / 2);
        const xg = stat.total_xg || 0;
        
        let color = 'rgba(0, 255, 136, 0.2)'; // Safe
        if (xg >= 0.8) color = 'rgba(255, 51, 102, 0.6)'; // Danger
        else if (xg >= 0.4) color = 'rgba(255, 170, 0, 0.4)'; // Warning

        return (
          <g key={zone} transform={`translate(${x}, ${y})`}>
            <rect width={105/3} height={68/2} fill={color} stroke="rgba(255,255,255,0.2)" strokeWidth="0.2" className="transition-all duration-500 hover:opacity-80" />
            <text x={(105/3)/2} y={(68/2)/2} fill="white" fontSize="3" textAnchor="middle" className="font-mono">{zone}</text>
            <text x={(105/3)/2} y={(68/2)/2 + 4} fill="rgba(255,255,255,0.7)" fontSize="2" textAnchor="middle" className="font-mono">xG: {xg.toFixed(2)}</text>
          </g>
        );
      });
    }

    if (activeTab === 'defensive' && defensiveData?.home_defense?.zones) {
      // Just showing Home Defense for visual demo
      return Object.entries(defensiveData.home_defense.zones).map(([zone, stat]) => {
        const [col, row] = [zone.charCodeAt(0) - 65, parseInt(zone[1])];
        const x = col * (105 / 3);
        const y = (row - 1) * (68 / 2);
        const xg = stat.total_xg || 0;
        
        let color = 'rgba(0, 191, 255, 0.2)'; // Base Blue
        if (xg >= 1.0) color = 'rgba(255, 51, 102, 0.6)'; // Danger
        else if (xg >= 0.5) color = 'rgba(255, 170, 0, 0.4)'; // Warning

        return (
          <g key={zone} transform={`translate(${x}, ${y})`}>
            <rect width={105/3} height={68/2} fill={color} stroke="rgba(255,255,255,0.2)" strokeWidth="0.2" className="transition-all duration-500" />
            <text x={(105/3)/2} y={(68/2)/2} fill="white" fontSize="3" textAnchor="middle" className="font-mono">{zone}</text>
            <text x={(105/3)/2} y={(68/2)/2 + 4} fill="rgba(255,255,255,0.7)" fontSize="2" textAnchor="middle" className="font-mono">Danger: {xg.toFixed(2)}</text>
          </g>
        );
      });
    }

    if (activeTab === 'heatmap' && heatmapData && heatmapData.length > 0) {
      // Very basic heatmap visualization mapping coordinates (approximate scaling)
      return heatmapData.map((d, i) => (
        <circle 
          key={i} 
          cx={d.x} 
          cy={d.y} 
          r={d.frequency * 0.5} 
          fill={d.team_name === matchData?.match?.home_team ? 'rgba(0,255,136,0.3)' : 'rgba(0,191,255,0.3)'} 
          style={{ filter: 'blur(2px)' }}
        />
      ));
    }

    return null;
  };

  return (
    <HUDLayout 
      title="TACTICAL ANALYSIS" 
      subtitle={matchData ? `${matchData.match.home_team} VS ${matchData.match.away_team} [LIVE]` : 'YOLO V1 PROCESSING'}
      onBack={onBack}
    >
      <div className="grid grid-cols-12 gap-6 h-full min-h-[600px]">
        {/* Left Panel: Controls & Summary */}
        <div className="col-span-3 flex flex-col gap-6">
          <HUDPanel title="ANALYSIS MODE">
            <div className="flex flex-col gap-3">
              <button 
                onClick={() => setActiveTab('setpiece')}
                className={`p-3 text-left font-mono text-sm border transition-all ${activeTab === 'setpiece' ? 'bg-axon-neon/20 border-axon-neon text-axon-neon shadow-[0_0_10px_rgba(0,255,136,0.2)]' : 'bg-black/20 border-white/10 text-gray-400 hover:border-white/30'}`}
              >
                [01] SET-PIECE VULNERABILITY
              </button>
              <button 
                onClick={() => setActiveTab('defensive')}
                className={`p-3 text-left font-mono text-sm border transition-all ${activeTab === 'defensive' ? 'bg-axon-neon/20 border-axon-neon text-axon-neon shadow-[0_0_10px_rgba(0,255,136,0.2)]' : 'bg-black/20 border-white/10 text-gray-400 hover:border-white/30'}`}
              >
                [02] DEFENSIVE ZONES
              </button>
              <button 
                onClick={() => setActiveTab('heatmap')}
                className={`p-3 text-left font-mono text-sm border transition-all ${activeTab === 'heatmap' ? 'bg-axon-neon/20 border-axon-neon text-axon-neon shadow-[0_0_10px_rgba(0,255,136,0.2)]' : 'bg-black/20 border-white/10 text-gray-400 hover:border-white/30'}`}
              >
                [03] HEATMAP OVERLAY
              </button>
            </div>
          </HUDPanel>

          <HUDPanel title="MATCH CONTEXT" className="flex-1">
            {matchData && (
              <div className="flex flex-col gap-4 font-mono text-sm">
                <div className="flex justify-between items-center border-b border-white/10 pb-2">
                  <span className="text-gray-400">HOME</span>
                  <span className="text-white">{matchData.match.home_team}</span>
                </div>
                <div className="flex justify-between items-center border-b border-white/10 pb-2">
                  <span className="text-gray-400">AWAY</span>
                  <span className="text-white">{matchData.match.away_team}</span>
                </div>
                <div className="flex justify-between items-center border-b border-white/10 pb-2">
                  <span className="text-gray-400">POSSESSION</span>
                  <span className="text-axon-neon">54% - 46%</span> {/* Mocked since YOLO possession isn't ready */}
                </div>
              </div>
            )}
          </HUDPanel>
        </div>

        {/* Center Panel: Tactical Pitch */}
        <div className="col-span-6 flex flex-col justify-center relative">
          <TacticalPitch>
            <svg viewBox="0 0 105 68" className="w-full h-full">
              {renderPitchOverlays()}
            </svg>
          </TacticalPitch>
          
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-4 text-xs font-mono">
            <div className="flex items-center gap-2"><div className="w-3 h-3 bg-[rgba(0,255,136,0.2)] border border-[rgba(0,255,136,0.5)]"></div> SAFE</div>
            <div className="flex items-center gap-2"><div className="w-3 h-3 bg-[rgba(255,170,0,0.4)] border border-[rgba(255,170,0,0.8)]"></div> WARNING</div>
            <div className="flex items-center gap-2"><div className="w-3 h-3 bg-[rgba(255,51,102,0.6)] border border-[rgba(255,51,102,0.8)]"></div> DANGER</div>
          </div>
        </div>

        {/* Right Panel: Deep Dive Stats */}
        <div className="col-span-3 flex flex-col gap-6">
          <HUDPanel title="DATA STREAM" className="flex-1">
            {activeTab === 'setpiece' && setpieceData && (
              <div className="flex flex-col gap-4 font-mono text-sm">
                <div className="text-axon-neon mb-2">총 세트피스 슈팅: {setpieceData.total_setpiece_shots}</div>
                {setpieceData.recommendations?.map((rec, i) => (
                  <div key={i} className="border-l-2 border-axon-neon pl-3 py-1 bg-axon-neon/5">
                    <div className="text-white font-bold">{rec.zone}</div>
                    <div className="text-gray-400 text-xs mt-1">{rec.text}</div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'defensive' && defensiveData && (
              <div className="flex flex-col gap-4 font-mono text-sm">
                <div className="text-axon-alert mb-2">HOME TEAM VULNERABILITY</div>
                <div className="flex justify-between border-b border-white/10 pb-2">
                  <span className="text-gray-400">Total Shots Allowed</span>
                  <span className="text-white">{defensiveData.home_defense.total_shots_allowed}</span>
                </div>
                <div className="flex justify-between border-b border-white/10 pb-2">
                  <span className="text-gray-400">Total xGA</span>
                  <span className="text-white">{defensiveData.home_defense.total_xg_allowed.toFixed(2)}</span>
                </div>
                <div className="flex justify-between border-b border-white/10 pb-2">
                  <span className="text-gray-400">Danger Zone</span>
                  <span className="text-axon-alert animate-pulse">{defensiveData.home_defense.most_dangerous}</span>
                </div>
              </div>
            )}

            {activeTab === 'heatmap' && (
              <div className="flex flex-col gap-4 font-mono text-sm">
                <div className="text-axon-blue">PLAYER DENSITY TRACKING</div>
                <p className="text-gray-400 text-xs">
                  Accumulated player coordinate data mapped via homography from YOLO V1 detections. High intensity indicates prolonged presence.
                </p>
              </div>
            )}
          </HUDPanel>
        </div>
      </div>
    </HUDLayout>
  );
}
