// [Task]: T-023
// [From]: speckit.plan §2.1

import { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export function Input({
  label,
  error,
  helperText,
  className = "",
  ...props
}: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-white mb-2">
          {label}
        </label>
      )}
      <input
        className={`w-full px-4 py-3 rounded-xl bg-white/10 backdrop-blur-sm border ${
          error 
            ? "border-red-500 focus:ring-red-500 focus:border-red-500" 
            : "border-white/20 focus:ring-purple-500 focus:border-purple-500"
        } text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-opacity-50 transition-colors ${
          className
        }`}
        {...props}
      />
      {helperText && !error && (
        <p className="mt-1 text-sm text-white/70">{helperText}</p>
      )}
      {error && (
        <p className="mt-1 text-sm text-red-400">{error}</p>
      )}
    </div>
  );
}