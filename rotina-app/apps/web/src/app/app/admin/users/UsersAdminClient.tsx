'use client';

import { useState, useEffect } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';

interface User {
  id: string;
  email: string;
  email_confirmed_at: string | null;
  created_at: string;
  last_sign_in_at: string | null;
  profile: {
    name: string | null;
    is_root: boolean;
  } | null;
}

export default function UsersAdminClient() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [isRoot, setIsRoot] = useState(false);
  const [showAddUser, setShowAddUser] = useState(false);
  const [newUserEmail, setNewUserEmail] = useState('');
  const [newUserPassword, setNewUserPassword] = useState('');
  const [newUserName, setNewUserName] = useState('');
  const [addingUser, setAddingUser] = useState(false);
  const router = useRouter();

  const supabase = createClient();

  useEffect(() => {
    checkRootAccess();
    loadUsers();
  }, []);

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

      if (!profile || !profile.is_root) {
        router.push('/app');
        return;
      }

      setIsRoot(true);
    } catch (error) {
      console.error('Erro ao verificar acesso root:', error);
      router.push('/app');
    }
  };

  const loadUsers = async () => {
    try {
      setLoading(true);

      // Buscar todos os usuários do auth.users via API
      const { data: usersData, error } = await supabase
        .from('user_profiles')
        .select(`
          user_id,
          name,
          is_root,
          user:auth.users!inner(
            id,
            email,
            email_confirmed_at,
            created_at,
            last_sign_in_at
          )
        `);

      if (error) {
        console.error('Erro ao carregar usuários:', error);
        // Tentar método alternativo via função RPC ou API route
        await loadUsersAlternative();
        return;
      }

      // Transformar dados para o formato esperado
      const formattedUsers: User[] = (usersData || []).map((item: any) => ({
        id: item.user_id,
        email: item.user?.email || '',
        email_confirmed_at: item.user?.email_confirmed_at || null,
        created_at: item.user?.created_at || '',
        last_sign_in_at: item.user?.last_sign_in_at || null,
        profile: {
          name: item.name,
          is_root: item.is_root || false,
        },
      }));

      setUsers(formattedUsers);
    } catch (error) {
      console.error('Erro ao carregar usuários:', error);
      await loadUsersAlternative();
    } finally {
      setLoading(false);
    }
  };

  const loadUsersAlternative = async () => {
    try {
      const response = await fetch('/api/admin/users');
      if (response.ok) {
        const data = await response.json();
        setUsers(data.users || []);
      } else {
        const errorData = await response.json();
        console.error('Erro ao carregar usuários:', errorData.error);
        alert('Erro ao carregar usuários: ' + errorData.error);
      }
    } catch (error) {
      console.error('Erro ao carregar usuários via API:', error);
      alert('Erro ao carregar usuários. Verifique o console.');
    }
  };

  const handleAddUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUserEmail || !newUserPassword) {
      alert('Preencha email e senha');
      return;
    }

    setAddingUser(true);
    try {
      const response = await fetch('/api/admin/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: newUserEmail,
          password: newUserPassword,
          name: newUserName || newUserEmail.split('@')[0],
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert('Usuário criado com sucesso!');
        setNewUserEmail('');
        setNewUserPassword('');
        setNewUserName('');
        setShowAddUser(false);
        loadUsers();
      } else {
        alert('Erro ao criar usuário: ' + (data.error || 'Erro desconhecido'));
      }
    } catch (error) {
      console.error('Erro ao criar usuário:', error);
      alert('Erro ao criar usuário. Verifique o console.');
    } finally {
      setAddingUser(false);
    }
  };

  const handleDeleteUser = async (userId: string, email: string) => {
    if (!confirm(`Tem certeza que deseja deletar o usuário ${email}? Esta ação é irreversível!`)) {
      return;
    }

    try {
      const response = await fetch(`/api/admin/users/${userId}`, {
        method: 'DELETE',
      });

      const data = await response.json();

      if (response.ok) {
        alert('Usuário deletado com sucesso!');
        loadUsers();
      } else {
        alert('Erro ao deletar usuário: ' + (data.error || 'Erro desconhecido'));
      }
    } catch (error) {
      console.error('Erro ao deletar usuário:', error);
      alert('Erro ao deletar usuário. Verifique o console.');
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
        <div className="text-white">Carregando usuários...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-white">Administração de Usuários</h1>
          <button
            onClick={() => setShowAddUser(!showAddUser)}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            {showAddUser ? 'Cancelar' : '+ Adicionar Usuário'}
          </button>
        </div>

        {showAddUser && (
          <div className="bg-gray-800 rounded-lg p-6 mb-6">
            <h2 className="text-xl font-bold text-white mb-4">Adicionar Novo Usuário</h2>
            <form onSubmit={handleAddUser} className="space-y-4">
              <div>
                <label className="block text-gray-300 mb-2">Email *</label>
                <input
                  type="email"
                  value={newUserEmail}
                  onChange={(e) => setNewUserEmail(e.target.value)}
                  className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-300 mb-2">Senha *</label>
                <input
                  type="password"
                  value={newUserPassword}
                  onChange={(e) => setNewUserPassword(e.target.value)}
                  className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg"
                  required
                  minLength={6}
                />
              </div>
              <div>
                <label className="block text-gray-300 mb-2">Nome (opcional)</label>
                <input
                  type="text"
                  value={newUserName}
                  onChange={(e) => setNewUserName(e.target.value)}
                  className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg"
                />
              </div>
              <button
                type="submit"
                disabled={addingUser}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors disabled:opacity-50"
              >
                {addingUser ? 'Criando...' : 'Criar Usuário'}
              </button>
            </form>
          </div>
        )}

        <div className="bg-gray-800 rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Nome
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Criado em
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="bg-gray-800 divide-y divide-gray-700">
                {users.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-4 text-center text-gray-400">
                      Nenhum usuário encontrado
                    </td>
                  </tr>
                ) : (
                  users.map((user) => (
                    <tr key={user.id} className="hover:bg-gray-700">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-white">{user.email}</div>
                        {user.profile?.is_root && (
                          <div className="text-xs text-yellow-400">ROOT</div>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {user.profile?.name || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {user.email_confirmed_at ? (
                          <span className="px-2 py-1 text-xs rounded-full bg-green-900 text-green-300">
                            Confirmado
                          </span>
                        ) : (
                          <span className="px-2 py-1 text-xs rounded-full bg-yellow-900 text-yellow-300">
                            Não Confirmado
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {new Date(user.created_at).toLocaleDateString('pt-BR')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {!user.profile?.is_root && (
                          <button
                            onClick={() => handleDeleteUser(user.id, user.email)}
                            className="text-red-400 hover:text-red-300 transition-colors"
                          >
                            Deletar
                          </button>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

