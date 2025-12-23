'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { DailyMeal, OptionSelected } from '@rotina/shared';
import { formatDateLocal, getTodayLocal } from '@/lib/utils/date';

const MEAL_TYPE_ORDER: Record<string, number> = {
  'pre': 1,
  'post': 2,
  'cafe': 3,
  'breakfast': 3,
  'almoco': 4,
  'lunch': 4,
  'lanche_tarde': 5,
  'snack': 5,
  'jantar': 6,
  'dinner': 6,
  'ceia': 999,
};

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
  'ceia': 'Ceia',
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

const DAYS_OF_WEEK = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];

export default function PlanPage() {
  const [meals, setMeals] = useState<DailyMeal[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const supabase = createClient();

  useEffect(() => {
    loadPlan();
  }, []);

  const loadPlan = async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      setLoading(false);
      return;
    }

    const today = new Date();
    const endDate = new Date();
    endDate.setDate(today.getDate() + 90); // Próximos 90 dias

    const { data } = await supabase
      .from('daily_meals')
      .select('*')
      .eq('user_id', user.id)
      .gte('date', formatDateLocal(today))
      .lte('date', formatDateLocal(endDate))
      .order('date')
      .order('meal_type');

    setMeals(data || []);
    setLoading(false);
  };

  const getMealsForDate = (date: Date): DailyMeal[] => {
    const dateStr = formatDateLocal(date);
    const dayMeals = meals.filter(m => m.date === dateStr);
    return dayMeals.sort((a, b) => {
      const orderA = MEAL_TYPE_ORDER[a.meal_type] || 999;
      const orderB = MEAL_TYPE_ORDER[b.meal_type] || 999;
      return orderA - orderB;
    });
  };

  const hasMealsForDate = (date: Date): boolean => {
    return getMealsForDate(date).length > 0;
  };

  const getDaysInMonth = (): Date[] => {
    const year = currentMonth.getFullYear();
    const month = currentMonth.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const days: Date[] = [];
    
    // Adicionar dias do mês anterior para completar a semana
    const startDay = firstDay.getDay();
    for (let i = startDay - 1; i >= 0; i--) {
      const date = new Date(firstDay);
      date.setDate(date.getDate() - i - 1);
      days.push(date);
    }
    
    // Adicionar dias do mês atual
    for (let day = 1; day <= lastDay.getDate(); day++) {
      days.push(new Date(year, month, day));
    }
    
    // Adicionar dias do próximo mês para completar a semana
    const remainingDays = 42 - days.length; // 6 semanas * 7 dias
    for (let day = 1; day <= remainingDays; day++) {
      const date = new Date(year, month + 1, day);
      if (date <= new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate() + 90)) {
        days.push(date);
      }
    }
    
    return days;
  };

  const changeMonth = (direction: number) => {
    const newDate = new Date(currentMonth);
    newDate.setMonth(newDate.getMonth() + direction);
    setCurrentMonth(newDate);
  };

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 p-4 flex items-center justify-center">
        <div className="text-white">Carregando...</div>
      </div>
    );
  }

  const days = getDaysInMonth();

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-white mb-2">Plano Alimentar</h1>
          <p className="text-gray-400">Próximos 90 dias</p>
        </div>

        {/* Navegação do Mês */}
        <div className="flex items-center justify-between mb-6 bg-gray-800/50 rounded-lg p-4 border border-gray-700">
          <button
            onClick={() => changeMonth(-1)}
            className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          
          <h2 className="text-xl font-semibold text-white">
            {currentMonth.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' })}
          </h2>
          
          <button
            onClick={() => changeMonth(1)}
            className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        {/* Calendário */}
        <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700 mb-6">
          {/* Cabeçalho dos dias da semana */}
          <div className="grid grid-cols-7 gap-2 mb-2">
            {DAYS_OF_WEEK.map(day => (
              <div key={day} className="text-center text-sm font-medium text-gray-400 py-2">
                {day}
              </div>
            ))}
          </div>

          {/* Dias do calendário */}
          <div className="grid grid-cols-7 gap-2">
            {days.map((date, index) => {
              const dateStr = formatDateLocal(date);
              const todayDate = new Date();
              const isToday = formatDateLocal(date) === formatDateLocal(todayDate);
              const isSelected = selectedDate?.toDateString() === date.toDateString();
              const isPast = date < today;
              const isFuture = date > new Date(today.getTime() + 90 * 24 * 60 * 60 * 1000);
              const hasMeals = hasMealsForDate(date);
              const isCurrentMonth = date.getMonth() === currentMonth.getMonth();

              if (isFuture) {
                return <div key={index} className="aspect-square"></div>;
              }

              return (
                <button
                  key={index}
                  onClick={() => {
                    if (!isPast && hasMeals) {
                      setSelectedDate(date);
                    }
                  }}
                  className={`
                    aspect-square rounded-lg border transition-all
                    ${!isCurrentMonth ? 'opacity-30' : ''}
                    ${isPast ? 'opacity-50 cursor-not-allowed' : ''}
                    ${isToday ? 'border-blue-500 bg-blue-900/20' : 'border-gray-700'}
                    ${isSelected ? 'ring-2 ring-blue-500 ring-offset-2 ring-offset-gray-800' : ''}
                    ${hasMeals && !isPast ? 'hover:bg-gray-700 cursor-pointer' : 'cursor-default'}
                    ${!hasMeals && !isPast ? 'bg-gray-800/30' : 'bg-gray-800/50'}
                  `}
                >
                  <div className="flex flex-col items-center justify-center h-full p-1">
                    <div className={`text-sm font-medium ${
                      isToday ? 'text-blue-400' : 'text-white'
                    }`}>
                      {date.getDate()}
                    </div>
                    {hasMeals && (
                      <div className="w-1.5 h-1.5 rounded-full bg-green-500 mt-1"></div>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Detalhes do Dia Selecionado */}
        {selectedDate && (
          <div className="bg-gray-800/50 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-white">
                {selectedDate.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' })}
              </h3>
              <button
                onClick={() => setSelectedDate(null)}
                className="text-gray-400 hover:text-white"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {getMealsForDate(selectedDate).length === 0 ? (
              <p className="text-gray-400">Nenhuma refeição planejada para este dia.</p>
            ) : (
              <div className="space-y-4">
                {getMealsForDate(selectedDate).map(meal => {
                  const mealIcon = MEAL_TYPE_ICONS[meal.meal_type] || '🍽️';
                  const mealLabel = MEAL_TYPE_LABELS[meal.meal_type] || meal.meal_type;

                  return (
                    <div
                      key={meal.id}
                      className={`
                        p-4 rounded-lg border
                        ${meal.option_selected 
                          ? 'bg-green-900/20 border-green-700' 
                          : 'bg-gray-700/50 border-gray-600'
                        }
                      `}
                    >
                      <div className="flex items-center gap-3 mb-3">
                        <span className="text-2xl">{mealIcon}</span>
                        <h4 className="text-white font-semibold text-lg">
                          {mealLabel}
                        </h4>
                      </div>

                      {meal.avoid && (
                        <div className="mb-3 p-2 bg-red-900/20 border border-red-700/50 rounded-lg">
                          <p className="text-red-400 text-xs">
                            ⚠️ Evitar: {meal.avoid}
                          </p>
                        </div>
                      )}

                      <div className="space-y-2">
                        {meal.opt1 && (
                          <div className={`
                            p-3 rounded-lg border
                            ${meal.option_selected === 'opt1' 
                              ? 'bg-blue-900/30 border-blue-600' 
                              : 'bg-gray-800/50 border-gray-600'
                            }
                          `}>
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs text-gray-400 font-medium">Opção 1</span>
                              {(meal as any).kcal_opt1 > 0 && (
                                <span className="text-xs text-yellow-400 font-medium">
                                  {(meal as any).kcal_opt1} kcal
                                </span>
                              )}
                            </div>
                            <p className="text-white text-sm">{meal.opt1}</p>
                          </div>
                        )}

                        {meal.opt2 && (
                          <div className={`
                            p-3 rounded-lg border
                            ${meal.option_selected === 'opt2' 
                              ? 'bg-blue-900/30 border-blue-600' 
                              : 'bg-gray-800/50 border-gray-600'
                            }
                          `}>
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs text-gray-400 font-medium">Opção 2</span>
                              {(meal as any).kcal_opt2 > 0 && (
                                <span className="text-xs text-yellow-400 font-medium">
                                  {(meal as any).kcal_opt2} kcal
                                </span>
                              )}
                            </div>
                            <p className="text-white text-sm">{meal.opt2}</p>
                          </div>
                        )}

                        {meal.opt3 && (
                          <div className={`
                            p-3 rounded-lg border
                            ${meal.option_selected === 'opt3' 
                              ? 'bg-blue-900/30 border-blue-600' 
                              : 'bg-gray-800/50 border-gray-600'
                            }
                          `}>
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs text-gray-400 font-medium">Opção 3</span>
                              {(meal as any).kcal_opt3 > 0 && (
                                <span className="text-xs text-yellow-400 font-medium">
                                  {(meal as any).kcal_opt3} kcal
                                </span>
                              )}
                            </div>
                            <p className="text-white text-sm">{meal.opt3}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
