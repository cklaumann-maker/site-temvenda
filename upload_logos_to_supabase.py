#!/usr/bin/env python3
"""
Script para fazer upload de logos de clientes para o Supabase Storage
"""

import os
import sys
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://mgcoyeohqelystqmytah.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTY3MDM2NCwiZXhwIjoyMDc3MjQ2MzY0fQ.wylX0wMD5teTcADuUvU81R1bft3pftGhhU-BGKYv9TQ')

# Nome do bucket
BUCKET_NAME = 'client-logos'

# Extensões de imagem permitidas
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.svg', '.webp', '.gif'}

def upload_logos(folder_path: str = None):
    """
    Faz upload de logos para o Supabase Storage
    
    Args:
        folder_path: Caminho da pasta com as imagens (opcional)
    """
    try:
        # Conectar ao Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"✅ Conectado ao Supabase: {SUPABASE_URL}")
        
        # Verificar se o bucket existe
        try:
            buckets = supabase.storage.list_buckets()
            bucket_exists = any(bucket.name == BUCKET_NAME for bucket in buckets)
            
            if not bucket_exists:
                print(f"❌ Bucket '{BUCKET_NAME}' não encontrado!")
                print(f"\n📋 Para criar o bucket:")
                print(f"1. Acesse: https://supabase.com/dashboard")
                print(f"2. Vá em Storage → New bucket")
                print(f"3. Nome: {BUCKET_NAME}")
                print(f"4. Marque 'Public bucket'")
                print(f"5. Crie o bucket")
                return False
            else:
                print(f"✅ Bucket '{BUCKET_NAME}' encontrado!")
        except Exception as e:
            print(f"⚠️ Erro ao verificar bucket: {e}")
            print("Continuando mesmo assim...")
        
        # Determinar pasta de imagens
        if folder_path:
            images_folder = Path(folder_path)
        else:
            # Procurar pasta de logos
            script_dir = Path(__file__).parent
            possible_folders = [
                script_dir / 'logos',
                script_dir / 'client-logos',
                script_dir / 'images' / 'logos',
                script_dir / 'assets' / 'logos',
            ]
            
            images_folder = None
            for folder in possible_folders:
                if folder.exists() and folder.is_dir():
                    images_folder = folder
                    break
            
            if not images_folder:
                print("❌ Pasta de logos não encontrada!")
                print("\n📁 Opções:")
                print("1. Crie uma pasta 'logos' na raiz do projeto")
                print("2. Coloque as imagens dos logos nessa pasta")
                print("3. Execute o script novamente")
                print("\nOu use:")
                print(f"python3 {sys.argv[0]} /caminho/para/pasta/logos")
                return False
        
        if not images_folder.exists():
            print(f"❌ Pasta não encontrada: {images_folder}")
            return False
        
        print(f"📁 Procurando imagens em: {images_folder}")
        
        # Encontrar todas as imagens
        image_files = []
        for ext in ALLOWED_EXTENSIONS:
            image_files.extend(images_folder.glob(f'*{ext}'))
            image_files.extend(images_folder.glob(f'*{ext.upper()}'))
        
        if not image_files:
            print(f"❌ Nenhuma imagem encontrada em: {images_folder}")
            print(f"Formatos suportados: {', '.join(ALLOWED_EXTENSIONS)}")
            return False
        
        print(f"📸 Encontradas {len(image_files)} imagens")
        print()
        
        # Fazer upload de cada imagem
        uploaded = 0
        failed = 0
        
        for image_file in image_files:
            try:
                file_name = image_file.name
                file_path = str(image_file)
                
                print(f"📤 Enviando: {file_name}...", end=" ")
                
                # Ler arquivo
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                
                # Fazer upload
                response = supabase.storage.from_(BUCKET_NAME).upload(
                    file_name,
                    file_data,
                    file_options={
                        "content-type": f"image/{image_file.suffix[1:]}",
                        "upsert": "true"  # Substituir se já existir
                    }
                )
                
                print("✅")
                uploaded += 1
                
            except Exception as e:
                print(f"❌ Erro: {e}")
                failed += 1
        
        print()
        print("=" * 50)
        print(f"✅ Upload concluído!")
        print(f"   Enviadas: {uploaded}")
        print(f"   Falhas: {failed}")
        print()
        print(f"🌐 Verifique no Supabase Dashboard:")
        print(f"   Storage → {BUCKET_NAME}")
        print()
        print(f"🔗 Teste no site:")
        print(f"   https://www.temvenda.com.br")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else None
    upload_logos(folder)

