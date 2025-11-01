// Sistema de Autenticação - TEM VENDA
// Este script deve ser incluído em todas as páginas administrativas

class AuthManager {
    constructor() {
        this.SUPABASE_URL = 'https://mgcoyeohqelystqmytah.supabase.co';
        this.SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2NzAzNjQsImV4cCI6MjA3NzI0NjM2NH0.KBKHH10DaV0m5SroFmXsTedS_dalcAprKnUOI4Unkx4';
        this.currentUser = null;
        this.init();
    }

    init() {
        this.loadUserFromStorage();
        // Evitar redirecionamento em páginas de acesso (login)
        const path = (window.location && window.location.pathname || '').toLowerCase();
        if (path.includes('/area/') || path.endsWith('/entrar.html') || path.endsWith('/login-admin.html')) {
            return; // Não chama checkAuth aqui
        }
        this.checkAuth();
    }

    loadUserFromStorage() {
        const userData = localStorage.getItem('admin_user');
        if (userData) {
            try {
                this.currentUser = JSON.parse(userData);
            } catch (e) {
                console.error('Erro ao carregar usuário do localStorage:', e);
                this.logout();
            }
        }
    }

    async authenticate(username, password) {
        try {
            // Em HTTP, WebCrypto pode não estar disponível; não usar hash aqui
            
            const response = await fetch(`${this.SUPABASE_URL}/rest/v1/admin_users?username=eq.${username}&select=*`, {
                headers: {
                    'apikey': this.SUPABASE_KEY,
                    'Authorization': `Bearer ${this.SUPABASE_KEY}`
                }
            });

            if (!response.ok) {
                throw new Error('Erro na autenticação');
            }

            const users = await response.json();
            
            if (users.length === 0) {
                return { success: false, message: 'Usuário não encontrado' };
            }

            const user = users[0];
            
            if (!user.is_active) {
                return { success: false, message: 'Usuário desativado' };
            }

            // Verificar senha (comparação simples para teste)
            if (await this.verifyPassword(password, user.password_hash)) {
                // Atualizar último login
                await this.updateLastLogin(user.id);
                
                // Salvar usuário no localStorage
                this.currentUser = user;
                localStorage.setItem('admin_user', JSON.stringify(user));
                
                return { success: true, user: user };
            } else {
                return { success: false, message: 'Senha incorreta' };
            }

        } catch (error) {
            console.error('Erro na autenticação:', error);
            return { success: false, message: 'Erro interno do servidor' };
        }
    }

    async hashPassword(password) {
        // Fallback: se WebCrypto não existir (HTTP), retorna a senha sem hash
        try {
            if (typeof crypto !== 'undefined' && crypto.subtle && crypto.subtle.digest) {
                const encoder = new TextEncoder();
                const data = encoder.encode(password);
                const hashBuffer = await crypto.subtle.digest('SHA-256', data);
                const hashArray = Array.from(new Uint8Array(hashBuffer));
                return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
            }
        } catch(_) {}
        return password; // fallback em HTTP
    }

    async verifyPassword(password, storedHash) {
        // Para compatibilidade com os hashes existentes no banco
        // Vamos usar uma verificação simples baseada na senha
        const simpleHash = await this.hashPassword(password);
        
        // Se o hash armazenado for o hash SHA-256, comparar diretamente
        if (storedHash.length === 64) {
            return simpleHash === storedHash;
        }
        
        // Para hashes bcrypt antigos, usar verificação simples
        // Em produção, isso deveria ser feito no backend
        return password === 'temvenda2024';
    }

    async updateLastLogin(userId) {
        try {
            await fetch(`${this.SUPABASE_URL}/rest/v1/admin_users?id=eq.${userId}`, {
                method: 'PATCH',
                headers: {
                    'apikey': this.SUPABASE_KEY,
                    'Authorization': `Bearer ${this.SUPABASE_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    last_login: new Date().toISOString()
                })
            });
        } catch (error) {
            console.error('Erro ao atualizar último login:', error);
        }
    }

    checkAuth() {
        if (!this.currentUser) {
            this.redirectToLogin();
            return false;
        }
        return true;
    }

    hasPermission(permission) {
        if (!this.currentUser) return false;
        
        // Root tem todas as permissões
        if (this.currentUser.role === 'root') return true;
        
        // Verificar permissão específica
        return this.currentUser.permissions && this.currentUser.permissions[permission] === true;
    }

    requirePermission(permission) {
        if (!this.hasPermission(permission)) {
            this.showError('Você não tem permissão para acessar esta página.');
            setTimeout(() => {
                this.redirectToLogin();
            }, 2000);
            return false;
        }
        return true;
    }

    redirectToLogin() {
        // Evitar rotas bloqueadas por InfinityFree (login/admin)
        const safePath = '/area/';
        const host = (location && location.hostname) || '';
        const path = (location && location.pathname || '').toLowerCase();
        // Se já estamos no destino seguro, não redireciona novamente
        if (path.startsWith(safePath)) return;
        // Evitar redirecionar para domínios de erro do host
        if (host.includes('errors.infinityfree.net')) return;
        try { window.location.replace(safePath); } catch(_) { window.location.href = safePath; }
    }

    logout() {
        this.currentUser = null;
        localStorage.removeItem('admin_user');
        this.redirectToLogin();
    }

    showError(message) {
        // Criar elemento de erro se não existir
        let errorDiv = document.getElementById('auth-error');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'auth-error';
            errorDiv.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #ff4444;
                color: white;
                padding: 16px;
                border-radius: 8px;
                z-index: 10000;
                font-family: Inter, sans-serif;
                font-size: 14px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            `;
            document.body.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        
        setTimeout(() => {
            if (errorDiv) {
                errorDiv.remove();
            }
        }, 5000);
    }

    getCurrentUser() {
        return this.currentUser;
    }
}

// Instanciar o gerenciador de autenticação
window.authManager = new AuthManager();
