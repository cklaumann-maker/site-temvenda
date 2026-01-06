/**
 * Converte uma Date para string no formato YYYY-MM-DD usando timezone local
 * Evita problemas com UTC que podem causar diferença de um dia
 */
export function formatDateLocal(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Obtém a data de hoje no formato YYYY-MM-DD usando timezone local
 */
export function getTodayLocal(): string {
  return formatDateLocal(new Date());
}

/**
 * Compara duas datas ignorando o horário
 */
export function isSameDate(date1: Date, date2: Date): boolean {
  return formatDateLocal(date1) === formatDateLocal(date2);
}







