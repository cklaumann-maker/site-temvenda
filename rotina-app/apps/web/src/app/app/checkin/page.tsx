'use client';

import { useState, useEffect } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';
import { dailyCheckinSchema } from '@rotina/shared';
import { formatDateLocal, getTodayLocal, isSameDate } from '@/lib/utils/date';

export default function CheckinPage() {
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [weight, setWeight] = useState('');
  const [workoutDone, setWorkoutDone] = useState(false);
  const [hasAerobic, setHasAerobic] = useState(false);
  const [workoutCalories, setWorkoutCalories] = useState('0');
  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);
  const router = useRouter();
  const supabase = createClient();
  const dateStr = formatDateLocal(selectedDate);
  const isToday = isSameDate(selectedDate, new Date());

  useEffect(() => {
    loadCheckinData();
  }, [selectedDate]);

  const loadCheckinData = async () => {
    setLoadingData(true);
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      setLoadingData(false);
      return;
    }

    const { data } = await (supabase
      .from('daily_checkins') as any)
      .select('*')
      .eq('user_id', user.id)
      .eq('date', dateStr)
      .single();

    if (data) {
      setWeight(data.weight_kg?.toString() || '');
      setWorkoutDone(data.workout_done || false);
      setHasAerobic(data.cardio_min > 0 || false);
      setWorkoutCalories((data.workout_calories || 0).toString());
    } else {
      setWeight('');
      setWorkoutDone(false);
      setHasAerobic(false);
      setWorkoutCalories('0');
    }
    setLoadingData(false);
  };

  const changeDate = (days: number) => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() + days);
    setSelectedDate(newDate);
  };

  const goToToday = () => {
    setSelectedDate(new Date());
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const data = {
      weight: weight ? parseFloat(weight) : undefined,
      workout_done: workoutDone,
      workout_calories: parseInt(workoutCalories) || 0,
      cardio_min: hasAerobic ? 30 : 0, // Se tem aeróbico, assume 30 minutos
      functional: false, // Campo obrigatório
    };

    // Validate
    const validation = dailyCheckinSchema.safeParse(data);
    if (!validation.success) {
      alert('Dados inválidos: ' + validation.error.message);
      setLoading(false);
      return;
    }

    // Get current user
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      router.push('/login');
      return;
    }

    // Upsert checkin - garantir que todos os campos obrigatórios estejam presentes
    const checkinData = {
      user_id: user.id,
      date: dateStr,
      weight_kg: data.weight || null,
      workout_done: data.workout_done,
      workout_calories: data.workout_calories || 0,
      cardio_min: data.cardio_min || 0,
      functional: false, // Campo obrigatório, sempre false por enquanto
    };

    const { error } = await (supabase
      .from('daily_checkins') as any)
      .upsert(checkinData, {
        onConflict: 'user_id,date',
      });

    if (error) {
      alert('Erro ao salvar check-in: ' + error.message);
    } else {
      // Voltar para a página anterior ou para today
      router.push('/app/today');
    }

    setLoading(false);
  };

  if (loadingData) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-400">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-md mx-auto">
        {/* Header com data e navegação */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
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
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Peso */}
          <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
            <label htmlFor="weight" className="block text-sm font-medium text-gray-300 mb-2">
              Peso (kg)
            </label>
            <input
              id="weight"
              type="number"
              step="0.1"
              min="0"
              max="500"
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              className="w-full px-4 py-3 bg-gray-700 text-white rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="75.2"
            />
          </div>

          {/* Treino */}
          <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
            <label className="flex items-center space-x-3 mb-4">
              <input
                type="checkbox"
                checked={workoutDone}
                onChange={(e) => {
                  setWorkoutDone(e.target.checked);
                  if (!e.target.checked) {
                    setHasAerobic(false);
                    setWorkoutCalories('0');
                  }
                }}
                className="w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
              />
              <span className="text-white font-medium text-lg">Fiz treino hoje</span>
            </label>

            {workoutDone && (
              <div className="space-y-4 mt-4 pt-4 border-t border-gray-700">
                {/* Aeróbico */}
                <label className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    checked={hasAerobic}
                    onChange={(e) => setHasAerobic(e.target.checked)}
                    className="w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
                  />
                  <span className="text-gray-300">Com aeróbico</span>
                </label>

                {/* Calorias gastas */}
                <div>
                  <label htmlFor="workoutCalories" className="block text-sm font-medium text-gray-300 mb-2">
                    Total de calorias gastas (kcal)
                  </label>
                  <input
                    id="workoutCalories"
                    type="number"
                    min="0"
                    max="2000"
                    value={workoutCalories}
                    onChange={(e) => setWorkoutCalories(e.target.value)}
                    className="w-full px-4 py-3 bg-gray-700 text-white rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="300"
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    Este valor aparecerá no resumo do dia em &quot;Gastas&quot;
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Botão Salvar */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Salvando...' : 'Salvar Check-in'}
          </button>
        </form>
      </div>
    </div>
  );
}
