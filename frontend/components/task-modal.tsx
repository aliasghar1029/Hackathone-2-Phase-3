"use client";

import { useState, useEffect, useCallback, useRef, type FormEvent } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Loader2 } from "lucide-react";
import type { Task } from "@/lib/types";

const MAX_TITLE = 200;
const MAX_DESC = 1000;

interface TaskModalProps {
  isOpen: boolean;
  task?: Task | null;
  onClose: () => void;
  onSave: (title: string, description: string) => Promise<void>;
}

export function TaskModal({ isOpen, task, onClose, onSave }: TaskModalProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const titleRef = useRef<HTMLInputElement>(null);

  const isEditMode = !!task;
  const isTitleValid = title.trim().length > 0 && title.length <= MAX_TITLE;
  const isDescValid = description.length <= MAX_DESC;
  const canSave = isTitleValid && isDescValid && !isLoading;

  useEffect(() => {
    if (isOpen) {
      setTitle(task?.title || "");
      setDescription(task?.description || "");
      setError("");
      setTimeout(() => titleRef.current?.focus(), 100);
    }
  }, [isOpen, task]);

  const handleClose = useCallback(() => {
    if (!isLoading) onClose();
  }, [isLoading, onClose]);

  useEffect(() => {
    function handleKey(e: KeyboardEvent) {
      if (e.key === "Escape" && isOpen) handleClose();
    }
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [isOpen, handleClose]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!canSave) return;

    setIsLoading(true);
    setError("");

    try {
      await onSave(title.trim(), description.trim());
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save task");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={handleClose}
            aria-hidden="true"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            className="relative w-full max-w-lg glass rounded-2xl overflow-hidden"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 pb-0">
              <h2
                id="modal-title"
                className="text-xl font-bold text-white"
              >
                {isEditMode ? "Edit Task" : "Add Task"}
              </h2>
              <motion.button
                onClick={handleClose}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-1.5 rounded-lg hover:bg-white/10 text-white/60 hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/50"
                aria-label="Close modal"
              >
                <X className="h-5 w-5" />
              </motion.button>
            </div>

            <div className="border-b border-white/10 mx-6 mt-4" />

            {/* Form */}
            <form onSubmit={handleSubmit} className="p-6 flex flex-col gap-5">
              {error && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  className="p-3 rounded-xl bg-red-500/20 border border-red-500/40 text-red-200 text-sm"
                  role="alert"
                >
                  {error}
                </motion.div>
              )}

              {/* Title */}
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <label
                    htmlFor="task-title"
                    className="text-sm font-medium text-white/80"
                  >
                    Title
                  </label>
                  <span
                    className={`text-xs ${
                      title.length > MAX_TITLE ? "text-red-300" : "text-white/40"
                    }`}
                  >
                    {title.length}/{MAX_TITLE}
                  </span>
                </div>
                <input
                  ref={titleRef}
                  id="task-title"
                  type="text"
                  required
                  maxLength={MAX_TITLE + 10}
                  placeholder="What needs to be done?"
                  value={title}
                  onChange={(e) => {
                    setTitle(e.target.value);
                    setError("");
                  }}
                  className={`glass-input rounded-xl px-4 py-3 w-full ${
                    title.length > MAX_TITLE ? "ring-2 ring-red-400/50" : ""
                  }`}
                  aria-required="true"
                  aria-invalid={title.length > MAX_TITLE}
                />
              </div>

              {/* Description */}
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <label
                    htmlFor="task-description"
                    className="text-sm font-medium text-white/80"
                  >
                    Description
                  </label>
                  <span
                    className={`text-xs ${
                      description.length > MAX_DESC
                        ? "text-red-300"
                        : "text-white/40"
                    }`}
                  >
                    {description.length}/{MAX_DESC}
                  </span>
                </div>
                <textarea
                  id="task-description"
                  rows={4}
                  maxLength={MAX_DESC + 10}
                  placeholder="Add some details (optional)"
                  value={description}
                  onChange={(e) => {
                    setDescription(e.target.value);
                    setError("");
                  }}
                  className={`glass-input rounded-xl px-4 py-3 w-full resize-none ${
                    description.length > MAX_DESC
                      ? "ring-2 ring-red-400/50"
                      : ""
                  }`}
                  aria-invalid={description.length > MAX_DESC}
                />
              </div>

              {/* Buttons */}
              <div className="flex flex-col-reverse sm:flex-row gap-3 pt-2">
                <motion.button
                  type="button"
                  onClick={handleClose}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.95 }}
                  disabled={isLoading}
                  className="flex-1 py-3 rounded-xl bg-white/10 hover:bg-white/20 text-white font-medium transition-all duration-200 disabled:opacity-50"
                >
                  Cancel
                </motion.button>
                <motion.button
                  type="submit"
                  disabled={!canSave}
                  whileHover={canSave ? { scale: 1.02 } : {}}
                  whileTap={canSave ? { scale: 0.95 } : {}}
                  className="flex-1 py-3 rounded-xl bg-white text-purple-700 font-bold transition-all duration-200 hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    "Save"
                  )}
                </motion.button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
