import { createClient } from '@/lib/supabase/server';
import { requireAuth } from '@/lib/auth';
import { generateCSV, EXPORT_CSV_HEADERS, DAYS_OF_WEEK } from '@rotina/shared';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  try {
    const user = await requireAuth();
    const supabase = createClient();
    const { searchParams } = new URL(request.url);
    const startDate = searchParams.get('start_date');
    const endDate = searchParams.get('end_date');

    if (!startDate || !endDate) {
      return NextResponse.json(
        { error: 'start_date e end_date são obrigatórios' },
        { status: 400 }
      );
    }

    // Get user's enrollment
    const { data: enrollment } = await supabase
      .from('enrollments')
      .select('program_id')
      .eq('user_id', user.id)
      .eq('active', true)
      .single();

    if (!enrollment) {
      return NextResponse.json(
        { error: 'Usuário não está inscrito em nenhum programa' },
        { status: 404 }
      );
    }

    // Get daily meals
    const { data: meals } = await supabase
      .from('daily_meals')
      .select('*')
      .eq('user_id', user.id)
      .gte('date', startDate)
      .lte('date', endDate)
      .order('date')
      .order('meal_type');

    if (!meals || meals.length === 0) {
      return NextResponse.json(
        { error: 'Nenhum dado encontrado para exportar' },
        { status: 404 }
      );
    }

    // Build CSV rows
    const rows: string[][] = [EXPORT_CSV_HEADERS.USER_SCHEDULE];

    for (const meal of meals) {
      const date = new Date(meal.date);
      const dayOfWeek = date.getDay() === 0 ? 7 : date.getDay();
      const dayLabel = DAYS_OF_WEEK[dayOfWeek] || '';

      rows.push([
        meal.date,
        dayLabel,
        meal.meal_type,
        meal.option_selected || '',
        meal.opt1 || '',
        meal.opt2 || '',
        meal.opt3 || '',
        meal.avoid || '',
      ]);
    }

    const csvContent = generateCSV(rows);
    const filename = `plano-usuario-${startDate}-${endDate}.csv`;

    return new NextResponse(csvContent, {
      headers: {
        'Content-Type': 'text/csv;charset=utf-8',
        'Content-Disposition': `attachment; filename="${filename}"`,
      },
    });
  } catch (error) {
    console.error('Export error:', error);
    return NextResponse.json(
      { error: 'Erro ao exportar dados' },
      { status: 500 }
    );
  }
}

