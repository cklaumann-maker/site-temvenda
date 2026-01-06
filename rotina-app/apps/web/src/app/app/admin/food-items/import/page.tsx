'use client';

import { useState } from 'react';
import { createClient } from '@/lib/supabase/client';
// @ts-ignore - xlsx não tem tipos completos
import * as XLSX from 'xlsx';

interface FoodItemRow {
  categoria?: string;
  alimento?: string;
  porcao_padrao?: string;
  calorias?: number | string;
}

export default function ImportFoodItemsPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<{
    total: number;
    inserted: number;
    skipped: number;
    errors: string[];
  } | null>(null);
  const [preview, setPreview] = useState<FoodItemRow[]>([]);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setResults(null);
    setPreview([]);

    // Ler e fazer preview do arquivo
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const data = new Uint8Array(event.target?.result as ArrayBuffer);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData: FoodItemRow[] = XLSX.utils.sheet_to_json(firstSheet);

        // Normalizar nomes das colunas (case insensitive)
        const normalized = jsonData.map((row: any) => {
          const normalizedRow: FoodItemRow = {};
          Object.keys(row).forEach((key) => {
            const lowerKey = key.toLowerCase().trim();
            if (lowerKey.includes('categoria') || lowerKey.includes('category')) {
              normalizedRow.categoria = String(row[key] || '').trim();
            } else if (lowerKey.includes('alimento') || lowerKey.includes('name') || lowerKey.includes('nome')) {
              normalizedRow.alimento = String(row[key] || '').trim();
            } else if (lowerKey.includes('porção') || lowerKey.includes('porcao') || lowerKey.includes('portion')) {
              normalizedRow.porcao_padrao = String(row[key] || '').trim();
            } else if (lowerKey.includes('caloria') || lowerKey.includes('calorie') || lowerKey.includes('kcal')) {
              const value = row[key];
              normalizedRow.calorias = typeof value === 'number' ? value : parseInt(String(value || '0')) || 0;
            }
          });
          return normalizedRow;
        });

        setPreview(normalized.slice(0, 10)); // Preview das primeiras 10 linhas
      } catch (error) {
        console.error('Erro ao ler arquivo:', error);
        alert('Erro ao ler arquivo Excel. Verifique o formato.');
      }
    };
    reader.readAsArrayBuffer(selectedFile);
  };

  const handleImport = async () => {
    if (!file) {
      alert('Selecione um arquivo primeiro');
      return;
    }

    setLoading(true);
    setResults(null);

    try {
      const reader = new FileReader();
      reader.onload = async (event) => {
        try {
          const data = new Uint8Array(event.target?.result as ArrayBuffer);
          const workbook = XLSX.read(data, { type: 'array' });
          const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
          const jsonData: any[] = XLSX.utils.sheet_to_json(firstSheet);

          // Normalizar dados
          const items: Array<{
            category: string;
            name: string;
            standard_portion: string;
            calories_kcal: number;
          }> = [];

          const errors: string[] = [];

          jsonData.forEach((row: any, index: number) => {
            try {
              // Normalizar nomes das colunas
              let categoria = '';
              let alimento = '';
              let porcao = '';
              let calorias = 0;

              Object.keys(row).forEach((key) => {
                const lowerKey = key.toLowerCase().trim();
                const value = String(row[key] || '').trim();

                if (lowerKey.includes('categoria') || lowerKey.includes('category')) {
                  categoria = value;
                } else if (lowerKey.includes('alimento') || lowerKey.includes('name') || lowerKey.includes('nome')) {
                  alimento = value;
                } else if (lowerKey.includes('porção') || lowerKey.includes('porcao') || lowerKey.includes('portion')) {
                  porcao = value;
                } else if (lowerKey.includes('caloria') || lowerKey.includes('calorie') || lowerKey.includes('kcal')) {
                  calorias = typeof row[key] === 'number' ? row[key] : parseInt(value) || 0;
                }
              });

              // Validar campos obrigatórios
              if (!categoria || !alimento || !porcao) {
                errors.push(`Linha ${index + 2}: Campos obrigatórios faltando (Categoria, Alimento, Porção)`);
                return;
              }

              if (calorias < 0) {
                errors.push(`Linha ${index + 2}: Calorias inválidas`);
                return;
              }

              items.push({
                category: categoria,
                name: alimento,
                standard_portion: porcao,
                calories_kcal: calorias,
              });
            } catch (error: any) {
              errors.push(`Linha ${index + 2}: ${error.message}`);
            }
          });

          if (items.length === 0) {
            alert('Nenhum item válido encontrado no arquivo');
            setLoading(false);
            return;
          }

          // Verificar duplicatas e inserir apenas novos
          const supabase = createClient();
          const { data: { user } } = await supabase.auth.getUser();
          if (!user) {
            alert('Usuário não autenticado');
            setLoading(false);
            return;
          }

          // Buscar todos os alimentos existentes
          const { data: existingItems, error: fetchError } = await supabase
            .from('food_items')
            .select('name, standard_portion');

          if (fetchError) {
            throw new Error('Erro ao buscar alimentos existentes: ' + fetchError.message);
          }

          // Criar conjunto de chaves únicas (name + standard_portion)
          const existingKeys = new Set(
            ((existingItems as any[]) || []).map((item: any) =>
              `${item.name.toLowerCase().trim()}_${item.standard_portion.toLowerCase().trim()}`
            )
          );

          // Filtrar apenas itens novos
          const newItems = items.filter((item) => {
            const key = `${item.name.toLowerCase().trim()}_${item.standard_portion.toLowerCase().trim()}`;
            return !existingKeys.has(key);
          });

          // Inserir novos itens em lotes
          let inserted = 0;
          const batchSize = 50;

          for (let i = 0; i < newItems.length; i += batchSize) {
            const batch = newItems.slice(i, i + batchSize).map((item) => ({
              ...item,
              created_by: user.id,
            }));

            const { error: insertError } = await supabase
              .from('food_items')
              .insert(batch as any);

            if (insertError) {
              errors.push(`Erro ao inserir lote ${Math.floor(i / batchSize) + 1}: ${insertError.message}`);
            } else {
              inserted += batch.length;
            }
          }

          setResults({
            total: items.length,
            inserted,
            skipped: items.length - inserted,
            errors: errors.slice(0, 20), // Limitar a 20 erros
          });
        } catch (error: any) {
          console.error('Erro ao processar arquivo:', error);
          alert('Erro ao processar arquivo: ' + error.message);
        } finally {
          setLoading(false);
        }
      };
      reader.readAsArrayBuffer(file);
    } catch (error: any) {
      console.error('Erro ao ler arquivo:', error);
      alert('Erro ao ler arquivo: ' + error.message);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-6">Importar Alimentos do Excel</h1>

        <div className="bg-gray-800 rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold text-white mb-4">Instruções</h2>
          <ul className="text-gray-300 space-y-2 list-disc list-inside">
            <li>O arquivo Excel deve ter as colunas: <strong>Categoria</strong>, <strong>Alimento</strong>, <strong>Porção Padrão</strong>, <strong>Calorias</strong></li>
            <li>Os nomes das colunas podem variar (ex: "Categoria" ou "Category")</li>
            <li>Apenas itens novos serão importados (duplicatas serão ignoradas)</li>
            <li>Duplicatas são identificadas pela combinação de Nome + Porção Padrão</li>
          </ul>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 mb-6">
          <label className="block text-white font-medium mb-2">
            Selecione o arquivo Excel (.xlsx, .xls)
          </label>
          <input
            type="file"
            accept=".xlsx,.xls"
            onChange={handleFileChange}
            className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
        </div>

        {preview.length > 0 && (
          <div className="bg-gray-800 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-white mb-4">Preview (primeiras 10 linhas)</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left text-gray-300">
                <thead className="text-xs uppercase bg-gray-700 text-gray-300">
                  <tr>
                    <th className="px-4 py-3">Categoria</th>
                    <th className="px-4 py-3">Alimento</th>
                    <th className="px-4 py-3">Porção</th>
                    <th className="px-4 py-3">Calorias</th>
                  </tr>
                </thead>
                <tbody>
                  {preview.map((row, index) => (
                    <tr key={index} className="border-b border-gray-700">
                      <td className="px-4 py-3">{row.categoria || '-'}</td>
                      <td className="px-4 py-3">{row.alimento || '-'}</td>
                      <td className="px-4 py-3">{row.porcao_padrao || '-'}</td>
                      <td className="px-4 py-3">{row.calorias || '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {file && (
          <div className="bg-gray-800 rounded-lg p-6 mb-6">
            <button
              onClick={handleImport}
              disabled={loading}
              className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Importando...' : 'Importar Alimentos'}
            </button>
          </div>
        )}

        {results && (
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Resultado da Importação</h3>
            <div className="space-y-2 text-gray-300">
              <p><strong>Total de itens no arquivo:</strong> {results.total}</p>
              <p className="text-green-400"><strong>Itens inseridos:</strong> {results.inserted}</p>
              <p className="text-yellow-400"><strong>Itens ignorados (duplicatas):</strong> {results.skipped}</p>
              {results.errors.length > 0 && (
                <div className="mt-4">
                  <p className="text-red-400 font-medium mb-2">Erros encontrados:</p>
                  <ul className="list-disc list-inside text-sm text-red-300 space-y-1">
                    {results.errors.map((error, index) => (
                      <li key={index}>{error}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

