'use client';

import { useState, useEffect } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { formatDateLocal, getTodayLocal } from '@/lib/utils/date';

interface User {
  id: string;
  email: string;
  profile: {
    name: string | null;
  } | null;
}

export default function PlanManagerPage() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [isRoot, setIsRoot] = useState(false);
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<string>('');
  const supabase = createClient();
  const router = useRouter();

  useEffect(() => {
    checkRootAndLoadUsers();
  }, []);

  const checkRootAndLoadUsers = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;

      // Verificar se é root
      const { data: profile } = await supabase
        .from('user_profiles')
        .select('is_root')
        .eq('user_id', user.id)
        .single();

      if (profile && (profile as any).is_root) {
        setIsRoot(true);
        // Carregar lista de usuários
        loadUsers();
        setSelectedUserId(user.id); // Default para o próprio usuário
      }
    } catch (error) {
      console.error('Erro ao verificar root:', error);
    }
  };

  const loadUsers = async () => {
    try {
      const response = await fetch('/api/admin/users');
      if (response.ok) {
        const data = await response.json();
        setUsers(data.users || []);
      }
    } catch (error) {
      console.error('Erro ao carregar usuários:', error);
    }
  };

  const replicatePlan = async () => {
    setLoading(true);
    setMessage(null);

    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        throw new Error('Usuário não autenticado');
      }

      // Se for root e tiver selecionado outro usuário, usar o selecionado
      const targetUserId = isRoot && selectedUserId ? selectedUserId : user.id;
      
      // Verificar se root está tentando replicar para outro usuário
      if (targetUserId !== user.id && !isRoot) {
        throw new Error('Apenas usuários root podem replicar planos para outros usuários');
      }

      // Get the last date with meals
      const { data: lastMeal } = await supabase
        .from('daily_meals')
        .select('date')
        .eq('user_id', targetUserId)
        .order('date', { ascending: false })
        .limit(1)
        .single();

      if (!lastMeal || !(lastMeal as any).date) {
        throw new Error('Nenhuma refeição encontrada. Importe o plano primeiro.');
      }

      const lastDate = new Date((lastMeal as any).date);
      const startDate = new Date(lastDate);
      startDate.setDate(startDate.getDate() + 1); // Start from next day

      // Get all meals from the first 14 days to replicate
      const firstDate = new Date(lastDate);
      firstDate.setDate(firstDate.getDate() - 13); // Get first day of the 14-day period

      const { data: templateMeals } = await supabase
        .from('daily_meals')
        .select('date, meal_type, opt1, opt2, opt3, avoid, kcal_opt1, kcal_opt2, kcal_opt3')
        .eq('user_id', targetUserId)
        .gte('date', formatDateLocal(firstDate))
        .lte('date', formatDateLocal(lastDate))
        .order('date')
        .order('meal_type');

      if (!templateMeals || templateMeals.length === 0) {
        throw new Error('Nenhuma refeição encontrada para replicar.');
      }

      // Group meals by date
      const mealsByDate: Record<string, Array<{
        meal_type: string;
        opt1: string | null;
        opt2: string | null;
        opt3: string | null;
        avoid: string | null;
        kcal_opt1?: number;
        kcal_opt2?: number;
        kcal_opt3?: number;
      }>> = {};
      
      (templateMeals as any[]).forEach((meal: any) => {
        const dateStr = meal.date;
        if (!mealsByDate[dateStr]) {
          mealsByDate[dateStr] = [];
        }
        mealsByDate[dateStr].push({
          meal_type: meal.meal_type,
          opt1: meal.opt1,
          opt2: meal.opt2,
          opt3: meal.opt3,
          avoid: meal.avoid,
          kcal_opt1: meal.kcal_opt1 || 0,
          kcal_opt2: meal.kcal_opt2 || 0,
          kcal_opt3: meal.kcal_opt3 || 0,
        });
      });

      // Get sorted dates (should be 14 days)
      const sortedDates = Object.keys(mealsByDate).sort();
      if (sortedDates.length === 0) {
        throw new Error('Nenhuma refeição organizada por data encontrada.');
      }

      // Insert replicated meals for next 14 days
      const newMeals: Array<{
        user_id: string;
        date: string;
        meal_type: string;
        opt1: string | null;
        opt2: string | null;
        opt3: string | null;
        avoid: string | null;
        kcal_opt1?: number;
        kcal_opt2?: number;
        kcal_opt3?: number;
      }> = [];
      for (let day = 0; day < 14; day++) {
        const currentDate = new Date(startDate);
        currentDate.setDate(startDate.getDate() + day);
        const dateStr = formatDateLocal(currentDate);

        // Cycle through the 14 days of template meals
        const templateDateIndex = day % sortedDates.length;
        const templateDate = sortedDates[templateDateIndex];
        const dayMeals = mealsByDate[templateDate] || [];

        dayMeals.forEach(meal => {
          newMeals.push({
            user_id: targetUserId,
            date: dateStr,
            meal_type: meal.meal_type,
            opt1: meal.opt1,
            opt2: meal.opt2,
            opt3: meal.opt3,
            avoid: meal.avoid,
            // IMPORTANTE: Copiar calorias dos templates originais
            kcal_opt1: meal.kcal_opt1 || 0,
            kcal_opt2: meal.kcal_opt2 || 0,
            kcal_opt3: meal.kcal_opt3 || 0,
          });
        });
      }

      // Insert/Update in batches using upsert to handle duplicates
      const batchSize = 50;
      for (let i = 0; i < newMeals.length; i += batchSize) {
        const batch = newMeals.slice(i, i + batchSize);
        const { error } = await (supabase
          .from('daily_meals') as any)
          .upsert(batch, {
            onConflict: 'user_id,date,meal_type',
          });

        if (error) {
          throw error;
        }
      }

      const targetUserEmail = isRoot && selectedUserId !== user.id 
        ? users.find(u => u.id === selectedUserId)?.email || 'usuário selecionado'
        : user.email;
      
      setMessage({ 
        type: 'success', 
        text: `Plano replicado com sucesso para ${targetUserEmail}! ${newMeals.length} refeições adicionadas para os próximos 14 dias.` 
      });
    } catch (error: any) {
      setMessage({ type: 'error', text: error.message || 'Erro ao replicar plano' });
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setMessage(null);

    try {
      const text = await file.text();
      const lines = text.split('\n').filter(line => line.trim());
      
      if (lines.length < 2) {
        throw new Error('Arquivo CSV inválido');
      }

      // Parse CSV - detecta se usa ponto e vírgula ou vírgula
      const delimiter = lines[0].includes(';') ? ';' : ',';
      const headers = lines[0].split(delimiter).map(h => h.trim().replace(/\ufeff/g, ''));
      const meals: any[] = [];

      // Função para limpar texto de opções - remove todos os prefixos
      const cleanOptionText = (text: string | null): string | null => {
        if (!text) return null;
        
        let cleaned = text.trim();
        
        // Remove valores vazios ou traços
        if (cleaned === '' || cleaned === '—' || cleaned === '-' || cleaned === 'null' || cleaned === 'NULL') {
          return null;
        }
        
        // Remove prefixos comuns (case insensitive, flexível com espaços e parênteses)
        // Padrões: "Opção 1 (Principal): ", "Opção 1 (Principal):", "Opção 1(Principal):", etc.
        cleaned = cleaned.replace(/^Opção\s*\d+\s*\(?\s*Principal\s*\)?\s*:\s*/i, '');
        cleaned = cleaned.replace(/^Opção\s*\d+\s*\(?\s*Substituição\s*\)?\s*:\s*/i, '');
        cleaned = cleaned.replace(/^Opção\s*\d+\s*\(?\s*Substituicao\s*\)?\s*:\s*/i, ''); // Sem acento
        cleaned = cleaned.replace(/^Evitar\s*:\s*/i, '');
        
        // Remove espaços extras
        cleaned = cleaned.trim();
        
        // Se ficou vazio após limpar, retorna null
        if (cleaned === '' || cleaned === '—' || cleaned === '-') {
          return null;
        }
        
        return cleaned;
      };

      // Função robusta para parsear linha CSV considerando valores entre aspas
      const parseCSVLine = (line: string, delimiter: string): string[] => {
        const result: string[] = [];
        let currentField = '';
        let inQuotes = false;
        
        for (let i = 0; i < line.length; i++) {
          const char = line[i];
          const nextChar = line[i + 1];
          
          if (char === '"') {
            if (inQuotes && nextChar === '"') {
              // Escaped quote dentro de aspas
              currentField += '"';
              i++; // Skip next quote
            } else {
              // Toggle quote state
              inQuotes = !inQuotes;
            }
          } else if (char === delimiter && !inQuotes) {
            // End of field
            result.push(currentField);
            currentField = '';
          } else {
            currentField += char;
          }
        }
        
        // Add last field
        result.push(currentField);
        return result;
      };

      // Find column indices
      const dayIdx = headers.indexOf('day_label');
      const mealIdx = headers.indexOf('meal_type');
      const opt1Idx = headers.indexOf('opt1');
      const opt2Idx = headers.indexOf('opt2');
      const opt3Idx = headers.indexOf('opt3');
      const avoidIdx = headers.indexOf('avoid');

      if (dayIdx === -1 || mealIdx === -1) {
        throw new Error('Colunas obrigatórias não encontradas no CSV');
      }

      for (let i = 1; i < lines.length; i++) {
        // Parse CSV line properly handling quoted values
        const parts = parseCSVLine(lines[i], delimiter);
        if (parts.length < 3) continue;

        const dayLabel = parts[dayIdx]?.trim() || '';
        const mealType = parts[mealIdx]?.trim() || '';
        const opt1Raw = opt1Idx >= 0 && opt1Idx < parts.length ? parts[opt1Idx]?.trim() : null;
        const opt2Raw = opt2Idx >= 0 && opt2Idx < parts.length ? parts[opt2Idx]?.trim() : null;
        const opt3Raw = opt3Idx >= 0 && opt3Idx < parts.length ? parts[opt3Idx]?.trim() : null;
        let avoidRaw = avoidIdx >= 0 && avoidIdx < parts.length ? parts[avoidIdx]?.trim() : null;
        
        // Handle case where delimiter inside value splits it - concatenate remaining parts for avoid
        if (avoidIdx >= 0 && avoidIdx + 1 < parts.length) {
          const remaining = parts.slice(avoidIdx + 1)
            .map(p => p.trim())
            .filter(p => p && p !== '' && p !== '—' && p !== '-')
            .join(delimiter === ';' ? '; ' : ', ');
          if (remaining) {
            avoidRaw = avoidRaw ? avoidRaw + (delimiter === ';' ? '; ' : ', ') + remaining : remaining;
          }
        }

        if (!dayLabel || !mealType) continue;

        // Determine week (Semana 2 = week 2, otherwise week 1)
        const weekIndex = dayLabel.includes('Semana 2') || dayLabel.includes('(S2)') ? 2 : 1;
        const dayName = dayLabel.replace(' (Semana 2)', '').replace(' (S2)', '').trim();

        // Map day name to day_of_week
        const dayMap: Record<string, number> = {
          'Segunda': 1,
          'Terça': 2,
          'Quarta': 3,
          'Quinta': 4,
          'Sexta': 5,
          'Sábado': 6,
          'Domingo': 7,
        };

        const dayOfWeek = dayMap[dayName];
        if (!dayOfWeek) continue;

        // Map meal type (português -> código)
        const mealTypeMap: Record<string, string> = {
          'Pré-treino': 'pre',
          'Pós-treino': 'post',
          'Café da manhã': 'cafe',
          'Almoço': 'almoco',
          'Lanche da tarde': 'lanche_tarde',
          'Jantar': 'jantar',
          // Fallback para formato antigo
          'pre': 'pre',
          'post': 'post',
          'breakfast': 'cafe',
          'lunch': 'almoco',
          'snack': 'lanche_tarde',
          'dinner': 'jantar',
        };

        const mappedMealType = mealTypeMap[mealType] || mealType;
        
        // Clean options - remove todos os prefixos
        const opt1 = cleanOptionText(opt1Raw);
        const opt2 = cleanOptionText(opt2Raw);
        const opt3 = cleanOptionText(opt3Raw);
        const avoid = cleanOptionText(avoidRaw);

        // Debug: log first few meals to verify parsing
        if (meals.length < 3) {
          console.log('Parsed meal:', {
            dayLabel,
            mealType,
            mappedMealType,
            opt1Raw,
            opt1,
            opt2Raw,
            opt2,
            opt3Raw,
            opt3,
            avoidRaw,
            avoid,
          });
        }

        meals.push({
          week_index: weekIndex,
          day_of_week: dayOfWeek,
          meal_type: mappedMealType,
          opt1,
          opt2,
          opt3,
          avoid,
        });
      }

      if (meals.length === 0) {
        throw new Error('Nenhuma refeição válida encontrada no arquivo');
      }

      // Get user and program
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        throw new Error('Usuário não autenticado');
      }

      // Se for root e tiver selecionado outro usuário, usar o selecionado
      const targetUserId = isRoot && selectedUserId ? selectedUserId : user.id;
      
      // Verificar se root está tentando importar para outro usuário
      if (targetUserId !== user.id && !isRoot) {
        throw new Error('Apenas usuários root podem importar planos para outros usuários');
      }

      const programId = '00000000-0000-0000-0000-000000000002';

      // Ensure target user has an active enrollment in the program
      const { data: enrollment, error: enrollmentError } = await supabase
        .from('enrollments')
        .select('id')
        .eq('user_id', targetUserId)
        .eq('program_id', programId)
        .eq('active', true)
        .single();

      if (enrollmentError || !enrollment) {
        // Create enrollment if it doesn't exist
        const { error: createEnrollmentError } = await (supabase
          .from('enrollments') as any)
          .upsert({
            user_id: targetUserId,
            program_id: programId,
            start_date: getTodayLocal(),
            active: true,
          }, {
            onConflict: 'user_id,program_id',
          });

        if (createEnrollmentError) {
          console.warn('Warning: Could not create enrollment:', createEnrollmentError);
          // Continue anyway - the RLS policy should allow if user is enrolled
        }
      }

      // Clear existing plan_templates for the program first
      const { error: deleteError } = await (supabase
        .from('plan_templates') as any)
        .delete()
        .eq('program_id', programId);

      if (deleteError) {
        console.warn('Warning: Could not clear existing templates:', deleteError);
        // Continue anyway - we'll try to insert/update
      }

      // Insert new plan_templates in batches
      const batchSize = 50;
      for (let i = 0; i < meals.length; i += batchSize) {
        const batch = meals.slice(i, i + batchSize).map(meal => ({
          program_id: programId,
          week_index: meal.week_index,
          day_of_week: meal.day_of_week,
          meal_type: meal.meal_type,
          opt1: meal.opt1,
          opt2: meal.opt2,
          opt3: meal.opt3,
          avoid: meal.avoid,
        }));

        const { error } = await (supabase
          .from('plan_templates') as any)
          .insert(batch);

        if (error) {
          throw error;
        }
      }

      // Regenerate daily_meals for next 30 days to ensure all meals are updated
      const today = new Date();
      let mealsRegenerated = 0;
      for (let i = 0; i < 30; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);
        const dateStr = formatDateLocal(date);

        try {
          const { data } = await (supabase.rpc as any)('generate_daily_meals', {
            p_user_id: targetUserId,
            p_date: dateStr,
          });
          if (data && data > 0) {
            mealsRegenerated += data;
          }
        } catch (error: any) {
          console.warn(`Could not generate meals for ${dateStr}:`, error.message);
        }
      }

      const targetUserEmail = isRoot && selectedUserId !== user.id 
        ? users.find(u => u.id === selectedUserId)?.email || 'usuário selecionado'
        : user.email;
      
      setMessage({ 
        type: 'success', 
        text: `Plano importado com sucesso para ${targetUserEmail}! ${meals.length} templates salvos. ${mealsRegenerated} refeições diárias geradas/atualizadas.` 
      });
      
      // Refresh the page after 2 seconds to show updated meals
      setTimeout(() => {
        if (isRoot && selectedUserId !== user.id) {
          // Se root importou para outro usuário, voltar para admin
          router.push('/app/admin/users');
        } else {
          router.push('/app/today');
        }
      }, 2000);
    } catch (error: any) {
      setMessage({ type: 'error', text: error.message || 'Erro ao importar plano' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-2xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Gerenciar Plano Alimentar</h1>
          <p className="text-gray-400">Replique ou importe um novo plano alimentar</p>
        </header>

        {message && (
          <div className={`mb-6 p-4 rounded-lg ${
            message.type === 'success' 
              ? 'bg-green-900/20 border border-green-700 text-green-400' 
              : 'bg-red-900/20 border border-red-700 text-red-400'
          }`}>
            {message.text}
          </div>
        )}

        <div className="space-y-6">
          {/* Replicar Plano */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Replicar Plano</h2>
            <p className="text-gray-400 mb-4">
              Replique as últimas 14 refeições para os próximos 14 dias.
            </p>
            
            {isRoot && (
              <div className="mb-4 p-4 bg-yellow-900/20 border border-yellow-700 rounded-lg">
                <label className="block text-yellow-300 text-sm font-medium mb-2">
                  🔑 Modo Root: Selecione o usuário para replicar o plano
                </label>
                <select
                  value={selectedUserId}
                  onChange={(e) => setSelectedUserId(e.target.value)}
                  disabled={loading}
                  className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-yellow-500 focus:outline-none disabled:opacity-50"
                >
                  {users.map((u) => (
                    <option key={u.id} value={u.id}>
                      {u.email} {u.profile?.name ? `(${u.profile.name})` : ''}
                    </option>
                  ))}
                </select>
                <p className="text-xs text-yellow-400 mt-2">
                  Você está replicando o plano para o usuário selecionado acima.
                </p>
              </div>
            )}
            
            <button
              onClick={replicatePlan}
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Replicando...' : 'Replicar Plano (14 dias)'}
            </button>
          </div>

          {/* Importar Novo Plano */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Importar Novo Plano</h2>
            <p className="text-gray-400 mb-4">
              Importe um novo plano alimentar a partir de um arquivo CSV.
            </p>
            
            {isRoot && (
              <div className="mb-4 p-4 bg-yellow-900/20 border border-yellow-700 rounded-lg">
                <label className="block text-yellow-300 text-sm font-medium mb-2">
                  🔑 Modo Root: Selecione o usuário para importar o plano
                </label>
                <select
                  value={selectedUserId}
                  onChange={(e) => setSelectedUserId(e.target.value)}
                  disabled={loading}
                  className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-yellow-500 focus:outline-none disabled:opacity-50"
                >
                  {users.map((u) => (
                    <option key={u.id} value={u.id}>
                      {u.email} {u.profile?.name ? `(${u.profile.name})` : ''}
                    </option>
                  ))}
                </select>
                <p className="text-xs text-yellow-400 mt-2">
                  Você está importando o plano para o usuário selecionado acima.
                </p>
              </div>
            )}
            
            <div className="space-y-4">
              <label className="block">
                <span className="sr-only">Escolher arquivo CSV</span>
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileUpload}
                  disabled={loading}
                  className="block w-full text-sm text-gray-400
                    file:mr-4 file:py-2 file:px-4
                    file:rounded-lg file:border-0
                    file:text-sm file:font-semibold
                    file:bg-blue-600 file:text-white
                    hover:file:bg-blue-700
                    disabled:opacity-50 disabled:cursor-not-allowed"
                />
              </label>
              <p className="text-xs text-gray-500">
                Formato esperado: CSV com colunas date, day_label, meal_type, option_selected, opt1, opt2, opt3, avoid
              </p>
            </div>
          </div>

          {/* Importar Alimentos do Excel */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Importar Alimentos</h2>
            <p className="text-gray-400 mb-4">
              Importe alimentos de um arquivo Excel para usar na lista de substituição de refeições.
              Duplicatas serão ignoradas automaticamente.
            </p>
            
            <Link
              href="/app/admin/food-items/import"
              className="block w-full bg-green-600 text-white py-3 rounded-lg font-medium hover:bg-green-700 text-center"
            >
              📥 Importar Alimentos do Excel
            </Link>
            
            <p className="text-xs text-gray-500 mt-2">
              Formato esperado: Excel com colunas Categoria, Alimento, Porção Padrão, Calorias
            </p>
          </div>

          {/* Voltar */}
          <div className="text-center">
            <button
              onClick={() => router.push('/app')}
              className="text-gray-400 hover:text-white"
            >
              ← Voltar para início
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

