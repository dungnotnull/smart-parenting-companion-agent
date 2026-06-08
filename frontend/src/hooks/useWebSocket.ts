import { useRef, useCallback, useState } from 'react';
import type { ChatMessage, WsMessage } from '../lib/types';

export function useWebSocket(childId: number | null) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const streamBufferRef = useRef('');

  const sendMessage = useCallback(
    (content: string) => {
      if (!childId) return;

      const userMsg: ChatMessage = { role: 'user', content };
      setMessages((prev) => [...prev, userMsg]);

      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${wsProtocol}//${window.location.host}/api/chat/stream`;
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;
      streamBufferRef.current = '';
      setIsStreaming(true);

      const assistantMsg: ChatMessage = { role: 'assistant', content: '' };
      setMessages((prev) => [...prev, assistantMsg]);

      ws.onopen = () => {
        ws.send(
          JSON.stringify({
            child_id: childId,
            message: content,
            session_id: localStorage.getItem('session_id') || undefined,
          }),
        );
      };

      ws.onmessage = (event) => {
        const data: WsMessage = JSON.parse(event.data);

        if (data.type === 'meta' && data.session_id) {
          localStorage.setItem('session_id', data.session_id);
        }

        if (data.type === 'token' && data.content) {
          streamBufferRef.current += data.content;
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            if (last.role === 'assistant') {
              last.content = streamBufferRef.current;
            }
            return updated;
          });
        }

        if (data.type === 'safety_alert') {
          streamBufferRef.current = data.content || '';
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            if (last.role === 'assistant') {
              last.content = data.content || '';
              last.safety_triggered = true;
            }
            return updated;
          });
          setIsStreaming(false);
        }

        if (data.type === 'error') {
          setMessages((prev) => [
            ...prev,
            { role: 'system', content: `Error: ${data.content}` },
          ]);
          setIsStreaming(false);
        }

        if (data.type === 'done') {
          setIsStreaming(false);
        }
      };

      ws.onerror = () => {
        setMessages((prev) => [
          ...prev,
          { role: 'system', content: 'Connection error. Please check if the backend is running.' },
        ]);
        setIsStreaming(false);
      };
    },
    [childId],
  );

  return { messages, sendMessage, isStreaming };
}
