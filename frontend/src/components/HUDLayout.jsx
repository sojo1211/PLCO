import React from 'react';

export default function HUDLayout({ title, subtitle, onBack, children }) {
  return (
    <div className="min-h-screen bg-axon-dark text-white font-sans flex flex-col">
      {/* Header */}
      <header className="border-b border-white/10 bg-black/40 backdrop-blur-md px-6 py-4 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-4">
          {onBack && (
            <button 
              onClick={onBack}
              className="text-gray-400 hover:text-axon-neon transition-colors"
            >
              ◀ BACK
            </button>
          )}
          <div>
            <h1 className="text-2xl font-mono text-axon-neon neon-text-green tracking-wider">{title}</h1>
            {subtitle && <p className="text-gray-400 text-sm mt-1">{subtitle}</p>}
          </div>
        </div>
        <div className="flex gap-4">
          <div className="px-3 py-1 rounded border border-axon-neon/50 text-axon-neon text-xs font-mono bg-axon-neon/10 shadow-[0_0_10px_rgba(0,255,136,0.2)]">
            LIVE DB CONNECTED
          </div>
          <div className="px-3 py-1 rounded border border-axon-blue/50 text-axon-blue text-xs font-mono bg-axon-blue/10 shadow-[0_0_10px_rgba(0,191,255,0.2)]">
            YOLO V1 ENGINE
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 p-6 flex flex-col gap-6 max-w-[1920px] mx-auto w-full">
        {children}
      </main>
    </div>
  );
}
