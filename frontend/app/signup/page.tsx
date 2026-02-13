"use client";

import { useAuth } from "@/components/auth-provider";
import { SignupForm } from "@/components/signup-form";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function SignupPage() {
  const { token, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && token) {
      router.replace("/tasks");
    }
  }, [isLoading, token, router]);

  if (isLoading || token) return null;

  return (
    <main className="min-h-screen flex items-center justify-center px-4 py-12">
      <SignupForm />
    </main>
  );
}
