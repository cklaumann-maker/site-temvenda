'use client';

import { useState, useMemo } from 'react';
import { createClient } from '@/lib/supabase/client';
import { DailyMeal, MEAL_TYPES } from '@rotina/shared';
import { formatDate, getDayLabel } from '@rotina/shared';

// Ordem dos tipos de refeição conforme a planilha importada
// ORDEM EXATA: Pré-treino, Pós-treino, Café da manhã, Almoço, Lanche da tarde, Jantar
const MEAL_TYPE_ORDER: Record<string, number> = {
  'pre': 1,           // Pré-treino
  'post': 2,          // Pós-treino
  'cafe': 3,          // Café da manhã
  'breakfast': 3,     // Café da manhã (alias)
  'almoco': 4,        // Almoço
  'lunch': 4,         // Almoço (alias)
  'lanche_tarde': 5,  // Lanche da tarde
  'snack': 5,         // Lanche da tarde (alias)
  'jantar': 6,        // Jantar
  'dinner': 6,        // Jantar (alias)
  'ceia': 7,          // Ceia (se houver)
};

// Função para ordenar refeições pela ordem da planilha
function sortMealsByType<T extends { meal_type: string }>(meals: T[]): T[] {
  return [...meals].sort((a, b) => {
    const orderA = MEAL_TYPE_ORDER[a.meal_type] || 999;
    const orderB = MEAL_TYPE_ORDER[b.meal_type] || 999;
    return orderA - orderB;
  });
}

interface TodayClientProps {
  meals: DailyMeal[];
  adherence: number;
}

export default function TodayClient({ meals: initialMeals, adherence }: TodayClientProps) {
  const [meals, setMeals] = useState(initialMeals);
  const [loading, setLoading] = useState<string | null>(null);
  const supabase = createClient();
  const today = new Date().toISOString().split('T')[0];
  
  // Ordenar refeições pela ordem da planilha
  const sortedMeals = useMemo(() => sortMealsByType(meals), [meals]);

  const handleMarkMeal = async (mealId: string, option: 'opt1' | 'opt2' | 'opt3') => {
    setLoading(mealId);
    
    const { error } = await (supabase
      .from('daily_meals') as any)
      .update({ option_selected: option })
      .eq('id', mealId);

    if (!error) {
      setMeals(meals.map(m => m.id === mealId ? { ...m, option_selected: option } : m));
    }
    
    setLoading(null);
  };

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-2xl mx-auto">
        <header className="mb-6">
          <h1 className="text-2xl font-bold text-white mb-2">Hoje</h1>
          <p className="text-gray-400">{getDayLabel(today)}, {formatDate(today)}</p>
        </header>

        <div className="bg-gray-800 rounded-lg p-4 mb-6">
          <h2 className="text-lg font-semibold text-white mb-2">Aderência</h2>
          <div className="text-3xl font-bold text-blue-400">{adherence}%</div>
          <div className="text-sm text-gray-400 mt-1">
            {sortedMeals.filter(m => m.option_selected).length} de {sortedMeals.length} refeições concluídas
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-white">Refeições de Hoje</h2>
          
          {sortedMeals.map((meal) => (
            <div key={meal.id} className="bg-gray-800 rounded-lg p-4">
              <h3 className="text-lg font-medium text-white mb-2">
                {MEAL_TYPES[meal.meal_type] || meal.meal_type}
              </h3>
              
              {meal.option_selected ? (
                <div className="text-green-400 mb-2">
                  ✓ Selecionado: {meal[meal.option_selected]}
                </div>
              ) : (
                <div className="space-y-2">
                  {meal.opt1 && (
                    <button
                      onClick={() => handleMarkMeal(meal.id, 'opt1')}
                      disabled={loading === meal.id}
                      className="block w-full text-left p-2 bg-gray-700 rounded hover:bg-gray-600 text-white"
                    >
                      Opção 1: {meal.opt1}
                    </button>
                  )}
                  {meal.opt2 && (
                    <button
                      onClick={() => handleMarkMeal(meal.id, 'opt2')}
                      disabled={loading === meal.id}
                      className="block w-full text-left p-2 bg-gray-700 rounded hover:bg-gray-600 text-white"
                    >
                      Opção 2: {meal.opt2}
                    </button>
                  )}
                  {meal.opt3 && (
                    <button
                      onClick={() => handleMarkMeal(meal.id, 'opt3')}
                      disabled={loading === meal.id}
                      className="block w-full text-left p-2 bg-gray-700 rounded hover:bg-gray-600 text-white"
                    >
                      Opção 3: {meal.opt3}
                    </button>
                  )}
                </div>
              )}
              
              {meal.avoid && (
                <div className="mt-2 text-sm text-yellow-400">
                  ⚠️ Evitar: {meal.avoid}
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-6">
          <a
            href="/app/checkin"
            className="block w-full bg-blue-600 text-white py-3 rounded-lg text-center font-medium hover:bg-blue-700"
          >
            Fazer Check-in Diário
          </a>
        </div>
      </div>
    </div>
  );
}

