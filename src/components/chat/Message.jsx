import './Message.css';

export default function Message({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-assistant'}`}>
      <div className="message-content">
        {message.content}
      </div>
      {message.sources && message.sources.length > 0 && (
        <div className="message-sources">
          <strong>Sources:</strong>
          <ul>
            {message.sources.map((source, i) => (
              <li key={i}>{source}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
