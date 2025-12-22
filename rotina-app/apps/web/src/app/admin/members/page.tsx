import { createClient } from '@/lib/supabase/server';
import { requireAdmin } from '@/lib/auth';
import { redirect } from 'next/navigation';
import MembersClient from './MembersClient';

export default async function MembersPage() {
  try {
    const user = await requireAdmin();
    const supabase = createClient();

    // Get user's org
    const { data: orgMember } = await supabase
      .from('org_members')
      .select('org_id, role')
      .eq('user_id', user.id)
      .eq('active', true)
      .single();

    if (!orgMember || !orgMember.org_id) {
      redirect('/app/today');
    }

    // Get members based on role
    let membersQuery = supabase
      .from('org_members')
      .select(`
        id,
        user_id,
        role,
        profiles:user_id (
          id,
          email,
          full_name
        )
      `)
      .eq('org_id', orgMember.org_id)
      .eq('active', true);

    // If coach, only show members in their programs
    if (orgMember.role === 'COACH') {
      const { data: programs } = await supabase
        .from('programs')
        .select('id')
        .eq('org_id', orgMember.org_id);

      const programIds = programs?.map(p => p.id) || [];

      const { data: enrollments } = await supabase
        .from('enrollments')
        .select('user_id')
        .in('program_id', programIds)
        .eq('active', true);

      const memberIds = enrollments?.map(e => e.user_id) || [];
      membersQuery = membersQuery.in('user_id', memberIds);
    }

    const { data: members } = await membersQuery;

    return <MembersClient members={members || []} />;
  } catch (error) {
    redirect('/app/today');
  }
}

