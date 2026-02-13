import React from "react"
import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/components/auth-provider";
import { Toaster } from "sonner";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "My Tasks - Glassmorphic Todo App",
  description:
    "A beautiful glassmorphic todo application to manage your tasks with style.",
};

export const viewport: Viewport = {
  themeColor: "#7c3aed",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.variable} font-sans antialiased min-h-screen bg-gradient-to-br from-purple-700 via-purple-600 to-blue-500`}
      >
        <AuthProvider>
          {children}
          <Toaster
            position="top-right"
            toastOptions={{
              style: {
                background: "rgba(255,255,255,0.15)",
                backdropFilter: "blur(12px)",
                border: "1px solid rgba(255,255,255,0.2)",
                color: "#fff",
              },
            }}
          />
        </AuthProvider>
      </body>
    </html>
  );
}
