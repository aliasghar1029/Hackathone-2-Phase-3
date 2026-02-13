"use client";

import { motion } from "framer-motion";
import { Pencil, Trash2, Check } from "lucide-react";
import type { Task } from "@/lib/types";
import { formatDistanceToNow, format } from "date-fns";

interface TaskCardProps {
  task: Task;
  onToggle: (taskId: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

function formatDate(dateStr: string) {
  try {
    const date = new Date(dateStr);
    const now = new Date();
    const diffDays = Math.floor(
      (now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24)
    );
    if (diffDays < 7) {
      return formatDistanceToNow(date, { addSuffix: true });
    }
    return format(date, "MMM d, yyyy");
  } catch {
    return dateStr;
  }
}

export function TaskCard({ task, onToggle, onEdit, onDelete }: TaskCardProps) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.02 }}
      className={`glass rounded-2xl p-5 flex flex-col gap-3 transition-all duration-200 hover:border-white/30 ${
        task.completed ? "opacity-70" : ""
      }`}
    >
      {/* Top row: checkbox, title, actions */}
      <div className="flex items-start gap-3">
        <button
          onClick={() => onToggle(task.id)}
          className={`mt-0.5 flex-shrink-0 h-6 w-6 rounded-lg border-2 flex items-center justify-center transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/50 ${
            task.completed
              ? "bg-white/90 border-white/90"
              : "border-white/40 hover:border-white/70 bg-transparent"
          }`}
          aria-label={
            task.completed
              ? `Mark "${task.title}" as pending`
              : `Mark "${task.title}" as completed`
          }
        >
          {task.completed && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", duration: 0.3, bounce: 0.5 }}
            >
              <Check className="h-4 w-4 text-purple-700" strokeWidth={3} />
            </motion.div>
          )}
        </button>

        <div className="flex-1 min-w-0">
          <h3
            className={`text-lg font-semibold text-white leading-tight transition-all duration-200 ${
              task.completed ? "line-through text-white/50" : ""
            }`}
          >
            {task.title}
          </h3>
        </div>

        <div className="flex items-center gap-1 flex-shrink-0">
          <motion.button
            onClick={() => onEdit(task)}
            whileHover={{ scale: 1.15 }}
            whileTap={{ scale: 0.9 }}
            className="p-1.5 rounded-lg hover:bg-white/10 text-white/60 hover:text-white transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/50"
            aria-label={`Edit "${task.title}"`}
          >
            <Pencil className="h-4 w-4" />
          </motion.button>
          <motion.button
            onClick={() => onDelete(task.id)}
            whileHover={{ scale: 1.15 }}
            whileTap={{ scale: 0.9 }}
            className="p-1.5 rounded-lg hover:bg-red-500/20 text-white/60 hover:text-red-300 transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/50"
            aria-label={`Delete "${task.title}"`}
          >
            <Trash2 className="h-4 w-4" />
          </motion.button>
        </div>
      </div>

      {/* Description */}
      {task.description && (
        <p className="text-white/70 text-sm leading-relaxed line-clamp-2 pl-9">
          {task.description}
        </p>
      )}

      {/* Date */}
      <p className="text-white/40 text-xs pl-9">{formatDate(task.created_at)}</p>
    </motion.div>
  );
}
