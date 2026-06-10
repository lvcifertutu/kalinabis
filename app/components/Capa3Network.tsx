'use client';

import React from 'react';
import type { Esfera, Semilla, Sincronicidad, Micorriza } from '@/app/hooks/useCapa3API';

interface Capa3NetworkProps {
  esferas: Esfera[];
  semillas: Semilla[];
  sincros: Sincronicidad[];
  micorrizas: Micorriza[];
}

/**
 * Visualización de las conexiones entre elementos de Capa 3.
 * Dibuja SVG con líneas que representan las relaciones en el árbol.
 */
export function Capa3Network({ esferas, semillas, sincros, micorrizas }: Capa3NetworkProps) {
  // Total de elementos
  const totalElements = esferas.length + semillas.length + sincros.length + micorrizas.length;

  if (totalElements === 0) {
    return (
      <div className="absolute inset-0 flex items-center justify-center opacity-30">
        <span className="text-gray-500 text-xs font-mono">Red aún no activada...</span>
      </div>
    );
  }

  // Crear posiciones para SVG en grilla
  const positions: Record<string, [number, number]> = {};
  let index = 0;

  // Posicionar Esferas (arriba)
  esferas.forEach((e) => {
    const x = 20 + ((index % 3) * 30);
    const y = 15 + Math.floor(index / 3) * 20;
    positions[`esfera-${e.id}`] = [x, y];
    index++;
  });

  // Posicionar Semillas (derecha)
  semillas.forEach((s) => {
    const offset = index % 2;
    positions[`semilla-${s.id}`] = [80 + offset * 10, 20 + Math.floor(index / 2) * 15];
    index++;
  });

  // Posicionar Sincros (abajo)
  sincros.forEach((s) => {
    const x = 20 + ((index % 3) * 30);
    positions[`sincro-${s.id}`] = [x, 85 + Math.floor(index / 3) * 10];
    index++;
  });

  // Posicionar Micorrizas (izquierda)
  micorrizas.forEach((m) => {
    const offset = index % 2;
    positions[`micro-${m.id}`] = [5, 40 + offset * 20];
    index++;
  });

  return (
    <svg
      className="absolute inset-0 w-full h-full opacity-40"
      style={{ pointerEvents: 'none' }}
      viewBox="0 0 100 100"
      preserveAspectRatio="xMidYMid slice"
    >
      <defs>
        <linearGradient id="esfera-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.6" />
          <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.2" />
        </linearGradient>
        <linearGradient id="semilla-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#16a34a" stopOpacity="0.6" />
          <stop offset="100%" stopColor="#16a34a" stopOpacity="0.2" />
        </linearGradient>
        <linearGradient id="sincro-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#eab308" stopOpacity="0.6" />
          <stop offset="100%" stopColor="#eab308" stopOpacity="0.2" />
        </linearGradient>
      </defs>

      {/* Líneas de conexión: Esferas → Semillas */}
      {esferas.slice(0, 3).map((e) =>
        semillas.slice(0, 2).map((s) => {
          const [x1, y1] = positions[`esfera-${e.id}`] || [50, 50];
          const [x2, y2] = positions[`semilla-${s.id}`] || [50, 50];
          return (
            <line
              key={`line-${e.id}-${s.id}`}
              x1={x1}
              y1={y1}
              x2={x2}
              y2={y2}
              stroke="url(#esfera-grad)"
              strokeWidth="0.5"
              opacity="0.4"
            />
          );
        })
      )}

      {/* Líneas de conexión: Semillas → Sincros */}
      {semillas.slice(0, 2).map((s) =>
        sincros.slice(0, 2).map((syn) => {
          const [x1, y1] = positions[`semilla-${s.id}`] || [50, 50];
          const [x2, y2] = positions[`sincro-${syn.id}`] || [50, 50];
          return (
            <line
              key={`line-${s.id}-${syn.id}`}
              x1={x1}
              y1={y1}
              x2={x2}
              y2={y2}
              stroke="url(#semilla-grad)"
              strokeWidth="0.5"
              opacity="0.4"
            />
          );
        })
      )}

      {/* Puntos nodales: Esferas */}
      {esferas.slice(0, 3).map((e) => {
        const [x, y] = positions[`esfera-${e.id}`] || [50, 50];
        return (
          <circle
            key={`dot-esfera-${e.id}`}
            cx={x}
            cy={y}
            r="1"
            fill="#06b6d4"
            opacity="0.7"
          />
        );
      })}

      {/* Puntos nodales: Semillas */}
      {semillas.slice(0, 2).map((s) => {
        const [x, y] = positions[`semilla-${s.id}`] || [50, 50];
        return (
          <circle
            key={`dot-semilla-${s.id}`}
            cx={x}
            cy={y}
            r="1"
            fill="#16a34a"
            opacity="0.7"
          />
        );
      })}

      {/* Puntos nodales: Sincros */}
      {sincros.slice(0, 2).map((s) => {
        const [x, y] = positions[`sincro-${s.id}`] || [50, 50];
        return (
          <circle
            key={`dot-sincro-${s.id}`}
            cx={x}
            cy={y}
            r="1"
            fill="#eab308"
            opacity="0.7"
          />
        );
      })}
    </svg>
  );
}
