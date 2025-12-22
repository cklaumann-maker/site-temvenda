'use client';

import { useState, useEffect } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';

interface UserProfile {
  user_id: string;
  name: string | null;
  phone: string | null;
  cpf: string | null;
  city: string | null;
  state: string | null;
  height_cm: number | null;
  weight_kg: number | null;
  max_daily_calories: number | null;
}

interface IMCStatus {
  value: number;
  classification: string;
  color: string;
}

const IMC_CLASSIFICATIONS: IMCStatus[] = [
  { value: 18.5, classification: 'Abaixo do peso', color: 'text-blue-400' },
  { value: 25, classification: 'Peso normal', color: 'text-green-400' },
  { value: 30, classification: 'Sobrepeso', color: 'text-yellow-400' },
  { value: 35, classification: 'Obesidade grau I', color: 'text-orange-400' },
  { value: 40, classification: 'Obesidade grau II', color: 'text-red-400' },
  { value: Infinity, classification: 'Obesidade grau III', color: 'text-red-600' },
];

function calculateIMC(weightKg: number, heightCm: number): number {
  if (!weightKg || !heightCm || heightCm === 0) return 0;
  const heightM = heightCm / 100;
  return weightKg / (heightM * heightM);
}

function getIMCClassification(imc: number): IMCStatus {
  if (imc === 0) {
    return { value: 0, classification: 'Não calculado', color: 'text-gray-400' };
  }
  
  for (const status of IMC_CLASSIFICATIONS) {
    if (imc < status.value) {
      return status;
    }
  }
  
  return IMC_CLASSIFICATIONS[IMC_CLASSIFICATIONS.length - 1];
}

export default function ProfilePage() {
  const router = useRouter();
  const supabase = createClient();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  
  const [profile, setProfile] = useState<UserProfile>({
    user_id: '',
    name: null,
    phone: null,
    cpf: null,
    city: null,
    state: null,
    height_cm: null,
    weight_kg: null,
    max_daily_calories: 2000,
  });
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [hasPassword, setHasPassword] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    setLoading(true);
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      router.push('/login');
      return;
    }

    setEmail(user.email || '');

    // Verificar se usuário tem senha cadastrada
    // No Supabase, verificamos se o usuário tem email_verified e se tem providers
    // Se tiver provider 'email', provavelmente tem senha
    if (user) {
      const providers = user.app_metadata?.providers || [];
      // Se tem provider 'email', significa que tem senha cadastrada
      setHasPassword(providers.includes('email') || user.email_confirmed_at !== null);
    }

    // Carregar perfil
    const { data: profileData } = await (supabase
      .from('user_profiles') as any)
      .select('*')
      .eq('user_id', user.id)
      .single();

    if (profileData) {
      setProfile({
        ...profileData,
        max_daily_calories: profileData.max_daily_calories || 2000,
      });
    } else {
      // Criar perfil vazio se não existir
      setProfile({
        user_id: user.id,
        name: null,
        phone: null,
        cpf: null,
        city: null,
        state: null,
        height_cm: null,
        weight_kg: null,
        max_daily_calories: 2000,
      });
    }

    setLoading(false);
  };

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);

    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      setMessage({ type: 'error', text: 'Usuário não autenticado' });
      setSaving(false);
      return;
    }

    try {
      // Salvar perfil
      const { error: profileError } = await (supabase
        .from('user_profiles') as any)
        .upsert({
          user_id: user.id,
          name: profile.name || null,
          phone: profile.phone || null,
          cpf: profile.cpf || null,
          city: profile.city || null,
          state: profile.state || null,
          height_cm: profile.height_cm || null,
          weight_kg: profile.weight_kg || null,
          max_daily_calories: profile.max_daily_calories || 2000,
        }, {
          onConflict: 'user_id',
        });

      if (profileError) {
        throw profileError;
      }

      // Atualizar email se mudou
      if (email !== user.email) {
        const { error: emailError } = await supabase.auth.updateUser({
          email: email,
        });
        if (emailError) {
          throw emailError;
        }
      }

      // Atualizar senha se fornecida
      if (password && password.length > 0) {
        if (password !== confirmPassword) {
          throw new Error('As senhas não coincidem');
        }
        if (password.length < 6) {
          throw new Error('A senha deve ter pelo menos 6 caracteres');
        }

        const { error: passwordError } = await supabase.auth.updateUser({
          password: password,
        });
        if (passwordError) {
          throw passwordError;
        }
        setPassword('');
        setConfirmPassword('');
        setHasPassword(true);
      }

      setMessage({ type: 'success', text: 'Perfil atualizado com sucesso!' });
      await loadProfile();
    } catch (error: any) {
      setMessage({ type: 'error', text: error.message || 'Erro ao salvar perfil' });
    } finally {
      setSaving(false);
    }
  };

  const imc = calculateIMC(profile.weight_kg || 0, profile.height_cm || 0);
  const imcStatus = getIMCClassification(imc);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 p-4 flex items-center justify-center">
        <div className="text-white">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-3xl mx-auto">
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-white mb-2">Meu Perfil</h1>
          <p className="text-gray-400">Gerencie suas informações pessoais</p>
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

        <form onSubmit={handleSaveProfile} className="space-y-6">
          {/* Dados Pessoais */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h2 className="text-xl font-semibold text-white mb-4">Dados Pessoais</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                  Nome Completo
                </label>
                <input
                  id="name"
                  type="text"
                  value={profile.name || ''}
                  onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Seu nome completo"
                />
              </div>

              <div>
                <label htmlFor="phone" className="block text-sm font-medium text-gray-300 mb-2">
                  Telefone
                </label>
                <input
                  id="phone"
                  type="tel"
                  value={profile.phone || ''}
                  onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="(00) 00000-0000"
                />
              </div>

              <div>
                <label htmlFor="cpf" className="block text-sm font-medium text-gray-300 mb-2">
                  CPF
                </label>
                <input
                  id="cpf"
                  type="text"
                  value={profile.cpf || ''}
                  onChange={(e) => setProfile({ ...profile, cpf: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="000.000.000-00"
                />
              </div>

              <div>
                <label htmlFor="city" className="block text-sm font-medium text-gray-300 mb-2">
                  Cidade
                </label>
                <input
                  id="city"
                  type="text"
                  value={profile.city || ''}
                  onChange={(e) => setProfile({ ...profile, city: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Sua cidade"
                />
              </div>

              <div>
                <label htmlFor="state" className="block text-sm font-medium text-gray-300 mb-2">
                  Estado (UF)
                </label>
                <input
                  id="state"
                  type="text"
                  maxLength={2}
                  value={profile.state || ''}
                  onChange={(e) => setProfile({ ...profile, state: e.target.value.toUpperCase() })}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="RS"
                />
              </div>
            </div>
          </div>

          {/* Dados Físicos */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h2 className="text-xl font-semibold text-white mb-4">Dados Físicos</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="height" className="block text-sm font-medium text-gray-300 mb-2">
                  Altura (cm)
                </label>
                <input
                  id="height"
                  type="number"
                  min="0"
                  max="300"
                  value={profile.height_cm || ''}
                  onChange={(e) => setProfile({ ...profile, height_cm: parseInt(e.target.value) || null })}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="175"
                />
              </div>

              <div>
                <label htmlFor="weight" className="block text-sm font-medium text-gray-300 mb-2">
                  Peso (kg)
                </label>
                <input
                  id="weight"
                  type="number"
                  step="0.1"
                  min="0"
                  max="500"
                  value={profile.weight_kg || ''}
                  onChange={(e) => setProfile({ ...profile, weight_kg: parseFloat(e.target.value) || null })}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="75.5"
                />
              </div>

              <div className="md:col-span-2">
                <label htmlFor="maxCalories" className="block text-sm font-medium text-gray-300 mb-2">
                  Calorias Máximas por Dia (kcal)
                </label>
                <input
                  id="maxCalories"
                  type="number"
                  min="0"
                  max="10000"
                  value={profile.max_daily_calories || 2000}
                  onChange={(e) => setProfile({ ...profile, max_daily_calories: parseInt(e.target.value) || 2000 })}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="2000"
                />
                <p className="mt-1 text-xs text-gray-500">
                  Este valor será usado para calcular déficit ou superávit calórico diário
                </p>
              </div>
            </div>

            {/* Cálculo de IMC */}
            {imc > 0 && (
              <div className="mt-4 p-4 bg-gray-700/50 rounded-lg border border-gray-600">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-400">Índice de Massa Corporal (IMC)</span>
                  <span className={`text-2xl font-bold ${imcStatus.color}`}>
                    {imc.toFixed(1)}
                  </span>
                </div>
                <div className={`text-sm font-medium ${imcStatus.color}`}>
                  {imcStatus.classification}
                </div>
                <div className="mt-3 text-xs text-gray-500">
                  <p className="mb-1">Classificação IMC:</p>
                  <ul className="list-disc list-inside space-y-0.5">
                    <li>&lt; 18.5: Abaixo do peso</li>
                    <li>18.5 - 24.9: Peso normal</li>
                    <li>25 - 29.9: Sobrepeso</li>
                    <li>30 - 34.9: Obesidade grau I</li>
                    <li>35 - 39.9: Obesidade grau II</li>
                    <li>≥ 40: Obesidade grau III</li>
                  </ul>
                </div>
              </div>
            )}
          </div>

          {/* Dados de Acesso */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h2 className="text-xl font-semibold text-white mb-4">Dados de Acesso</h2>
            <div className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                  E-mail
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                  {hasPassword ? 'Nova Senha (deixe em branco para manter)' : 'Definir Senha'}
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder={hasPassword ? 'Nova senha' : 'Mínimo 6 caracteres'}
                  minLength={hasPassword ? 0 : 6}
                />
                {!hasPassword && (
                  <p className="mt-1 text-xs text-gray-500">
                    Ao definir uma senha, você poderá fazer login sem precisar do link por e-mail
                  </p>
                )}
              </div>

              {password && password.length > 0 && (
                <div>
                  <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-300 mb-2">
                    Confirmar Senha
                  </label>
                  <input
                    id="confirmPassword"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Confirme a senha"
                  />
                </div>
              )}
            </div>
          </div>

          {/* Botão Salvar */}
          <button
            type="submit"
            disabled={saving}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold text-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {saving ? 'Salvando...' : 'Salvar Alterações'}
          </button>
        </form>
      </div>
    </div>
  );
}

