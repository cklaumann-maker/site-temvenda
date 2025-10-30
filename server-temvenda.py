#!/usr/bin/env python3
"""Servidor HTTP com roteamento para TEM VENDA"""
import http.server
import socketserver
import urllib.parse
import os
import subprocess
import sys

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        
        routes = {
            '/login-admin': '/login-admin.html',
            '/admin': '/admin.html',
            '/admin-panel': '/admin-panel.html',
            '/admin-stats': '/admin-stats.html',
            '/admin-users': '/admin-users.html',
            '/diagnostico': '/diagnostico.html',
            '/consultoria': '/consultoria.html',
            '/formacao-lideres': '/formacao-lideres.html',
            '/treinamento-incompany': '/treinamento-incompany.html',
            '/palestras': '/palestras.html',
            '/noticias': '/noticias.html',
            '/instagram': '/instagram.html',
        }
        
        if path in routes:
            self.path = routes[path]
            return super().do_GET()
        
        if path == '/' or path == '':
            self.path = '/index.html'
            return super().do_GET()
        
        return super().do_GET()

def kill_process_on_port(port):
    """Mata processo usando uma porta específica"""
    try:
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    subprocess.run(['kill', '-9', pid], capture_output=True)
                    print(f"🛑 Processo {pid} encerrado na porta {port}")
                    return True
    except Exception as e:
        pass
    return False

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8000
    
    # Tentar liberar a porta se estiver em uso
    print(f"🔍 Verificando porta {PORT}...")
    if kill_process_on_port(PORT):
        import time
        time.sleep(1)
    
    Handler = CustomHTTPRequestHandler
    
    try:
        with ReusableTCPServer(("", PORT), Handler) as httpd:
            print(f"\n✅ Servidor rodando em http://localhost:{PORT}")
            print(f"📄 Login Admin: http://localhost:{PORT}/login-admin")
            print(f"📄 Login Admin (com .html): http://localhost:{PORT}/login-admin.html")
            print(f"\n💡 Pressione Ctrl+C para parar\n")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:
            print(f"\n❌ ERRO: Porta {PORT} já está em uso!")
            print(f"\n🔧 SOLUÇÃO:")
            print(f"   1. Execute: lsof -ti:8000 | xargs kill -9")
            print(f"   2. Ou use outra porta: python3 server-temvenda.py 8001")
            sys.exit(1)
        else:
            raise
    except PermissionError as e:
        # Tentar fallback automático para 8001 em caso de permissão negada
        print(f"\n⚠️  Permissão negada na porta {PORT}. Tentando porta alternativa 8001...")
        alt_port = 8001
        try:
            with ReusableTCPServer(("", alt_port), Handler) as httpd:
                print(f"\n✅ Servidor rodando em http://localhost:{alt_port}")
                print(f"📄 Login Admin: http://localhost:{alt_port}/login-admin")
                print(f"📄 Login Admin (com .html): http://localhost:{alt_port}/login-admin.html")
                print(f"\n💡 Pressione Ctrl+C para parar\n")
                httpd.serve_forever()
        except Exception as e2:
            print("❌ Não foi possível iniciar o servidor em 8001 também.")
            raise e2
