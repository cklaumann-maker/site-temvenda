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
            const defaultOptions = {
              path: '/',
              sameSite: 'lax' as const,
              secure: window.location.protocol === 'https:',
              ...options,
            };
            
            let cookieString = `${name}=${encodeURIComponent(value)}`;
            cookieString += `; path=${defaultOptions.path}`;
            
            if (defaultOptions.maxAge) {
              cookieString += `; max-age=${defaultOptions.maxAge}`;
            }
            
            if (defaultOptions.domain) {
              cookieString += `; domain=${defaultOptions.domain}`;
            }
            
            cookieString += `; samesite=${defaultOptions.sameSite}`;
            
            if (defaultOptions.secure) {
              cookieString += `; secure`;
            }
            
            document.cookie = cookieString;
          });
        },
      },
    }
  );
}
