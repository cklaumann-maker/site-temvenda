'use client';

import { useState, useEffect } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';
import { getAuthCallbackUrl } from '@/lib/utils/url';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [mounted, setMounted] = useState(false);
  const router = useRouter();
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  const supabase = mounted ? createClient() : null;

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!supabase) return;
    
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
              emailRedirectTo: getAuthCallbackUrl('/app'),
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
      console.log('📧 Iniciando envio de magic link para:', email);
      console.log('🔗 URL de callback:', getAuthCallbackUrl('/app'));
      
      // Primeiro, tentar criar usuário se não existir usando signUp
      // Isso garante que o usuário seja criado mesmo se não existir
      console.log('👤 Verificando/criando usuário...');
      const { data: signUpData, error: signUpError } = await supabase.auth.signUp({
        email,
        options: {
          emailRedirectTo: getAuthCallbackUrl('/app'),
          shouldCreateUser: true,
        },
      });
      
      if (signUpError) {
        console.error('❌ Erro ao criar/verificar usuário:', signUpError);
        
        // Se o erro for que o usuário já existe, tentar signInWithOtp
        if (signUpError.message.includes('already registered') || signUpError.message.includes('User already registered')) {
          console.log('✅ Usuário já existe, enviando magic link...');
          
          const { error: otpError } = await supabase.auth.signInWithOtp({
            email,
            options: {
              emailRedirectTo: getAuthCallbackUrl('/app'),
            },
          });
          
          if (otpError) {
            console.error('❌ Erro ao enviar magic link:', otpError);
            setMessage('Erro ao enviar link de login: ' + otpError.message);
          } else {
            console.log('✅ Magic link enviado com sucesso!');
            console.log('🍪 Cookies após envio:', document.cookie);
            setMessage('✅ Link de login enviado! Verifique seu email (inclua a pasta de spam). O link expira em 1 hora. IMPORTANTE: Clique no link no mesmo navegador onde solicitou.');
          }
        } else {
          setMessage('Erro ao criar conta: ' + signUpError.message);
        }
      } else {
        console.log('✅ Usuário criado/verificado com sucesso!');
        console.log('📧 Email de confirmação enviado');
        console.log('🍪 Cookies após criação:', document.cookie);
        
        if (signUpData.user) {
          setMessage('✅ Conta criada! Verifique seu email para confirmar (inclua a pasta de spam). O link expira em 1 hora. IMPORTANTE: Clique no link no mesmo navegador onde solicitou.');
        } else {
          setMessage('✅ Link de login enviado! Verifique seu email (inclua a pasta de spam). O link expira em 1 hora. IMPORTANTE: Clique no link no mesmo navegador onde solicitou.');
        }
      }
    }

    setLoading(false);
  };

  if (!mounted) {
    return null; // Evita renderização no servidor
  }

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
            disabled={loading || !mounted}
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
          
          {/* Mostrar erro da URL se houver */}
          {typeof window !== 'undefined' && window.location.search.includes('error=') && (
            <div className="mt-4 p-3 bg-red-900/20 border border-red-700 rounded-lg">
              <p className="text-sm text-red-400 font-semibold mb-1">Erro de Autenticação</p>
              <p className="text-xs text-red-300 font-mono mb-2">
                {new URLSearchParams(window.location.search).get('error')}
              </p>
              {new URLSearchParams(window.location.search).get('message') && (
                <div className="text-xs text-red-300 mt-1 mb-2 whitespace-pre-wrap">
                  {new URLSearchParams(window.location.search).get('message')}
                </div>
              )}
              {new URLSearchParams(window.location.search).get('description') && (
                <div className="text-xs text-red-300 mt-1 mb-2 whitespace-pre-wrap">
                  {new URLSearchParams(window.location.search).get('description')}
                </div>
              )}
              <p className="text-xs text-gray-400 mt-2">
                💡 Dica: Limpe os cookies do navegador e tente novamente. O erro PKCE geralmente ocorre quando o código verificador não é encontrado.
              </p>
              <button
                onClick={() => {
                  // Limpar cookies do Supabase
                  document.cookie.split(';').forEach(c => {
                    const [name] = c.trim().split('=');
                    if (name.includes('supabase') || name.includes('sb-')) {
                      document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
                    }
                  });
                  // Recarregar página
                  window.location.href = '/login';
                }}
                className="mt-2 text-xs text-blue-400 hover:text-blue-300 underline"
              >
                Limpar cookies e tentar novamente
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
