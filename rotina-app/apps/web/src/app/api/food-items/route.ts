import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

// Forçar rota dinâmica para garantir que seja detectada pelo Next.js
export const dynamic = 'force-dynamic';

// GET - Buscar alimentos (com filtro opcional)
export async function GET(request: Request) {
  try {
    const supabase = await createClient();
    const { searchParams } = new URL(request.url);
    const search = searchParams.get('search');
    const category = searchParams.get('category');

    let query = supabase
      .from('food_items')
      .select('*')
      .order('category', { ascending: true })
      .order('name', { ascending: true });

    // Filtrar por busca de texto
    if (search) {
      query = query.ilike('name', `%${search}%`);
    }

    // Filtrar por categoria
    if (category) {
      query = query.eq('category', category);
    }

    const { data, error } = await query;

    if (error) {
      console.error('Erro ao buscar alimentos:', error);
      return NextResponse.json({ error: 'Erro ao buscar alimentos' }, { status: 500 });
    }

    return NextResponse.json({ items: data || [] });
  } catch (error) {
    console.error('Erro na API de alimentos:', error);
    return NextResponse.json({ error: 'Erro interno do servidor' }, { status: 500 });
  }
}

// POST - Criar novo alimento
export async function POST(request: Request) {
  try {
    const supabase = await createClient();
    
    // Verificar autenticação
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      return NextResponse.json({ error: 'Não autenticado' }, { status: 401 });
    }

    const body = await request.json();
    const { category, name, standard_portion, calories_kcal } = body;

    // Validações
    if (!category || !name || !standard_portion || calories_kcal === undefined) {
      return NextResponse.json({ 
        error: 'Campos obrigatórios: category, name, standard_portion, calories_kcal' 
      }, { status: 400 });
    }

    if (calories_kcal < 0) {
      return NextResponse.json({ error: 'Calorias não podem ser negativas' }, { status: 400 });
    }

    // Verificar se já existe
    const { data: existing } = await supabase
      .from('food_items')
      .select('id')
      .eq('name', name)
      .eq('standard_portion', standard_portion)
      .single();

    if (existing) {
      return NextResponse.json({ 
        error: 'Este alimento com esta porção já existe' 
      }, { status: 409 });
    }

    // Inserir novo alimento
    const { data: newItem, error: insertError } = await supabase
      .from('food_items')
      .insert({
        category,
        name,
        standard_portion,
        calories_kcal: parseInt(calories_kcal),
        created_by: user.id,
      } as any)
      .select()
      .single();

    if (insertError) {
      console.error('Erro ao criar alimento:', insertError);
      return NextResponse.json({ error: 'Erro ao criar alimento' }, { status: 500 });
    }

    return NextResponse.json({ item: newItem }, { status: 201 });
  } catch (error) {
    console.error('Erro na API de criação de alimento:', error);
    return NextResponse.json({ error: 'Erro interno do servidor' }, { status: 500 });
  }
}

