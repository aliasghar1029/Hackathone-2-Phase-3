"use client";

import { AnimatePresence, motion } from "framer-motion";
import { ClipboardList } from "lucide-react";
import type { Task } from "@/lib/types";
import { TaskCard } from "@/components/task-card";

interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  onToggle: (taskId: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

function SkeletonCard() {
  return (
    <div className="glass rounded-2xl p-5 flex flex-col gap-3 animate-pulse">
      <div className="flex items-start gap-3">
        <div className="h-6 w-6 rounded-lg bg-white/10" />
        <div className="flex-1 flex flex-col gap-2">
          <div className="h-5 bg-white/10 rounded-lg w-3/4" />
        </div>
      </div>
      <div className="h-4 bg-white/10 rounded-lg w-full ml-9" />
      <div className="h-3 bg-white/10 rounded-lg w-24 ml-9" />
    </div>
  );
}

export function TaskList({
  tasks,
  isLoading,
  onToggle,
  onEdit,
  onDelete,
}: TaskListProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <SkeletonCard key={`skeleton-${i}`} />
        ))}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex flex-col items-center justify-center py-20 gap-4"
      >
        <motion.div
          animate={{ y: [0, -8, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        >
          <ClipboardList className="h-16 w-16 text-white/30" />
        </motion.div>
        <p className="text-white/50 text-lg text-center">
          No tasks yet. Create your first task!
        </p>
      </motion.div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <AnimatePresence mode="popLayout">
        {tasks.map((task, index) => (
          <motion.div
            key={task.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
          >
            <TaskCard
              task={task}
              onToggle={onToggle}
              onEdit={onEdit}
              onDelete={onDelete}
            />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
