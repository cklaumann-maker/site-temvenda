import { DEFAULT_TIMEZONE, DAYS_OF_WEEK } from './constants';

export function formatDate(date: Date | string, timezone: string = DEFAULT_TIMEZONE): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('pt-BR', { timeZone: timezone });
}

export function getDayOfWeek(date: Date | string): number {
  const d = typeof date === 'string' ? new Date(date) : date;
  const day = d.getDay();
  // Convert to 1-7 (Monday-Sunday)
  return day === 0 ? 7 : day;
}

export function getDayLabel(date: Date | string): string {
  const dayOfWeek = getDayOfWeek(date);
  return DAYS_OF_WEEK[dayOfWeek] || '';
}

export function getWeekStart(date: Date | string): Date {
  const d = typeof date === 'string' ? new Date(date) : date;
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Adjust when day is Sunday
  return new Date(d.setDate(diff));
}

export function getWeekEnd(date: Date | string): Date {
  const weekStart = getWeekStart(date);
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekEnd.getDate() + 6);
  return weekEnd;
}

export function generateCSV(rows: string[][]): string {
  // Add BOM for Excel compatibility
  const BOM = '\uFEFF';
  const csvContent = rows
    .map(row => row.map(cell => {
      // Escape quotes and wrap in quotes if contains comma, quote, or newline
      if (cell.includes(',') || cell.includes('"') || cell.includes('\n')) {
        return `"${cell.replace(/"/g, '""')}"`;
      }
      return cell;
    }).join(','))
    .join('\n');
  
  return BOM + csvContent;
}

export function downloadCSV(content: string, filename: string): void {
  // Only works in browser environment
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    console.warn('downloadCSV only works in browser environment');
    return;
  }
  
  const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Ordem dos tipos de refeição conforme a planilha importada
export const MEAL_TYPE_ORDER: Record<string, number> = {
  'pre': 1,           // Pré-treino
  'post': 2,          // Pós-treino
  'cafe': 3,          // Café da manhã
  'breakfast': 3,     // Café da manhã (alias)
  'almoco': 4,        // Almoço
  'lunch': 4,         // Almoço (alias)
  'lanche_tarde': 5,  // Lanche da tarde
  'snack': 5,         // Lanche da tarde (alias)
  'jantar': 6,        // Jantar
  'dinner': 6,       // Jantar (alias)
  'ceia': 7,          // Ceia
};

// Função para ordenar refeições pela ordem da planilha
export function sortMealsByType<T extends { meal_type: string }>(meals: T[]): T[] {
  return [...meals].sort((a, b) => {
    const orderA = MEAL_TYPE_ORDER[a.meal_type] || 999;
    const orderB = MEAL_TYPE_ORDER[b.meal_type] || 999;
    return orderA - orderB;
  });
}

