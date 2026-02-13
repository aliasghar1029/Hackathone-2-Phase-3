'use client';

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/components/auth-provider';
import { sendChatMessage } from '@/lib/api';
import { Send, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export function ChatInterface() {
  const { user, token } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | undefined>();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  async function handleSend() {
    if (!input.trim() || loading || !user || !token) return;

    const userMessage = input.trim();
    setInput('');
    setLoading(true);

    // Add user message immediately
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);

    try {
      const response = await sendChatMessage(
        user.id,
        token,
        userMessage,
        conversationId
      );

      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add AI response
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: response.response }
      ]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.'
        }
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyPress(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-200px)] max-w-4xl mx-auto">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] px-4 py-3 rounded-2xl ${
                  msg.role === 'user'
                    ? 'bg-purple-600 text-white font-medium'
                    : 'bg-white/10 backdrop-blur-lg text-white border border-white/20'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="bg-white/10 backdrop-blur-lg text-white px-4 py-3 rounded-2xl border border-white/20">
              <Loader2 className="w-5 h-5 animate-spin" />
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white/10 backdrop-blur-lg border-t border-white/20">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type a message... (e.g., 'Add a task to buy milk')"
            className="flex-1 px-4 py-3 rounded-full bg-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50"
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="px-6 py-3 bg-white text-purple-600 rounded-full font-semibold hover:bg-white/90 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center gap-2"
          >
            <Send className="w-5 h-5" />
            Send
          </button>
        </div>
        
        <p className="text-white/60 text-xs mt-2 text-center">
          Try: "Add a task", "Show my tasks", "Mark task 1 as done"
        </p>
      </div>
    </div>
  );
}