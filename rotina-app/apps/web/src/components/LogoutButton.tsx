'use client';

import { createClient } from '@/lib/supabase/client';
import { useState } from 'react';

export function LogoutButton() {
  const [loading, setLoading] = useState(false);

  const handleLogout = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (loading) return;
    
    setLoading(true);
    
    try {
      const supabase = createClient();
      
      console.log('🚪 [ROTINA APP] Iniciando logout...');
      
      // Fazer logout no Supabase
      const { error } = await supabase.auth.signOut();
      
      if (error) {
        console.error('❌ [ROTINA APP] Logout error:', error);
        // Mesmo com erro, continua com o logout local
      } else {
        console.log('✅ [ROTINA APP] Logout do Supabase realizado');
      }
      
      // Limpar qualquer estado local se necessário
      if (typeof window !== 'undefined') {
        console.log('🧹 [ROTINA APP] Limpando storage local...');
        
        // Limpar todos os itens do localStorage relacionados ao Supabase
        const keysToRemove: string[] = [];
        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i);
          if (key && (key.includes('supabase') || key.includes('sb-'))) {
            keysToRemove.push(key);
          }
        }
        keysToRemove.forEach(key => {
          localStorage.removeItem(key);
          console.log('🗑️ [ROTINA APP] Removido do localStorage:', key);
        });
        
        // Limpar sessionStorage também
        const sessionKeysToRemove: string[] = [];
        for (let i = 0; i < sessionStorage.length; i++) {
          const key = sessionStorage.key(i);
          if (key && (key.includes('supabase') || key.includes('sb-'))) {
            sessionKeysToRemove.push(key);
          }
        }
        sessionKeysToRemove.forEach(key => {
          sessionStorage.removeItem(key);
          console.log('🗑️ [ROTINA APP] Removido do sessionStorage:', key);
        });
        
        // Limpar cookies manualmente
        const cookiesToDelete = document.cookie.split(';');
        cookiesToDelete.forEach(cookie => {
          const eqPos = cookie.indexOf('=');
          const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
          
          // Remover cookies do Supabase
          if (name.includes('sb-') || name.includes('supabase') || name.includes('code-verifier') || name.includes('pkce')) {
            // Remover cookie para o domínio atual
            document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
            // Remover também para o domínio sem www
            document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=${window.location.hostname}`;
            // Remover também para o domínio com www
            if (!window.location.hostname.startsWith('www.')) {
              document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=.${window.location.hostname}`;
            }
            console.log('🗑️ [ROTINA APP] Removido cookie:', name);
          }
        });
        
        console.log('✅ [ROTINA APP] Limpeza concluída, redirecionando...');
        
        // Aguardar um pouco para garantir que tudo foi limpo
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Forçar reload completo para limpar todo o estado
        // Usar window.location.replace para evitar voltar com botão voltar
        window.location.href = '/login';
      }
    } catch (error) {
      console.error('❌ [ROTINA APP] Logout exception:', error);
      // Mesmo com erro, redireciona para login
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    // Não precisa setLoading(false) porque a página será redirecionada
  };

  return (
    <button
      onClick={handleLogout}
      disabled={loading}
      type="button"
      className="text-gray-400 hover:text-white text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {loading ? 'Saindo...' : 'Sair'}
    </button>
  );
}

