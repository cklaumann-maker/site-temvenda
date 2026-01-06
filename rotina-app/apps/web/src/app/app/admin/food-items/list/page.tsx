'use client';

import { useState, useEffect } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

interface FoodItem {
  id: string;
  category: string;
  name: string;
  standard_portion: string;
  calories_kcal: number;
  created_at: string;
}

export default function FoodItemsListPage() {
  const [foodItems, setFoodItems] = useState<FoodItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [isRoot, setIsRoot] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const router = useRouter();
  const supabase = createClient();

  const categories = [
    'Bebidas',
    'Carboidratos',
    'Doces/Ultraprocessados',
    'Frutas',
    'Gorduras',
    'Legumes/Verduras',
    'Laticínios',
    'Ovos',
    'Proteínas',
    'Sementes/Oleaginosas',
    'Suplementos',
    'Outros',
  ];

  useEffect(() => {
    checkRootAccess();
    loadFoodItems();
  }, []);

  useEffect(() => {
    if (isRoot) {
      loadFoodItems();
    }
  }, [searchTerm, selectedCategory, isRoot]);

  const checkRootAccess = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        router.push('/login');
        return;
      }

      const { data: profile } = await supabase
        .from('user_profiles')
        .select('is_root')
        .eq('user_id', user.id)
        .single();

      if (profile && (profile as any).is_root) {
        setIsRoot(true);
      } else {
        router.push('/app');
      }
    } catch (error) {
      console.error('Erro ao verificar acesso root:', error);
      router.push('/app');
    }
  };

  const loadFoodItems = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (searchTerm) {
        params.append('search', searchTerm);
      }
      if (selectedCategory) {
        params.append('category', selectedCategory);
      }

      const response = await fetch(`/api/food-items?${params.toString()}`);
      if (!response.ok) {
        throw new Error('Erro ao carregar alimentos');
      }

      const data = await response.json();
      setFoodItems(data.items || []);
    } catch (error) {
      console.error('Erro ao carregar alimentos:', error);
      alert('Erro ao carregar alimentos. Verifique o console.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string, name: string) => {
    if (!confirm(`Tem certeza que deseja deletar "${name}"? Esta ação é irreversível!`)) {
      return;
    }

    setDeletingId(id);
    try {
      const { error } = await supabase
        .from('food_items')
        .delete()
        .eq('id', id);

      if (error) {
        throw error;
      }

      alert('Alimento deletado com sucesso!');
      loadFoodItems();
    } catch (error: any) {
      console.error('Erro ao deletar alimento:', error);
      alert('Erro ao deletar alimento: ' + (error.message || 'Erro desconhecido'));
    } finally {
      setDeletingId(null);
    }
  };

  if (!isRoot) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-white">Verificando acesso...</div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-white">Carregando alimentos...</div>
      </div>
    );
  }

  const filteredItems = foodItems.filter((item) => {
    const matchesSearch = !searchTerm || 
      item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.category.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !selectedCategory || item.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <Link
            href="/app/admin/food-items"
            className="text-blue-400 hover:text-blue-300 mb-4 inline-block"
          >
            ← Voltar para Gerenciar Alimentos
          </Link>
        </div>

        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-white">Lista de Alimentos</h1>
          <div className="text-gray-400">
            Total: {filteredItems.length} alimento{filteredItems.length !== 1 ? 's' : ''}
          </div>
        </div>

        {/* Filtros */}
        <div className="bg-gray-800 rounded-lg p-4 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-300 mb-2 text-sm">Buscar</label>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Buscar por nome ou categoria..."
                className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-gray-300 mb-2 text-sm">Categoria</label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Todas as Categorias</option>
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Lista de Alimentos */}
        <div className="bg-gray-800 rounded-lg overflow-hidden">
          {filteredItems.length === 0 ? (
            <div className="p-8 text-center text-gray-400">
              {searchTerm || selectedCategory
                ? 'Nenhum alimento encontrado com os filtros aplicados.'
                : 'Nenhum alimento cadastrado ainda.'}
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      Nome
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      Categoria
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      Porção Padrão
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      Calorias (kcal)
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                      Ações
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-gray-800 divide-y divide-gray-700">
                  {filteredItems.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-700">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-white">{item.name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 text-xs rounded-full bg-blue-900 text-blue-300">
                          {item.category}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {item.standard_portion}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-yellow-400 font-medium">
                        {item.calories_kcal} kcal
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <button
                          onClick={() => handleDelete(item.id, item.name)}
                          disabled={deletingId === item.id}
                          className="text-red-400 hover:text-red-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          {deletingId === item.id ? 'Deletando...' : 'Deletar'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

