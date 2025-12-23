/**
 * Obtém a URL base da aplicação
 * Em produção, usa a variável de ambiente ou detecta automaticamente
 */
export function getBaseUrl(): string {
  // Client-side: detecta se está em produção
  if (typeof window !== 'undefined') {
    const origin = window.location.origin;
    
    // Se não for localhost, usa a URL atual (produção)
    if (!origin.includes('localhost')) {
      return origin;
    }
    
    // Se for localhost mas tiver variável de ambiente, usa ela
    if (process.env.NEXT_PUBLIC_SITE_URL) {
      return process.env.NEXT_PUBLIC_SITE_URL;
    }
    
    // Fallback para localhost em desenvolvimento
    return origin;
  }
  
  // Server-side: usa variável de ambiente ou fallback
  // NEXT_PUBLIC_SITE_URL tem prioridade (configurada no Vercel)
  if (process.env.NEXT_PUBLIC_SITE_URL) {
    return process.env.NEXT_PUBLIC_SITE_URL;
  }
  
  // VERCEL_URL é automaticamente definida pelo Vercel
  if (process.env.VERCEL_URL) {
    return `https://${process.env.VERCEL_URL}`;
  }
  
  // Fallback para desenvolvimento local
  return 'http://localhost:3001';
}

/**
 * Obtém a URL completa para redirecionamento de autenticação
 */
export function getAuthCallbackUrl(next: string = '/app'): string {
  const baseUrl = getBaseUrl();
  return `${baseUrl}/auth/callback?next=${encodeURIComponent(next)}`;
}

