import { useEffect, useRef } from 'react';
import Message from './Message';
import './MessageList.css';

export default function MessageList({ messages, isLoading }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="message-list">
      {messages.map((message, i) => (
        <Message key={i} message={message} />
      ))}
      {isLoading && (
        <div className="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      )}
      <div ref={endRef} />
    </div>
  );
}
