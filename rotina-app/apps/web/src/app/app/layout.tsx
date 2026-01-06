import { createClient } from '@/lib/supabase/server';
import { redirect } from 'next/navigation';
import Link from 'next/link';
import { LogoutButton } from '@/components/LogoutButton';

export default async function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) {
    redirect('/login');
  }

  // Verificar se o usuário tem perfil (não é obrigatório, mas útil para root)
  // Se não tiver perfil, criar um básico
  try {
    const { data: profile, error: profileError } = await supabase
      .from('user_profiles')
      .select('user_id')
      .eq('user_id', user.id)
      .single();

    // Se não tiver perfil e não for erro de "não encontrado", pode ser problema
    if (profileError && profileError.code !== 'PGRST116') {
      console.error('Erro ao verificar perfil:', profileError);
    }
  } catch (error) {
    // Ignorar erros de perfil - não é crítico para acesso
    console.warn('Aviso ao verificar perfil:', error);
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Navigation Bar - Fixa no topo */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-8">
              <Link href="/app" className="text-white font-bold text-lg">
                Rotina
              </Link>
              <div className="hidden md:flex space-x-4">
                <Link
                  href="/app"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Início
                </Link>
                <Link
                  href="/app/today"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Hoje
                </Link>
                <Link
                  href="/app/plan"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Plano
                </Link>
                <Link
                  href="/app/dashboard"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Dashboard
                </Link>
                <Link
                  href="/app/checkin"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Check-in
                </Link>
                <Link
                  href="/app/plan-manager"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Gerenciar Plano
                </Link>
                <Link
                  href="/app/profile"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Perfil
                </Link>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-400 text-sm">{user.email}</span>
              {/* Link para admin apenas se for root - será verificado no componente */}
              <Link
                href="/app/admin/users"
                className="text-yellow-400 hover:text-yellow-300 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Admin Usuários
              </Link>
              <Link
                href="/app/admin/food-items"
                className="text-yellow-400 hover:text-yellow-300 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Admin Alimentos
              </Link>
              <LogoutButton />
            </div>
          </div>
        </div>
      </nav>

      {/* Page Content - Com padding-top para compensar a navbar fixa */}
      <div className="pt-16">
        {children}
      </div>
    </div>
  );
}

