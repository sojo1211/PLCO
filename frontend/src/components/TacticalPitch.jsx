
// Pitch proportions: 105 x 68 meters.
// We use a viewBox of 0 0 105 68 so child elements can be absolutely positioned using percentages (x/105*100)% or directly mapped.
export default function TacticalPitch({ children, className = '' }) {
  return (
    <div className={`relative w-full max-w-4xl mx-auto aspect-[105/68] bg-axon-dark border border-axon-neon/50 rounded-lg overflow-hidden shadow-[0_0_15px_rgba(0,255,136,0.2)] ${className}`}>
      {/* Pitch SVG Background */}
      <svg viewBox="0 0 105 68" className="absolute inset-0 w-full h-full opacity-50">
        <rect width="105" height="68" fill="#0B1319" />
        {/* Pitch Lines */}
        <g stroke="#00FF88" strokeWidth="0.3" fill="none" className="opacity-70">
          <rect x="0" y="0" width="105" height="68" />
          <line x1="52.5" y1="0" x2="52.5" y2="68" />
          <circle cx="52.5" cy="34" r="9.15" />
          <rect x="0" y="13.84" width="16.5" height="40.32" />
          <rect x="88.5" y="13.84" width="16.5" height="40.32" />
          <rect x="0" y="24.84" width="5.5" height="18.32" />
          <rect x="99.5" y="24.84" width="5.5" height="18.32" />
          {/* Penalty Spots */}
          <circle cx="11" cy="34" r="0.3" fill="#00FF88" />
          <circle cx="94" cy="34" r="0.3" fill="#00FF88" />
        </g>
      </svg>
      
      {/* Data Overlays */}
      <div className="absolute inset-0 w-full h-full pointer-events-none">
        {children}
      </div>
    </div>
  );
}
