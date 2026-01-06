import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value;
        },
        set(name: string, value: string, options: any) {
          request.cookies.set({
            name,
            value,
            ...options,
          });
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          });
          response.cookies.set({
            name,
            value,
            ...options,
          });
        },
        remove(name: string, options: any) {
          request.cookies.set({
            name,
            value: '',
            ...options,
          });
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          });
          response.cookies.set({
            name,
            value: '',
            ...options,
          });
        },
      },
    }
  );

  const { data: { user } } = await supabase.auth.getUser();

  // Handle auth routes - don't redirect during callback or logout
  if (request.nextUrl.pathname === '/auth/callback' || 
      request.nextUrl.pathname === '/auth/logout') {
    return response;
  }

  // Protect /app/admin routes (admin de usuários e alimentos)
  if (request.nextUrl.pathname.startsWith('/app/admin')) {
    if (!user) {
      return NextResponse.redirect(new URL('/login', request.url));
    }

    // Check if user is root usando a função RPC para evitar recursão
    try {
      const { data: isRoot } = await supabase.rpc('is_root_user');
      
      if (!isRoot) {
        console.warn(`Acesso negado a ${request.nextUrl.pathname} para user ${user.id}. Não é root.`);
        return NextResponse.redirect(new URL('/app', request.url));
      }
    } catch (error) {
      // Se a função não existir, tentar verificar diretamente (fallback)
      const { data: profile } = await supabase
        .from('user_profiles')
        .select('is_root')
        .eq('user_id', user.id)
        .single();

      if (!profile || !(profile as any).is_root) {
        console.warn(`Acesso negado a ${request.nextUrl.pathname} para user ${user.id}. Não é root.`);
        return NextResponse.redirect(new URL('/app', request.url));
      }
    }
  }

  // Protect /admin routes (admin de organização - mantido para compatibilidade)
  if (request.nextUrl.pathname.startsWith('/admin') && !request.nextUrl.pathname.startsWith('/app/admin')) {
    if (!user) {
      return NextResponse.redirect(new URL('/login', request.url));
    }

    // Check if user is owner or coach
    const { data: orgMember } = await supabase
      .from('org_members')
      .select('role')
      .eq('user_id', user.id)
      .eq('active', true)
      .single();

    if (!orgMember || (orgMember.role !== 'OWNER' && orgMember.role !== 'COACH')) {
      return NextResponse.redirect(new URL('/app/today', request.url));
    }
  }

  // Protect /app routes
  if (request.nextUrl.pathname.startsWith('/app') && !user) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Redirect logged-in users away from login
  if (request.nextUrl.pathname === '/login' && user) {
    return NextResponse.redirect(new URL('/app', request.url));
  }

  return response;
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};

