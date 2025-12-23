import { createClient } from '@/lib/supabase/server';
import { requireAuth } from '@/lib/auth';
import { redirect } from 'next/navigation';
import DashboardClient from './DashboardClient';
import { formatDateLocal, getTodayLocal } from '@/lib/utils/date';

export default async function DashboardPage() {
  try {
    const user = await requireAuth();
    const supabase = createClient();

    // Get last 30 days of checkins
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    const startDate = formatDateLocal(thirtyDaysAgo);

    const { data: checkins } = await supabase
      .from('daily_checkins')
      .select('*')
      .eq('user_id', user.id)
      .gte('date', startDate)
      .order('date', { ascending: false });

    // Calculate average adherence
    const today = getTodayLocal();
    const { data: adherence } = await (supabase.rpc as any)('calculate_adherence', {
        p_user_id: user.id,
        p_date: today,
      });

    return <DashboardClient checkins={checkins || []} adherence={adherence || 0} />;
  } catch (error) {
    redirect('/login');
  }
}

