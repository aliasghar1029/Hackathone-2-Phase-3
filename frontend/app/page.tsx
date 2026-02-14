"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/auth-provider";
import { Loader2 } from "lucide-react";

export default function HomePage() {
  const { token, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      // Redirect based on auth status
      if (token) {
        router.replace("/tasks");
      } else {
        router.replace("/signin");
      }
    }
  }, [isLoading, token, router]);

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-700 via-purple-600 to-blue-500">
      <div className="text-center">
        <Loader2 className="h-8 w-8 animate-spin text-white/80 mx-auto mb-4" />
        <p className="text-white/80">Loading...</p>
      </div>
    </main>
  );
}
