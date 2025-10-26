import React, { useState, useEffect, useRef } from 'react';
import api from '../services/api';

const Chat = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm your AI language tutor. Ask me anything or just start a conversation.", sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (input.trim() && !loading) {
      const userMessage = { text: input, sender: 'user' };
      setMessages(prev => [...prev, userMessage]);
      setInput('');
      setLoading(true);

      try {
        // Reverted to the reliable, non-streaming api.post call
        const response = await api.post('/chat', { text: input });
        const botMessage = { text: response.data.message, sender: 'bot' };
        setMessages(prev => [...prev, botMessage]);
      } catch (error) {
        const errorMessage = { text: "Sorry, I couldn't connect to the server.", sender: 'bot' };
        setMessages(prev => [...prev, errorMessage]);
        console.error("Chat send failed", error);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-md">
      <div className="p-4 border-b">
        <h2 className="text-xl font-bold">Conversation</h2>
      </div>
      <div className="flex-grow p-4 overflow-y-auto">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
            <div className={`max-w-lg px-4 py-2 rounded-lg shadow ${msg.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}>
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="p-4 border-t">
        <div className="flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            className="flex-grow p-2 border rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type your message..."
            disabled={loading}
          />
          <button onClick={handleSend} className="px-4 py-2 bg-blue-600 text-white rounded-r-md hover:bg-blue-700 disabled:bg-blue-300" disabled={loading}>
            {loading ? '...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;