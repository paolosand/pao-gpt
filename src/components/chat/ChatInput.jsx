import { useState } from 'react';
import './ChatInput.css';

export default function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <form className="chat-input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="chat-input"
        placeholder="Ask anything..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={disabled}
      />
      <button
        type="submit"
        className="chat-send-btn"
        disabled={disabled || !input.trim()}
      >
        Send
      </button>
    </form>
  );
}
