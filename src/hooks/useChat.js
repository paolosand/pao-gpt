import { useState, useCallback } from 'react';
import { sendMessage } from '../services/api';

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const send = useCallback(async (userMessage) => {
    // Add user message immediately
    const userMsg = {
      role: 'user',
      content: userMessage,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMsg]);

    setIsLoading(true);
    setError(null);

    try {
      const response = await sendMessage(userMessage, conversationId);

      // Update conversation ID if new
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant message
      const assistantMsg = {
        role: 'assistant',
        content: response.response,
        sources: response.sources,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, assistantMsg]);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, [conversationId]);

  const reset = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    send,
    reset,
  };
}
