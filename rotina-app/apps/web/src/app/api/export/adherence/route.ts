import { createClient } from '@/lib/supabase/server';
import { requireAuth } from '@/lib/auth';
import { generateCSV, EXPORT_CSV_HEADERS } from '@rotina/shared';
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

    // Get checkins
    const { data: checkins } = await supabase
      .from('daily_checkins')
      .select('*')
      .eq('user_id', user.id)
      .gte('date', startDate)
      .lte('date', endDate)
      .order('date');

    if (!checkins || checkins.length === 0) {
      return NextResponse.json(
        { error: 'Nenhum dado encontrado para exportar' },
        { status: 404 }
      );
    }

    // Build CSV rows
    const rows: string[][] = [EXPORT_CSV_HEADERS.ADHERENCE];

    for (const checkin of checkins) {
      // Calculate adherence for this date
      const { data: adherence } = await supabase.rpc('calculate_adherence', {
        p_user_id: user.id,
        p_date: checkin.date,
      });

      // Count meals
      const { data: meals } = await supabase
        .from('daily_meals')
        .select('*')
        .eq('user_id', user.id)
        .eq('date', checkin.date);

      const mealsDone = meals?.filter(m => m.option_selected).length || 0;
      const mealsPlanned = meals?.length || 0;

      rows.push([
        checkin.date,
        adherence?.toString() || '0',
        mealsDone.toString(),
        mealsPlanned.toString(),
        checkin.weight_kg?.toString() || '',
        checkin.cardio_min.toString(),
        checkin.workout_done ? 'Sim' : 'Não',
        checkin.functional ? 'Sim' : 'Não',
      ]);
    }

    const csvContent = generateCSV(rows);
    const filename = `aderencia-${startDate}-${endDate}.csv`;

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

