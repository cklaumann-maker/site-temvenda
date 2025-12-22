'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { DailyMeal } from '@rotina/shared';
import Link from 'next/link';

const MEAL_TYPE_LABELS: Record<string, string> = {
  'pre': 'Pré-treino',
  'post': 'Pós-treino',
  'cafe': 'Café da Manhã',
  'breakfast': 'Café da Manhã',
  'almoco': 'Almoço',
  'lunch': 'Almoço',
  'lanche_tarde': 'Lanche da Tarde',
  'snack': 'Lanche da Tarde',
  'jantar': 'Jantar',
  'dinner': 'Jantar',
};

const MEAL_TYPE_ICONS: Record<string, string> = {
  'pre': '⚡',
  'post': '💪',
  'cafe': '☕',
  'breakfast': '☕',
  'almoco': '🍽️',
  'lunch': '🍽️',
  'lanche_tarde': '🍎',
  'snack': '🍎',
  'jantar': '🌙',
  'dinner': '🌙',
};

export default function TodaySummary() {
  const [meals, setMeals] = useState<DailyMeal[]>([]);
  const [workoutCalories, setWorkoutCalories] = useState<number>(0);
  const [maxDailyCalories, setMaxDailyCalories] = useState<number>(2000);
  const [loading, setLoading] = useState(true);
  const supabase = createClient();
  const today = new Date().toISOString().split('T')[0];

  useEffect(() => {
    loadTodayData();
  }, []);

  const loadTodayData = async () => {
    setLoading(true);
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      setLoading(false);
      return;
    }

    // Load meals
    const { data: mealsData } = await supabase
      .from('daily_meals')
      .select('*')
      .eq('user_id', user.id)
      .eq('date', today)
      .order('meal_type', { ascending: true });

    setMeals((mealsData || []) as DailyMeal[]);

    // Load workout calories
    const { data: checkinData } = await (supabase
      .from('daily_checkins') as any)
      .select('workout_calories')
      .eq('user_id', user.id)
      .eq('date', today)
      .maybeSingle();

    if (checkinData) {
      setWorkoutCalories((checkinData as any).workout_calories || 0);
    }

    // Load max daily calories from profile
    const { data: profileData } = await (supabase
      .from('user_profiles') as any)
      .select('max_daily_calories')
      .eq('user_id', user.id)
      .single();

    if (profileData && profileData.max_daily_calories) {
      setMaxDailyCalories(profileData.max_daily_calories);
    }

    setLoading(false);
  };

  const getMealCalories = (meal: DailyMeal): number => {
    if (meal.option_selected) {
      if (meal.option_selected === 'opt1') return (meal as any).kcal_opt1 || 0;
      if (meal.option_selected === 'opt2') return (meal as any).kcal_opt2 || 0;
      if (meal.option_selected === 'opt3') return (meal as any).kcal_opt3 || 0;
    }
    if ((meal as any).kcal_other && (meal as any).kcal_other > 0) {
      return (meal as any).kcal_other || 0;
    }
    return 0;
  };

  const selectedMeals = meals.filter(m => {
    return m.option_selected || ((m as any).kcal_other && (m as any).kcal_other > 0);
  });

  const totalConsumed = meals.reduce((total, meal) => total + getMealCalories(meal), 0);
  const totalBurned = workoutCalories || 0;
  // Saldo = Consumidas - Gastas
  const netBalance = totalConsumed - totalBurned;
  // Déficit/Superávit = Saldo - Máximo
  // Positivo = Superávit (acima da meta), Negativo = Déficit (abaixo da meta)
  const deficitSurplus = netBalance - maxDailyCalories;

  if (loading) {
    return (
      <div className="bg-gray-800 rounded-lg p-6">
        <p className="text-gray-400">Carregando...</p>
      </div>
    );
  }

  return (
    <Link href="/app/today" className="block">
      <div className="bg-gray-800 rounded-lg p-6 hover:bg-gray-700 transition-colors cursor-pointer">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-white">Hoje</h2>
          <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>

        {/* Resumo de Refeições Selecionadas */}
        {selectedMeals.length > 0 ? (
          <div className="mb-4">
            <p className="text-xs text-gray-400 mb-2">Refeições selecionadas:</p>
            <div className="flex flex-wrap gap-2">
              {selectedMeals.slice(0, 4).map(meal => {
                const mealIcon = MEAL_TYPE_ICONS[meal.meal_type] || '🍽️';
                const mealLabel = MEAL_TYPE_LABELS[meal.meal_type] || meal.meal_type;
                const calories = getMealCalories(meal);
                const isManual = !meal.option_selected && (meal as any).kcal_other > 0;

                return (
                  <div
                    key={meal.id}
                    className={`
                      flex items-center gap-1 px-2 py-1 rounded text-xs
                      ${isManual 
                        ? 'bg-red-900/30 text-red-300 border border-red-700/50' 
                        : 'bg-green-900/30 text-green-300 border border-green-700/50'
                      }
                    `}
                  >
                    <span>{mealIcon}</span>
                    <span className="font-medium">{mealLabel}</span>
                    {calories > 0 && (
                      <span className="text-yellow-400">{calories}kcal</span>
                    )}
                  </div>
                );
              })}
              {selectedMeals.length > 4 && (
                <div className="flex items-center px-2 py-1 rounded text-xs bg-gray-700 text-gray-400 border border-gray-600">
                  +{selectedMeals.length - 4} mais
                </div>
              )}
            </div>
          </div>
        ) : (
          <p className="text-sm text-gray-500 mb-4">Nenhuma refeição selecionada ainda</p>
        )}

        {/* Resumo de Calorias */}
        <div className="space-y-3 pt-4 border-t border-gray-700">
          <div className="grid grid-cols-2 md:grid-cols-6 gap-2">
            <div className="text-center">
              <div className="text-xs text-gray-400 mb-1">Consumidas</div>
              <div className="text-lg font-bold text-yellow-400">{totalConsumed}</div>
              <div className="text-xs text-gray-500">kcal</div>
            </div>
            <div className="text-center">
              <div className="text-xs text-gray-400 mb-1">Gastas</div>
              <div className="text-lg font-bold text-orange-400">{totalBurned}</div>
              <div className="text-xs text-gray-500">kcal</div>
            </div>
            <div className={`text-center rounded-lg p-2 ${
              deficitSurplus < 0 
                ? 'bg-green-900/20 border border-green-700/50' 
                : 'bg-red-900/20 border border-red-700/50'
            }`}>
              <div className="text-xs text-gray-400 mb-1">Saldo</div>
              <div className={`text-lg font-bold ${
                deficitSurplus < 0 ? 'text-green-400' : 'text-red-300'
              }`}>
                {netBalance}
              </div>
              <div className="text-xs text-gray-500">kcal</div>
            </div>
            <div className="text-center">
              <div className="text-xs text-gray-400 mb-1">Máximo</div>
              <div className="text-lg font-bold text-purple-400">{maxDailyCalories}</div>
              <div className="text-xs text-gray-500">kcal</div>
            </div>
            <div className={`text-center rounded-lg p-2 ${
              deficitSurplus < 0 
                ? 'bg-green-900/20 border border-green-700' 
                : 'bg-red-900/20 border border-red-700'
            }`}>
              <div className="text-xs text-gray-400 mb-1">
                {deficitSurplus < 0 ? 'Déficit' : 'Superávit'}
              </div>
              <div className={`text-lg font-bold ${
                deficitSurplus < 0 ? 'text-green-400' : 'text-red-400'
              }`}>
                {Math.abs(deficitSurplus)}
              </div>
              <div className="text-xs text-gray-500">kcal</div>
            </div>
          </div>
        </div>

        <div className="mt-4 text-center">
          <span className="text-xs text-blue-400 hover:text-blue-300">
            Ver detalhes →
          </span>
        </div>
      </div>
    </Link>
  );
}

