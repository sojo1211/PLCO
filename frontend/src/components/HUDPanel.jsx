import React from 'react';

export default function HUDPanel({ title, children, className = '' }) {
  return (
    <div className={`glass-panel p-4 flex flex-col ${className}`}>
      {title && (
        <h3 className="text-axon-neon text-sm font-mono tracking-wider mb-3 uppercase neon-text-green border-b border-axon-neon/30 pb-2">
          {title}
        </h3>
      )}
      <div className="flex-1 overflow-auto">
        {children}
      </div>
    </div>
  );
}
