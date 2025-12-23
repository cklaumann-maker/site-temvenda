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
      
      // Fazer logout
      const { error } = await supabase.auth.signOut();
      
      if (error) {
        console.error('Logout error:', error);
        // Mesmo com erro, continua com o logout
      }
      
      // Limpar qualquer estado local se necessário
      if (typeof window !== 'undefined') {
        // Limpar todos os itens do localStorage relacionados ao Supabase
        const keysToRemove: string[] = [];
        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i);
          if (key && (key.includes('supabase') || key.includes('sb-'))) {
            keysToRemove.push(key);
          }
        }
        keysToRemove.forEach(key => localStorage.removeItem(key));
        
        // Limpar sessionStorage também
        const sessionKeysToRemove: string[] = [];
        for (let i = 0; i < sessionStorage.length; i++) {
          const key = sessionStorage.key(i);
          if (key && (key.includes('supabase') || key.includes('sb-'))) {
            sessionKeysToRemove.push(key);
          }
        }
        sessionKeysToRemove.forEach(key => sessionStorage.removeItem(key));
        
        // Forçar reload completo para limpar todo o estado
        // Usar window.location.replace para evitar voltar com botão voltar
        window.location.replace('/login');
      }
    } catch (error) {
      console.error('Logout exception:', error);
      // Mesmo com erro, redireciona para login
      if (typeof window !== 'undefined') {
        window.location.replace('/login');
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

