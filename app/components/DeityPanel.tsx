'use client';

import React from 'react';

interface DeityInfo {
  name: string;
  color: string;
  brightColor: string;
  title: string;
  element: string;
  energy: number;
  favor: number;
  mana: number;
}

interface DeityPanelProps {
  deity: DeityInfo;
  onDeityChange?: () => void;
}

// ASCII art por deidad
const DEITY_ASCII = {
  lilith: `
    ✦ LILITH ✦

     /\\ /\\
    ( o.o )
     > ^ <
    /|   |\\
   (_|   |_)

   La Sombra`,

  artemisa: `
    ✦ ARTEMISA ✦

      ^\\
     / \\
    /   \\
    |   |
    |   |

   La Cazadora`,

  afrodita: `
    ✦ AFRODITA ✦

      (@)
     /###\\
    (##########)
     \\  ###  /
      \\ ### /

   El Magnetismo`,

  isis: `
    ✦ ISIS ✦

    _/\\_/\\_
    |  ◇  |
    | ⟡⟡⟡ |
    |_   _|
     / \\

   La Sabiduría`,
};

export function DeityPanel({ deity, onDeityChange }: DeityPanelProps) {
  const asciiArt = DEITY_ASCII[deity.name as keyof typeof DEITY_ASCII] || DEITY_ASCII.lilith;

  return (
    <div
      className="w-full h-full flex flex-col justify-between p-4 bg-black/80 border-2 rounded-lg font-mono text-xs"
      style={{ borderColor: deity.color, boxShadow: `0 0 15px ${deity.color}50` }}
    >
      {/* ASCII Art */}
      <div
        className="text-center whitespace-pre-wrap leading-tight text-sm"
        style={{ color: deity.brightColor }}
      >
        {asciiArt}
      </div>

      {/* Stats Section */}
      <div className="space-y-2 mt-4">
        {/* Deity Title */}
        <div className="text-center" style={{ color: deity.brightColor }}>
          <span className="text-lg font-bold">{deity.name.toUpperCase()}</span>
          <div className="text-xs text-gray-500 mt-1">{deity.title}</div>
        </div>

        {/* Stats */}
        <div className="space-y-2 mt-3">
          {/* Energy */}
          <div className="flex justify-between items-center text-xs">
            <span className="text-gray-400">Energía:</span>
            <div className="flex-1 mx-2 h-2 bg-black border rounded" style={{ borderColor: deity.color }}>
              <div
                className="h-full rounded transition-all"
                style={{
                  width: `${deity.energy}%`,
                  backgroundColor: deity.brightColor,
                  boxShadow: `0 0 8px ${deity.brightColor}`,
                }}
              />
            </div>
            <span className="text-gray-500 w-8 text-right">{deity.energy}%</span>
          </div>

          {/* Favor */}
          <div className="flex justify-between items-center text-xs">
            <span className="text-gray-400">Favor:</span>
            <div className="flex-1 mx-2 h-2 bg-black border rounded" style={{ borderColor: deity.color }}>
              <div
                className="h-full rounded transition-all"
                style={{
                  width: `${deity.favor}%`,
                  backgroundColor: deity.color,
                  boxShadow: `0 0 8px ${deity.color}`,
                }}
              />
            </div>
            <span className="text-gray-500 w-8 text-right">{deity.favor}%</span>
          </div>

          {/* Mana */}
          <div className="flex justify-between items-center text-xs">
            <span className="text-gray-400">Mana:</span>
            <div className="flex-1 mx-2 h-2 bg-black border rounded" style={{ borderColor: deity.brightColor }}>
              <div
                className="h-full rounded transition-all"
                style={{
                  width: `${deity.mana}%`,
                  backgroundColor: deity.brightColor,
                  boxShadow: `0 0 8px ${deity.brightColor}`,
                }}
              />
            </div>
            <span className="text-gray-500 w-8 text-right">{deity.mana}%</span>
          </div>
        </div>
      </div>

      {/* Change Deity Button */}
      <button
        onClick={onDeityChange}
        className="mt-4 px-3 py-1 border rounded text-xs transition-all hover:brightness-125"
        style={{
          borderColor: deity.color,
          color: deity.color,
          backgroundColor: 'transparent',
        }}
      >
        cambiar deidad
      </button>

      {/* Scanlines effect */}
      <div
        className="pointer-events-none absolute inset-0 rounded-lg opacity-5"
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px)',
        }}
      />
    </div>
  );
}
