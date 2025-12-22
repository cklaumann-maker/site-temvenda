import { createClient } from '@/lib/supabase/server';
import { requireAdmin } from '@/lib/auth';
import { generateCSV, EXPORT_CSV_HEADERS, DAYS_OF_WEEK } from '@rotina/shared';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  try {
    await requireAdmin();
    const supabase = createClient();
    const { searchParams } = new URL(request.url);
    const programId = searchParams.get('program_id');
    const weekIndex = searchParams.get('week_index');

    if (!programId || !weekIndex) {
      return NextResponse.json(
        { error: 'program_id e week_index são obrigatórios' },
        { status: 400 }
      );
    }

    // Get program and org
    const { data: program } = await supabase
      .from('programs')
      .select(`
        id,
        name,
        orgs:org_id (
          id,
          name
        )
      `)
      .eq('id', programId)
      .single();

    if (!program) {
      return NextResponse.json(
        { error: 'Programa não encontrado' },
        { status: 404 }
      );
    }

    // Get templates
    const { data: templates } = await supabase
      .from('plan_templates')
      .select('*')
      .eq('program_id', programId)
      .eq('week_index', parseInt(weekIndex))
      .order('day_of_week')
      .order('meal_type');

    if (!templates || templates.length === 0) {
      return NextResponse.json(
        { error: 'Nenhum template encontrado' },
        { status: 404 }
      );
    }

    // Build CSV rows
    const rows: string[][] = [EXPORT_CSV_HEADERS.PLAN_TEMPLATE];

    for (const template of templates) {
      const dayLabel = DAYS_OF_WEEK[template.day_of_week] || '';

      rows.push([
        (program.orgs as any)?.name || '',
        program.name,
        template.week_index.toString(),
        template.day_of_week.toString(),
        dayLabel,
        template.meal_type,
        template.opt1 || '',
        template.opt2 || '',
        template.opt3 || '',
        template.avoid || '',
      ]);
    }

    const csvContent = generateCSV(rows);
    const filename = `template-plano-${program.name}-semana-${weekIndex}.csv`;

    return new NextResponse(csvContent, {
      headers: {
        'Content-Type': 'text/csv;charset=utf-8',
        'Content-Disposition': `attachment; filename="${filename}"`,
      },
    });
  } catch (error) {
    console.error('Export error:', error);
    return NextResponse.json(
      { error: 'Erro ao exportar template' },
      { status: 500 }
    );
  }
}

