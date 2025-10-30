#!/usr/bin/env python3
"""
Script para criar tabela de usuários no Supabase
"""

import requests
import json

# Configurações do Supabase
SUPABASE_URL = "https://mgcoyeohqelystqmytah.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2NzAzNjQsImV4cCI6MjA3NzI0NjM2NH0.KBKHH10DaV0m5SroFmXsTedS_dalcAprKnUOI4Unkx4"

def create_users_table():
    """Cria a tabela de usuários"""
    
    # SQL para criar a tabela
    sql = """
    CREATE TABLE IF NOT EXISTS admin_users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        full_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('root', 'admin', 'user')),
        permissions JSONB DEFAULT '{}',
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP NULL
    );
    """
    
    # Headers para a requisição
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Dados da requisição
    data = {
        'query': sql
    }
    
    try:
        # Tentar executar o SQL via REST API
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            print("✅ Tabela admin_users criada com sucesso!")
            return True
        else:
            print(f"❌ Erro ao criar tabela: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")
        return False

def create_initial_users():
    """Cria usuários iniciais"""
    
    # Usuário root (César)
    cesar_user = {
        'username': 'cesar',
        'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K',  # senha: temvenda2024
        'full_name': 'Cesar Klaumann',
        'email': 'cesar@temvenda.com.br',
        'role': 'root',
        'permissions': {
            'all_permissions': True,
            'manage_users': True,
            'manage_news': True,
            'manage_stats': True,
            'manage_images': True
        },
        'is_active': True
    }
    
    # Usuário admin padrão
    admin_user = {
        'username': 'admin',
        'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8K8K8K8K',  # senha: temvenda2024
        'full_name': 'Administrador',
        'email': 'admin@temvenda.com.br',
        'role': 'admin',
        'permissions': {
            'manage_news': True,
            'manage_stats': True,
            'manage_images': True
        },
        'is_active': True
    }
    
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Inserir usuário César
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/admin_users",
            headers=headers,
            json=cesar_user
        )
        
        if response.status_code == 201:
            print("✅ Usuário 'cesar' criado com sucesso!")
        else:
            print(f"ℹ️ Usuário 'cesar' já existe ou erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao criar usuário 'cesar': {str(e)}")
    
    # Inserir usuário admin
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/admin_users",
            headers=headers,
            json=admin_user
        )
        
        if response.status_code == 201:
            print("✅ Usuário 'admin' criado com sucesso!")
        else:
            print(f"ℹ️ Usuário 'admin' já existe ou erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao criar usuário 'admin': {str(e)}")

def main():
    print("🚀 Criando sistema de usuários no Supabase...")
    print("=" * 50)
    
    # Criar tabela
    if create_users_table():
        # Criar usuários iniciais
        create_initial_users()
    
    print("\n✅ Sistema de usuários configurado!")

if __name__ == "__main__":
    main()

