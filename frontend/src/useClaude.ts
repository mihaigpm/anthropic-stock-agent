import { useState } from 'react';

export const useClaude = () => {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (prompt: string) => {
    setIsLoading(true);
    const newMessages = [...messages, { role: 'user', content: prompt }];
    
    // Add a loading placeholder for the assistant
    setMessages([...newMessages, { role: 'assistant', content: 'Thinking...' }]);

    try {
      // 1. Point to the new agent endpoint
      const response = await fetch('http://localhost:8000/v1/chat/agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // 2. Parse standard JSON instead of a stream
      const data = await response.json();
      
      // 3. Update the UI with the final result
      setMessages([...newMessages, { role: 'assistant', content: data.content }]);
      
    } catch (err: any) {
      console.error('API Error:', err);
      setMessages([...newMessages, { role: 'assistant', content: 'Error connecting to Claude.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return { messages, sendMessage, isLoading };
};