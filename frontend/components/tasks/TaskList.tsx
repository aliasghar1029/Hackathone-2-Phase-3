// [Task]: T-020
// [From]: speckit.plan §2.1

"use client";

import { useState, useEffect } from "react";
import { TaskCard } from "./TaskCard";
import { getTasks, toggleComplete, deleteTask, updateTask } from "@/lib/api";

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
}

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<"all" | "pending" | "completed">("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTasks();
  }, [filter]);

  async function loadTasks() {
    try {
      setLoading(true);
      const data = await getTasks(filter);
      setTasks(data);
    } catch (error) {
      console.error("Failed to load tasks:", error);
    } finally {
      setLoading(false);
    }
  }

  async function handleToggle(taskId: number) {
    try {
      await toggleComplete(taskId);
      // Optimistically update UI
      setTasks(prev => prev.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      ));
    } catch (error) {
      console.error("Failed to toggle task:", error);
    }
  }

  async function handleDelete(taskId: number) {
    try {
      await deleteTask(taskId);
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } catch (error) {
      console.error("Failed to delete task:", error);
    }
  }

  async function handleUpdate(taskId: number, title: string, description: string) {
    try {
      await updateTask(taskId, title, description);
      // Optimistically update UI
      setTasks(prev => prev.map(task =>
        task.id === taskId ? { ...task, title, description } : task
      ));
    } catch (error) {
      console.error("Failed to update task:", error);
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-3">
        <button
          onClick={() => setFilter("all")}
          className={`px-5 py-2.5 rounded-xl transition-all ${
            filter === "all"
              ? "bg-gradient-to-r from-purple-600 to-blue-500 text-white shadow-lg shadow-purple-500/20"
              : "bg-white/10 text-white hover:bg-white/20 border border-white/20"
          }`}
        >
          All Tasks
        </button>
        <button
          onClick={() => setFilter("pending")}
          className={`px-5 py-2.5 rounded-xl transition-all ${
            filter === "pending"
              ? "bg-gradient-to-r from-purple-600 to-blue-500 text-white shadow-lg shadow-purple-500/20"
              : "bg-white/10 text-white hover:bg-white/20 border border-white/20"
          }`}
        >
          Pending
        </button>
        <button
          onClick={() => setFilter("completed")}
          className={`px-5 py-2.5 rounded-xl transition-all ${
            filter === "completed"
              ? "bg-gradient-to-r from-purple-600 to-blue-500 text-white shadow-lg shadow-purple-500/20"
              : "bg-white/10 text-white hover:bg-white/20 border border-white/20"
          }`}
        >
          Completed
        </button>
      </div>

      <div className="space-y-4">
        {tasks.length === 0 ? (
          <div className="text-center py-16">
            <div className="mx-auto w-24 h-24 bg-gradient-to-br from-purple-600/20 to-blue-500/20 rounded-full flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 002 2h2a2 2 0 002-2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">No tasks yet</h3>
            <p className="text-white/70 max-w-md mx-auto">
              {filter === "completed" 
                ? "You haven't completed any tasks yet." 
                : "Add your first task to get started!"}
            </p>
          </div>
        ) : (
          tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onToggle={handleToggle}
              onDelete={handleDelete}
              onUpdate={handleUpdate}
            />
          ))
        )}
      </div>
    </div>
  );
}