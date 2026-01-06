'use client';

import { useState, useEffect, useRef } from 'react';
import { createClient } from '@/lib/supabase/client';

interface FoodItem {
  id: string;
  category: string;
  name: string;
  standard_portion: string;
  calories_kcal: number;
}

interface SelectedFoodItem extends FoodItem {
  quantity: number; // Multiplicador da porção padrão
}

interface FoodItemSelectorProps {
  mealId: string;
  initialCalories: number;
  initialDescription: string;
  onSave: (kcal: number, description: string) => void;
}

export function FoodItemSelector({
  mealId,
  initialCalories,
  initialDescription,
  onSave,
}: FoodItemSelectorProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [foodItems, setFoodItems] = useState<FoodItem[]>([]);
  const [selectedItems, setSelectedItems] = useState<SelectedFoodItem[]>([]);
  const [showSearch, setShowSearch] = useState(false);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newItem, setNewItem] = useState({
    category: '',
    name: '',
    standard_portion: '',
    calories_kcal: '',
  });
  const searchRef = useRef<HTMLInputElement>(null);

  const categories = [
    'Bebidas',
    'Carboidratos',
    'Doces/Ultraprocessados',
    'Frutas',
    'Gorduras',
    'Laticínios',
    'Proteínas',
    'Verduras/Legumes',
    'Temperos/Ingredientes',
    'Outros',
  ];

  // Carregar alimentos
  useEffect(() => {
    if (showSearch) {
      loadFoodItems();
    }
  }, [showSearch, searchTerm, selectedCategory]);

  // Parsear descrição inicial para carregar itens selecionados
  useEffect(() => {
    if (initialDescription && initialCalories > 0) {
      // Tentar parsear se a descrição contém informações dos itens
      // Por enquanto, apenas mostra as calorias
    }
  }, []);

  const loadFoodItems = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (searchTerm) {
        params.append('search', searchTerm);
      }
      if (selectedCategory) {
        params.append('category', selectedCategory);
      }

      const response = await fetch(`/api/food-items?${params.toString()}`);
      
      if (!response.ok) {
        // Se a tabela não existir, retornar array vazio mas não bloquear o componente
        if (response.status === 404 || response.status === 500) {
          console.warn('⚠️ [ROTINA APP] Tabela food_items pode não existir. Execute a migration primeiro.');
          setFoodItems([]);
          return;
        }
        throw new Error(`Erro ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setFoodItems(data.items || []);
    } catch (error) {
      console.error('❌ [ROTINA APP] Erro ao carregar alimentos:', error);
      // Não bloquear o componente mesmo se houver erro
      setFoodItems([]);
    } finally {
      setLoading(false);
    }
  };

  const addFoodItem = (item: FoodItem) => {
    const existing = selectedItems.find((si) => si.id === item.id);
    if (existing) {
      // Aumentar quantidade
      setSelectedItems(
        selectedItems.map((si) =>
          si.id === item.id ? { ...si, quantity: si.quantity + 1 } : si
        )
      );
    } else {
      // Adicionar novo item
      setSelectedItems([...selectedItems, { ...item, quantity: 1 }]);
    }
  };

  const removeFoodItem = (itemId: string) => {
    setSelectedItems(selectedItems.filter((si) => si.id !== itemId));
  };

  const updateQuantity = (itemId: string, quantity: number) => {
    if (quantity <= 0) {
      removeFoodItem(itemId);
      return;
    }
    setSelectedItems(
      selectedItems.map((si) =>
        si.id === itemId ? { ...si, quantity } : si
      )
    );
  };

  const calculateTotalCalories = () => {
    return selectedItems.reduce(
      (total, item) => total + item.calories_kcal * item.quantity,
      0
    );
  };

  const handleSave = async () => {
    const totalCalories = calculateTotalCalories();
    const description = selectedItems
      .map(
        (item) =>
          `${item.name} (${item.standard_portion}${item.quantity > 1 ? ` x${item.quantity}` : ''})`
      )
      .join(', ');

    setSaving(true);
    try {
      await onSave(totalCalories, description);
      setShowSearch(false);
    } catch (error) {
      console.error('Erro ao salvar:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleAddNewItem = async () => {
    if (!newItem.category || !newItem.name || !newItem.standard_portion || !newItem.calories_kcal) {
      alert('Preencha todos os campos');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/food-items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: newItem.category,
          name: newItem.name,
          standard_portion: newItem.standard_portion,
          calories_kcal: parseInt(newItem.calories_kcal),
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Erro ao criar alimento');
      }

      const data = await response.json();
      // Adicionar à lista e selecionar
      addFoodItem(data.item);
      setShowAddForm(false);
      setNewItem({ category: '', name: '', standard_portion: '', calories_kcal: '' });
      // Recarregar lista
      loadFoodItems();
    } catch (error: any) {
      alert(error.message || 'Erro ao criar alimento');
    } finally {
      setLoading(false);
    }
  };

  const totalCalories = calculateTotalCalories();

  if (!showSearch && initialCalories === 0) {
    return (
      <button
        onClick={() => {
          setShowSearch(true);
          setTimeout(() => searchRef.current?.focus(), 100);
        }}
        className="w-full mt-3 text-sm text-gray-400 hover:text-blue-400 transition-colors border border-dashed border-gray-600 rounded-lg p-3 hover:border-blue-500"
      >
        + Selecionar alimentos da lista
      </button>
    );
  }

  return (
    <div className="mt-3 p-4 rounded-lg border border-gray-600 bg-gray-800/50">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs text-gray-400 font-medium">Alimentos selecionados:</span>
        {totalCalories > 0 && (
          <span className="text-xs text-yellow-400 font-medium">
            {totalCalories} kcal
          </span>
        )}
      </div>

      {/* Itens selecionados */}
      {selectedItems.length > 0 && (
        <div className="mb-3 space-y-2">
          {selectedItems.map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between p-2 bg-gray-700 rounded-lg"
            >
              <div className="flex-1">
                <div className="text-sm text-white">{item.name}</div>
                <div className="text-xs text-gray-400">
                  {item.standard_portion} - {item.calories_kcal} kcal/un
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => updateQuantity(item.id, item.quantity - 1)}
                  className="w-6 h-6 flex items-center justify-center bg-gray-600 text-white rounded hover:bg-gray-500"
                >
                  -
                </button>
                <span className="text-sm text-white w-8 text-center">{item.quantity}</span>
                <button
                  onClick={() => updateQuantity(item.id, item.quantity + 1)}
                  className="w-6 h-6 flex items-center justify-center bg-gray-600 text-white rounded hover:bg-gray-500"
                >
                  +
                </button>
                <button
                  onClick={() => removeFoodItem(item.id)}
                  className="ml-2 text-red-400 hover:text-red-300 text-sm"
                >
                  ✕
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Busca de alimentos */}
      {showSearch && (
        <div className="mb-3">
          <div className="flex gap-2 mb-2">
            <input
              ref={searchRef}
              type="text"
              placeholder="Buscar alimento..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1 px-3 py-2 bg-gray-700 text-white rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-3 py-2 bg-gray-700 text-white rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todas categorias</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          {/* Lista de alimentos */}
          {loading ? (
            <div className="text-center text-gray-400 py-4">Carregando...</div>
          ) : foodItems.length > 0 ? (
            <div className="max-h-48 overflow-y-auto space-y-1">
              {foodItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => addFoodItem(item)}
                  className="w-full text-left p-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm text-white"
                >
                  <div className="font-medium">{item.name}</div>
                  <div className="text-xs text-gray-400">
                    {item.standard_portion} - {item.calories_kcal} kcal
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-400 py-4">
              Nenhum alimento encontrado
            </div>
          )}

          {/* Botão para adicionar novo alimento */}
          {!showAddForm && (
            <button
              onClick={() => setShowAddForm(true)}
              className="w-full mt-2 text-sm text-blue-400 hover:text-blue-300 border border-dashed border-blue-500 rounded-lg p-2"
            >
              + Cadastrar novo alimento
            </button>
          )}

          {/* Formulário para adicionar novo alimento */}
          {showAddForm && (
            <div className="mt-3 p-3 bg-gray-700 rounded-lg space-y-2">
              <select
                value={newItem.category}
                onChange={(e) => setNewItem({ ...newItem, category: e.target.value })}
                className="w-full px-3 py-2 bg-gray-600 text-white rounded-lg text-sm"
              >
                <option value="">Selecione a categoria</option>
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
              <input
                type="text"
                placeholder="Nome do alimento"
                value={newItem.name}
                onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
                className="w-full px-3 py-2 bg-gray-600 text-white rounded-lg text-sm"
              />
              <input
                type="text"
                placeholder="Porção padrão (ex: 100g, 200ml, 1 un)"
                value={newItem.standard_portion}
                onChange={(e) => setNewItem({ ...newItem, standard_portion: e.target.value })}
                className="w-full px-3 py-2 bg-gray-600 text-white rounded-lg text-sm"
              />
              <input
                type="number"
                placeholder="Calorias (kcal)"
                value={newItem.calories_kcal}
                onChange={(e) => setNewItem({ ...newItem, calories_kcal: e.target.value })}
                className="w-full px-3 py-2 bg-gray-600 text-white rounded-lg text-sm"
                min="0"
              />
              <div className="flex gap-2">
                <button
                  onClick={handleAddNewItem}
                  disabled={loading}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? 'Salvando...' : 'Adicionar'}
                </button>
                <button
                  onClick={() => {
                    setShowAddForm(false);
                    setNewItem({ category: '', name: '', standard_portion: '', calories_kcal: '' });
                  }}
                  className="px-4 py-2 bg-gray-600 text-white rounded-lg text-sm hover:bg-gray-500"
                >
                  Cancelar
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Botões de ação */}
      <div className="flex gap-2 mt-3">
        {selectedItems.length > 0 && (
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {saving ? 'Salvando...' : 'Salvar'}
          </button>
        )}
        {!showSearch && (
          <button
            onClick={() => setShowSearch(true)}
            className="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg text-sm font-medium hover:bg-gray-600 transition-colors"
          >
            Adicionar mais
          </button>
        )}
        {(showSearch || selectedItems.length > 0 || initialCalories > 0) && (
          <button
            onClick={() => {
              setSelectedItems([]);
              setShowSearch(false);
              onSave(0, '');
            }}
            className="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg text-sm font-medium hover:bg-gray-600 transition-colors"
          >
            Remover
          </button>
        )}
      </div>
    </div>
  );
}

