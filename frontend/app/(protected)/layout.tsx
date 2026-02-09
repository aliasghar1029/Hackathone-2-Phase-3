// [Task]: T-030
// [From]: speckit.plan §2.1

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getToken } from '@/lib/auth';
import { Button } from '@/components/ui/Button';
import ErrorBoundary from '@/components/ErrorBoundary';

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const router = useRouter();

  useEffect(() => {
    const token = getToken();
    if (token) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
      router.push('/signin');
    }
  }, [router]);

  if (isAuthenticated === null) {
    // Loading state
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 to-blue-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect via useEffect
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gradient-to-br from-purple-900 to-blue-900">
        {/* Navigation */}
        <nav className="p-4 flex justify-between items-center border-b border-white/10 bg-white/5 backdrop-blur-sm">
          <div className="text-xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">TODO AI</div>
          <div className="flex gap-2">
            <Button 
              variant="secondary" 
              onClick={() => router.push('/chat')}
              className="px-4 py-2"
            >
              💬 Chat
            </Button>
            <Button 
              variant="secondary" 
              onClick={() => router.push('/tasks')}
              className="px-4 py-2"
            >
              ✅ Tasks
            </Button>
            <Button
              variant="secondary"
              onClick={() => {
                localStorage.removeItem('auth_token');
                localStorage.removeItem('user_id');
                router.push('/');
              }}
              className="px-4 py-2"
            >
              🚪 Sign Out
            </Button>
          </div>
        </nav>

        <main className="p-4">{children}</main>
      </div>
    </ErrorBoundary>
  );
}