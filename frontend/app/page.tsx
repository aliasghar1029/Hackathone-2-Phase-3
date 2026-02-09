// [Task]: T-027
// [From]: speckit.plan §2.1

import Link from 'next/link';
import { Button } from '@/components/ui/Button';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900 flex flex-col">
      {/* Navigation */}
      <nav className="p-6 flex justify-between items-center">
        <div className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">TODO AI</div>
        <div className="flex gap-4">
          <Link href="/signin">
            <Button variant="secondary">Sign In</Button>
          </Link>
          <Link href="/signup">
            <Button>Get Started</Button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center p-6 text-center">
        <div className="max-w-4xl mx-auto">
          <div className="inline-block px-4 py-1 mb-4 rounded-full bg-white/10 backdrop-blur-sm border border-white/20">
            <span className="text-sm font-medium text-purple-300">AI-Powered Task Management</span>
          </div>
          
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight">
            Transform Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">Productivity</span> with AI
          </h1>
          
          <p className="text-lg md:text-xl text-white/80 max-w-2xl mx-auto mb-10 leading-relaxed">
            Manage your tasks naturally with AI conversation. Simply tell us what you need to do and we'll handle the rest.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/signup">
              <Button size="lg" className="min-w-[200px]">
                Start Free Trial
              </Button>
            </Link>
            <Link href="/chat">
              <Button variant="secondary" size="lg" className="min-w-[200px]">
                Try Demo
              </Button>
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="p-6 text-center text-white/60 text-sm">
        © {new Date().getFullYear()} TODO AI Chatbot. All rights reserved.
      </footer>
    </div>
  );
}