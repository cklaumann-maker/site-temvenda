import { redirect } from 'next/navigation';
import { createClient } from '@/lib/supabase/server';
import Link from 'next/link';

export default async function FoodItemsAdminPage() {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) {
    redirect('/login');
  }

  // Verificar se é root
  const { data: profile } = await supabase
    .from('user_profiles')
    .select('is_root')
    .eq('user_id', user.id)
    .single();

  if (!profile || !(profile as any).is_root) {
    redirect('/app');
  }

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <Link
            href="/app/admin/users"
            className="text-blue-400 hover:text-blue-300 mb-4 inline-block"
          >
            ← Voltar para Admin
          </Link>
        </div>

        <h1 className="text-3xl font-bold text-white mb-6">Gerenciar Alimentos</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            href="/app/admin/food-items/import"
            className="block p-6 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"
          >
            <h2 className="text-xl font-semibold text-white mb-2">Importar do Excel</h2>
            <p className="text-gray-400">
              Importe alimentos de um arquivo Excel. Duplicatas serão ignoradas automaticamente.
            </p>
          </Link>

          <Link
            href="/app/admin/food-items/list"
            className="block p-6 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"
          >
            <h2 className="text-xl font-semibold text-white mb-2">Listar Alimentos</h2>
            <p className="text-gray-400">
              Visualize e gerencie todos os alimentos cadastrados no sistema.
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
}

