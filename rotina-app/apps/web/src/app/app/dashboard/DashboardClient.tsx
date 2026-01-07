'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { createClient } from '@/lib/supabase/client';
import { DailyCheckin, DailyMeal } from '@rotina/shared';
import { formatDateLocal, getTodayLocal } from '@/lib/utils/date';

interface DashboardClientProps {
  checkins: DailyCheckin[];
  adherence: number;
}

interface DailySummary {
  date: string;
  consumed: number;
  burned: number;
  netBalance: number;
  maxDaily: number;
  deficitSurplus: number;
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
  const [dailySummaries, setDailySummaries] = useState<DailySummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const supabase = createClient();

  useEffect(() => {
    // Inicializar com mês atual
    const today = new Date();
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
    const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    setStartDate(formatDateLocal(firstDay));
    setEndDate(formatDateLocal(lastDay));
  }, []);

  useEffect(() => {
    if (startDate && endDate) {
      loadMonthlyCalories();
    }
  }, [startDate, endDate]);

  const loadMonthlyCalories = async () => {
    setLoading(true);
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      setLoading(false);
      return;
    }

    // Carregar calorias máximas do perfil
    const { data: profileData } = await (supabase
      .from('user_profiles') as any)
      .select('max_daily_calories')
      .eq('user_id', user.id)
      .single();

    const maxDaily = profileData?.max_daily_calories || 2000;

    // Carregar refeições do período
    const { data: mealsData } = await supabase
      .from('daily_meals')
      .select('*')
      .eq('user_id', user.id)
      .gte('date', startDate)
      .lte('date', endDate)
      .order('date', { ascending: false });

    // Calcular calorias consumidas por dia
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

    // Calcular calorias gastas por dia
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

    // Criar resumos diários
    const daysWithData = new Set([
      ...Object.keys(consumedByDay).filter(day => consumedByDay[day] > 0),
      ...Object.keys(burnedByDay).filter(day => burnedByDay[day] > 0)
    ]);

    const summaries: DailySummary[] = Array.from(daysWithData)
      .sort()
      .reverse()
      .map(date => {
        const consumed = consumedByDay[date] || 0;
        const burned = burnedByDay[date] || 0;
        const netBalance = consumed - burned;
        const deficitSurplus = netBalance - maxDaily;
        
        return {
          date,
          consumed,
          burned,
          netBalance,
          maxDaily,
          deficitSurplus,
        };
      });

    setDailySummaries(summaries);

    // Calcular totais
    const consumed = Object.values(consumedByDay).reduce((total, val) => total + val, 0);
    const burned = Object.values(burnedByDay).reduce((total, val) => total + val, 0);
    const daysCounted = daysWithData.size;
    const totalMaxCalories = maxDaily * daysCounted;
    const netBalance = consumed - burned;
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
    const startDateExport = formatDateLocal(thirtyDaysAgo);
    const endDateExport = getTodayLocal();

    window.open(`/api/export/adherence?start_date=${startDateExport}&end_date=${endDateExport}`, '_blank');
  };

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-6xl mx-auto">
        <header className="mb-4">
          <h1 className="text-xl font-bold text-white">Dashboard</h1>
        </header>

        {/* Filtro de Período */}
        <div className="bg-gray-800 rounded-lg p-3 mb-4 border border-gray-700">
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <label className="block text-xs text-gray-400 mb-1">Data Inicial</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full bg-gray-700 text-white text-sm px-3 py-1.5 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="flex-1">
              <label className="block text-xs text-gray-400 mb-1">Data Final</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="w-full bg-gray-700 text-white text-sm px-3 py-1.5 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Resumo Mensal de Calorias - Uma linha, 20% menor */}
        {!loading && (
          <div className="bg-gray-800 rounded-lg p-3 mb-4 border border-gray-700">
            <h2 className="text-sm font-semibold text-white mb-2">Resumo do Período</h2>
            
            {/* Cards em uma linha */}
            <div className="grid grid-cols-5 gap-2">
              <div className="bg-gray-700/50 rounded-lg p-2">
                <div className="text-xs text-gray-400 mb-0.5">Consumidas</div>
                <div className="text-lg font-bold text-yellow-400">{monthlyCalories.consumed.toLocaleString()}</div>
                <div className="text-xs text-gray-500">kcal</div>
              </div>
              <div className="bg-gray-700/50 rounded-lg p-2">
                <div className="text-xs text-gray-400 mb-0.5">Gastas</div>
                <div className="text-lg font-bold text-orange-400">{monthlyCalories.burned.toLocaleString()}</div>
                <div className="text-xs text-gray-500">kcal</div>
              </div>
              <div className={`rounded-lg p-2 ${
                monthlyCalories.deficitSurplus < 0 
                  ? 'bg-green-900/20 border border-green-700/50' 
                  : 'bg-red-900/20 border border-red-700/50'
              }`}>
                <div className="text-xs text-gray-400 mb-0.5">Saldo</div>
                <div className={`text-lg font-bold ${
                  monthlyCalories.deficitSurplus < 0 ? 'text-green-400' : 'text-red-300'
                }`}>
                  {(monthlyCalories.consumed - monthlyCalories.burned).toLocaleString()}
                </div>
                <div className="text-xs text-gray-500">kcal</div>
              </div>
              <div className="bg-gray-700/50 rounded-lg p-2">
                <div className="text-xs text-gray-400 mb-0.5">Máximo</div>
                <div className="text-lg font-bold text-purple-400">
                  {(monthlyCalories.maxDaily * monthlyCalories.daysCounted).toLocaleString()}
                </div>
                <div className="text-xs text-gray-500">({monthlyCalories.daysCounted} dias)</div>
              </div>
              <div className={`rounded-lg p-2 ${
                monthlyCalories.deficitSurplus < 0 
                  ? 'bg-green-900/20 border border-green-700' 
                  : 'bg-red-900/20 border border-red-700'
              }`}>
                <div className="text-xs text-gray-400 mb-0.5">
                  {monthlyCalories.deficitSurplus < 0 ? 'Déficit' : 'Superávit'}
                </div>
                <div className={`text-lg font-bold ${
                  monthlyCalories.deficitSurplus < 0 ? 'text-green-400' : 'text-red-400'
                }`}>
                  {Math.abs(monthlyCalories.deficitSurplus).toLocaleString()}
                </div>
                <div className="text-xs text-gray-500">kcal</div>
              </div>
            </div>
          </div>
        )}

        {/* Tabela com dados diários */}
        {!loading && dailySummaries.length > 0 && (
          <div className="bg-gray-800 rounded-lg p-3 mb-4 border border-gray-700">
            <h2 className="text-sm font-semibold text-white mb-2">Relatório Diário</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                <thead className="bg-gray-700">
                  <tr>
                    <th className="px-3 py-1.5 text-left text-gray-300 font-medium">Data</th>
                    <th className="px-3 py-1.5 text-left text-gray-300 font-medium">Consumidas</th>
                    <th className="px-3 py-1.5 text-left text-gray-300 font-medium">Gastas</th>
                    <th className="px-3 py-1.5 text-left text-gray-300 font-medium">Saldo</th>
                    <th className="px-3 py-1.5 text-left text-gray-300 font-medium">Máximo</th>
                    <th className="px-3 py-1.5 text-left text-gray-300 font-medium">Déficit/Superávit</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {dailySummaries.map((summary) => (
                    <tr key={summary.date} className="hover:bg-gray-700/50">
                      <td className="px-3 py-1.5 text-white">
                        {new Date(summary.date).toLocaleDateString('pt-BR')}
                      </td>
                      <td className="px-3 py-1.5 text-yellow-400">{summary.consumed.toLocaleString()}</td>
                      <td className="px-3 py-1.5 text-orange-400">{summary.burned.toLocaleString()}</td>
                      <td className={`px-3 py-1.5 ${
                        summary.netBalance < 0 ? 'text-red-300' : 'text-green-400'
                      }`}>
                        {summary.netBalance.toLocaleString()}
                      </td>
                      <td className="px-3 py-1.5 text-purple-400">{summary.maxDaily.toLocaleString()}</td>
                      <td className={`px-3 py-1.5 ${
                        summary.deficitSurplus < 0 ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {summary.deficitSurplus >= 0 ? '+' : ''}{summary.deficitSurplus.toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Cards de informações - 50% menores */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
          <div className="bg-gray-800 rounded-lg p-3">
            <h2 className="text-xs font-semibold text-white mb-1">Aderência</h2>
            <div className="text-lg font-bold text-blue-400">{adherence}%</div>
          </div>

          <div className="bg-gray-800 rounded-lg p-3">
            <h2 className="text-xs font-semibold text-white mb-1">Peso Atual</h2>
            <div className="text-lg font-bold text-green-400">
              {latestWeight ? `${latestWeight} kg` : 'N/A'}
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-3">
            <h2 className="text-xs font-semibold text-white mb-1">Cardio (30 dias)</h2>
            <div className="text-lg font-bold text-purple-400">{totalCardio} min</div>
          </div>

          <div className="bg-gray-800 rounded-lg p-3">
            <h2 className="text-xs font-semibold text-white mb-1">Treinos (30 dias)</h2>
            <div className="text-lg font-bold text-orange-400">{workoutsDone}</div>
          </div>
        </div>

        {/* Botões pequenos */}
        <div className="flex gap-2">
          <button
            onClick={handleExportAdherence}
            className="px-4 py-1.5 bg-green-600 text-white text-sm rounded-lg font-medium hover:bg-green-700 transition-colors"
          >
            Exportar Relatório
          </button>

          <Link
            href="/app/plan"
            className="px-4 py-1.5 bg-blue-600 text-white text-sm rounded-lg text-center font-medium hover:bg-blue-700 transition-colors"
          >
            Ver Meu Plano
          </Link>
        </div>
      </div>
    </div>
  );
}
