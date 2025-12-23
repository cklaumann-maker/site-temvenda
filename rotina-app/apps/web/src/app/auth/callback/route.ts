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
    return NextResponse.redirect(
      new URL(`/login?error=${encodeURIComponent(error)}&description=${encodeURIComponent(errorDescription || '')}`, request.url)
    );
  }

  if (!code) {
    console.error('Auth callback: No code provided');
    return NextResponse.redirect(new URL('/login?error=no_code', request.url));
  }

  try {
    const cookieStore = cookies();
    
    // Criar cliente do servidor com cookies do request
    const supabase = createServerClient<Database>(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          get(name: string) {
            return cookieStore.get(name)?.value;
          },
          set(name: string, value: string, options: CookieOptions) {
            try {
              cookieStore.set({ name, value, ...options });
            } catch (error) {
              // Ignorar erro se chamado de Server Component
            }
          },
          remove(name: string, options: CookieOptions) {
            try {
              cookieStore.set({ name, value: '', ...options });
            } catch (error) {
              // Ignorar erro se chamado de Server Component
            }
          },
        },
      }
    );

    const { data, error: exchangeError } = await supabase.auth.exchangeCodeForSession(code);
    
    if (exchangeError) {
      console.error('Auth exchange error:', exchangeError.message, exchangeError.status);
      return NextResponse.redirect(
        new URL(`/login?error=auth_failed&message=${encodeURIComponent(exchangeError.message)}`, request.url)
      );
    }

    if (data.session) {
      // Successfully exchanged code for session
      const response = NextResponse.redirect(new URL(next, request.url));
      
      // Garantir que os cookies da sessão sejam passados na resposta
      cookieStore.getAll().forEach(cookie => {
        if (cookie.name.startsWith('sb-') || cookie.name.includes('supabase')) {
          response.cookies.set(cookie.name, cookie.value, {
            path: '/',
            httpOnly: true,
            sameSite: 'lax',
            secure: process.env.NODE_ENV === 'production',
          });
        }
      });
      
      return response;
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

