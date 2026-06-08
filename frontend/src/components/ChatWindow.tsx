import ReactMarkdown from 'react-markdown';
import type { ChatMessage } from '../lib/types';

interface Props {
  messages: ChatMessage[];
  isStreaming: boolean;
}

export default function ChatWindow({ messages, isStreaming }: Props) {
  return (
    <div className="flex flex-col gap-3 p-4 overflow-y-auto h-full">
      {messages.length === 0 && (
        <div className="flex-1 flex items-center justify-center text-gray-400 text-sm">
          Select a child profile and ask a parenting question to get started.
        </div>
      )}
      {messages.map((msg, i) => (
        <div
          key={i}
          className={
            msg.role === 'user'
              ? 'flex justify-end'
              : msg.role === 'system'
                ? 'flex justify-center'
                : 'flex justify-start'
          }
        >
          {msg.role === 'system' ? (
            <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-2 text-sm max-w-[80%]">
              {msg.content}
            </div>
          ) : msg.safety_triggered ? (
            <div className="bg-red-50 border-2 border-red-400 rounded-2xl px-5 py-4 max-w-[80%]">
              <ReactMarkdown className="prose prose-sm text-red-800">
                {msg.content}
              </ReactMarkdown>
            </div>
          ) : (
            <div className={msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-assistant'}>
              <ReactMarkdown className="prose prose-sm max-w-none">
                {msg.content}
              </ReactMarkdown>
            </div>
          )}
        </div>
      ))}
      {isStreaming && (
        <div className="flex justify-start">
          <div className="chat-bubble-assistant">
            <span className="inline-block w-2 h-4 bg-primary-500 animate-pulse rounded-full" />
          </div>
        </div>
      )}
    </div>
  );
}
