import { useState, useRef, useEffect } from 'react';

interface Props {
  onSend: (message: string) => void;
  isStreaming: boolean;
  disabled: boolean;
}

export default function ChatInput({ onSend, isStreaming, disabled }: Props) {
  const [input, setInput] = useState('');
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (!isStreaming && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isStreaming]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming || disabled) return;
    onSend(input.trim());
    setInput('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-gray-200 p-4 flex gap-3 items-end"
    >
      <textarea
        ref={inputRef}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={
          disabled
            ? 'Select a child profile to start...'
            : 'Ask a parenting question... (e.g., "What should my 6-month-old be eating?")'
        }
        rows={2}
        disabled={isStreaming || disabled}
        className="flex-1 px-4 py-2 border border-gray-300 rounded-xl text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary-400 disabled:bg-gray-100"
      />
      <button
        type="submit"
        disabled={isStreaming || disabled || !input.trim()}
        className="px-5 py-2 bg-primary-500 text-white rounded-xl text-sm font-medium hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isStreaming ? 'Thinking...' : 'Send'}
      </button>
    </form>
  );
}
