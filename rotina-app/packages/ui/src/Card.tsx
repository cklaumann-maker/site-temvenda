import React from 'react';

export interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  title,
}) => {
  return (
    <div className={`bg-gray-800 rounded-lg p-4 shadow-lg ${className}`}>
      {title && <h3 className="text-lg font-semibold mb-2 text-white">{title}</h3>}
      {children}
    </div>
  );
};

