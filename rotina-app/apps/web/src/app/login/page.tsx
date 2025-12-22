'use client';

import { useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const router = useRouter();
  const supabase = createClient();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    // Se tem senha preenchida, tenta login com senha primeiro
    if (password && password.length > 0) {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) {
        // Se falhar, pode ser que não tenha senha cadastrada, então usa magic link
        if (error.message.includes('Invalid login') || error.message.includes('Email not confirmed')) {
          // Tenta magic link como fallback
          const { error: otpError } = await supabase.auth.signInWithOtp({
            email,
            options: {
              emailRedirectTo: `${window.location.origin}/auth/callback?next=/app`,
            },
          });

          if (otpError) {
            setMessage('Erro ao enviar link de login: ' + otpError.message);
          } else {
            setMessage('Verifique seu email para o link de login!');
          }
        } else {
          setMessage('Erro ao fazer login: ' + error.message);
        }
      } else if (data.user) {
        router.push('/app');
        return;
      }
    } else {
      // Login com magic link (sem senha)
      const { error } = await supabase.auth.signInWithOtp({
        email,
        options: {
          emailRedirectTo: `${window.location.origin}/auth/callback?next=/app`,
        },
      });

      if (error) {
        setMessage('Erro ao enviar link de login: ' + error.message);
      } else {
        setMessage('Verifique seu email para o link de login!');
      }
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Rotina</h1>
          <p className="text-gray-400">Disciplina de Hábitos</p>
        </div>
        
        <form onSubmit={handleLogin} className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="seu@email.com"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
              Senha <span className="text-gray-500 text-xs">(opcional)</span>
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Se você tem senha cadastrada"
            />
            <p className="mt-1 text-xs text-gray-500">
              {password 
                ? 'Login será feito com senha' 
                : 'Se não preencher, você receberá um link por e-mail'}
            </p>
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading 
              ? (password ? 'Entrando...' : 'Enviando...') 
              : (password ? 'Entrar' : 'Enviar Magic Link')
            }
          </button>
          
          {message && (
            <p className={`mt-4 text-sm ${message.includes('Erro') ? 'text-red-400' : 'text-green-400'}`}>
              {message}
            </p>
          )}
        </form>
      </div>
    </div>
  );
}
