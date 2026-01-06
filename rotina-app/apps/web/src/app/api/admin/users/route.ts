import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

// GET - Listar todos os usuários (apenas root)
export async function GET() {
  try {
    const supabase = await createClient();
    
    // Verificar se o usuário é root
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      return NextResponse.json({ error: 'Não autenticado' }, { status: 401 });
    }

    const { data: profile, error: profileError } = await supabase
      .from('user_profiles')
      .select('is_root')
      .eq('user_id', user.id)
      .single();

    if (profileError || !profile || !(profile as any).is_root) {
      return NextResponse.json({ error: 'Acesso negado. Apenas root pode acessar.' }, { status: 403 });
    }

    // Buscar todos os usuários via função RPC
    const { data: usersData, error: rpcError } = await supabase
      .rpc('list_users_for_admin');

    if (rpcError) {
      console.error('Erro ao buscar usuários via RPC:', rpcError);
      // Fallback: buscar apenas perfis
      const { data: profiles, error } = await supabase
        .from('user_profiles')
        .select('user_id, name, is_root, created_at')
        .order('created_at', { ascending: false });

      if (error) {
        return NextResponse.json({ error: 'Erro ao buscar usuários' }, { status: 500 });
      }

      const users = (profiles || []).map((profile) => ({
        id: profile.user_id,
        email: profile.user_id.substring(0, 8) + '...', // Placeholder
        email_confirmed_at: null,
        created_at: profile.created_at,
        last_sign_in_at: null,
        profile: {
          name: profile.name,
          is_root: profile.is_root || false,
        },
      }));

      return NextResponse.json({ users });
    }

    // Transformar dados da função RPC para o formato esperado
    const users = (usersData || []).map((user: any) => ({
      id: user.id,
      email: user.email,
      email_confirmed_at: user.email_confirmed_at,
      created_at: user.created_at,
      last_sign_in_at: user.last_sign_in_at,
      profile: {
        name: user.profile_name,
        is_root: user.is_root || false,
      },
    }));

    return NextResponse.json({ users });
  } catch (error) {
    console.error('Erro na API de usuários:', error);
    return NextResponse.json({ error: 'Erro interno do servidor' }, { status: 500 });
  }
}

// POST - Criar novo usuário (apenas root)
export async function POST(request: Request) {
  try {
    const supabase = await createClient();
    
    // Verificar se o usuário é root
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      return NextResponse.json({ error: 'Não autenticado' }, { status: 401 });
    }

    const { data: profile, error: profileError } = await supabase
      .from('user_profiles')
      .select('is_root')
      .eq('user_id', user.id)
      .single();

    if (profileError || !profile || !(profile as any).is_root) {
      return NextResponse.json({ error: 'Acesso negado. Apenas root pode criar usuários.' }, { status: 403 });
    }

    const body = await request.json();
    const { email, password, name } = body;

    if (!email || !password) {
      return NextResponse.json({ error: 'Email e senha são obrigatórios' }, { status: 400 });
    }

    // Criar usuário no Supabase Auth
    // Nota: Isso requer service_role_key, que não deve ser exposto no cliente
    // Vamos usar signUp do Supabase (mas isso envia email de confirmação)
    // Para produção, você deve criar uma função RPC no Supabase que use service_role
    
    const { data: newUser, error: signUpError } = await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'}/app`,
        data: {
          name: name || email.split('@')[0],
        },
      },
    });

    if (signUpError) {
      console.error('Erro ao criar usuário:', signUpError);
      return NextResponse.json({ error: signUpError.message }, { status: 400 });
    }

    if (!newUser.user) {
      return NextResponse.json({ error: 'Erro ao criar usuário' }, { status: 500 });
    }

    // Criar perfil do usuário
    const { error: profileInsertError } = await supabase
      .from('user_profiles')
      .insert({
        user_id: newUser.user.id,
        name: name || email.split('@')[0],
        is_root: false,
        max_daily_calories: 2000,
      });

    if (profileInsertError) {
      console.error('Erro ao criar perfil:', profileInsertError);
      // Não retornar erro aqui, o perfil pode ser criado depois
    }

    return NextResponse.json({ 
      success: true, 
      user: {
        id: newUser.user.id,
        email: newUser.user.email,
      }
    });
  } catch (error) {
    console.error('Erro na API de criação de usuário:', error);
    return NextResponse.json({ error: 'Erro interno do servidor' }, { status: 500 });
  }
}

