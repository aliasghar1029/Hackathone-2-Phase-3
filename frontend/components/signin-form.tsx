"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";
import { useAuth } from "@/components/auth-provider";
import { signin } from "@/lib/api";

export function SigninForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { login } = useAuth();

  const isValid =
    email.includes("@") && email.includes(".") && password.length >= 8;

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!isValid) return;

    setIsLoading(true);
    setError("");

    try {
      const data = await signin(email, password);
      login(data.user, data.token);
      router.push("/tasks");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Invalid email or password");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="w-full max-w-md mx-auto"
    >
      <div className="glass rounded-2xl p-8">
        <h1 className="text-3xl font-bold text-white text-center mb-8">
          Sign In
        </h1>

        {error && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            className="mb-6 p-3 rounded-xl bg-red-500/20 border border-red-500/40 text-red-200 text-sm"
            role="alert"
          >
            {error}
          </motion.div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-5">
          <div className="flex flex-col gap-2">
            <label
              htmlFor="email"
              className="text-sm font-medium text-white/80"
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              required
              placeholder="you@example.com"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setError("");
              }}
              className="glass-input rounded-xl px-4 py-3 w-full"
              aria-required="true"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label
              htmlFor="password"
              className="text-sm font-medium text-white/80"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              minLength={8}
              placeholder="••••••••"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setError("");
              }}
              className="glass-input rounded-xl px-4 py-3 w-full"
              aria-required="true"
            />
          </div>

          <motion.button
            type="submit"
            disabled={!isValid || isLoading}
            whileHover={isValid && !isLoading ? { scale: 1.02 } : {}}
            whileTap={isValid && !isLoading ? { scale: 0.95 } : {}}
            className="w-full py-3 rounded-xl bg-white text-purple-700 font-bold text-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:brightness-110 flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                Signing in...
              </>
            ) : (
              "Sign In"
            )}
          </motion.button>
        </form>

        <p className="text-center text-white/60 mt-6 text-sm">
          {"Don't have an account?"}{" "}
          <Link
            href="/signup"
            className="text-white font-bold hover:underline"
          >
            Sign up
          </Link>
        </p>
      </div>
    </motion.div>
  );
}
