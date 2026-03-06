import { useChat } from '../../hooks/useChat';
import WelcomeScreen from './WelcomeScreen';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import './ChatInterface.css';

export default function ChatInterface() {
  const { messages, isLoading, error, send } = useChat();

  return (
    <div className="chat-interface">
      {messages.length === 0 ? (
        <WelcomeScreen />
      ) : (
        <MessageList messages={messages} isLoading={isLoading} />
      )}

      {error && (
        <div className="chat-error">
          Error: {error}
        </div>
      )}

      <ChatInput onSend={send} disabled={isLoading} />
    </div>
  );
}
