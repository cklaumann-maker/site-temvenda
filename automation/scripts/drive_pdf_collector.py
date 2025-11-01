#!/usr/bin/env python3
"""
📚 COLETOR DE ARTIGOS DE PDFs DO GOOGLE DRIVE - TEM VENDA
Lê PDFs do Google Drive e cria notícias automaticamente
"""

import os
import json
import re
import logging
from datetime import datetime
from supabase import create_client, Client
from openai import OpenAI
import hashlib

# Importações para Google Drive
try:
    from google.oauth2.credentials import Credentials
    from google.oauth2 import service_account
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    from googleapiclient.errors import HttpError
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False
    Request = None
    print("⚠️ Google Drive API não disponível. Instale: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")

# Importações para PDF
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    try:
        import pdfplumber
        PDF_AVAILABLE = True
    except ImportError:
        PDF_AVAILABLE = False
        print("⚠️ Biblioteca de PDF não disponível. Instale: pip install PyPDF2 ou pip install pdfplumber")

# Carregar variáveis de ambiente
def load_env_file():
    """Carrega variáveis de ambiente de um arquivo .env"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env_file()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('drive_pdf_collector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DrivePDFCollector:
    def __init__(self):
        # Configurações Supabase
        self.supabase_url = "https://mgcoyeohqelystqmytah.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ"
        
        # Configurações OpenAI
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        # Inicializar clientes
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.openai = OpenAI(api_key=self.openai_key) if self.openai_key else None
        
        # Configurações Google Drive
        self.drive_service = None
        self.google_drive_folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID', '')
        self.google_credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
        self.google_token_path = os.getenv('GOOGLE_TOKEN_PATH', 'token.json')
        
        # SCOPES necessários para Google Drive
        self.SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        
        logger.info("🚀 DrivePDFCollector inicializado!")

    def authenticate_google_drive(self):
        """Autentica no Google Drive usando OAuth2"""
        try:
            creds = None
            
            # Tentar carregar token salvo
            if os.path.exists(self.google_token_path):
                creds = Credentials.from_authorized_user_file(self.google_token_path, self.SCOPES)
            
            # Se não há credenciais válidas, fazer login
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token and Request:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.google_credentials_path):
                        logger.error(f"❌ Arquivo de credenciais não encontrado: {self.google_credentials_path}")
                        logger.error("📝 Crie um projeto no Google Cloud Console e baixe as credenciais OAuth2")
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.google_credentials_path, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Salvar credenciais para próxima execução
                with open(self.google_token_path, 'w') as token:
                    token.write(creds.to_json())
            
            # Criar serviço do Drive
            self.drive_service = build('drive', 'v3', credentials=creds)
            logger.info("✅ Autenticado no Google Drive com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro na autenticação Google Drive: {e}")
            return False

    def authenticate_google_drive_service_account(self):
        """Autentica usando Service Account (melhor para automação)"""
        try:
            service_account_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH', 'service_account.json')
            
            if not os.path.exists(service_account_path):
                logger.error(f"❌ Arquivo de Service Account não encontrado: {service_account_path}")
                logger.error("📝 Configure GOOGLE_SERVICE_ACCOUNT_PATH no .env com o caminho do arquivo JSON")
                return False
            
            creds = service_account.Credentials.from_service_account_file(
                service_account_path, scopes=self.SCOPES)
            
            self.drive_service = build('drive', 'v3', credentials=creds)
            logger.info("✅ Autenticado no Google Drive via Service Account!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro na autenticação Service Account: {e}")
            return False

    def list_pdf_files(self, folder_id=None):
        """Lista todos os arquivos PDF no Google Drive"""
        if not self.drive_service:
            logger.error("❌ Serviço do Drive não inicializado. Autentique primeiro.")
            return []
        
        try:
            folder_id = folder_id or self.google_drive_folder_id
            
            query = "mimeType='application/pdf' and trashed=false"
            if folder_id:
                query += f" and '{folder_id}' in parents"
            
            results = self.drive_service.files().list(
                q=query,
                pageSize=50,
                fields="files(id, name, modifiedTime, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            logger.info(f"📁 Encontrados {len(files)} arquivos PDF")
            
            return files
            
        except HttpError as e:
            logger.error(f"❌ Erro ao listar arquivos: {e}")
            return []

    def download_pdf(self, file_id, output_path):
        """Baixa um PDF do Google Drive"""
        try:
            request = self.drive_service.files().get_media(fileId=file_id)
            
            with open(output_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    logger.debug(f"   Baixando: {int(status.progress() * 100)}%")
            
            logger.info(f"✅ PDF baixado: {output_path}")
            return True
            
        except HttpError as e:
            logger.error(f"❌ Erro ao baixar PDF: {e}")
            return False

    def extract_text_from_pdf(self, pdf_path):
        """Extrai texto de um arquivo PDF"""
        text = ""
        
        try:
            # Tentar com PyPDF2 primeiro
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                logger.debug(f"✅ Texto extraído com PyPDF2: {len(text)} caracteres")
                return text
            except Exception:
                pass
            
            # Tentar com pdfplumber
            try:
                import pdfplumber
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
                logger.debug(f"✅ Texto extraído com pdfplumber: {len(text)} caracteres")
                return text
            except Exception:
                pass
            
            logger.warning(f"⚠️ Não foi possível extrair texto do PDF: {pdf_path}")
            return ""
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair texto do PDF: {e}")
            return ""

    def create_article_from_pdf(self, pdf_text, pdf_name, pdf_id, pdf_url):
        """Cria um artigo de notícia a partir do texto do PDF"""
        if not pdf_text or len(pdf_text.strip()) < 200:
            logger.warning(f"⚠️ Texto do PDF muito curto ou vazio: {pdf_name}")
            return None
        
        # Limitar tamanho do texto para análise (economizar tokens)
        text_for_analysis = pdf_text[:5000] if len(pdf_text) > 5000 else pdf_text
        
        # Analisar com IA para criar artigo
        article = self.analyze_pdf_with_ai(text_for_analysis, pdf_name)
        
        if not article:
            return None
        
        # Preparar dados do artigo
        article_data = {
            'title': article.get('title', pdf_name.replace('.pdf', '')),
            'excerpt': article.get('summary', text_for_analysis[:200] + '...'),
            'content': pdf_text[:10000],  # Limitar conteúdo completo
            'url': pdf_url or f"https://drive.google.com/file/d/{pdf_id}",
            'source_id': self.get_or_create_pdf_source(),
            'status': 'pending',
            'priority': article.get('priority', 1),
            'published_at': datetime.now().isoformat(),
            'scraped_at': datetime.now().isoformat()
        }
        
        # Buscar categoria
        category = self.supabase.table('news_categories').select('id').eq('slug', article.get('category', 'gestao')).execute()
        article_data['category_id'] = category.data[0]['id'] if category.data else None
        
        # Adicionar análise comercial
        if 'commercial_analysis' in article:
            article_data['commercial_analysis'] = json.dumps(article['commercial_analysis'])
        
        if 'executive_summary' in article:
            article_data['executive_summary'] = article['executive_summary']
        
        return article_data

    def analyze_pdf_with_ai(self, pdf_text, pdf_name):
        """Usa IA para analisar PDF e criar artigo estruturado"""
        if not self.openai:
            logger.warning("⚠️ OpenAI não configurada, usando análise básica")
            return self.basic_pdf_analysis(pdf_text, pdf_name)
        
        try:
            prompt = f"""
            Você é um consultor prático de gestão comercial farmacêutica. Analise este artigo de vendas/gestão em PDF e extraia INSIGHTS PRÁTICOS E ACIONÁVEIS que podem ser aplicados IMEDIATAMENTE.
            
            Nome do arquivo: {pdf_name}
            Conteúdo (primeiros 5000 caracteres): {pdf_text[:5000]}
            
            FOCO: Transforme o conteúdo do PDF em AÇÕES CONCRETAS que um gestor de farmácia pode executar HOJE. Seja ESPECÍFICO e PRÁTICO.
            
            Responda APENAS em JSON com a seguinte estrutura:
            {{
                "title": "Título atrativo focado no insight principal (máximo 80 caracteres)",
                "summary": "Resumo executivo em 2-3 frases destacando o principal insight prático",
                "category": "gestao|mercado|tecnologia|regulamentacao",
                "tags": ["tag1", "tag2", "tag3"],
                "priority": 0|1|2,
                "relevance_score": 1-10,
                "commercial_analysis": {{
                    "business_impact": "alta/média/baixa",
                    "sales_opportunities": "Oportunidades ESPECÍFICAS de vendas extraídas do artigo (ex: 'Focar em produto X que está em alta, aumentar mix em 15%')",
                    "competitive_advantage": "Como usar isso para vantagem competitiva de forma CONCRETA (ex: 'Implementar estratégia Y diferenciada que concorrentes ainda não usam')",
                    "action_items": "AÇÕES IMEDIATAS em 3-5 itens numerados e ESPECÍFICOS extraídas do artigo (formato: '1. [Ação específica] até [data/prazo]. 2. [Ação específica] com [recurso]. 3. ...')",
                    "immediate_insights": "3 insights práticos e acionáveis do artigo que podem ser aplicados AGORA (lista numerada com ações concretas do PDF)",
                    "quick_wins": "2-3 ações rápidas (< 1 hora) do artigo que geram resultado imediato",
                    "practical_tips": "Dicas práticas específicas do artigo que podem ser implementadas hoje",
                    "risk_factors": "Riscos identificados no artigo e ações práticas de mitigação",
                    "market_trends": "Tendências do artigo e como capitalizar AGORA com ações concretas"
                }},
                "executive_summary": "Resumo executivo focando em 'O QUE FAZER AGORA' baseado no artigo em 1 parágrafo"
            }}
            
            IMPORTANTE: 
            - Extraia ações ESPECÍFICAS do conteúdo do PDF, não genérico
            - action_items deve ter passos CONCRETOS e EXECUTÁVEIS extraídos do artigo
            - immediate_insights devem ser aplicáveis HOJE baseados no que está no PDF
            - quick_wins devem ser ações RÁPIDAS (< 1h) com resultado IMEDIATO do artigo
            - Seja ESPECÍFICO: evite genérico, use dados e ações concretas do PDF
            """
            
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,  # Aumentado para insights mais detalhados
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na análise IA: {e}")
            return self.basic_pdf_analysis(pdf_text, pdf_name)

    def basic_pdf_analysis(self, pdf_text, pdf_name):
        """Análise básica sem IA"""
        text_lower = pdf_text.lower()
        
        # Extrair título das primeiras linhas ou nome do arquivo
        first_lines = pdf_text.split('\n')[:3]
        title = ' '.join([line.strip() for line in first_lines if line.strip()])[:80]
        if not title:
            title = pdf_name.replace('.pdf', '').replace('_', ' ').title()
        
        # Categorização básica
        if any(word in text_lower for word in ['venda', 'vendas', 'comercial', 'faturamento']):
            category = 'mercado'
        elif any(word in text_lower for word in ['gestão', 'gestao', 'liderança', 'equipe']):
            category = 'gestao'
        elif any(word in text_lower for word in ['tecnologia', 'digital', 'app', 'sistema']):
            category = 'tecnologia'
        else:
            category = 'gestao'
        
        # Resumo básico
        summary = pdf_text[:300].replace('\n', ' ').strip() + '...'
        
        return {
            'title': title,
            'summary': summary,
            'category': category,
            'tags': ['artigo-pdf', 'gestao-comercial'],
            'priority': 1,
            'relevance_score': 7,
            'commercial_analysis': {
                'business_impact': 'média',
                'sales_opportunities': 'Extraia oportunidades específicas do conteúdo do PDF',
                'competitive_advantage': 'Implemente estratégias práticas do artigo para se destacar',
                'action_items': '1. Revisar estratégias específicas do PDF\n2. Implementar ações práticas mencionadas\n3. Aplicar técnicas apresentadas no artigo',
                'immediate_insights': '1. Extrair insights práticos do PDF\n2. Identificar ações aplicáveis hoje\n3. Compartilhar com equipe',
                'quick_wins': '1. Ler estratégias rápidas do PDF (15 min)\n2. Implementar primeira ação prática (30 min)',
                'practical_tips': 'Aplique dicas específicas do artigo no seu dia a dia',
                'risk_factors': 'Avalie riscos mencionados no PDF e ações de mitigação',
                'market_trends': 'Identifique tendências do artigo e capitalize com ações práticas'
            },
            'executive_summary': summary
        }

    def get_or_create_pdf_source(self):
        """Obtém ou cria fonte 'Google Drive PDFs'"""
        try:
            # Buscar fonte existente
            result = self.supabase.table('news_sources').select('id').eq('name', 'Google Drive - Artigos PDF').execute()
            
            if result.data:
                return result.data[0]['id']
            
            # Criar nova fonte
            new_source = self.supabase.table('news_sources').insert({
                'name': 'Google Drive - Artigos PDF',
                'url': 'https://drive.google.com',
                'rss_url': None,
                'is_active': True,
                'scraping_frequency': 24
            }).execute()
            
            if new_source.data:
                return new_source.data[0]['id']
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar fonte PDF: {e}")
            return None

    def check_pdf_already_processed(self, pdf_id):
        """Verifica se um PDF já foi processado usando a URL"""
        try:
            # Verificar pela URL do Drive (que contém o ID do arquivo)
            pdf_url = f"https://drive.google.com/file/d/{pdf_id}"
            
            # Buscar artigos com URL que contenha o ID do PDF
            result = self.supabase.table('news_articles').select('id, url').ilike('url', f"%{pdf_id}%").execute()
            
            if result.data:
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao verificar PDF processado: {e}")
            return False

    def save_article(self, article_data):
        """Salva artigo no banco de dados"""
        try:
            # Gerar slug
            slug = re.sub(r'[^\w\s-]', '', article_data['title'].lower())
            slug = re.sub(r'[-\s]+', '-', slug)[:100]
            slug = f"{slug}-{int(datetime.now().timestamp())}"
            article_data['slug'] = slug
            
            # Verificar duplicatas por título
            existing = self.supabase.table('news_articles').select('id').ilike('title', f"%{article_data['title'][:50]}%").execute()
            if existing.data:
                logger.info(f"📄 Artigo similar já existe: {article_data['title'][:50]}...")
                return False
            
            # Inserir artigo
            result = self.supabase.table('news_articles').insert(article_data).execute()
            
            if result.data:
                article_id = result.data[0]['id']
                logger.info(f"✅ Artigo criado do PDF: {article_data['title']} (ID: {article_id})")
                
                # Salvar tags
                tags = article_data.get('tags', ['artigo-pdf'])
                if isinstance(tags, str):
                    tags = json.loads(tags) if tags.startswith('[') else [tags]
                
                self.save_article_tags(article_id, tags)
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar artigo: {e}")
            return False

    def save_article_tags(self, article_id, tags):
        """Salva tags do artigo"""
        try:
            for tag_name in tags:
                if not tag_name or not tag_name.strip():
                    continue
                    
                tag_name = tag_name.strip()
                tag_slug = tag_name.lower().replace(' ', '-')
                
                # Buscar tag existente
                tag_result = self.supabase.table('news_tags').select('id').eq('slug', tag_slug).execute()
                
                if tag_result.data:
                    tag_id = tag_result.data[0]['id']
                else:
                    # Criar nova tag
                    try:
                        new_tag = self.supabase.table('news_tags').insert({
                            'name': tag_name,
                            'slug': tag_slug
                        }).execute()
                        tag_id = new_tag.data[0]['id']
                    except Exception:
                        # Se der erro, buscar novamente
                        tag_result = self.supabase.table('news_tags').select('id').eq('slug', tag_slug).execute()
                        if tag_result.data:
                            tag_id = tag_result.data[0]['id']
                        else:
                            continue
                
                # Relacionar artigo com tag
                try:
                    self.supabase.table('news_article_tags').insert({
                        'article_id': article_id,
                        'tag_id': tag_id
                    }).execute()
                except Exception:
                    pass  # Já existe
                    
        except Exception as e:
            logger.warning(f"⚠️ Erro ao salvar tags: {e}")

    def process_pdfs_from_drive(self, folder_id=None):
        """Processa todos os PDFs do Google Drive"""
        if not GOOGLE_DRIVE_AVAILABLE:
            logger.error("❌ Google Drive API não disponível. Instale as dependências necessárias.")
            return 0
        
        if not PDF_AVAILABLE:
            logger.error("❌ Biblioteca de PDF não disponível. Instale PyPDF2 ou pdfplumber.")
            return 0
        
        # Autenticar (tentar Service Account primeiro, depois OAuth)
        if not self.authenticate_google_drive_service_account():
            if not self.authenticate_google_drive():
                logger.error("❌ Falha na autenticação do Google Drive")
                return 0
        
        # Listar PDFs
        pdf_files = self.list_pdf_files(folder_id)
        
        if not pdf_files:
            logger.warning("⚠️ Nenhum PDF encontrado no Google Drive")
            return 0
        
        processed = 0
        temp_dir = '/tmp/drive_pdfs'
        os.makedirs(temp_dir, exist_ok=True)
        
        for pdf_file in pdf_files:
            pdf_id = pdf_file['id']
            pdf_name = pdf_file['name']
            pdf_url = pdf_file.get('webViewLink', f"https://drive.google.com/file/d/{pdf_id}")
            
            logger.info(f"📄 Processando: {pdf_name}")
            
            # Verificar se já foi processado
            if self.check_pdf_already_processed(pdf_id):
                logger.info(f"⏭️ PDF já processado: {pdf_name}")
                continue
            
            # Baixar PDF
            temp_pdf_path = os.path.join(temp_dir, f"{pdf_id}.pdf")
            if not self.download_pdf(pdf_id, temp_pdf_path):
                continue
            
            # Extrair texto
            pdf_text = self.extract_text_from_pdf(temp_pdf_path)
            if not pdf_text:
                logger.warning(f"⚠️ Não foi possível extrair texto: {pdf_name}")
                os.remove(temp_pdf_path)
                continue
            
            # Criar artigo
            article_data = self.create_article_from_pdf(pdf_text, pdf_name, pdf_id, pdf_url)
            if not article_data:
                logger.warning(f"⚠️ Não foi possível criar artigo: {pdf_name}")
                os.remove(temp_pdf_path)
                continue
            
            # Salvar artigo
            if self.save_article(article_data):
                processed += 1
            
            # Limpar arquivo temporário
            os.remove(temp_pdf_path)
        
        logger.info(f"✅ Processamento concluído! {processed} artigos criados de {len(pdf_files)} PDFs")
        return processed

def main():
    """Função principal"""
    collector = DrivePDFCollector()
    processed = collector.process_pdfs_from_drive()
    print(f"\n🎉 {processed} artigos criados a partir de PDFs do Google Drive!")

if __name__ == "__main__":
    main()

