#!/usr/bin/env python3
"""
Sistema de Gerenciamento de Usuários - TEM VENDA
"""

import os
import json
import hashlib
import secrets
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://mgcoyeohqelystqmytah.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.8K8K8K8K8K8K8K8K8K8K8K8K8K8K8K8K8K8K8K8K8K')

# Inicializar cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def hash_password(password: str) -> str:
    """Gera hash da senha usando bcrypt"""
    import bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verifica se a senha está correta"""
    import bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_user(username: str, password: str, full_name: str, email: str, role: str = 'user', permissions: dict = None):
    """Cria um novo usuário"""
    try:
        password_hash = hash_password(password)
        
        user_data = {
            'username': username,
            'password_hash': password_hash,
            'full_name': full_name,
            'email': email,
            'role': role,
            'permissions': permissions or {},
            'is_active': True
        }
        
        result = supabase.table('admin_users').insert(user_data).execute()
        
        if result.data:
            print(f"✅ Usuário '{username}' criado com sucesso!")
            return result.data[0]
        else:
            print(f"❌ Erro ao criar usuário '{username}'")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao criar usuário '{username}': {str(e)}")
        return None

def get_user_by_username(username: str):
    """Busca usuário por username"""
    try:
        result = supabase.table('admin_users').select('*').eq('username', username).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"❌ Erro ao buscar usuário '{username}': {str(e)}")
        return None

def get_all_users():
    """Lista todos os usuários"""
    try:
        result = supabase.table('admin_users').select('*').order('created_at', desc=True).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"❌ Erro ao listar usuários: {str(e)}")
        return []

def update_user(user_id: int, **kwargs):
    """Atualiza dados do usuário"""
    try:
        # Remove campos vazios
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        
        if 'password' in update_data:
            update_data['password_hash'] = hash_password(update_data.pop('password'))
        
        result = supabase.table('admin_users').update(update_data).eq('id', user_id).execute()
        
        if result.data:
            print(f"✅ Usuário atualizado com sucesso!")
            return result.data[0]
        else:
            print(f"❌ Erro ao atualizar usuário")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao atualizar usuário: {str(e)}")
        return None

def delete_user(user_id: int):
    """Desativa usuário (soft delete)"""
    try:
        result = supabase.table('admin_users').update({'is_active': False}).eq('id', user_id).execute()
        
        if result.data:
            print(f"✅ Usuário desativado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao desativar usuário")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao desativar usuário: {str(e)}")
        return False

def authenticate_user(username: str, password: str):
    """Autentica usuário"""
    user = get_user_by_username(username)
    
    if not user:
        return None
    
    if not user.get('is_active', False):
        return None
    
    if verify_password(password, user['password_hash']):
        # Atualizar último login
        supabase.table('admin_users').update({'last_login': datetime.now().isoformat()}).eq('id', user['id']).execute()
        return user
    
    return None

def setup_initial_users():
    """Configura usuários iniciais"""
    print("🔧 Configurando usuários iniciais...")
    
    # Usuário root (César)
    cesar_user = get_user_by_username('cesar')
    if not cesar_user:
        create_user(
            username='cesar',
            password='temvenda2024',
            full_name='Cesar Klaumann',
            email='cesar@temvenda.com.br',
            role='root',
            permissions={
                'all_permissions': True,
                'manage_users': True,
                'manage_news': True,
                'manage_stats': True,
                'manage_images': True
            }
        )
    else:
        print("👤 Usuário 'cesar' já existe")
    
    # Usuário admin padrão
    admin_user = get_user_by_username('admin')
    if not admin_user:
        create_user(
            username='admin',
            password='temvenda2024',
            full_name='Administrador',
            email='admin@temvenda.com.br',
            role='admin',
            permissions={
                'manage_news': True,
                'manage_stats': True,
                'manage_images': True
            }
        )
    else:
        print("👤 Usuário 'admin' já existe")

def main():
    """Função principal"""
    print("🚀 Sistema de Gerenciamento de Usuários - TEM VENDA")
    print("=" * 50)
    
    # Configurar usuários iniciais
    setup_initial_users()
    
    # Listar usuários
    print("\n📋 Usuários cadastrados:")
    users = get_all_users()
    for user in users:
        status = "✅ Ativo" if user['is_active'] else "❌ Inativo"
        print(f"  • {user['username']} ({user['full_name']}) - {user['role']} - {status}")

if __name__ == "__main__":
    main()

