#!/usr/bin/env python3
"""
Script alternativo para criar usuários no Supabase
Usa uma abordagem diferente para contornar limitações da API
"""

import requests
import json
import hashlib
import secrets

# Configurações do Supabase
SUPABASE_URL = "https://mgcoyeohqelystqmytah.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2NzAzNjQsImV4cCI6MjA3NzI0NjM2NH0.KBKHH10DaV0m5SroFmXsTedS_dalcAprKnUOI4Unkx4"

def hash_password(password: str) -> str:
    """Gera hash simples da senha (para teste)"""
    # Em produção, use bcrypt
    return hashlib.sha256(password.encode()).hexdigest()

def test_connection():
    """Testa a conexão com o Supabase"""
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Tentar acessar uma tabela existente para testar a conexão
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/news_articles?limit=1",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Conexão com Supabase funcionando!")
            return True
        else:
            print(f"❌ Erro na conexão: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False

def create_user_via_api():
    """Tenta criar usuário via API (assumindo que a tabela já existe)"""
    
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Usuário César
    cesar_user = {
        'username': 'cesar',
        'password_hash': hash_password('temvenda2024'),
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
    
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/admin_users",
            headers=headers,
            json=cesar_user
        )
        
        if response.status_code == 201:
            print("✅ Usuário 'cesar' criado com sucesso!")
            return True
        elif response.status_code == 409:
            print("ℹ️ Usuário 'cesar' já existe")
            return True
        else:
            print(f"❌ Erro ao criar usuário 'cesar': {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao criar usuário 'cesar': {str(e)}")
        return False

def main():
    print("🚀 Testando sistema de usuários no Supabase...")
    print("=" * 50)
    
    # Testar conexão
    if test_connection():
        # Tentar criar usuário
        create_user_via_api()
    
    print("\n📋 INSTRUÇÕES:")
    print("1. Acesse o painel do Supabase: https://supabase.com/dashboard")
    print("2. Vá para o projeto: mgcoyeohqelystqmytah")
    print("3. Acesse SQL Editor")
    print("4. Execute o arquivo: create_users_table.sql")
    print("5. Após executar o SQL, teste o login em: http://localhost:8080/login-admin")
    
    print("\n🔑 CREDENCIAIS DE TESTE:")
    print("Username: cesar")
    print("Senha: temvenda2024")

if __name__ == "__main__":
    main()
