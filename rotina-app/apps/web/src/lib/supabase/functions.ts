import { createClient } from './server';

export async function generate_daily_meals(userId: string, date: string) {
  const supabase = createClient();
  
  // Call the database function
  const { data, error } = await supabase.rpc('generate_daily_meals', {
    p_user_id: userId,
    p_date: date,
  });

  if (error) {
    throw error;
  }

  return data;
}

export async function calculate_adherence(userId: string, date: string) {
  const supabase = createClient();
  
  const { data, error } = await supabase.rpc('calculate_adherence', {
    p_user_id: userId,
    p_date: date,
  });

  if (error) {
    throw error;
  }

  return data;
}

