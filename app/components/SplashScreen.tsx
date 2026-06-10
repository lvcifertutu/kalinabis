'use client';

import React, { useEffect, useState } from 'react';

interface SplashScreenProps {
  onComplete: () => void;
  duration?: number;
}

export function SplashScreen({ onComplete, duration = 4200 }: SplashScreenProps) {
  const [phase, setPhase] = useState<'dark' | 'candle' | 'text' | 'fade'>('dark');

  useEffect(() => {
    const t1 = setTimeout(() => setPhase('candle'), 400);
    const t2 = setTimeout(() => setPhase('text'), 1400);
    const t3 = setTimeout(() => setPhase('fade'), duration - 600);
    const t4 = setTimeout(() => onComplete(), duration);
    return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); clearTimeout(t4); };
  }, [duration, onComplete]);

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: '#040508',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        transition: 'opacity 0.7s ease',
        opacity: phase === 'fade' ? 0 : 1,
        zIndex: 1000,
      }}
    >
      {/* Grain */}
      <div className="grain-overlay" />

      {/* Vela */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          transition: 'opacity 0.8s ease',
          opacity: phase === 'dark' ? 0 : 1,
          marginBottom: '2.5rem',
          position: 'relative',
        }}
      >
        {/* Halo de luz ambiental */}
        <div
          style={{
            position: 'absolute',
            width: '180px',
            height: '180px',
            borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(255, 180, 60, 0.12) 0%, transparent 70%)',
            top: '-60px',
            left: '50%',
            transform: 'translateX(-50%)',
            animation: 'flicker 3s ease-in-out infinite',
          }}
        />

        {/* Llama */}
        <div
          style={{
            width: '18px',
            height: '26px',
            background: 'linear-gradient(to top, #ff8c00, #ffd700, #fff8e0)',
            clipPath: 'polygon(50% 0%, 80% 60%, 100% 85%, 70% 100%, 30% 100%, 0% 85%, 20% 60%)',
            animation: 'flame-body 1.8s ease-in-out infinite, flicker 2.3s ease-in-out infinite',
            filter: 'drop-shadow(0 0 6px rgba(255, 180, 60, 0.8)) drop-shadow(0 0 14px rgba(255, 140, 0, 0.5))',
            marginBottom: '-2px',
          }}
        />

        {/* Mecha */}
        <div
          style={{
            width: '2px',
            height: '8px',
            background: 'linear-gradient(to bottom, #555, #222)',
            marginBottom: '-1px',
            zIndex: 1,
          }}
        />

        {/* Cuerpo de la vela */}
        <div
          style={{
            width: '16px',
            height: '56px',
            background: 'linear-gradient(to right, #e8dcc8, #f5f1e8, #e0d4b8)',
            borderRadius: '2px 2px 1px 1px',
            boxShadow: '0 2px 12px rgba(0,0,0,0.6)',
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          {/* Cera derretida */}
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: '3px',
              width: '4px',
              height: '12px',
              background: 'rgba(255,220,160,0.5)',
              borderRadius: '0 0 50% 50%',
            }}
          />
        </div>

        {/* Base de la vela */}
        <div
          style={{
            width: '28px',
            height: '6px',
            background: 'linear-gradient(to right, #3a2a1a, #6b4f35, #3a2a1a)',
            borderRadius: '1px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.8)',
          }}
        />
      </div>

      {/* Texto */}
      <div
        style={{
          textAlign: 'center',
          opacity: phase === 'dark' || phase === 'candle' ? 0 : 1,
          transform: phase === 'dark' || phase === 'candle' ? 'translateY(10px)' : 'translateY(0)',
          transition: 'opacity 1s ease, transform 1s ease',
        }}
      >
        {/* Línea decorativa superior */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.75rem',
            marginBottom: '1rem',
          }}
        >
          <div style={{ width: '40px', height: '1px', background: 'linear-gradient(to right, transparent, rgba(200,157,92,0.6))' }} />
          <span style={{ color: 'rgba(200,157,92,0.6)', fontSize: '10px', letterSpacing: '0.3em', fontFamily: 'var(--font-display)' }}>✦</span>
          <div style={{ width: '40px', height: '1px', background: 'linear-gradient(to left, transparent, rgba(200,157,92,0.6))' }} />
        </div>

        {/* Nombre */}
        <h1
          style={{
            fontFamily: 'var(--font-deco)',
            fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            fontWeight: 400,
            letterSpacing: '0.25em',
            color: 'transparent',
            background: 'linear-gradient(135deg, #c89d5c, #f0d898, #c89d5c)',
            backgroundSize: '200% 200%',
            WebkitBackgroundClip: 'text',
            backgroundClip: 'text',
            animation: 'shimmer-gold 4s ease infinite',
            margin: '0 0 0.5rem',
            lineHeight: 1.1,
          }}
        >
          KALINABIS
        </h1>

        {/* Subtítulo */}
        <p
          style={{
            fontFamily: 'var(--font-sacred)',
            fontStyle: 'italic',
            fontSize: '0.9rem',
            letterSpacing: '0.12em',
            color: 'rgba(245, 241, 232, 0.45)',
            margin: '0 0 2rem',
          }}
        >
          Altar de Magia del Caos
        </p>

        {/* Línea de carga */}
        <div
          style={{
            width: '120px',
            height: '1px',
            background: 'rgba(200,157,92,0.15)',
            margin: '0 auto',
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background: 'linear-gradient(to right, transparent, rgba(200,157,92,0.8), transparent)',
              animation: 'shimmer-gold 2s ease-in-out infinite',
            }}
          />
        </div>

        {/* Línea decorativa inferior */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.75rem',
            marginTop: '2rem',
          }}
        >
          <div style={{ width: '40px', height: '1px', background: 'linear-gradient(to right, transparent, rgba(200,157,92,0.6))' }} />
          <span style={{ color: 'rgba(200,157,92,0.6)', fontSize: '10px', letterSpacing: '0.3em', fontFamily: 'var(--font-display)' }}>✦</span>
          <div style={{ width: '40px', height: '1px', background: 'linear-gradient(to left, transparent, rgba(200,157,92,0.6))' }} />
        </div>
      </div>

      {/* Glow en el suelo */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: '50%',
          transform: 'translateX(-50%)',
          width: '300px',
          height: '1px',
          background: 'linear-gradient(to right, transparent, rgba(200,157,92,0.15), transparent)',
          transition: 'opacity 1s ease',
          opacity: phase === 'dark' ? 0 : 1,
        }}
      />
    </div>
  );
}
