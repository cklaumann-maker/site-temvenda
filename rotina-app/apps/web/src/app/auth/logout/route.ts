import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

// Suportar tanto POST quanto GET para compatibilidade
export async function POST(request: Request) {
  return handleLogout(request);
}

export async function GET(request: Request) {
  return handleLogout(request);
}

async function handleLogout(request: Request) {
  try {
    const supabase = createClient();
    await supabase.auth.signOut();
    
    // Obter a URL base corretamente
    const url = new URL(request.url);
    const baseUrl = url.origin;
    
    // Redirecionar para login
    return NextResponse.redirect(new URL('/login', baseUrl), {
      status: 302,
    });
  } catch (error) {
    console.error('Logout error:', error);
    // Mesmo em caso de erro, redireciona para login
    const url = new URL(request.url);
    const baseUrl = url.origin;
    return NextResponse.redirect(new URL('/login', baseUrl), {
      status: 302,
    });
  }
}

