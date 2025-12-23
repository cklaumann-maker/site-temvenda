import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
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
    const supabase = createClient();
    const { data, error: exchangeError } = await supabase.auth.exchangeCodeForSession(code);
    
    if (exchangeError) {
      console.error('Auth exchange error:', exchangeError.message, exchangeError.status);
      return NextResponse.redirect(
        new URL(`/login?error=auth_failed&message=${encodeURIComponent(exchangeError.message)}`, request.url)
      );
    }

    if (data.session) {
      // Successfully exchanged code for session
      return NextResponse.redirect(new URL(next, request.url));
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

