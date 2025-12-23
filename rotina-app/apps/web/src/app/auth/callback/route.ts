import { createServerClient, type CookieOptions } from '@supabase/ssr';
import { cookies } from 'next/headers';
import { NextResponse, type NextRequest } from 'next/server';
import type { Database } from '@/lib/supabase/database.types';

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');
  const error = requestUrl.searchParams.get('error');
  const errorDescription = requestUrl.searchParams.get('error_description');
  const next = requestUrl.searchParams.get('next') || '/app';

  // Se há erro na URL (do Supabase), redireciona para login com erro
  if (error) {
    console.error('Auth callback error:', error, errorDescription);
    let errorMessage = errorDescription || error;
    
    // Traduzir mensagens de erro comuns
    if (error === 'access_denied') {
      if (errorDescription?.includes('expired') || errorDescription?.includes('invalid')) {
        errorMessage = 'O link de login expirou ou já foi usado. Por favor, solicite um novo link.';
      } else {
        errorMessage = 'Acesso negado. Por favor, tente novamente.';
      }
    }
    
    return NextResponse.redirect(
      new URL(`/login?error=${encodeURIComponent(error)}&message=${encodeURIComponent(errorMessage)}&description=${encodeURIComponent(errorDescription || '')}`, request.url)
    );
  }

  if (!code) {
    console.error('Auth callback: No code provided');
    return NextResponse.redirect(new URL('/login?error=no_code', request.url));
  }

  try {
    const cookieStore = cookies();
    
    // Criar resposta primeiro para poder definir cookies
    const response = NextResponse.next();
    
    // Criar cliente do servidor com cookies do request
    const supabase = createServerClient<Database>(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          get(name: string) {
            // Primeiro tentar do cookieStore (Next.js cookies)
            let value = cookieStore.get(name)?.value;
            
            // Se não encontrou, tentar ler diretamente do header do request
            if (!value) {
              const cookieHeader = request.headers.get('cookie');
              if (cookieHeader) {
                const cookies = cookieHeader.split(';').map(c => c.trim());
                const cookie = cookies.find(c => c.startsWith(`${name}=`));
                if (cookie) {
                  value = cookie.split('=').slice(1).join('=');
                  // Decodificar se necessário
                  try {
                    value = decodeURIComponent(value);
                  } catch (e) {
                    // Manter valor original se não conseguir decodificar
                  }
                }
              }
            }
            
            // Log para debug de cookies PKCE
            if (name.includes('code-verifier') || name.includes('pkce')) {
              console.log(`🔑 [ROTINA APP] Buscando cookie PKCE: ${name} = ${value ? 'ENCONTRADO' : 'NÃO ENCONTRADO'}`);
            }
            
            return value;
          },
          set(name: string, value: string, options: CookieOptions) {
            try {
              // Configurações padrão para cookies PKCE e sessão
              const cookieOptions = {
                path: '/',
                sameSite: 'lax' as const,
                secure: process.env.NODE_ENV === 'production',
                maxAge: options?.maxAge || 3600, // 1 hora padrão
                ...options,
              };
              
              cookieStore.set({ 
                name, 
                value, 
                ...cookieOptions
              });
              // Também definir na resposta para garantir persistência
              response.cookies.set(name, value, cookieOptions);
            } catch (error) {
              // Ignorar erro se chamado de Server Component
            }
          },
          remove(name: string, options: CookieOptions) {
            try {
              cookieStore.set({ name, value: '', ...options });
              response.cookies.delete(name);
            } catch (error) {
              // Ignorar erro se chamado de Server Component
            }
          },
        },
      }
    );

    // Log todos os cookies disponíveis para debug
    const allCookies = cookieStore.getAll();
    console.log('🍪 [ROTINA APP] Cookies disponíveis no callback:', allCookies.map(c => c.name));
    console.log('🍪 [ROTINA APP] Cookies do request header:', request.headers.get('cookie'));
    
    // Verificar especificamente se o código verificador PKCE está presente
    const pkceCookies = allCookies.filter(c => 
      c.name.includes('code-verifier') || 
      c.name.includes('pkce') ||
      c.name.includes('sb-') && c.name.includes('auth-token')
    );
    console.log('🔑 [ROTINA APP] Cookies PKCE encontrados:', pkceCookies.map(c => ({ name: c.name, hasValue: !!c.value })));
    
    // Tentar exchange do código pela sessão
    const { data, error: exchangeError } = await supabase.auth.exchangeCodeForSession(code);
    
    if (exchangeError) {
      console.error('Auth exchange error:', exchangeError.message, exchangeError.status);
      console.error('Código recebido:', code.substring(0, 20) + '...');
      console.error('Cookies do request:', request.headers.get('cookie'));
      
      // Se o erro for PKCE, tentar sem PKCE (fallback)
      if (exchangeError.message.includes('PKCE') || exchangeError.message.includes('code verifier')) {
        console.warn('Erro PKCE detectado. Tentando fallback...');
        // Não há fallback direto, mas podemos melhorar a mensagem de erro
      }
      
      return NextResponse.redirect(
        new URL(`/login?error=auth_failed&message=${encodeURIComponent(exchangeError.message)}`, request.url)
      );
    }

    if (data.session) {
      // Successfully exchanged code for session
      const redirectResponse = NextResponse.redirect(new URL(next, request.url));
      
      // Copiar todos os cookies do cookieStore para a resposta de redirect
      cookieStore.getAll().forEach(cookie => {
        if (cookie.name.startsWith('sb-') || cookie.name.includes('supabase')) {
          redirectResponse.cookies.set(cookie.name, cookie.value, {
            path: '/',
            sameSite: 'lax',
            secure: process.env.NODE_ENV === 'production',
            httpOnly: cookie.name.includes('auth-token'), // Apenas tokens de auth devem ser httpOnly
          });
        }
      });
      
      return redirectResponse;
    }

    // No session created
    console.error('Auth callback: No session created after exchange');
    return NextResponse.redirect(new URL('/login?error=no_session', request.url));
  } catch (err) {
    console.error('Auth callback exception:', err);
    return NextResponse.redirect(
      new URL(`/login?error=exception&message=${encodeURIComponent(err instanceof Error ? err.message : 'Unknown error')}`, request.url)
    );
  }
}

