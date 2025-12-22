'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { createClient } from '@/lib/supabase/client';
import { DailyCheckin, DailyMeal } from '@rotina/shared';

interface DashboardClientProps {
  checkins: DailyCheckin[];
  adherence: number;
}

export default function DashboardClient({ checkins, adherence }: DashboardClientProps) {
  const [monthlyCalories, setMonthlyCalories] = useState<{
    consumed: number;
    burned: number;
    maxDaily: number;
    deficitSurplus: number;
    daysCounted: number;
  }>({
    consumed: 0,
    burned: 0,
    maxDaily: 2000,
    deficitSurplus: 0,
    daysCounted: 0,
  });
  const [loading, setLoading] = useState(true);
  const supabase = createClient();

  useEffect(() => {
    loadMonthlyCalories();
  }, []);

  const loadMonthlyCalories = async () => {
    setLoading(true);
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      setLoading(false);
      return;
    }

    // Período do mês atual
    const today = new Date();
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
    const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    const startDate = firstDay.toISOString().split('T')[0];
    const endDate = lastDay.toISOString().split('T')[0];

    // Carregar calorias máximas do perfil
    const { data: profileData } = await (supabase
      .from('user_profiles') as any)
      .select('max_daily_calories')
      .eq('user_id', user.id)
      .single();

    const maxDaily = profileData?.max_daily_calories || 2000;

    // Carregar refeições do mês
    const { data: mealsData } = await supabase
      .from('daily_meals')
      .select('*')
      .eq('user_id', user.id)
      .gte('date', startDate)
      .lte('date', endDate);

    // Calcular calorias consumidas apenas dos dias que foram contabilizados
    // Um dia é contabilizado se tem pelo menos uma refeição selecionada ou calorias manuais
    const consumedByDay: Record<string, number> = {};
    (mealsData || []).forEach((meal: any) => {
      const dayKey = meal.date;
      if (!consumedByDay[dayKey]) {
        consumedByDay[dayKey] = 0;
      }
      
      if (meal.option_selected) {
        if (meal.option_selected === 'opt1') consumedByDay[dayKey] += (meal.kcal_opt1 || 0);
        if (meal.option_selected === 'opt2') consumedByDay[dayKey] += (meal.kcal_opt2 || 0);
        if (meal.option_selected === 'opt3') consumedByDay[dayKey] += (meal.kcal_opt3 || 0);
      }
      if (meal.kcal_other && meal.kcal_other > 0) {
        consumedByDay[dayKey] += meal.kcal_other;
      }
    });

    // Calcular calorias gastas apenas dos dias que foram contabilizados
    const burnedByDay: Record<string, number> = {};
    const { data: checkinsData } = await (supabase
      .from('daily_checkins') as any)
      .select('date, workout_calories')
      .eq('user_id', user.id)
      .gte('date', startDate)
      .lte('date', endDate);

    (checkinsData || []).forEach((checkin: any) => {
      if (checkin.workout_calories && checkin.workout_calories > 0) {
        burnedByDay[checkin.date] = (burnedByDay[checkin.date] || 0) + (checkin.workout_calories || 0);
      }
    });

    // Somar apenas dos dias que foram contabilizados (têm consumo ou gasto)
    const daysWithData = new Set([
      ...Object.keys(consumedByDay).filter(day => consumedByDay[day] > 0),
      ...Object.keys(burnedByDay).filter(day => burnedByDay[day] > 0)
    ]);

    const consumed = Object.values(consumedByDay).reduce((total, val) => total + val, 0);
    const burned = Object.values(burnedByDay).reduce((total, val) => total + val, 0);
    
    // Calcular apenas para dias contabilizados
    const daysCounted = daysWithData.size;
    const totalMaxCalories = maxDaily * daysCounted;
    
    // Saldo = Consumidas - Gastas
    const netBalance = consumed - burned;
    // Déficit/Superávit = Saldo - Máximo
    const deficitSurplus = netBalance - totalMaxCalories;

    setMonthlyCalories({
      consumed,
      burned,
      maxDaily,
      deficitSurplus,
      daysCounted,
    });
    setLoading(false);
  };

  const latestWeight = checkins.find(c => c.weight_kg)?.weight_kg;
  const totalCardio = checkins.reduce((sum, c) => sum + c.cardio_min, 0);
  const workoutsDone = checkins.filter(c => c.workout_done).length;

  const handleExportAdherence = async () => {
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    const startDate = thirtyDaysAgo.toISOString().split('T')[0];
    const endDate = new Date().toISOString().split('T')[0];

    window.open(`/api/export/adherence?start_date=${startDate}&end_date=${endDate}`, '_blank');
  };

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-4xl mx-auto">
        <header className="mb-6">
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        </header>

        {/* Resumo Mensal de Calorias */}
        {!loading && (
          <div className="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
            <h2 className="text-xl font-semibold text-white mb-4">Resumo Mensal de Calorias</h2>
            
            {/* Racional da conta */}
            <div className="bg-gray-700/30 rounded-lg p-4 mb-4 border border-gray-600">
              <div className="text-xs text-gray-400 mb-2">Racional do cálculo:</div>
              <div className="space-y-1 text-sm">
                <div className="text-gray-300">
                  <span className="text-yellow-400">{monthlyCalories.consumed.toLocaleString()}</span> kcal consumidas - <span className="text-orange-400">{monthlyCalories.burned.toLocaleString()}</span> kcal gastas = <span className="text-blue-400 font-semibold">{(monthlyCalories.consumed - monthlyCalories.burned).toLocaleString()}</span> kcal (saldo)
                </div>
                <div className="text-gray-300">
                  <span className="text-blue-400 font-semibold">{(monthlyCalories.consumed - monthlyCalories.burned).toLocaleString()}</span> kcal (saldo) - <span className="text-purple-400">{(monthlyCalories.maxDaily * monthlyCalories.daysCounted).toLocaleString()}</span> kcal máximas ({monthlyCalories.daysCounted} dias × {monthlyCalories.maxDaily}/dia) = <span className={`font-semibold ${monthlyCalories.deficitSurplus < 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {monthlyCalories.deficitSurplus >= 0 ? '+' : ''}{monthlyCalories.deficitSurplus.toLocaleString()}
                  </span> kcal ({monthlyCalories.deficitSurplus < 0 ? 'déficit' : 'superávit'})
                </div>
                <div className="text-xs text-gray-500 mt-2">
                  * Cálculo baseado apenas nos {monthlyCalories.daysCounted} dias do mês que foram contabilizados
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
              <div className="bg-gray-700/50 rounded-lg p-4">
                <div className="text-xs text-gray-400 mb-1">Consumidas</div>
                <div className="text-2xl font-bold text-yellow-400">{monthlyCalories.consumed.toLocaleString()}</div>
                <div className="text-xs text-gray-500">kcal</div>
              </div>
              <div className="bg-gray-700/50 rounded-lg p-4">
                <div className="text-xs text-gray-400 mb-1">Gastas</div>
                <div className="text-2xl font-bold text-orange-400">{monthlyCalories.burned.toLocaleString()}</div>
                <div className="text-xs text-gray-500">kcal</div>
              </div>
              <div className={`rounded-lg p-4 ${
                monthlyCalories.deficitSurplus < 0 
                  ? 'bg-green-900/20 border border-green-700/50' 
                  : 'bg-red-900/20 border border-red-700/50'
              }`}>
                <div className="text-xs text-gray-400 mb-1">Saldo</div>
                <div className={`text-2xl font-bold ${
                  monthlyCalories.deficitSurplus < 0 ? 'text-green-400' : 'text-red-300'
                }`}>
                  {(monthlyCalories.consumed - monthlyCalories.burned).toLocaleString()}
                </div>
                <div className="text-xs text-gray-500">kcal</div>
              </div>
              <div className="bg-gray-700/50 rounded-lg p-4">
                <div className="text-xs text-gray-400 mb-1">Máximo</div>
                <div className="text-2xl font-bold text-purple-400">
                  {(monthlyCalories.maxDaily * monthlyCalories.daysCounted).toLocaleString()}
                </div>
                <div className="text-xs text-gray-500">kcal ({monthlyCalories.daysCounted} dias)</div>
              </div>
              <div className={`rounded-lg p-4 ${
                monthlyCalories.deficitSurplus < 0 
                  ? 'bg-green-900/20 border border-green-700' 
                  : 'bg-red-900/20 border border-red-700'
              }`}>
                <div className="text-xs text-gray-400 mb-1">
                  {monthlyCalories.deficitSurplus < 0 ? 'Déficit' : 'Superávit'}
                </div>
                <div className={`text-2xl font-bold ${
                  monthlyCalories.deficitSurplus < 0 ? 'text-green-400' : 'text-red-400'
                }`}>
                  {Math.abs(monthlyCalories.deficitSurplus).toLocaleString()}
                </div>
                <div className="text-xs text-gray-500">kcal</div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold text-white mb-2">Aderência</h2>
            <div className="text-3xl font-bold text-blue-400">{adherence}%</div>
          </div>

          <div className="bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold text-white mb-2">Peso Atual</h2>
            <div className="text-3xl font-bold text-green-400">
              {latestWeight ? `${latestWeight} kg` : 'N/A'}
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold text-white mb-2">Cardio (30 dias)</h2>
            <div className="text-3xl font-bold text-purple-400">{totalCardio} min</div>
          </div>

          <div className="bg-gray-800 rounded-lg p-4">
            <h2 className="text-lg font-semibold text-white mb-2">Treinos (30 dias)</h2>
            <div className="text-3xl font-bold text-orange-400">{workoutsDone}</div>
          </div>
        </div>

        <div className="space-y-4">
          <button
            onClick={handleExportAdherence}
            className="w-full bg-green-600 text-white py-3 rounded-lg font-medium hover:bg-green-700"
          >
            Exportar Relatório de Aderência (CSV)
          </button>

          <Link
            href="/app/plan"
            className="block w-full bg-blue-600 text-white py-3 rounded-lg text-center font-medium hover:bg-blue-700"
          >
            Ver Meu Plano
          </Link>
        </div>
      </div>
    </div>
  );
}

