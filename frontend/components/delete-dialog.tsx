"use client";

import { motion, AnimatePresence } from "framer-motion";
import { AlertTriangle } from "lucide-react";

interface DeleteDialogProps {
  isOpen: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

export function DeleteDialog({ isOpen, onConfirm, onCancel }: DeleteDialogProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={onCancel}
            aria-hidden="true"
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            role="alertdialog"
            aria-modal="true"
            aria-labelledby="delete-title"
            aria-describedby="delete-desc"
            className="relative glass rounded-2xl p-6 max-w-sm w-full flex flex-col items-center gap-4 text-center"
          >
            <div className="h-12 w-12 rounded-full bg-red-500/20 flex items-center justify-center">
              <AlertTriangle className="h-6 w-6 text-red-300" />
            </div>
            <h3 id="delete-title" className="text-lg font-bold text-white">
              Delete Task
            </h3>
            <p id="delete-desc" className="text-white/60 text-sm">
              Are you sure you want to delete this task? This action cannot be undone.
            </p>
            <div className="flex gap-3 w-full">
              <motion.button
                onClick={onCancel}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.95 }}
                className="flex-1 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-medium transition-all duration-200"
              >
                Cancel
              </motion.button>
              <motion.button
                onClick={onConfirm}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.95 }}
                className="flex-1 py-2.5 rounded-xl bg-red-500/80 hover:bg-red-500 text-white font-bold transition-all duration-200"
              >
                Delete
              </motion.button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
