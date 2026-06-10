'use client';

import React, { useRef, useEffect, useState } from 'react';

interface Message {
  type: 'input' | 'output' | 'system';
  content: string;
  timestamp?: Date;
}

interface TerminalProps {
  onCommand?: (cmd: string) => void;
  messages?: Message[];
  isLoading?: boolean;
  deityColor?: string;
}

export function Terminal({
  onCommand,
  messages = [],
  isLoading = false,
  deityColor = '#00ffff',
}: TerminalProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const terminalRef = useRef<HTMLDivElement>(null);
  const [inputValue, setInputValue] = useState('');

  // Auto-scroll terminal
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && onCommand) {
      onCommand(inputValue);
      setInputValue('');
    }
  };

  return (
    <div
      className="flex flex-col w-full h-full bg-black/80 border-2 rounded-lg p-4 font-mono text-sm"
      style={{ borderColor: deityColor, boxShadow: `0 0 10px ${deityColor}40` }}
    >
      {/* Terminal Header */}
      <div className="flex items-center justify-between pb-3 mb-3 border-b" style={{ borderColor: deityColor }}>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full" style={{ backgroundColor: deityColor }} />
          <span style={{ color: deityColor }}>KALINABIS TERMINAL</span>
        </div>
        <span className="text-gray-500 text-xs">v2.0</span>
      </div>

      {/* Output Area */}
      <div
        ref={terminalRef}
        className="flex-1 overflow-y-auto mb-3 space-y-1 pr-2"
        style={{
          maskImage: 'linear-gradient(to bottom, transparent, black 20px)',
          WebkitMaskImage: 'linear-gradient(to bottom, transparent, black 20px)',
        }}
      >
        {messages.length === 0 && (
          <div className="text-gray-600">
            {'> '}
            <span style={{ color: deityColor }}>awaiting_command.../</span>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className="break-words">
            {msg.type === 'input' && (
              <span>
                {'> '}
                <span style={{ color: deityColor }}>{msg.content}</span>
              </span>
            )}
            {msg.type === 'output' && (
              <span className="text-gray-300 block whitespace-pre-wrap">{msg.content}</span>
            )}
            {msg.type === 'system' && (
              <span style={{ color: deityColor }} className="text-xs opacity-75">
                {msg.content}
              </span>
            )}
          </div>
        ))}

        {isLoading && (
          <div style={{ color: deityColor }} className="animate-pulse">
            ▌ processing...
          </div>
        )}
      </div>

      {/* Input Line */}
      <form onSubmit={handleSubmit} className="flex items-center border-t pt-3" style={{ borderColor: deityColor }}>
        <span style={{ color: deityColor }}>{'>'}</span>
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="write command... (/runas, /iching, /tarot, /ayuda)"
          className="flex-1 ml-2 bg-transparent text-gray-100 placeholder-gray-600 outline-none"
          style={{ caretColor: deityColor }}
        />
        {inputValue && (
          <span
            className="animate-pulse ml-2"
            style={{ color: deityColor }}
          >
            ▌
          </span>
        )}
      </form>

      {/* Scanlines effect */}
      <div
        className="pointer-events-none absolute inset-0 rounded-lg opacity-5"
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,255,0.03) 2px, rgba(0,255,255,0.03) 4px)',
        }}
      />
    </div>
  );
}
