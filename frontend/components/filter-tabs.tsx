"use client";

import { motion } from "framer-motion";
import type { TaskFilter } from "@/lib/types";

const filters: { value: TaskFilter; label: string }[] = [
  { value: "all", label: "All" },
  { value: "pending", label: "Pending" },
  { value: "completed", label: "Completed" },
];

interface FilterTabsProps {
  activeFilter: TaskFilter;
  onFilterChange: (filter: TaskFilter) => void;
}

export function FilterTabs({ activeFilter, onFilterChange }: FilterTabsProps) {
  return (
    <div
      className="flex items-center gap-1 glass rounded-xl p-1"
      role="tablist"
      aria-label="Filter tasks"
    >
      {filters.map((filter) => (
        <button
          key={filter.value}
          role="tab"
          aria-selected={activeFilter === filter.value}
          onClick={() => onFilterChange(filter.value)}
          className="relative px-5 py-2 rounded-lg text-sm font-medium transition-colors duration-200 text-white/70 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/50"
        >
          {activeFilter === filter.value && (
            <motion.div
              layoutId="activeTab"
              className="absolute inset-0 bg-white rounded-lg"
              transition={{ type: "spring", duration: 0.4, bounce: 0.15 }}
            />
          )}
          <span
            className={`relative z-10 ${
              activeFilter === filter.value
                ? "text-purple-700 font-bold"
                : "text-white/70"
            }`}
          >
            {filter.label}
          </span>
        </button>
      ))}
    </div>
  );
}
