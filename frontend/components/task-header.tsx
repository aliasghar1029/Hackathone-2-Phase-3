"use client";

import { motion } from "framer-motion";
import { LogOut } from "lucide-react";
import type { User } from "@/lib/types";

interface TaskHeaderProps {
  user: User;
  onSignout: () => void;
}

export function TaskHeader({ user, onSignout }: TaskHeaderProps) {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="glass rounded-2xl p-4 md:p-6"
    >
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-col gap-1">
          <h1 className="text-2xl md:text-3xl font-bold text-white text-balance">
            My Tasks
          </h1>
          <div className="flex flex-col sm:flex-row sm:items-center sm:gap-2">
            <p className="text-white/80 text-sm font-medium">{user.name}</p>
            <span className="hidden sm:block text-white/40">{"/"}</span>
            <p className="text-white/60 text-sm">{user.email}</p>
          </div>
        </div>
        <motion.button
          onClick={onSignout}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white/80 hover:text-white transition-all duration-200 text-sm font-medium self-start sm:self-center"
          aria-label="Sign out"
        >
          <LogOut className="h-4 w-4" />
          Sign Out
        </motion.button>
      </div>
    </motion.header>
  );
}
