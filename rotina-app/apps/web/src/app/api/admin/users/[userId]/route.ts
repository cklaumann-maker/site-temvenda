import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

// DELETE - Deletar usuário (apenas root)
export async function DELETE(
  request: Request,
  { params }: { params: { userId: string } }
) {
  try {
    const supabase = await createClient();
    
    // Verificar se o usuário é root
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      return NextResponse.json({ error: 'Não autenticado' }, { status: 401 });
    }

    const { data: profile } = await supabase
      .from('user_profiles')
      .select('is_root')
      .eq('user_id', user.id)
      .single();

    if (!profile || !profile.is_root) {
      return NextResponse.json({ error: 'Acesso negado. Apenas root pode deletar usuários.' }, { status: 403 });
    }

    const userId = params.userId;

    // Verificar se não está tentando deletar outro root
    const { data: targetProfile } = await supabase
      .from('user_profiles')
      .select('is_root')
      .eq('user_id', userId)
      .single();

    if (targetProfile?.is_root) {
      return NextResponse.json({ error: 'Não é possível deletar um usuário root' }, { status: 403 });
    }

    // Deletar registros relacionados primeiro
    // 1. Deletar resumos de calorias
    await supabase
      .from('daily_calorie_summaries')
      .delete()
      .eq('user_id', userId);

    // 2. Deletar refeições
    await supabase
      .from('daily_meals')
      .delete()
      .eq('user_id', userId);

    // 3. Deletar check-ins
    await supabase
      .from('daily_checkins')
      .delete()
      .eq('user_id', userId);

    // 4. Deletar enrollments
    await supabase
      .from('enrollments')
      .delete()
      .eq('user_id', userId);

    // 5. Deletar perfil
    const { error: deleteError } = await supabase
      .from('user_profiles')
      .delete()
      .eq('user_id', userId);

    if (deleteError) {
      console.error('Erro ao deletar perfil:', deleteError);
      return NextResponse.json({ error: 'Erro ao deletar perfil do usuário' }, { status: 500 });
    }

    // Nota: Para deletar de auth.users, você precisa usar o Dashboard do Supabase
    // ou criar uma função RPC que use service_role_key
    // Por enquanto, apenas deletamos os registros relacionados

    return NextResponse.json({ 
      success: true,
      message: 'Registros relacionados deletados. Delete o usuário manualmente do Dashboard do Supabase.'
    });
  } catch (error) {
    console.error('Erro na API de deleção de usuário:', error);
    return NextResponse.json({ error: 'Erro interno do servidor' }, { status: 500 });
  }
}

