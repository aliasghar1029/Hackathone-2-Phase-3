"use client";

import { useState, useCallback, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Plus, MessageCircle } from "lucide-react";
import { toast } from "sonner";
import { useAuth } from "@/components/auth-provider";
import { ProtectedRoute } from "@/components/protected-route";
import { TaskHeader } from "@/components/task-header";
import { FilterTabs } from "@/components/filter-tabs";
import { TaskList } from "@/components/task-list";
import { TaskModal } from "@/components/task-modal";
import { DeleteDialog } from "@/components/delete-dialog";
import type { Task, TaskFilter } from "@/lib/types";
import * as api from "@/lib/api";
import Link from "next/link";

function TasksContent() {
  const { user, token, logout } = useAuth();
  const router = useRouter();

  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState<TaskFilter>("all");

  // Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Delete dialog state
  const [deleteTaskId, setDeleteTaskId] = useState<string | null>(null);

  const fetchTasks = useCallback(async () => {
    if (!user || !token) return;
    setIsLoading(true);
    try {
      const data = await api.getTasks(user.id, token, filter);
      setTasks(data);
    } catch (err) {
      toast.error("Failed to load tasks", {
        description: err instanceof Error ? err.message : "Please try again",
        action: {
          label: "Retry",
          onClick: () => fetchTasks(),
        },
      });
    } finally {
      setIsLoading(false);
    }
  }, [user, token, filter]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  function handleSignout() {
    logout();
    router.push("/signin");
  }

  function handleAddTask() {
    setEditingTask(null);
    setIsModalOpen(true);
  }

  function handleEditTask(task: Task) {
    setEditingTask(task);
    setIsModalOpen(true);
  }

  async function handleSaveTask(title: string, description: string) {
    if (!user || !token) return;

    if (editingTask) {
      const updated = await api.updateTask(
        user.id,
        token,
        editingTask.id,
        title,
        description
      );
      setTasks((prev) =>
        prev.map((t) => (t.id === updated.id ? updated : t))
      );
      toast.success("Task updated");
    } else {
      const created = await api.createTask(user.id, token, title, description);
      setTasks((prev) => [created, ...prev]);
      toast.success("Task created");
    }
  }

  async function handleToggle(taskId: string) {
    if (!user || !token) return;
    try {
      const updated = await api.toggleComplete(user.id, token, taskId);
      setTasks((prev) =>
        prev.map((t) => (t.id === updated.id ? updated : t))
      );
    } catch (err) {
      toast.error("Failed to update task", {
        description: err instanceof Error ? err.message : "Please try again",
      });
    }
  }

  async function handleDelete() {
    if (!user || !token || !deleteTaskId) return;
    try {
      await api.deleteTask(user.id, token, deleteTaskId);
      setTasks((prev) => prev.filter((t) => t.id !== deleteTaskId));
      toast.success("Task deleted");
    } catch (err) {
      toast.error("Failed to delete task", {
        description: err instanceof Error ? err.message : "Please try again",
      });
    } finally {
      setDeleteTaskId(null);
    }
  }

  if (!user) return null;

  return (
    <main className="min-h-screen px-4 py-6 md:px-6 lg:px-8 max-w-7xl mx-auto flex flex-col gap-6">
      <TaskHeader user={user} onSignout={handleSignout} />

      {/* Action bar + Filter */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex gap-2">
          <motion.button
            onClick={handleAddTask}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-white text-purple-700 font-bold text-base hover:brightness-110 transition-all duration-200 w-full sm:w-auto"
          >
            <Plus className="h-5 w-5" />
            Add Task
          </motion.button>
          <Link
            href="/chat"
            className="px-6 py-3 bg-white/20 text-white rounded-xl font-semibold hover:bg-white/30 transition flex items-center gap-2 w-full sm:w-auto justify-center"
          >
            <MessageCircle className="w-5 h-5" />
            AI Chat
          </Link>
        </div>
        <FilterTabs activeFilter={filter} onFilterChange={setFilter} />
      </div>

      {/* Task list */}
      <TaskList
        tasks={tasks}
        isLoading={isLoading}
        onToggle={handleToggle}
        onEdit={handleEditTask}
        onDelete={(id) => setDeleteTaskId(id)}
      />

      {/* Modal */}
      <TaskModal
        isOpen={isModalOpen}
        task={editingTask}
        onClose={() => setIsModalOpen(false)}
        onSave={handleSaveTask}
      />

      {/* Delete confirmation */}
      <DeleteDialog
        isOpen={!!deleteTaskId}
        onConfirm={handleDelete}
        onCancel={() => setDeleteTaskId(null)}
      />
    </main>
  );
}

export default function TasksPage() {
  return (
    <ProtectedRoute>
      <TasksContent />
    </ProtectedRoute>
  );
}
