// Sistema de Autenticação - Feira Digital Farma
// Autenticação específica para a área administrativa da FDF

class FDFAuthManager {
    constructor() {
        // Configuração Supabase - usar a mesma do projeto principal
        this.SUPABASE_URL = window.SUPABASE_CONFIG?.url || 'https://mgcoyeohqelystqmytah.supabase.co';
        this.SUPABASE_KEY = window.SUPABASE_CONFIG?.anonKey || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nY295ZW9ocWVseXN0cW15dGFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2NzAzNjQsImV4cCI6MjA3NzI0NjM2NH0.KBKHH10DaV0m5SroFmXsTedS_dalcAprKnUOI4Unkx4';
        this.currentUser = null;
        this.init();
    }

    init() {
        this.loadUserFromStorage();
    }

    loadUserFromStorage() {
        const userData = localStorage.getItem('fdf_admin_user');
        if (userData) {
            try {
                this.currentUser = JSON.parse(userData);
            } catch (e) {
                console.error('Erro ao carregar usuário:', e);
                this.logout();
            }
        }
    }

    async authenticate(login, password) {
        try {
            console.log('Iniciando autenticação para:', login);
            
            // Login agora é apenas texto (cesar, root), não email
            const response = await fetch(`${this.SUPABASE_URL}/rest/v1/fdf_usuarios_admin?email=eq.${encodeURIComponent(login)}&select=*`, {
                headers: {
                    'apikey': this.SUPABASE_KEY,
                    'Authorization': `Bearer ${this.SUPABASE_KEY}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Erro na autenticação');
            }

            const users = await response.json();
            
            console.log('Usuários encontrados:', users.length);
            
            if (users.length === 0) {
                return { success: false, message: 'Usuário não encontrado' };
            }

            const user = users[0];
            
            console.log('Usuário encontrado:', {
                email: user.email,
                ativo: user.ativo,
                hashLength: user.senha_hash?.length,
                hashStart: user.senha_hash?.substring(0, 10)
            });
            
            if (!user.ativo) {
                return { success: false, message: 'Usuário desativado' };
            }

            // Verificar senha usando bcrypt
            const passwordMatch = await this.verifyPassword(password, user.senha_hash);
            
            console.log('Resultado da verificação de senha:', passwordMatch);
            
            if (passwordMatch) {
                // Atualizar último login
                await this.updateLastLogin(user.id);
                
                // Remover senha_hash antes de salvar
                const { senha_hash, ...userSafe } = user;
                
                // Salvar usuário no localStorage
                this.currentUser = userSafe;
                localStorage.setItem('fdf_admin_user', JSON.stringify(userSafe));
                
                console.log('Login bem-sucedido!');
                return { success: true, user: userSafe };
            } else {
                console.error('Senha incorreta');
                return { success: false, message: 'Senha incorreta' };
            }

        } catch (error) {
            console.error('Erro na autenticação:', error);
            return { success: false, message: 'Erro ao conectar com o servidor' };
        }
    }

    async verifyPassword(password, storedHash) {
        if (!storedHash) {
            console.error('Hash não fornecido');
            return false;
        }

        console.log('Verificando senha...', {
            hashLength: storedHash.length,
            hashStart: storedHash.substring(0, 20),
            hashType: storedHash.startsWith('$2') ? 'bcrypt' : 'outro'
        });

        // Se o hash começa com $2a$ ou $2b$, é bcrypt
        if (storedHash.startsWith('$2a$') || storedHash.startsWith('$2b$')) {
            // Aguardar bcrypt carregar se necessário
            let tentativas = 0;
            while ((typeof bcrypt === 'undefined' || !bcrypt.compareSync) && tentativas < 10) {
                await new Promise(resolve => setTimeout(resolve, 100));
                tentativas++;
            }

            // Usar bcrypt.js se disponível
            if (typeof bcrypt !== 'undefined' && bcrypt.compareSync) {
                try {
                    const resultado = bcrypt.compareSync(password, storedHash);
                    console.log('Resultado bcrypt.compareSync:', resultado);
                    return resultado;
                } catch (error) {
                    console.error('Erro ao verificar senha com bcrypt:', error);
                    return false;
                }
            } else {
                console.error('bcrypt.js não disponível após espera');
                alert('Erro: Biblioteca de segurança não carregou. Por favor, recarregue a página.');
                return false;
            }
        }
        
        // Detectar placeholders no banco (SEU_HASH_CEASR_AQUI, SEU_HASH_ROOT_AQUI, SUBSTITUA_PELO_HASH_, etc)
        if (storedHash.includes('SEU_HASH') || 
            storedHash.includes('SUBSTITUA') || 
            storedHash.includes('placeholder') || 
            storedHash.length < 40 ||
            !storedHash.startsWith('$2')) {
            console.warn('Hash placeholder detectado - usando senhas temporárias');
            // IMPORTANTE: Isso é temporário - deve ser removido após atualizar os hashes no banco
            const senhasPermitidas = ['cesar*26', 'root*26', 'Cesar*26', 'Root*26'];
            const senhaValida = senhasPermitidas.includes(password);
            console.log('Verificação temporária:', senhaValida ? '✅ Senha aceita (temporário)' : '❌ Senha rejeitada');
            return senhaValida;
        }
        
        console.error('Hash em formato desconhecido:', storedHash.substring(0, 20));
        return false;
    }

    async updateLastLogin(userId) {
        try {
            await fetch(`${this.SUPABASE_URL}/rest/v1/fdf_usuarios_admin?id=eq.${userId}`, {
                method: 'PATCH',
                headers: {
                    'apikey': this.SUPABASE_KEY,
                    'Authorization': `Bearer ${this.SUPABASE_KEY}`,
                    'Content-Type': 'application/json',
                    'Prefer': 'return=minimal'
                },
                body: JSON.stringify({
                    last_login: new Date().toISOString()
                })
            });
        } catch (error) {
            console.error('Erro ao atualizar último login:', error);
        }
    }

    getCurrentUser() {
        return this.currentUser;
    }

    isAuthenticated() {
        return this.currentUser !== null;
    }

    hasPermission(permission) {
        if (!this.currentUser) return false;
        
        // Root tem todas as permissões
        if (this.currentUser.tipo === 'root') {
            return true;
        }
        
        // Verificar permissões específicas
        const permissoes = this.currentUser.permissoes || {};
        return permissoes[permission] === true || permissoes.all === true;
    }

    logout() {
        this.currentUser = null;
        localStorage.removeItem('fdf_admin_user');
        window.location.href = 'login.html';
    }

    redirectToLogin() {
        window.location.href = 'login.html';
    }

    checkAuth() {
        if (!this.isAuthenticated()) {
            this.redirectToLogin();
            return false;
        }
        return true;
    }
}

// Criar instância global
window.fdfAuth = new FDFAuthManager();
