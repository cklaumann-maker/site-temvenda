import { createBrowserClient } from '@supabase/ssr';
import { Database } from './database.types';

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      auth: {
        // Aumentar o tempo de expiração do código verificador PKCE
        // para garantir que esteja disponível quando o usuário clicar no link
        flowType: 'pkce',
        storage: typeof window !== 'undefined' ? window.localStorage : undefined,
        autoRefreshToken: true,
        persistSession: true,
        detectSessionInUrl: true,
      },
      cookies: {
        getAll() {
          if (typeof document === 'undefined') return [];
          return document.cookie.split('; ').map(cookie => {
            const [name, ...rest] = cookie.split('=');
            return { name, value: decodeURIComponent(rest.join('=')) };
          });
        },
        setAll(cookiesToSet: Array<{ name: string; value: string; options?: { path?: string; maxAge?: number; domain?: string; sameSite?: 'strict' | 'lax' | 'none'; secure?: boolean } }>) {
          if (typeof document === 'undefined') return;
          
          cookiesToSet.forEach(({ name, value, options }) => {
            // Configurações padrão para garantir que cookies sejam salvos corretamente
            // maxAge aumentado para 2 horas (7200 segundos) para código verificador PKCE
            // IMPORTANTE: Cookies PKCE precisam ser acessíveis quando o callback é executado
            const defaultOptions = {
              path: '/',
              sameSite: 'lax' as const,
              secure: window.location.protocol === 'https:',
              maxAge: 7200, // 2 horas - aumentar tempo para garantir disponibilidade
              ...options,
            };
            
            // Log cookies PKCE sendo criados
            if (name.includes('code-verifier') || name.includes('pkce') || name.includes('sb-')) {
              console.log('🔑 [ROTINA APP] Criando cookie:', name.substring(0, 30), 'com maxAge:', defaultOptions.maxAge);
            }
            
            let cookieString = `${name}=${encodeURIComponent(value)}`;
            cookieString += `; path=${defaultOptions.path}`;
            cookieString += `; max-age=${defaultOptions.maxAge}`;
            
            if (defaultOptions.domain) {
              cookieString += `; domain=${defaultOptions.domain}`;
            }
            
            cookieString += `; samesite=${defaultOptions.sameSite}`;
            
            if (defaultOptions.secure) {
              cookieString += `; secure`;
            }
            
            document.cookie = cookieString;
            
            // Verificar se o cookie foi salvo corretamente
            if (name.includes('code-verifier') || name.includes('pkce')) {
              const saved = document.cookie.includes(name);
              console.log('✅ [ROTINA APP] Cookie PKCE salvo?', saved, 'Nome:', name.substring(0, 30));
            }
          });
        },
      },
    }
  );
}
