import { createBrowserClient } from '@supabase/ssr';
import { Database } from './database.types';

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return document.cookie.split('; ').map(cookie => {
            const [name, ...rest] = cookie.split('=');
            return { name, value: decodeURIComponent(rest.join('=')) };
          });
        },
        setAll(cookiesToSet: Array<{ name: string; value: string; options?: { path?: string; maxAge?: number; domain?: string; sameSite?: 'strict' | 'lax' | 'none'; secure?: boolean } }>) {
          cookiesToSet.forEach(({ name, value, options }) => {
            // Configurações padrão para garantir que cookies sejam salvos corretamente
            // maxAge padrão de 1 hora (3600 segundos) para código verificador PKCE
            // IMPORTANTE: Cookies PKCE precisam ser acessíveis quando o callback é executado
            const defaultOptions = {
              path: '/',
              sameSite: 'lax' as const,
              secure: window.location.protocol === 'https:',
              maxAge: 3600, // 1 hora - tempo padrão de expiração do magic link
              ...options,
            };
            
            // Log cookies PKCE sendo criados
            if (name.includes('code-verifier') || name.includes('pkce')) {
              console.log('🔑 [ROTINA APP] Criando cookie PKCE:', name, 'com maxAge:', defaultOptions.maxAge);
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
              console.log('✅ [ROTINA APP] Cookie PKCE salvo?', saved, 'Nome:', name);
            }
          });
        },
      },
    }
  );
}
