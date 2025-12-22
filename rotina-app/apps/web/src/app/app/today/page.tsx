import { createClient } from '@/lib/supabase/server';
import { generate_daily_meals } from '@/lib/supabase/functions';
import { redirect } from 'next/navigation';
import TodayCalendar from './TodayCalendar';

export default async function TodayPage() {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) {
    redirect('/login');
  }

  const today = new Date().toISOString().split('T')[0];
  
  // Generate meals if they don't exist
  try {
    await generate_daily_meals(user.id, today);
  } catch (error) {
    console.error('Error generating meals:', error);
  }

  return <TodayCalendar />;
}

