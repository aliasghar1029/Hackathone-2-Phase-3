// [Task]: T-031
// [From]: speckit.plan §2.1

import { ChatInterface } from '@/components/chat/ChatInterface';

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 to-blue-900 flex flex-col">
      <div className="p-6 text-center">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-2">AI Task Assistant</h1>
        <p className="text-white/70">Chat with your AI assistant to manage your tasks</p>
      </div>
      <div className="flex-1">
        <ChatInterface />
      </div>
    </div>
  );
}