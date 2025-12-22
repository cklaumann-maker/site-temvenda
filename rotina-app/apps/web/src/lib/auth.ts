import { createClient } from './supabase/server';
import { UserRole } from '@rotina/shared';

export async function getCurrentUser() {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  return user;
}

export async function getUserRole(): Promise<UserRole | null> {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) return null;
  
  const { data } = await supabase
    .from('org_members')
    .select('role')
    .eq('user_id', user.id)
    .eq('active', true)
    .single();
  
  return data?.role as UserRole | null;
}

export async function isOwnerOrCoach(): Promise<boolean> {
  const role = await getUserRole();
  return role === 'OWNER' || role === 'COACH';
}

export async function requireAuth() {
  const user = await getCurrentUser();
  if (!user) {
    throw new Error('Unauthorized');
  }
  return user;
}

export async function requireAdmin() {
  const user = await requireAuth();
  const isAdmin = await isOwnerOrCoach();
  if (!isAdmin) {
    throw new Error('Forbidden');
  }
  return user;
}

