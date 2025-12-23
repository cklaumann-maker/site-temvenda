'use client';

import { useState, useEffect, useCallback } from 'react';
import { createClient } from '@/lib/supabase/client';
import { DailyMeal, OptionSelected } from '@rotina/shared';
import { formatDateLocal, getTodayLocal } from '@/lib/utils/date';

// Ordem dos tipos de refeição conforme a planilha importada
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
  'lanche_manha': 999,
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
  'lanche_manha': 'Lanche da Manhã',
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

// Componente para opção "Outros"
function OtherMealOption({ 
  meal, 
  onSave 
}: { 
  meal: DailyMeal; 
  onSave: (kcal: number, description: string) => void;
}) {
  const [showOther, setShowOther] = useState(!!(meal as any).kcal_other);
  const [kcalOther, setKcalOther] = useState((meal as any).kcal_other?.toString() || '');
  const [otherDescription, setOtherDescription] = useState((meal as any).other_description || '');
  const [saving, setSaving] = useState(false);

  // Sincronizar estado quando meal mudar
  useEffect(() => {
    setKcalOther((meal as any).kcal_other?.toString() || '');
    setOtherDescription((meal as any).other_description || '');
    setShowOther(!!(meal as any).kcal_other);
  }, [meal]);

  const handleSave = async () => {
    const kcal = parseInt(kcalOther) || 0;
    setSaving(true);
    try {
      await onSave(kcal, otherDescription);
      if (kcal === 0) {
        setShowOther(false);
      }
    } catch (error) {
      console.error('Error saving:', error);
    } finally {
      setSaving(false);
    }
  };

  if (!showOther && !(meal as any).kcal_other) {
    return (
      <button
        onClick={() => setShowOther(true)}
        className="w-full mt-3 text-sm text-gray-400 hover:text-blue-400 transition-colors border border-dashed border-gray-600 rounded-lg p-3 hover:border-blue-500"
      >
        + Outros (inserir calorias)
      </button>
    );
  }

  return (
    <div className="mt-3 p-3 rounded-lg border border-gray-600 bg-gray-800/50">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-gray-400 font-medium">Outros:</span>
        {(meal as any).kcal_other && (
          <span className="text-xs text-yellow-400 font-medium">
            {(meal as any).kcal_other} kcal
          </span>
        )}
      </div>
      <input
        type="number"
        placeholder="Calorias"
        value={kcalOther}
        onChange={(e) => setKcalOther(e.target.value)}
        className="w-full mb-2 px-3 py-2 bg-gray-700 text-white rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        min="0"
      />
      <input
        type="text"
        placeholder="Descrição (opcional)"
        value={otherDescription}
        onChange={(e) => setOtherDescription(e.target.value)}
        className="w-full mb-2 px-3 py-2 bg-gray-700 text-white rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <div className="flex gap-2">
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {saving ? 'Salvando...' : 'OK'}
        </button>
        {(meal as any).kcal_other && (
          <button
            onClick={() => {
              setKcalOther('');
              setOtherDescription('');
              onSave(0, '');
              setShowOther(false);
            }}
            className="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg text-sm font-medium hover:bg-gray-600 transition-colors"
          >
            Remover
          </button>
        )}
      </div>
    </div>
  );
}

// Componente de resumo de calorias do dia
function DailyCaloriesSummary({ 
  date, 
  meals, 
  getMealCalories 
}: { 
  date: Date; 
  meals: DailyMeal[]; 
  getMealCalories: (meal: DailyMeal) => number;
}) {
  const [workoutCalories, setWorkoutCalories] = useState<number>(0);
  const [maxDailyCalories, setMaxDailyCalories] = useState<number>(2000);
  const supabase = createClient();
  const dateStr = formatDateLocal(date);

  useEffect(() => {
    const loadData = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;

      // Carregar calorias do treino
      const { data: checkinData, error: checkinError } = await (supabase
        .from('daily_checkins') as any)
        .select('workout_calories')
        .eq('user_id', user.id)
        .eq('date', dateStr)
        .maybeSingle();

      if (checkinError) {
        console.error('Error loading workout calories:', checkinError);
        setWorkoutCalories(0);
      } else if (checkinData) {
        setWorkoutCalories((checkinData as any).workout_calories || 0);
      } else {
        setWorkoutCalories(0);
      }

      // Carregar calorias máximas do perfil
      const { data: profileData } = await (supabase
        .from('user_profiles') as any)
        .select('max_daily_calories')
        .eq('user_id', user.id)
        .single();

      if (profileData && profileData.max_daily_calories) {
        setMaxDailyCalories(profileData.max_daily_calories);
      }
    };

    loadData();
  }, [dateStr, supabase]);

  const dayMeals = meals.filter(m => m.date === dateStr);
  const totalConsumed = dayMeals.reduce((total, meal) => total + getMealCalories(meal), 0);
  const totalBurned = workoutCalories || 0;
  // Saldo = Consumidas - Gastas
  const netBalance = totalConsumed - totalBurned;
  // Déficit/Superávit = Saldo - Máximo
  // Positivo = Superávit (acima da meta), Negativo = Déficit (abaixo da meta)
  const deficitSurplus = netBalance - maxDailyCalories;

  return (
    <div className="space-y-4 mt-4">
      {/* Racional da conta */}
      <div className="bg-gray-800/30 rounded-lg p-4 border border-gray-700">
        <div className="text-xs text-gray-400 mb-2">Racional do cálculo:</div>
        <div className="space-y-1 text-sm">
          <div className="text-gray-300">
            <span className="text-yellow-400">{totalConsumed}</span> kcal consumidas - <span className="text-orange-400">{totalBurned}</span> kcal gastas = <span className="text-blue-400 font-semibold">{netBalance}</span> kcal (saldo)
          </div>
          <div className="text-gray-300">
            <span className="text-blue-400 font-semibold">{netBalance}</span> kcal (saldo) - <span className="text-purple-400">{maxDailyCalories}</span> kcal máximas = <span className={`font-semibold ${deficitSurplus < 0 ? 'text-green-400' : 'text-red-400'}`}>
              {deficitSurplus >= 0 ? '+' : ''}{deficitSurplus}
            </span> kcal ({deficitSurplus < 0 ? 'déficit' : 'superávit'})
          </div>
        </div>
      </div>

      {/* Cards de resumo */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
        <div className="bg-gray-800/50 rounded-lg p-3 border border-gray-700">
          <div className="text-xs text-gray-400 mb-1">Consumidas</div>
          <div className="text-xl font-bold text-yellow-400">{totalConsumed}</div>
          <div className="text-xs text-gray-500">kcal</div>
        </div>
        <div className="bg-gray-800/50 rounded-lg p-3 border border-gray-700">
          <div className="text-xs text-gray-400 mb-1">Gastas</div>
          <div className="text-xl font-bold text-orange-400">{totalBurned}</div>
          <div className="text-xs text-gray-500">kcal</div>
        </div>
        <div className={`rounded-lg p-3 border ${
          deficitSurplus < 0 
            ? 'bg-green-900/20 border-green-700/50' 
            : 'bg-red-900/20 border-red-700/50'
        }`}>
          <div className="text-xs text-gray-400 mb-1">Saldo</div>
          <div className={`text-xl font-bold ${
            deficitSurplus < 0 ? 'text-green-400' : 'text-red-300'
          }`}>
            {netBalance}
          </div>
          <div className="text-xs text-gray-500">kcal</div>
        </div>
        <div className="bg-gray-800/50 rounded-lg p-3 border border-gray-700">
          <div className="text-xs text-gray-400 mb-1">Máximo</div>
          <div className="text-xl font-bold text-purple-400">{maxDailyCalories}</div>
          <div className="text-xs text-gray-500">kcal</div>
        </div>
        <div className={`rounded-lg p-3 border ${
          deficitSurplus < 0 
            ? 'bg-green-900/20 border-green-700' 
            : 'bg-red-900/20 border-red-700'
        }`}>
          <div className="text-xs text-gray-400 mb-1">
            {deficitSurplus < 0 ? 'Déficit' : 'Superávit'}
          </div>
          <div className={`text-xl font-bold ${
            deficitSurplus < 0 ? 'text-green-400' : 'text-red-400'
          }`}>
            {Math.abs(deficitSurplus)}
          </div>
          <div className="text-xs text-gray-500">kcal</div>
        </div>
      </div>
    </div>
  );
}

export default function TodayCalendar() {
  const [meals, setMeals] = useState<DailyMeal[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [expandedMeals, setExpandedMeals] = useState<Set<string>>(new Set());
  const supabase = createClient();

  const loadMeals = useCallback(async () => {
    setLoading(true);
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      setLoading(false);
      return;
    }

    const dateStr = formatDateLocal(selectedDate);
    
    try {
      await (supabase.rpc as any)('generate_daily_meals', {
        p_user_id: user.id,
        p_date: dateStr,
      });
    } catch (error: any) {
      // Continue even if generation fails
    }

    const { data, error } = await supabase
      .from('daily_meals')
      .select('*')
      .eq('user_id', user.id)
      .eq('date', dateStr)
      .order('meal_type', { ascending: true });

    if (error) {
      console.error('Error loading meals:', error);
      setMeals([]);
    } else {
      const mealsData = (data || []) as DailyMeal[];
      const sortedMeals = mealsData.sort((a, b) => {
        const orderA = MEAL_TYPE_ORDER[a.meal_type] || 999;
        const orderB = MEAL_TYPE_ORDER[b.meal_type] || 999;
        return orderA - orderB;
      });
      setMeals(sortedMeals);
    }
    setLoading(false);
  }, [selectedDate, supabase]);

  useEffect(() => {
    loadMeals();
  }, [loadMeals]);

  const toggleMeal = (mealId: string) => {
    const newExpanded = new Set(expandedMeals);
    if (newExpanded.has(mealId)) {
      newExpanded.delete(mealId);
    } else {
      newExpanded.add(mealId);
    }
    setExpandedMeals(newExpanded);
  };

  const selectOption = async (mealId: string, option: OptionSelected | null) => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

    // Se selecionar uma opção do plano, limpar calorias manuais
    const updatedMeals = meals.map(m => 
      m.id === mealId ? { 
        ...m, 
        option_selected: option,
        // Limpar kcal_other quando selecionar uma opção do plano
        kcal_other: option ? null : (m as any).kcal_other,
        other_description: option ? null : (m as any).other_description
      } : m
    );
    setMeals(updatedMeals);

    // Atualizar no banco: limpar kcal_other se selecionar opção do plano
    const updateData: any = { option_selected: option };
    if (option) {
      // Se selecionou uma opção, limpar calorias manuais
      updateData.kcal_other = null;
      updateData.other_description = null;
    }

    const { error } = await (supabase
      .from('daily_meals') as any)
      .update(updateData)
      .eq('id', mealId)
      .eq('user_id', user.id);

    if (error) {
      console.error('Error updating meal:', error);
      loadMeals();
    }
  };

  const saveOtherMeal = async (mealId: string, kcalOther: number, otherDescription: string) => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

    // Se inserir calorias manuais, limpar opção selecionada do plano
    const updatedMeals = meals.map(m => 
      m.id === mealId ? { 
        ...m, 
        kcal_other: kcalOther > 0 ? kcalOther : null, 
        other_description: otherDescription || null,
        // Limpar option_selected quando inserir calorias manuais
        option_selected: kcalOther > 0 ? null : m.option_selected
      } : m
    );
    setMeals(updatedMeals);

    // Save to database - limpar option_selected se inserir calorias manuais
    const updateData: any = {
      kcal_other: kcalOther > 0 ? kcalOther : null,
      other_description: otherDescription || null
    };
    
    // Se inserir calorias manuais, limpar a opção selecionada
    if (kcalOther > 0) {
      updateData.option_selected = null;
    }

    const { error } = await (supabase
      .from('daily_meals') as any)
      .update(updateData)
      .eq('id', mealId)
      .eq('user_id', user.id);

    if (error) {
      console.error('Error updating other meal:', error);
      // Revert on error - reload from database
      await loadMeals();
      alert('Erro ao salvar calorias: ' + error.message);
    } else {
      // Success - ensure state is updated
      console.log('Calorias salvas com sucesso:', { mealId, kcalOther, otherDescription });
    }
  };

  const getMealCalories = (meal: DailyMeal): number => {
    // Se tem opção selecionada, retorna calorias da opção
    if (meal.option_selected) {
      if (meal.option_selected === 'opt1') return (meal as any).kcal_opt1 || 0;
      if (meal.option_selected === 'opt2') return (meal as any).kcal_opt2 || 0;
      if (meal.option_selected === 'opt3') return (meal as any).kcal_opt3 || 0;
    }
    
    // Se não tem opção selecionada mas tem kcal_other, retorna kcal_other
    // Isso permite somar calorias inseridas manualmente mesmo sem selecionar uma opção
    if ((meal as any).kcal_other && (meal as any).kcal_other > 0) {
      return (meal as any).kcal_other || 0;
    }
    
    return 0;
  };

  const hasManualCalories = (meal: DailyMeal): boolean => {
    return !!(meal as any).kcal_other && (meal as any).kcal_other > 0 && !meal.option_selected;
  };

  const changeDate = (days: number) => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() + days);
    setSelectedDate(newDate);
    setExpandedMeals(new Set());
  };

  const goToToday = () => {
    setSelectedDate(new Date());
    setExpandedMeals(new Set());
  };

  const isToday = formatDateLocal(selectedDate) === getTodayLocal();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-400">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-2xl mx-auto">
        {/* Header com data e navegação */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <button
                onClick={() => changeDate(-1)}
                className="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              
              <div className="text-center">
                <div className="text-2xl font-bold text-white">
                  {selectedDate.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' })}
                </div>
                {!isToday && (
                  <button
                    onClick={goToToday}
                    className="text-sm text-blue-400 hover:text-blue-300 mt-1"
                  >
                    Ir para hoje
                  </button>
                )}
              </div>
              
              <button
                onClick={() => changeDate(1)}
                className="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
            
            <button
              onClick={() => loadMeals()}
              className="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
              title="Recarregar"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
          </div>

          {/* Resumo de Calorias */}
          <DailyCaloriesSummary 
            date={selectedDate} 
            meals={meals} 
            getMealCalories={getMealCalories} 
          />
        </div>

        {/* Lista de Períodos de Refeição */}
        {meals.length === 0 ? (
          <div className="text-center py-12 text-gray-400">
            <p>Nenhuma refeição planejada para este dia.</p>
          </div>
        ) : (
          <div className="space-y-3">
            {meals.map(meal => {
              const isExpanded = expandedMeals.has(meal.id);
              const hasOptions = meal.opt1 || meal.opt2 || meal.opt3;
              const selectedCalories = getMealCalories(meal);
              const mealIcon = MEAL_TYPE_ICONS[meal.meal_type] || '🍽️';
              const mealLabel = MEAL_TYPE_LABELS[meal.meal_type] || meal.meal_type;
              const hasManual = hasManualCalories(meal);
              const hasSelected = !!meal.option_selected;

              return (
                <div
                  key={meal.id}
                  className={`
                    rounded-lg border transition-all
                    ${hasSelected 
                      ? 'bg-green-900/10 border-green-600/50' 
                      : hasManual
                      ? 'bg-red-900/10 border-red-600/50'
                      : 'bg-gray-800/50 border-gray-700'
                    }
                    ${isExpanded ? 'shadow-lg' : ''}
                  `}
                >
                  {/* Header do Período */}
                  <button
                    onClick={() => toggleMeal(meal.id)}
                    className="w-full p-4 flex items-center justify-between hover:bg-gray-800/30 transition-colors rounded-lg"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{mealIcon}</span>
                      <div className="text-left">
                        <div className="text-white font-semibold text-lg">
                          {mealLabel}
                        </div>
                        {selectedCalories > 0 && (
                          <div className={`text-xs mt-0.5 ${
                            hasSelected ? 'text-yellow-400' : 'text-red-400'
                          }`}>
                            {selectedCalories} kcal {hasSelected ? 'selecionadas' : 'inseridas manualmente'}
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      {hasSelected && (
                        <div className="w-3 h-3 rounded-full bg-green-500"></div>
                      )}
                      {hasManual && !hasSelected && (
                        <div className="w-3 h-3 rounded-full bg-red-500"></div>
                      )}
                      <svg
                        className={`w-5 h-5 text-gray-400 transition-transform ${
                          isExpanded ? 'rotate-180' : ''
                        }`}
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                  </button>

                  {/* Conteúdo Expandido */}
                  {isExpanded && (
                    <div className="px-4 pb-4 border-t border-gray-700 pt-4">
                      {meal.avoid && (
                        <div className="mb-4 p-3 bg-red-900/20 border border-red-700/50 rounded-lg">
                          <div className="text-xs text-red-400 font-medium mb-1">⚠️ Evitar:</div>
                          <div className="text-sm text-red-300">{meal.avoid}</div>
                        </div>
                      )}

                      {hasOptions ? (
                        <div className="space-y-2">
                          {/* Opção 1 */}
                          {meal.opt1 && (
                            <button
                              onClick={() => selectOption(meal.id, meal.option_selected === 'opt1' ? null : 'opt1')}
                              className={`
                                w-full flex items-start p-3 rounded-lg border transition-all text-left
                                ${meal.option_selected === 'opt1' 
                                  ? 'bg-blue-900/30 border-blue-500 ring-2 ring-blue-500/50' 
                                  : 'bg-gray-700/30 border-gray-600 hover:bg-gray-700/50'
                                }
                              `}
                            >
                              <div className={`
                                w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 mt-0.5 flex-shrink-0
                                ${meal.option_selected === 'opt1'
                                  ? 'border-blue-500 bg-blue-500'
                                  : 'border-gray-500 bg-transparent'
                                }
                              `}>
                                {meal.option_selected === 'opt1' && (
                                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                  </svg>
                                )}
                              </div>
                              <div className="flex-1">
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
                            </button>
                          )}

                          {/* Opção 2 */}
                          {meal.opt2 && (
                            <button
                              onClick={() => selectOption(meal.id, meal.option_selected === 'opt2' ? null : 'opt2')}
                              className={`
                                w-full flex items-start p-3 rounded-lg border transition-all text-left
                                ${meal.option_selected === 'opt2' 
                                  ? 'bg-blue-900/30 border-blue-500 ring-2 ring-blue-500/50' 
                                  : 'bg-gray-700/30 border-gray-600 hover:bg-gray-700/50'
                                }
                              `}
                            >
                              <div className={`
                                w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 mt-0.5 flex-shrink-0
                                ${meal.option_selected === 'opt2'
                                  ? 'border-blue-500 bg-blue-500'
                                  : 'border-gray-500 bg-transparent'
                                }
                              `}>
                                {meal.option_selected === 'opt2' && (
                                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                  </svg>
                                )}
                              </div>
                              <div className="flex-1">
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
                            </button>
                          )}

                          {/* Opção 3 */}
                          {meal.opt3 && (
                            <button
                              onClick={() => selectOption(meal.id, meal.option_selected === 'opt3' ? null : 'opt3')}
                              className={`
                                w-full flex items-start p-3 rounded-lg border transition-all text-left
                                ${meal.option_selected === 'opt3' 
                                  ? 'bg-blue-900/30 border-blue-500 ring-2 ring-blue-500/50' 
                                  : 'bg-gray-700/30 border-gray-600 hover:bg-gray-700/50'
                                }
                              `}
                            >
                              <div className={`
                                w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 mt-0.5 flex-shrink-0
                                ${meal.option_selected === 'opt3'
                                  ? 'border-blue-500 bg-blue-500'
                                  : 'border-gray-500 bg-transparent'
                                }
                              `}>
                                {meal.option_selected === 'opt3' && (
                                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                  </svg>
                                )}
                              </div>
                              <div className="flex-1">
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
                            </button>
                          )}

                          {/* Opção Outros */}
                          <OtherMealOption
                            meal={meal}
                            onSave={(kcal, description) => saveOtherMeal(meal.id, kcal, description)}
                          />

                        </div>
                      ) : (
                        <div className="text-gray-400 text-sm text-center py-4">
                          Nenhuma opção disponível para este período.
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
