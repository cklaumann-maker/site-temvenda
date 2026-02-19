// Login de Participante - Feira Digital Farma

class LoginParticipante {
    constructor() {
        this.supabase = null;
        this.init();
    }

    async init() {
        const config = window.SUPABASE_CONFIG;
        this.supabase = supabase.createClient(config.url, config.anonKey);
        this.setupEventListeners();
    }

    setupEventListeners() {
        const form = document.getElementById('loginForm');
        const cnpjInput = document.getElementById('cnpj');

        // Máscara de CNPJ
        cnpjInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/\D/g, '').slice(0, 14);
        });

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });
    }

    async handleLogin() {
        const form = document.getElementById('loginForm');
        const submitBtn = document.getElementById('submitBtn');
        const formData = new FormData(form);

        const cnpj = formData.get('cnpj').replace(/\D/g, '');
        const senha = formData.get('senha');

        // Validar CNPJ
        if (cnpj.length !== 14) {
            this.showError('cnpjError', 'CNPJ deve ter 14 dígitos');
            return;
        }

        // Desabilitar botão e mostrar loading
        submitBtn.disabled = true;
        submitBtn.textContent = 'Entrando...';

        try {
            // Buscar participante pelo CNPJ
            const { data: participante, error: searchError } = await this.supabase
                .from('fdf_participantes')
                .select('id, cnpj, nome_participante, nome_farmacia, email, senha_hash, email_confirmado, ativo')
                .eq('cnpj', cnpj)
                .single();

            if (searchError || !participante) {
                this.showError('senhaError', 'CNPJ ou senha incorretos');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Entrar';
                return;
            }

            // Verificar se está ativo
            if (!participante.ativo) {
                this.showError('senhaError', 'Sua conta está desativada. Entre em contato com o suporte.');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Entrar';
                return;
            }

            // Verificar se email foi confirmado
            if (!participante.email_confirmado) {
                this.showError('senhaError', 'Por favor, confirme seu email antes de fazer login. Verifique sua caixa de entrada.');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Entrar';
                return;
            }

            // Verificar senha
            console.log('Participante encontrado:', {
                cnpj: participante.cnpj,
                hashLength: participante.senha_hash?.length,
                hashStart: participante.senha_hash?.substring(0, 20),
                hashType: participante.senha_hash?.startsWith('$2') ? 'bcrypt' : 'outro'
            });
            
            const senhaValida = await this.verificarSenha(senha, participante.senha_hash);
            
            if (!senhaValida) {
                console.error('Senha inválida para CNPJ:', participante.cnpj);
                this.showError('senhaError', 'CNPJ ou senha incorretos');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Entrar';
                return;
            }
            
            console.log('Login bem-sucedido!');

            // Salvar sessão no localStorage
            const sessao = {
                id: participante.id,
                cnpj: participante.cnpj,
                nome: participante.nome_participante,
                farmacia: participante.nome_farmacia,
                email: participante.email,
                tipo: 'participante',
                loginAt: new Date().toISOString()
            };

            localStorage.setItem('fdf_participante_session', JSON.stringify(sessao));

            // Redirecionar para área do participante (ou página inicial)
            window.location.href = 'index.html?login=success';

        } catch (error) {
            console.error('Erro ao fazer login:', error);
            this.showError('senhaError', 'Erro ao fazer login. Tente novamente.');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Entrar';
        }
    }

    async verificarSenha(senha, hash) {
        console.log('Verificando senha...', { 
            hashLength: hash?.length, 
            hashStart: hash?.substring(0, 10),
            hashType: hash?.startsWith('$2') ? 'bcrypt' : 'outro'
        });
        
        if (!hash) {
            console.error('Hash não fornecido');
            return false;
        }

        // Se o hash é bcrypt (começa com $2a$ ou $2b$)
        if (hash.startsWith('$2a$') || hash.startsWith('$2b$')) {
            // Aguardar bcrypt carregar se necessário
            let tentativas = 0;
            while ((typeof bcrypt === 'undefined' || !bcrypt.compareSync) && tentativas < 10) {
                await new Promise(resolve => setTimeout(resolve, 100));
                tentativas++;
            }

            if (typeof bcrypt !== 'undefined' && bcrypt.compareSync) {
                try {
                    const resultado = bcrypt.compareSync(senha, hash);
                    console.log('Resultado bcrypt.compareSync:', resultado);
                    return resultado;
                } catch (e) {
                    console.error('Erro ao comparar com bcrypt:', e);
                    return false;
                }
            } else {
                console.error('bcrypt não disponível após espera');
                alert('Erro: Biblioteca de segurança não carregou. Por favor, recarregue a página.');
                return false;
            }
        }

        // Fallback: se o hash for base64 (temporário), comparar diretamente
        try {
            const decoded = atob(hash);
            const resultado = decoded === senha;
            console.log('Resultado fallback base64:', resultado);
            return resultado;
        } catch (e) {
            console.error('Erro no fallback:', e);
            return false;
        }
    }

    showError(fieldId, message) {
        const errorDiv = document.getElementById(fieldId);
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.classList.add('show');
        }
    }
}

// Inicializar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new LoginParticipante();
    });
} else {
    new LoginParticipante();
}
