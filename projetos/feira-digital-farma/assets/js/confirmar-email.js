// Confirmação de Email - Feira Digital Farma

class ConfirmarEmail {
    constructor() {
        this.supabase = null;
        this.init();
    }

    async init() {
        const config = window.SUPABASE_CONFIG;
        this.supabase = supabase.createClient(config.url, config.anonKey);
        
        // Obter token da URL
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('token');
        
        if (!token) {
            this.showError('Token não fornecido na URL.');
            return;
        }

        await this.confirmarEmail(token);
    }

    async confirmarEmail(token) {
        try {
            // Buscar participante pelo token
            const { data: participante, error: searchError } = await this.supabase
                .from('fdf_participantes')
                .select('id, email, email_confirmado, token_expires_at')
                .eq('email_token', token)
                .single();

            if (searchError || !participante) {
                this.showError('Token inválido ou não encontrado.');
                return;
            }

            // Verificar se já está confirmado
            if (participante.email_confirmado) {
                this.showSuccess('Seu email já estava confirmado. Você pode fazer login normalmente.');
                return;
            }

            // Verificar se o token expirou
            if (participante.token_expires_at) {
                const expiresAt = new Date(participante.token_expires_at);
                const now = new Date();
                
                if (now > expiresAt) {
                    this.showError('O link de confirmação expirou. Por favor, solicite um novo link de confirmação.');
                    return;
                }
            }

            // Confirmar email
            const { error: updateError } = await this.supabase
                .from('fdf_participantes')
                .update({
                    email_confirmado: true,
                    email_confirmado_at: new Date().toISOString(),
                    email_token: null, // Limpar token após confirmação
                    token_expires_at: null
                })
                .eq('id', participante.id);

            if (updateError) {
                throw updateError;
            }

            this.showSuccess('Email confirmado com sucesso!');

        } catch (error) {
            console.error('Erro ao confirmar email:', error);
            this.showError(`Erro ao confirmar email: ${error.message || 'Tente novamente mais tarde.'}`);
        }
    }

    showSuccess(message) {
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('errorState').style.display = 'none';
        document.getElementById('successState').style.display = 'block';
    }

    showError(message) {
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('successState').style.display = 'none';
        document.getElementById('errorState').style.display = 'block';
        document.getElementById('errorMessage').textContent = message;
    }
}

// Inicializar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ConfirmarEmail();
    });
} else {
    new ConfirmarEmail();
}
