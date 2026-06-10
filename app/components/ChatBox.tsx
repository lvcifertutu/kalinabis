'use client';

import React, { useRef, useEffect } from 'react';

interface ChatMessage {
  role: 'user' | 'deity' | 'system' | 'presentation';
  content: string;
  timestamp?: Date;
}

interface ChatBoxProps {
  messages: ChatMessage[];
  isLoading?: boolean;
  deityName?: string;
  deityColor?: string;
  onMessage?: (text: string) => void;
}

export function ChatBox({
  messages,
  isLoading = false,
  deityName = 'LILITH',
  deityColor = '#00ffff',
  onMessage,
}: ChatBoxProps) {
  const chatRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = () => {
    const text = inputRef.current?.value.trim();
    if (text && onMessage) {
      onMessage(text);
      inputRef.current!.value = '';
    }
  };

  return (
    <div
      className="flex flex-col w-full h-full bg-black/80 border-2 rounded-lg p-4 font-mono text-sm"
      style={{ borderColor: deityColor, boxShadow: `0 0 10px ${deityColor}40` }}
    >
      {/* Chat Header */}
      <div className="flex items-center justify-between pb-3 mb-3 border-b" style={{ borderColor: deityColor }}>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full" style={{ backgroundColor: deityColor }} />
          <span style={{ color: deityColor }}>CHAT RITUAL</span>
        </div>
        <span style={{ color: deityColor }} className="text-xs">
          {deityName}
        </span>
      </div>

      {/* Messages Area */}
      <div
        ref={chatRef}
        className="flex-1 overflow-y-auto mb-3 space-y-2 pr-2"
        style={{
          maskImage: 'linear-gradient(to bottom, transparent, black 20px)',
          WebkitMaskImage: 'linear-gradient(to bottom, transparent, black 20px)',
        }}
      >
        {messages.length === 0 && (
          <div style={{ color: deityColor }} className="text-center py-4">
            <span style={{ color: deityColor }}>✦ Ritual awaiting... ✦</span>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className="break-words">
            {msg.role === 'presentation' && (
              <div className="mb-4 p-3 rounded-lg" style={{ backgroundColor: `${deityColor}15`, borderLeft: `2px solid ${deityColor}` }}>
                <pre style={{ color: deityColor }} className="text-xs font-mono whitespace-pre-wrap overflow-x-auto text-center leading-relaxed">
                  {msg.content}
                </pre>
              </div>
            )}

            {msg.role === 'deity' && (
              <div className="mb-2">
                <div style={{ color: deityColor }} className="font-bold text-xs mb-1">
                  {deityName}:
                </div>
                <div className="text-gray-200 text-xs leading-relaxed pl-3 border-l-2" style={{ borderColor: deityColor }}>
                  &quot;{msg.content}&quot;
                </div>
              </div>
            )}

            {msg.role === 'user' && (
              <div className="mb-2">
                <div className="text-gray-400 text-xs">TÚ:</div>
                <div className="text-gray-300 text-xs pl-3">&quot;{msg.content}&quot;</div>
              </div>
            )}

            {msg.role === 'system' && (
              <div className="text-gray-500 text-xs italic">{msg.content}</div>
            )}
          </div>
        ))}

        {isLoading && (
          <div style={{ color: deityColor }} className="animate-pulse text-xs">
            ▌ {deityName} está respondiendo...
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t pt-3" style={{ borderColor: deityColor }}>
        <textarea
          ref={inputRef}
          placeholder="Escribe tu respuesta al ritual..."
          className="w-full bg-black text-gray-100 placeholder-gray-600 outline-none text-xs p-2 border rounded resize-none"
          style={{ borderColor: deityColor, caretColor: deityColor }}
          rows={2}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <button
          onClick={handleSend}
          disabled={isLoading}
          className="mt-2 px-3 py-1 border rounded text-xs transition-all hover:brightness-125 disabled:opacity-50"
          style={{
            borderColor: deityColor,
            color: deityColor,
            backgroundColor: 'transparent',
          }}
        >
          enviar
        </button>
      </div>

      {/* Scanlines */}
      <div
        className="pointer-events-none absolute inset-0 rounded-lg opacity-5"
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,255,0.03) 2px, rgba(0,255,255,0.03) 4px)',
        }}
      />
    </div>
  );
}
