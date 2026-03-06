const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function sendMessage(message, conversationId = null) {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to send message');
  }

  return response.json();
}

export async function getKnowledgeGraph() {
  const response = await fetch(`${API_URL}/api/knowledge-graph`);

  if (!response.ok) {
    throw new Error('Failed to fetch knowledge graph');
  }

  return response.json();
}
