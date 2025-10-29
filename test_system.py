#!/usr/bin/env python3
"""
🧪 SISTEMA DE TESTE - TEM VENDA NEWS
Testa todas as funcionalidades do sistema de notícias
"""

import os
import sys
import requests
import json
from datetime import datetime
from supabase import create_client, Client

class NewsSystemTester:
    def __init__(self):
        self.supabase_url = "https://mgcoyeohqelystqmytah.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ"
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Registra resultado do teste"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} - {test_name}"
        if message:
            result += f": {message}"
        
        print(result)
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
    def test_database_connection(self):
        """Testa conexão com Supabase"""
        try:
            response = self.supabase.table('news_categories').select('count').execute()
            self.log_test("Conexão com Supabase", True, f"Encontradas {len(response.data)} categorias")
            return True
        except Exception as e:
            self.log_test("Conexão com Supabase", False, str(e))
            return False
    
    def test_tables_structure(self):
        """Testa estrutura das tabelas"""
        tables = [
            'news_categories',
            'news_sources', 
            'news_tags',
            'news_articles',
            'news_article_tags',
            'news_approvals',
            'news_settings'
        ]
        
        all_tables_ok = True
        
        for table in tables:
            try:
                response = self.supabase.table(table).select('*').limit(1).execute()
                self.log_test(f"Tabela {table}", True, "Estrutura OK")
            except Exception as e:
                self.log_test(f"Tabela {table}", False, str(e))
                all_tables_ok = False
        
        return all_tables_ok
    
    def test_sample_data(self):
        """Testa dados de exemplo"""
        try:
            # Testar categorias
            categories = self.supabase.table('news_categories').select('*').execute()
            if len(categories.data) > 0:
                self.log_test("Dados de Categorias", True, f"{len(categories.data)} categorias encontradas")
            else:
                self.log_test("Dados de Categorias", False, "Nenhuma categoria encontrada")
            
            # Testar fontes
            sources = self.supabase.table('news_sources').select('*').execute()
            if len(sources.data) > 0:
                self.log_test("Dados de Fontes", True, f"{len(sources.data)} fontes encontradas")
            else:
                self.log_test("Dados de Fontes", False, "Nenhuma fonte encontrada")
            
            # Testar tags
            tags = self.supabase.table('news_tags').select('*').execute()
            if len(tags.data) > 0:
                self.log_test("Dados de Tags", True, f"{len(tags.data)} tags encontradas")
            else:
                self.log_test("Dados de Tags", False, "Nenhuma tag encontrada")
                
        except Exception as e:
            self.log_test("Dados de Exemplo", False, str(e))
    
    def test_news_collector(self):
        """Testa o coletor de notícias"""
        try:
            # Verificar se o arquivo existe
            if os.path.exists('news_collector.py'):
                self.log_test("Arquivo news_collector.py", True, "Arquivo encontrado")
            else:
                self.log_test("Arquivo news_collector.py", False, "Arquivo não encontrado")
                return False
            
            # Testar importação das dependências
            try:
                import feedparser
                import requests
                from bs4 import BeautifulSoup
                self.log_test("Dependências Python", True, "Todas as dependências disponíveis")
            except ImportError as e:
                self.log_test("Dependências Python", False, f"Dependência faltando: {e}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Coletor de Notícias", False, str(e))
            return False
    
    def test_admin_panel(self):
        """Testa painel administrativo"""
        try:
            if os.path.exists('admin-panel.html'):
                self.log_test("Painel Admin HTML", True, "Arquivo encontrado")
                
                # Verificar se contém elementos essenciais
                with open('admin-panel.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                required_elements = [
                    'SUPABASE_URL',
                    'SUPABASE_KEY',
                    'loadArticles',
                    'approveArticle',
                    'rejectArticle'
                ]
                
                missing_elements = []
                for element in required_elements:
                    if element not in content:
                        missing_elements.append(element)
                
                if not missing_elements:
                    self.log_test("Painel Admin Funcional", True, "Todos os elementos essenciais presentes")
                else:
                    self.log_test("Painel Admin Funcional", False, f"Elementos faltando: {missing_elements}")
                    
            else:
                self.log_test("Painel Admin HTML", False, "Arquivo não encontrado")
                
        except Exception as e:
            self.log_test("Painel Admin", False, str(e))
    
    def test_public_news_page(self):
        """Testa página pública de notícias"""
        try:
            if os.path.exists('noticias.html'):
                self.log_test("Página Notícias HTML", True, "Arquivo encontrado")
                
                # Verificar elementos essenciais
                with open('noticias.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                required_elements = [
                    'SUPABASE_URL',
                    'SUPABASE_KEY',
                    'loadArticles',
                    'createArticleCard',
                    'pagination'
                ]
                
                missing_elements = []
                for element in required_elements:
                    if element not in content:
                        missing_elements.append(element)
                
                if not missing_elements:
                    self.log_test("Página Notícias Funcional", True, "Todos os elementos essenciais presentes")
                else:
                    self.log_test("Página Notícias Funcional", False, f"Elementos faltando: {missing_elements}")
                    
            else:
                self.log_test("Página Notícias HTML", False, "Arquivo não encontrado")
                
        except Exception as e:
            self.log_test("Página Notícias", False, str(e))
    
    def test_automation_scripts(self):
        """Testa scripts de automação"""
        try:
            # Verificar script de cron
            if os.path.exists('cron-automation.sh'):
                self.log_test("Script Cron Automation", True, "Arquivo encontrado")
                
                # Verificar se é executável
                if os.access('cron-automation.sh', os.X_OK):
                    self.log_test("Permissões Script Cron", True, "Script executável")
                else:
                    self.log_test("Permissões Script Cron", False, "Script não executável")
            else:
                self.log_test("Script Cron Automation", False, "Arquivo não encontrado")
            
            # Verificar documentação
            if os.path.exists('CRON_SETUP.md'):
                self.log_test("Documentação Cron", True, "Arquivo encontrado")
            else:
                self.log_test("Documentação Cron", False, "Arquivo não encontrado")
                
        except Exception as e:
            self.log_test("Scripts de Automação", False, str(e))
    
    def test_api_endpoints(self):
        """Testa endpoints da API"""
        try:
            # Testar endpoint de artigos
            url = f"{self.supabase_url}/rest/v1/news_articles"
            headers = {
                'apikey': self.supabase_key,
                'Authorization': f'Bearer {self.supabase_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.log_test("API Endpoint Artigos", True, f"Status {response.status_code}")
            else:
                self.log_test("API Endpoint Artigos", False, f"Status {response.status_code}")
            
            # Testar endpoint de categorias
            url = f"{self.supabase_url}/rest/v1/news_categories"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.log_test("API Endpoint Categorias", True, f"Status {response.status_code}")
            else:
                self.log_test("API Endpoint Categorias", False, f"Status {response.status_code}")
                
        except Exception as e:
            self.log_test("API Endpoints", False, str(e))
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🧪 INICIANDO TESTES DO SISTEMA TEM VENDA NEWS")
        print("=" * 60)
        
        # Testes de banco de dados
        print("\n📊 TESTES DE BANCO DE DADOS")
        print("-" * 30)
        self.test_database_connection()
        self.test_tables_structure()
        self.test_sample_data()
        
        # Testes de componentes
        print("\n🔧 TESTES DE COMPONENTES")
        print("-" * 30)
        self.test_news_collector()
        self.test_admin_panel()
        self.test_public_news_page()
        self.test_automation_scripts()
        
        # Testes de API
        print("\n🌐 TESTES DE API")
        print("-" * 30)
        self.test_api_endpoints()
        
        # Resumo
        print("\n📋 RESUMO DOS TESTES")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"✅ Testes Aprovados: {passed}")
        print(f"❌ Testes Falharam: {total - passed}")
        print(f"📊 Taxa de Sucesso: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 TODOS OS TESTES PASSARAM! Sistema pronto para uso.")
        else:
            print(f"\n⚠️ {total - passed} TESTES FALHARAM. Verifique os erros acima.")
        
        # Salvar relatório
        self.save_report()
        
        return passed == total
    
    def save_report(self):
        """Salva relatório de testes"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'total_tests': len(self.test_results),
                'passed_tests': sum(1 for r in self.test_results if r['success']),
                'failed_tests': sum(1 for r in self.test_results if not r['success']),
                'success_rate': (sum(1 for r in self.test_results if r['success']) / len(self.test_results)) * 100,
                'results': self.test_results
            }
            
            with open('test_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"\n📄 Relatório salvo em: test_report.json")
            
        except Exception as e:
            print(f"\n❌ Erro ao salvar relatório: {e}")

def main():
    """Função principal"""
    tester = NewsSystemTester()
    success = tester.run_all_tests()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
