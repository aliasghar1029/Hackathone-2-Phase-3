// [Task]: T-016
// [From]: speckit.plan §5

// lib/auth.ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  jwt: {
    enabled: true,
    expiresIn: "7d"
  }
});

export async function signup(email: string, name: string, password: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, name, password })
  });

  if (!res.ok) throw new Error("Signup failed");

  const data = await res.json();
  localStorage.setItem("auth_token", data.token);
  localStorage.setItem("user_id", data.user.id);
  return data;
}

export async function signin(email: string, password: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signin`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  if (!res.ok) throw new Error("Invalid credentials");

  const data = await res.json();
  localStorage.setItem("auth_token", data.token);
  localStorage.setItem("user_id", data.user.id);
  return data;
}

export function signout() {
  localStorage.removeItem("auth_token");
  localStorage.removeItem("user_id");
}

export function getToken() {
  return localStorage.getItem("auth_token");
}

export function getUserId() {
  return localStorage.getItem("user_id");
}