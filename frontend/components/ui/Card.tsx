// [Task]: T-025
// [From]: speckit.plan §2.1

import { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
  elevated?: boolean;
}

export function Card({ children, className = "", elevated = false }: CardProps) {
  return (
    <div
      className={`
        rounded-2xl
        bg-gradient-to-br
        from-white/10
        to-white/5
        backdrop-blur-lg
        border
        border-white/20
        shadow-lg
        ${elevated ? 'shadow-purple-500/10' : ''}
        ${className}
      `}
    >
      {children}
    </div>
  );
}