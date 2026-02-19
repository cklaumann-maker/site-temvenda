// Cadastro de Participante - Feira Digital Farma
// Validação CNPJ, verificação na base, cadastro e confirmação de email
// Suporta múltiplos tipos: varejo, distribuidora, indústria, corporativo

class CadastroParticipante {
    constructor() {
        this.supabase = null;
        this.tipoSelecionado = null;
        this.init();
    }

    async init() {
        const config = window.SUPABASE_CONFIG;
        this.supabase = supabase.createClient(config.url, config.anonKey);
        this.setupEventListeners();
    }

    setupEventListeners() {
        const form = document.getElementById('cadastroForm');
        const tipoSelect = document.getElementById('tipoParticipante');
        const submitBtn = document.getElementById('submitBtn');

        // Listener para mudança de tipo
        tipoSelect.addEventListener('change', (e) => {
            this.tipoSelecionado = e.target.value;
            this.mostrarCamposPorTipo(this.tipoSelecionado);
        });

        // Listener para CNPJ do varejo (buscar na base)
        const cnpjInput = document.getElementById('cnpj');
        if (cnpjInput) {
            cnpjInput.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/\D/g, '').slice(0, 14);
                if (e.target.value.length === 14) {
                    this.validarCNPJ(e.target.value);
                    this.buscarCNPJNaBase(e.target.value);
                } else {
                    this.limparValidacaoCNPJ();
                }
            });
        }

        // Máscaras e validações para campos do varejo
        const cpfInput = document.getElementById('cpf');
        if (cpfInput) {
            cpfInput.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/\D/g, '').slice(0, 11);
                this.validarCPF(e.target.value);
            });
        }

        const telefoneInput = document.getElementById('telefone');
        if (telefoneInput) {
            telefoneInput.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/\D/g, '');
                if (e.target.value.length > 0) {
                    e.target.value = this.formatarTelefone(e.target.value);
                }
            });
        }

        // Máscaras para outros tipos
        ['Distribuidora', 'Industria', 'Corporativo'].forEach(tipo => {
            const telefoneId = `telefone${tipo}`;
            const telefoneEl = document.getElementById(telefoneId);
            if (telefoneEl) {
                telefoneEl.addEventListener('input', (e) => {
                    e.target.value = e.target.value.replace(/\D/g, '');
                    if (e.target.value.length > 0) {
                        e.target.value = this.formatarTelefone(e.target.value);
                    }
                });
            }
        });

        const senhaInput = document.getElementById('senha');
        const confirmarSenhaInput = document.getElementById('confirmarSenha');
        if (senhaInput && confirmarSenhaInput) {
            senhaInput.addEventListener('input', () => {
                this.validarSenhas();
            });
            confirmarSenhaInput.addEventListener('input', () => {
                this.validarSenhas();
            });
        }

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });
    }

    mostrarCamposPorTipo(tipo) {
        // Esconder todos os campos
        document.querySelectorAll('.campos-tipo').forEach(el => {
            el.style.display = 'none';
        });

        const submitBtn = document.getElementById('submitBtn');

        // Mostrar campos do tipo selecionado
        if (tipo === 'varejo') {
            document.getElementById('camposVarejo').style.display = 'block';
            submitBtn.style.display = 'block';
        } else if (tipo === 'distribuidora') {
            document.getElementById('camposDistribuidora').style.display = 'block';
            submitBtn.style.display = 'block';
        } else if (tipo === 'industria') {
            document.getElementById('camposIndustria').style.display = 'block';
            submitBtn.style.display = 'block';
        } else if (tipo === 'corporativo') {
            document.getElementById('camposCorporativo').style.display = 'block';
            submitBtn.style.display = 'block';
        } else {
            submitBtn.style.display = 'none';
        }
    }

    async buscarCNPJNaBase(cnpj) {
        if (!cnpj || cnpj.length !== 14) return;

        try {
            const { data, error } = await this.supabase
                .from('fdf_cnpjs_base')
                .select('razao_social, nome_fantasia, telefone, email')
                .eq('cnpj', cnpj)
                .eq('ativo', true)
                .single();

            if (data) {
                // Preencher campos automaticamente
                const nomeFarmaciaInput = document.getElementById('nomeFarmacia');
                if (nomeFarmaciaInput && !nomeFarmaciaInput.value) {
                    nomeFarmaciaInput.value = data.nome_fantasia || data.razao_social || '';
                }

                const telefoneInput = document.getElementById('telefone');
                if (telefoneInput && !telefoneInput.value && data.telefone) {
                    telefoneInput.value = this.formatarTelefone(data.telefone.replace(/\D/g, ''));
                }

                const emailInput = document.getElementById('email');
                if (emailInput && !emailInput.value && data.email) {
                    emailInput.value = data.email;
                }

                // Mostrar mensagem de sucesso
                const successDiv = document.getElementById('cnpjSuccess');
                if (successDiv) {
                    successDiv.textContent = `✅ Dados carregados da base: ${data.nome_fantasia || data.razao_social}`;
                    successDiv.classList.add('show');
                }
            }
        } catch (err) {
            // CNPJ não encontrado na base - não é erro, pode continuar
            console.log('CNPJ não encontrado na base, permitindo cadastro manual');
        }
    }

    formatarTelefone(value) {
        const numbers = value.replace(/\D/g, '');
        if (numbers.length <= 10) {
            return numbers.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3').trim();
        } else {
            return numbers.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3').trim();
        }
    }

    async validarCNPJ(cnpj) {
        const cnpjInput = document.getElementById('cnpj');
        const errorDiv = document.getElementById('cnpjError');
        const successDiv = document.getElementById('cnpjSuccess');

        // Validar formato (14 dígitos)
        if (cnpj.length !== 14) {
            if (cnpjInput) {
                cnpjInput.classList.remove('success');
                cnpjInput.classList.add('error');
            }
            if (errorDiv) {
                errorDiv.textContent = 'CNPJ deve ter exatamente 14 dígitos';
                errorDiv.classList.add('show');
            }
            if (successDiv) successDiv.classList.remove('show');
            return false;
        }

        // Validar dígitos verificadores
        if (!this.validarDigitosCNPJ(cnpj)) {
            if (cnpjInput) {
                cnpjInput.classList.remove('success');
                cnpjInput.classList.add('error');
            }
            if (errorDiv) {
                errorDiv.textContent = 'CNPJ inválido (dígitos verificadores incorretos)';
                errorDiv.classList.add('show');
            }
            if (successDiv) successDiv.classList.remove('show');
            return false;
        }

        // Verificar se já existe participante com este CNPJ (apenas para varejo)
        if (this.tipoSelecionado === 'varejo') {
            try {
                const { data, error } = await this.supabase
                    .from('fdf_participantes')
                    .select('id')
                    .eq('cnpj', cnpj)
                    .single();

                if (data) {
                    if (cnpjInput) {
                        cnpjInput.classList.remove('success');
                        cnpjInput.classList.add('error');
                    }
                    if (errorDiv) {
                        errorDiv.textContent = 'Este CNPJ já está cadastrado';
                        errorDiv.classList.add('show');
                    }
                    if (successDiv) successDiv.classList.remove('show');
                    return false;
                }
            } catch (err) {
                // CNPJ não encontrado, pode continuar
            }
        }

        // CNPJ válido
        if (cnpjInput) {
            cnpjInput.classList.remove('error');
            cnpjInput.classList.add('success');
        }
        if (errorDiv) errorDiv.classList.remove('show');
        if (successDiv && !successDiv.classList.contains('show')) {
            successDiv.textContent = '✅ CNPJ válido';
            successDiv.classList.add('show');
        }

        return true;
    }

    validarDigitosCNPJ(cnpj) {
        if (cnpj.length !== 14) return false;
        if (/^(\d)\1+$/.test(cnpj)) return false;

        let tamanho = cnpj.length - 2;
        let numeros = cnpj.substring(0, tamanho);
        let digitos = cnpj.substring(tamanho);
        let soma = 0;
        let pos = tamanho - 7;

        for (let i = tamanho; i >= 1; i--) {
            soma += numeros.charAt(tamanho - i) * pos--;
            if (pos < 2) pos = 9;
        }

        let resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
        if (resultado != digitos.charAt(0)) return false;

        tamanho = tamanho + 1;
        numeros = cnpj.substring(0, tamanho);
        soma = 0;
        pos = tamanho - 7;

        for (let i = tamanho; i >= 1; i--) {
            soma += numeros.charAt(tamanho - i) * pos--;
            if (pos < 2) pos = 9;
        }

        resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
        if (resultado != digitos.charAt(1)) return false;

        return true;
    }

    limparValidacaoCNPJ() {
        const cnpjInput = document.getElementById('cnpj');
        const errorDiv = document.getElementById('cnpjError');
        const successDiv = document.getElementById('cnpjSuccess');
        
        if (cnpjInput) cnpjInput.classList.remove('error', 'success');
        if (errorDiv) errorDiv.classList.remove('show');
        if (successDiv) successDiv.classList.remove('show');
    }

    validarCPF(cpf) {
        const cpfInput = document.getElementById('cpf');
        const errorDiv = document.getElementById('cpfError');

        if (!cpfInput || !errorDiv) return false;

        if (cpf.length !== 11) {
            if (cpf.length > 0) {
                cpfInput.classList.add('error');
                errorDiv.textContent = 'CPF deve ter exatamente 11 dígitos';
                errorDiv.classList.add('show');
            } else {
                cpfInput.classList.remove('error');
                errorDiv.classList.remove('show');
            }
            return false;
        }

        if (!this.validarDigitosCPF(cpf)) {
            cpfInput.classList.add('error');
            errorDiv.textContent = 'CPF inválido';
            errorDiv.classList.add('show');
            return false;
        }

        cpfInput.classList.remove('error');
        errorDiv.classList.remove('show');
        return true;
    }

    validarDigitosCPF(cpf) {
        if (cpf.length !== 11) return false;
        if (/^(\d)\1+$/.test(cpf)) return false;

        let soma = 0;
        for (let i = 0; i < 9; i++) {
            soma += parseInt(cpf.charAt(i)) * (10 - i);
        }
        let digito = 11 - (soma % 11);
        if (digito >= 10) digito = 0;
        if (digito != parseInt(cpf.charAt(9))) return false;

        soma = 0;
        for (let i = 0; i < 10; i++) {
            soma += parseInt(cpf.charAt(i)) * (11 - i);
        }
        digito = 11 - (soma % 11);
        if (digito >= 10) digito = 0;
        if (digito != parseInt(cpf.charAt(10))) return false;

        return true;
    }

    validarSenhas() {
        const senhaInput = document.getElementById('senha');
        const confirmarSenhaInput = document.getElementById('confirmarSenha');
        const errorDiv = document.getElementById('senhaError');

        if (!senhaInput || !confirmarSenhaInput || !errorDiv) return true;

        const senha = senhaInput.value;
        const confirmarSenha = confirmarSenhaInput.value;

        if (confirmarSenha.length > 0 && senha !== confirmarSenha) {
            confirmarSenhaInput.classList.add('error');
            errorDiv.textContent = 'As senhas não coincidem';
            errorDiv.classList.add('show');
            return false;
        }

        confirmarSenhaInput.classList.remove('error');
        errorDiv.classList.remove('show');
        return true;
    }

    async handleSubmit() {
        const form = document.getElementById('cadastroForm');
        const submitBtn = document.getElementById('submitBtn');

        if (!this.tipoSelecionado) {
            alert('Por favor, selecione o tipo de participante.');
            return;
        }

        // Validar campos específicos do tipo
        if (this.tipoSelecionado === 'varejo') {
            const cnpj = document.getElementById('cnpj')?.value.replace(/\D/g, '') || '';
            const cpf = document.getElementById('cpf')?.value.replace(/\D/g, '') || '';

            if (!this.validarCNPJ(cnpj) || !this.validarCPF(cpf) || !this.validarSenhas()) {
                alert('Por favor, corrija os erros no formulário antes de continuar.');
                return;
            }
        } else {
            // Validar CNPJ para outros tipos
            const cnpjId = `cnpj${this.tipoSelecionado.charAt(0).toUpperCase() + this.tipoSelecionado.slice(1)}`;
            const cnpjInput = document.getElementById(cnpjId);
            if (cnpjInput) {
                const cnpj = cnpjInput.value.replace(/\D/g, '');
                if (!this.validarCNPJ(cnpj)) {
                    alert('Por favor, informe um CNPJ válido.');
                    return;
                }
            }
        }

        // Desabilitar botão e mostrar loading
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Processando... <span class="loading-spinner"></span>';

        try {
            if (this.tipoSelecionado === 'varejo') {
                await this.cadastrarVarejo();
            } else if (this.tipoSelecionado === 'distribuidora') {
                await this.cadastrarDistribuidora();
            } else if (this.tipoSelecionado === 'industria') {
                await this.cadastrarIndustria();
            } else if (this.tipoSelecionado === 'corporativo') {
                await this.cadastrarCorporativo();
            }
        } catch (error) {
            console.error('Erro ao cadastrar:', error);
            alert(`Erro ao realizar cadastro: ${error.message || 'Tente novamente mais tarde.'}`);
            submitBtn.disabled = false;
            submitBtn.textContent = 'Finalizar Cadastro';
        }
    }

    async cadastrarVarejo() {
        const cnpj = document.getElementById('cnpj').value.replace(/\D/g, '');
        const nomeFarmacia = document.getElementById('nomeFarmacia').value;
        const nomeParticipante = document.getElementById('nomeParticipante').value;
        const cpf = document.getElementById('cpf').value.replace(/\D/g, '');
        const telefone = document.getElementById('telefone').value.replace(/\D/g, '');
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;

        // Gerar hash da senha
        const senhaHash = await this.hashPassword(senha);
        const emailToken = this.gerarToken();

        const participanteData = {
            cnpj: cnpj,
            nome_farmacia: nomeFarmacia,
            nome_participante: nomeParticipante,
            cpf: cpf,
            telefone: telefone,
            email: email,
            senha_hash: senhaHash,
            email_confirmado: false,
            email_token: emailToken,
            token_expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
        };

        const { data, error } = await this.supabase
            .from('fdf_participantes')
            .insert([participanteData])
            .select();

        if (error) {
            if (error.code === '23505') {
                throw new Error('Este CNPJ ou email já está cadastrado.');
            }
            throw error;
        }

        await this.enviarEmailConfirmacao(email, emailToken, nomeParticipante);
        this.mostrarSucesso(email);
    }

    async cadastrarDistribuidora() {
        const nome = document.getElementById('nomeDistribuidora').value;
        const cnpj = document.getElementById('cnpjDistribuidora').value.replace(/\D/g, '');
        const email = document.getElementById('emailDistribuidora').value;
        const telefone = document.getElementById('telefoneDistribuidora').value.replace(/\D/g, '');

        const distribuidoraData = {
            nome: nome,
            cnpj: cnpj,
            contato_email: email,
            contato_telefone: telefone,
            status: 'aguardando'
        };

        const { data, error } = await this.supabase
            .from('fdf_distribuidoras')
            .insert([distribuidoraData])
            .select();

        if (error) {
            throw error;
        }

        alert('Cadastro realizado com sucesso! Sua solicitação será analisada pela equipe.');
        window.location.href = 'index.html';
    }

    async cadastrarIndustria() {
        const nome = document.getElementById('nomeIndustria').value;
        const cnpj = document.getElementById('cnpjIndustria').value.replace(/\D/g, '');
        const email = document.getElementById('emailIndustria').value;
        const telefone = document.getElementById('telefoneIndustria').value.replace(/\D/g, '');

        const industriaData = {
            nome: nome,
            cnpj: cnpj,
            contato_email: email,
            contato_telefone: telefone,
            status: 'aguardando'
        };

        const { data, error } = await this.supabase
            .from('fdf_industrias')
            .insert([industriaData])
            .select();

        if (error) {
            throw error;
        }

        alert('Cadastro realizado com sucesso! Sua solicitação será analisada pela equipe.');
        window.location.href = 'index.html';
    }

    async cadastrarCorporativo() {
        const nome = document.getElementById('nomeCorporativo').value;
        const cnpj = document.getElementById('cnpjCorporativo').value.replace(/\D/g, '');
        const email = document.getElementById('emailCorporativo').value;
        const telefone = document.getElementById('telefoneCorporativo').value.replace(/\D/g, '');

        const corporativoData = {
            nome: nome,
            cnpj: cnpj,
            contato_email: email,
            contato_telefone: telefone,
            status: 'aguardando'
        };

        const { data, error } = await this.supabase
            .from('fdf_corporativos')
            .insert([corporativoData])
            .select();

        if (error) {
            throw error;
        }

        alert('Cadastro realizado com sucesso! Sua solicitação será analisada pela equipe.');
        window.location.href = 'index.html';
    }

    mostrarSucesso(email) {
        const form = document.getElementById('cadastroForm');
        const successMessage = document.getElementById('successMessage');
        const emailConfirmado = document.getElementById('emailConfirmado');

        form.style.display = 'none';
        if (emailConfirmado) emailConfirmado.textContent = email;
        if (successMessage) successMessage.style.display = 'block';
    }

    async hashPassword(password) {
        let tentativas = 0;
        while ((typeof bcrypt === 'undefined' || !bcrypt.hashSync) && tentativas < 10) {
            await new Promise(resolve => setTimeout(resolve, 100));
            tentativas++;
        }

        return new Promise((resolve, reject) => {
            try {
                if (typeof bcrypt === 'undefined' || !bcrypt.hashSync) {
                    alert('Erro: Biblioteca de segurança não carregou. Por favor, recarregue a página.');
                    reject(new Error('bcrypt não disponível'));
                    return;
                }
                
                const salt = bcrypt.genSaltSync(10);
                const hash = bcrypt.hashSync(password, salt);
                
                if (!hash || (!hash.startsWith('$2a$') && !hash.startsWith('$2b$'))) {
                    reject(new Error('Erro ao gerar hash da senha'));
                    return;
                }
                
                resolve(hash);
            } catch (error) {
                reject(error);
            }
        });
    }

    gerarToken() {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let token = '';
        for (let i = 0; i < 32; i++) {
            token += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return token;
    }

    async enviarEmailConfirmacao(email, token, nome) {
        const confirmUrl = `${window.location.origin}/confirmar-email.html?token=${token}`;
        
        console.log('Email de confirmação:', {
            to: email,
            subject: 'Confirme seu cadastro - Feira Digital Farma',
            body: `Olá ${nome},\n\nClique no link abaixo para confirmar seu email:\n\n${confirmUrl}\n\nEste link expira em 7 dias.\n\nAtenciosamente,\nEquipe Feira Digital Farma`
        });

        return { success: true };
    }
}

// Inicializar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.cadastroParticipante = new CadastroParticipante();
    });
} else {
    window.cadastroParticipante = new CadastroParticipante();
}
