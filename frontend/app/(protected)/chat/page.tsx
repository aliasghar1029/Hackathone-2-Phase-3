'use client';

import { ChatInterface } from '@/components/chat/ChatInterface';
import { useAuth } from '@/components/auth-provider';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export default function ChatPage() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-500 p-4">
      {/* Header */}
      <div className="max-w-4xl mx-auto mb-4">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-4 border border-white/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link
                href="/tasks"
                className="text-white/80 hover:text-white transition"
              >
                <ArrowLeft className="w-6 h-6" />
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-white">AI Chat Assistant</h1>
                <p className="text-white/80 text-sm">Manage tasks with natural language</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-white font-medium">{user?.name}</p>
              <button
                onClick={logout}
                className="text-white/80 hover:text-white text-sm transition"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Chat Interface */}
      <ChatInterface />
    </div>
  );
}