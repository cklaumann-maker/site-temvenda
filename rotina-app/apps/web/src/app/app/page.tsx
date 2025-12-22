import { createClient } from '@/lib/supabase/server';
import { redirect } from 'next/navigation';
import Link from 'next/link';
import TodaySummary from './TodaySummary';

export default async function AppHomePage() {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) {
    redirect('/login');
  }

  // Carregar perfil do usuário para pegar o nome
  let userName: string | null = null;
  try {
    const { data: profile } = await (supabase
      .from('user_profiles') as any)
      .select('name')
      .eq('user_id', user.id)
      .single();
    
    if (profile && profile.name) {
      userName = profile.name;
    }
  } catch (error) {
    // Perfil não encontrado ou erro, continua sem nome
  }

  // Get today's adherence for quick view
  const today = new Date().toISOString().split('T')[0];
  let adherence: number | null = null;
  
  try {
    const { data } = await (supabase.rpc('calculate_adherence', {
      p_user_id: user.id,
      p_date: today,
    } as any));
    adherence = data || 0;
  } catch (error) {
    // If function doesn't exist, calculate manually
    const { data: meals } = await supabase
      .from('daily_meals')
      .select('option_selected')
      .eq('user_id', user.id)
      .eq('date', today);
    
    const planned = meals?.length || 0;
    const done = (meals || []).filter((m: any) => m.option_selected).length || 0;
    adherence = planned > 0 ? Math.round((done / planned) * 100) : 0;
  }

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            {userName ? `Bem vindo ${userName}!` : 'Bem vindo'}
          </h1>
          <p className="text-gray-400">Disciplina de Hábitos</p>
        </header>

        {/* Resumo do Dia */}
        <div className="mb-8">
          <TodaySummary />
        </div>

        {/* Menu Options */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Plan - Plano de Refeições */}
          <Link href="/app/plan" className="block">
            <div className="bg-gray-800 rounded-lg p-6 hover:bg-gray-700 transition-colors cursor-pointer">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xl font-semibold text-white">Plano</h3>
                <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <p className="text-gray-400 text-sm">Veja seu plano de refeições</p>
            </div>
          </Link>

          {/* Dashboard */}
          <Link href="/app/dashboard" className="block">
            <div className="bg-gray-800 rounded-lg p-6 hover:bg-gray-700 transition-colors cursor-pointer">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xl font-semibold text-white">Dashboard</h3>
                <svg className="w-6 h-6 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <p className="text-gray-400 text-sm">Acompanhe seu progresso</p>
            </div>
          </Link>

          {/* Check-in Diário */}
          <Link href="/app/checkin" className="block">
            <div className="bg-gray-800 rounded-lg p-6 hover:bg-gray-700 transition-colors cursor-pointer">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xl font-semibold text-white">Check-in</h3>
                <svg className="w-6 h-6 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p className="text-gray-400 text-sm">Registre seu check-in diário</p>
            </div>
          </Link>

          {/* Gerenciar Plano */}
          <Link href="/app/plan-manager" className="block">
            <div className="bg-gray-800 rounded-lg p-6 hover:bg-gray-700 transition-colors cursor-pointer">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xl font-semibold text-white">Gerenciar Plano</h3>
                <svg className="w-6 h-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                </svg>
              </div>
              <p className="text-gray-400 text-sm">Replique ou importe plano alimentar</p>
            </div>
          </Link>

          {/* Perfil */}
          <Link href="/app/profile" className="block">
            <div className="bg-gray-800 rounded-lg p-6 hover:bg-gray-700 transition-colors cursor-pointer">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xl font-semibold text-white">Perfil</h3>
                <svg className="w-6 h-6 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <p className="text-gray-400 text-sm">Gerencie seus dados pessoais</p>
            </div>
          </Link>
        </div>

        {/* Logout Button */}
        <div className="mt-8 text-center">
          <form action="/auth/logout" method="post">
            <button
              type="submit"
              className="text-gray-400 hover:text-white text-sm"
            >
              Sair
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

