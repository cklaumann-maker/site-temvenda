// CRUD Manager - Gerencia operações CRUD para todas as entidades
// Feira Digital Farma

class CRUDManager {
    constructor(entityType, tableName) {
        this.entityType = entityType;
        this.tableName = tableName;
        this.supabase = null;
        this.currentData = [];
        this.logoUploadManager = null;
        this.init();
    }

    async init() {
        try {
            console.log(`Inicializando CRUD Manager para ${this.entityType}...`);
            
            if (!window.SUPABASE_CONFIG) {
                throw new Error('SUPABASE_CONFIG não encontrado');
            }
            
            const config = window.SUPABASE_CONFIG;
            
            if (typeof supabase === 'undefined') {
                throw new Error('Biblioteca Supabase não carregada');
            }
            
            this.supabase = supabase.createClient(config.url, config.anonKey);
            
            // LogoUploadManager é opcional
            try {
                if (typeof LogoUploadManager !== 'undefined') {
                    this.logoUploadManager = new LogoUploadManager(this.supabase);
                }
            } catch (e) {
                console.warn('LogoUploadManager não disponível:', e);
            }
            
            await this.loadData();
        } catch (error) {
            console.error(`Erro ao inicializar CRUD Manager para ${this.entityType}:`, error);
            let container = document.getElementById('moduleBody') || document.getElementById('tabContent');
            if (container) {
                container.innerHTML = `
                    <div class="error-message show" style="margin: 24px; padding: 24px;">
                        <strong>Erro ao inicializar:</strong><br>
                        ${error.message || 'Erro desconhecido'}<br>
                        <small>Verifique o console para mais detalhes</small>
                    </div>
                `;
            }
        }
    }

    async loadData() {
        try {
            console.log(`Carregando dados de ${this.entityType} da tabela ${this.tableName}...`);
            
            const { data, error } = await this.supabase
                .from(this.tableName)
                .select('*')
                .order('created_at', { ascending: false });
            
            if (error) {
                console.error(`Erro na query para ${this.entityType}:`, error);
                throw error;
            }
            
            console.log(`Dados carregados para ${this.entityType}:`, data?.length || 0, 'registros');
            
            this.currentData = data || [];
            await this.renderTable();
        } catch (error) {
            console.error(`Erro ao carregar ${this.entityType}:`, error);
            let container = document.getElementById('moduleBody') || document.getElementById('tabContent');
            if (container) {
                container.innerHTML = `
                    <div class="error-message show" style="margin: 24px;">
                        <strong>Erro ao carregar dados:</strong><br>
                        ${error.message || 'Erro desconhecido'}<br>
                        <small>Tabela: ${this.tableName}</small>
                    </div>
                `;
            }
        }
    }

    async renderTable() {
        // Tentar novo container primeiro, depois fallback para o antigo
        let container = document.getElementById('moduleBody') || document.getElementById('tabContent');
        if (!container) {
            console.error('Container não encontrado!');
            return;
        }
        
        console.log(`Renderizando tabela para ${this.entityType}...`);

        // Se for CNPJs, adicionar interface de upload
        if (this.entityType === 'cnpjs' && window.cnpjUploadManager) {
            window.cnpjUploadManager.createUploadInterface('cnpjUploadContainer');
        }

        if (this.currentData.length === 0) {
            container.innerHTML = `
                ${this.entityType === 'cnpjs' ? '<div id="cnpjUploadContainer"></div>' : ''}
                <div class="empty-state">
                    <div class="empty-state-icon">📭</div>
                    <div class="empty-state-text">Nenhum registro encontrado</div>
                    <button class="btn-primary" onclick="window.crudManager.openModal('create')">
                        + Adicionar ${this.entityType}
                    </button>
                </div>
            `;
            if (this.entityType === 'cnpjs' && window.cnpjUploadManager) {
                window.cnpjUploadManager.createUploadInterface('cnpjUploadContainer');
            }
            return;
        }

        // Gerar cabeçalhos da tabela baseado no tipo de entidade
        const headers = this.getTableHeaders();
        const rows = await Promise.all(this.currentData.map(item => this.renderRow(item)));

        // Botão adicional para cotas (gerar relatório)
        const extraButton = this.entityType === 'cotas' ? 
            `<button class="btn-primary" onclick="window.crudManager.gerarRelatorioCotas()" style="margin-left: 12px;">
                📊 Gerar Relatório
            </button>` : '';

        container.innerHTML = `
            ${this.entityType === 'cnpjs' ? '<div id="cnpjUploadContainer"></div>' : ''}
            <div class="data-table">
                <div class="table-header">
                    <h2 class="table-title">${this.entityType}</h2>
                    <div style="display: flex; align-items: center;">
                        <button class="btn-primary" onclick="window.crudManager.openModal('create')">
                            + Adicionar ${this.entityType}
                        </button>
                        ${extraButton}
                    </div>
                </div>
                <table>
                    <thead>
                        <tr>
                            ${headers.map(h => `<th>${h.label}</th>`).join('')}
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${rows.join('')}
                    </tbody>
                </table>
            </div>
        `;

        // Se for CNPJs, criar interface de upload após renderizar tabela
        if (this.entityType === 'cnpjs' && window.cnpjUploadManager) {
            window.cnpjUploadManager.createUploadInterface('cnpjUploadContainer');
        }
    }

    getTableHeaders() {
        // Headers específicos por tipo de entidade
        const headersMap = {
            'industrias': [
                { key: 'nome', label: 'Nome' },
                { key: 'status', label: 'Status' },
                { key: 'valor_cota', label: 'Valor Cota' },
                { key: 'contato_email', label: 'Email' },
                { key: 'contato_telefone', label: 'Telefone' }
            ],
            'distribuidoras': [
                { key: 'nome', label: 'Nome' },
                { key: 'status', label: 'Status' },
                { key: 'valor_cota', label: 'Valor Cota' },
                { key: 'contato_email', label: 'Email' },
                { key: 'contato_telefone', label: 'Telefone' }
            ],
            'corporativos': [
                { key: 'nome', label: 'Nome' },
                { key: 'status', label: 'Status' },
                { key: 'contato_email', label: 'Email' },
                { key: 'contato_telefone', label: 'Telefone' }
            ],
            'participantes': [
                { key: 'nome_farmacia', label: 'Farmácia' },
                { key: 'nome_participante', label: 'Participante' },
                { key: 'cnpj', label: 'CNPJ' },
                { key: 'email', label: 'Email' },
                { key: 'email_confirmado', label: 'Confirmado' }
            ],
            'cnpjs': [
                { key: 'cnpj', label: 'CNPJ' },
                { key: 'razao_social', label: 'Razão Social' },
                { key: 'nome_fantasia', label: 'Nome Fantasia' },
                { key: 'ativo', label: 'Ativo' }
            ],
            'cotas': [
                { key: 'tipo_parceiro', label: 'Tipo' },
                { key: 'nome_parceiro', label: 'Parceiro' },
                { key: 'valor_cota', label: 'Valor' },
                { key: 'status_pagamento', label: 'Status' },
                { key: 'data_pagamento', label: 'Data Pagamento' }
            ]
        };

        return headersMap[this.entityType] || [{ key: 'id', label: 'ID' }];
    }

    async renderRow(item) {
        const headers = this.getTableHeaders();
        
        // Buscar dados relacionados uma vez para todas as células
        let parceiroData = null;
        if (this.entityType === 'cotas') {
            if (item.industria_id) {
                const { data } = await this.supabase.from('fdf_industrias').select('nome').eq('id', item.industria_id).single();
                parceiroData = { tipo: 'Indústria', nome: data?.nome || '-' };
            } else if (item.distribuidora_id) {
                const { data } = await this.supabase.from('fdf_distribuidoras').select('nome').eq('id', item.distribuidora_id).single();
                parceiroData = { tipo: 'Distribuidora', nome: data?.nome || '-' };
            }
        }

        const cells = headers.map(header => {
            let value = item[header.key];
            
            // Usar dados do parceiro se necessário
            if (header.key === 'tipo_parceiro' && parceiroData) {
                value = parceiroData.tipo;
            } else if (header.key === 'nome_parceiro' && parceiroData) {
                value = parceiroData.nome;
            }
            
            if (header.key === 'status') {
                return `<td><span class="status-badge status-${value}">${this.formatStatus(value)}</span></td>`;
            }
            if (header.key === 'valor_cota') {
                return `<td>${this.formatCurrency(value)}</td>`;
            }
            if (header.key === 'email_confirmado' || header.key === 'ativo') {
                return `<td>${value ? '✅' : '❌'}</td>`;
            }
            if (header.key === 'status_pagamento') {
                const statusMap = {
                    'pendente': '<span style="color: var(--fdf-orange);">⏰ Pendente</span>',
                    'pago': '<span style="color: var(--fdf-green);">✅ Pago</span>',
                    'isento': '<span style="color: var(--fdf-white-medium);">🆓 Isento</span>'
                };
                return `<td>${statusMap[value] || value || '-'}</td>`;
            }
            if (header.key === 'data_pagamento' && value) {
                const date = new Date(value);
                return `<td>${date.toLocaleDateString('pt-BR')}</td>`;
            }
            return `<td>${value || '-'}</td>`;
        });

        // Ações específicas para cotas
        let actionsHTML = '';
        if (this.entityType === 'cotas') {
            if (item.status_pagamento !== 'pago' && item.status_pagamento !== 'isento') {
                actionsHTML = `
                    <button class="btn-icon" onclick="window.crudManager.marcarComoPago(${item.id})" title="Marcar como Pago" style="background: rgba(94, 225, 0, 0.1); border-color: var(--fdf-green); color: var(--fdf-green);">
                        💰
                    </button>
                `;
            }
            actionsHTML += `
                <button class="btn-icon" onclick="window.crudManager.openModal('edit', ${item.id})" title="Editar">
                    ✏️
                </button>
                <button class="btn-icon delete" onclick="window.crudManager.deleteItem(${item.id})" title="Excluir">
                    🗑️
                </button>
            `;
        } else {
            actionsHTML = `
                <button class="btn-icon" onclick="window.crudManager.openModal('edit', ${item.id})" title="Editar">
                    ✏️
                </button>
                <button class="btn-icon delete" onclick="window.crudManager.deleteItem(${item.id})" title="Excluir">
                    🗑️
                </button>
            `;
        }

        return `
            <tr>
                ${cells.join('')}
                <td>
                    <div class="actions">
                        ${actionsHTML}
                    </div>
                </td>
            </tr>
        `;
    }

    formatStatus(status) {
        const statusMap = {
            'ativo': 'Ativo',
            'aguardando': 'Aguardando',
            'inativo': 'Inativo'
        };
        return statusMap[status] || status;
    }

    formatCurrency(value) {
        if (!value) return 'R$ 0,00';
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    }

    async openModal(mode, id = null) {
        const item = id ? this.currentData.find(i => i.id === id) : null;
        await this.renderModal(mode, item);
    }

    async renderModal(mode, item = null) {
        const isEdit = mode === 'edit';
        const title = isEdit ? `Editar ${this.entityType}` : `Adicionar ${this.entityType}`;
        const formFields = await this.getFormFields(item);

        const modalHTML = `
            <div class="modal show" id="crudModal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2 class="modal-title">${title}</h2>
                        <button class="modal-close" onclick="window.crudManager.closeModal()">×</button>
                    </div>
                    <form id="crudForm" onsubmit="window.crudManager.handleSubmit(event, ${item?.id || null})">
                        ${formFields}
                        <div class="form-actions">
                            <button type="button" class="btn-secondary" onclick="window.crudManager.closeModal()">Cancelar</button>
                            <button type="submit" class="btn-primary">${isEdit ? 'Salvar' : 'Criar'}</button>
                        </div>
                    </form>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    async getFormFields(item) {
        // Campos específicos por tipo de entidade
        const fieldsMap = {
            'industrias': () => `
                <div class="form-group">
                    <label class="form-label">Nome *</label>
                    <input type="text" class="form-input" name="nome" value="${item?.nome || ''}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Logo</label>
                    <input type="file" class="form-input" name="logo" id="logoInput" accept="image/png,image/jpeg,image/jpg" onchange="window.crudManager.handleLogoPreview(event, 'logoPreview')">
                    <div id="logoPreview"></div>
                    ${item?.logo_url ? `<div style="margin-top: 8px;"><img src="${item.logo_url}" alt="Logo atual" style="max-width: 150px; border-radius: 8px;"></div>` : ''}
                </div>
                <div class="form-group">
                    <label class="form-label">Status *</label>
                    <select class="form-select" name="status" required>
                        <option value="ativo" ${item?.status === 'ativo' ? 'selected' : ''}>Ativo</option>
                        <option value="aguardando" ${item?.status === 'aguardando' ? 'selected' : ''}>Aguardando</option>
                        <option value="inativo" ${item?.status === 'inativo' ? 'selected' : ''}>Inativo</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Valor da Cota (R$)</label>
                    <input type="number" step="0.01" class="form-input" name="valor_cota" value="${item?.valor_cota || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Email de Contato</label>
                    <input type="email" class="form-input" name="contato_email" value="${item?.contato_email || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Telefone de Contato</label>
                    <input type="text" class="form-input" name="contato_telefone" value="${item?.contato_telefone || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Observações</label>
                    <textarea class="form-textarea" name="observacoes">${item?.observacoes || ''}</textarea>
                </div>
            `,
            'distribuidoras': () => `
                <div class="form-group">
                    <label class="form-label">Nome *</label>
                    <input type="text" class="form-input" name="nome" value="${item?.nome || ''}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Logo</label>
                    <input type="file" class="form-input" name="logo" id="logoInput" accept="image/png,image/jpeg,image/jpg" onchange="window.crudManager.handleLogoPreview(event, 'logoPreview')">
                    <div id="logoPreview"></div>
                    ${item?.logo_url ? `<div style="margin-top: 8px;"><img src="${item.logo_url}" alt="Logo atual" style="max-width: 150px; border-radius: 8px;"></div>` : ''}
                </div>
                <div class="form-group">
                    <label class="form-label">Status *</label>
                    <select class="form-select" name="status" required>
                        <option value="ativo" ${item?.status === 'ativo' ? 'selected' : ''}>Ativo</option>
                        <option value="aguardando" ${item?.status === 'aguardando' ? 'selected' : ''}>Aguardando</option>
                        <option value="inativo" ${item?.status === 'inativo' ? 'selected' : ''}>Inativo</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Valor da Cota (R$)</label>
                    <input type="number" step="0.01" class="form-input" name="valor_cota" value="${item?.valor_cota || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Email de Contato</label>
                    <input type="email" class="form-input" name="contato_email" value="${item?.contato_email || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Telefone de Contato</label>
                    <input type="text" class="form-input" name="contato_telefone" value="${item?.contato_telefone || ''}">
                </div>
            `,
            'corporativos': () => `
                <div class="form-group">
                    <label class="form-label">Nome *</label>
                    <input type="text" class="form-input" name="nome" value="${item?.nome || ''}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Status *</label>
                    <select class="form-select" name="status" required>
                        <option value="ativo" ${item?.status === 'ativo' ? 'selected' : ''}>Ativo</option>
                        <option value="aguardando" ${item?.status === 'aguardando' ? 'selected' : ''}>Aguardando</option>
                        <option value="inativo" ${item?.status === 'inativo' ? 'selected' : ''}>Inativo</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Email de Contato</label>
                    <input type="email" class="form-input" name="contato_email" value="${item?.contato_email || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Telefone de Contato</label>
                    <input type="text" class="form-input" name="contato_telefone" value="${item?.contato_telefone || ''}">
                </div>
            `,
            'participantes': async () => {
                // Buscar parceiros para vincular
                const [industrias, distribuidoras, corporativos] = await Promise.all([
                    this.supabase.from('fdf_industrias').select('id, nome').eq('status', 'ativo'),
                    this.supabase.from('fdf_distribuidoras').select('id, nome').eq('status', 'ativo'),
                    this.supabase.from('fdf_corporativos').select('id, nome').eq('status', 'ativo')
                ]);

                const optionsIndustrias = (industrias.data || []).map(i => 
                    `<option value="${i.id}" ${item?.industria_id === i.id ? 'selected' : ''}>${i.nome}</option>`
                ).join('');
                const optionsDistribuidoras = (distribuidoras.data || []).map(d => 
                    `<option value="${d.id}" ${item?.distribuidora_id === d.id ? 'selected' : ''}>${d.nome}</option>`
                ).join('');
                const optionsCorporativos = (corporativos.data || []).map(c => 
                    `<option value="${c.id}" ${item?.corporativo_id === c.id ? 'selected' : ''}>${c.nome}</option>`
                ).join('');

                return `
                    <div class="form-group">
                        <label class="form-label">CNPJ *</label>
                        <input type="text" class="form-input" name="cnpj" value="${item?.cnpj || ''}" maxlength="14" pattern="[0-9]{14}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Nome da Farmácia *</label>
                        <input type="text" class="form-input" name="nome_farmacia" value="${item?.nome_farmacia || ''}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Nome do Participante *</label>
                        <input type="text" class="form-input" name="nome_participante" value="${item?.nome_participante || ''}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">CPF *</label>
                        <input type="text" class="form-input" name="cpf" value="${item?.cpf || ''}" maxlength="11" pattern="[0-9]{11}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Telefone *</label>
                        <input type="text" class="form-input" name="telefone" value="${item?.telefone || ''}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Email *</label>
                        <input type="email" class="form-input" name="email" value="${item?.email || ''}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Vincular a Indústria</label>
                        <select class="form-select" name="industria_id">
                            <option value="">Nenhuma</option>
                            ${optionsIndustrias}
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Vincular a Distribuidora</label>
                        <select class="form-select" name="distribuidora_id">
                            <option value="">Nenhuma</option>
                            ${optionsDistribuidoras}
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Vincular a Corporativo</label>
                        <select class="form-select" name="corporativo_id">
                            <option value="">Nenhuma</option>
                            ${optionsCorporativos}
                        </select>
                    </div>
                    ${item ? `
                    <div class="form-group">
                        <label class="form-label">Email Confirmado</label>
                        <div class="form-checkbox">
                            <input type="checkbox" name="email_confirmado" ${item?.email_confirmado ? 'checked' : ''}>
                            <span>Confirmado</span>
                        </div>
                    </div>
                    ` : ''}
                `;
            },
            'cnpjs': () => `
                <div class="form-group">
                    <label class="form-label">CNPJ *</label>
                    <input type="text" class="form-input" name="cnpj" value="${item?.cnpj || ''}" maxlength="14" pattern="[0-9]{14}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Razão Social *</label>
                    <input type="text" class="form-input" name="razao_social" value="${item?.razao_social || ''}" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Nome Fantasia</label>
                    <input type="text" class="form-input" name="nome_fantasia" value="${item?.nome_fantasia || ''}">
                </div>
                <div class="form-group">
                    <label class="form-label">Ativo</label>
                    <div class="form-checkbox">
                        <input type="checkbox" name="ativo" ${item?.ativo !== false ? 'checked' : ''}>
                        <span>Ativo</span>
                    </div>
                </div>
            `,
            'cotas': async () => {
                // Buscar parceiros para vincular
                const [industrias, distribuidoras] = await Promise.all([
                    this.supabase.from('fdf_industrias').select('id, nome, valor_cota').eq('status', 'ativo'),
                    this.supabase.from('fdf_distribuidoras').select('id, nome, valor_cota').eq('status', 'ativo')
                ]);

                let options = '<option value="">Selecione...</option>';
                (industrias.data || []).forEach(i => {
                    options += `<option value="industria_${i.id}" ${item?.industria_id === i.id ? 'selected' : ''}>Indústria: ${i.nome} (R$ ${this.formatCurrency(i.valor_cota)})</option>`;
                });
                (distribuidoras.data || []).forEach(d => {
                    options += `<option value="distribuidora_${d.id}" ${item?.distribuidora_id === d.id ? 'selected' : ''}>Distribuidora: ${d.nome} (R$ ${this.formatCurrency(d.valor_cota)})</option>`;
                });

                // Determinar status atual
                const statusAtual = item?.status_pagamento || 'pendente';
                const isPago = statusAtual === 'pago';
                const isIsento = statusAtual === 'isento';

                return `
                    <div class="form-group">
                        <label class="form-label">Parceiro *</label>
                        <select class="form-select" name="parceiro" id="parceiroSelect" required>
                            ${options}
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Valor da Cota (R$)</label>
                        <input type="number" step="0.01" class="form-input" name="valor_cota" id="valorCota" value="${item?.valor_cota || ''}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Status do Pagamento *</label>
                        <select class="form-select" name="status_pagamento" required>
                            <option value="pendente" ${statusAtual === 'pendente' ? 'selected' : ''}>⏰ Pendente</option>
                            <option value="pago" ${isPago ? 'selected' : ''}>✅ Pago</option>
                            <option value="isento" ${isIsento ? 'selected' : ''}>🆓 Isento</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Data de Pagamento</label>
                        <input type="date" class="form-input" name="data_pagamento" value="${item?.data_pagamento ? item.data_pagamento.split('T')[0] : ''}">
                    </div>
                    <script>
                        // Atualizar valor da cota quando selecionar parceiro
                        document.getElementById('parceiroSelect')?.addEventListener('change', function() {
                            const option = this.options[this.selectedIndex];
                            const text = option.text;
                            const match = text.match(/R\\$ ([0-9.,]+)/);
                            if (match) {
                                const valor = match[1].replace(/[.,]/g, m => m === ',' ? '.' : '');
                                document.getElementById('valorCota').value = valor;
                            }
                        });
                    </script>
                `;
            }
        };

        const fieldsFn = fieldsMap[this.entityType];
        if (!fieldsFn) {
            return '<p>Formulário não configurado para este tipo de entidade</p>';
        }

        // Se for função assíncrona, aguardar resultado
        if (fieldsFn.constructor.name === 'AsyncFunction') {
            return await fieldsFn();
        }
        return fieldsFn();
    }

    async handleSubmit(event, id) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const data = {};
        let logoFile = null;
        
        // Processar dados do formulário
        for (const [key, value] of formData.entries()) {
            if (key === 'logo') {
                logoFile = value;
                continue; // Processar logo depois
            }
            if (key === 'ativo' || key === 'email_confirmado') {
                data[key] = value === 'on';
            } else if (key === 'valor_cota') {
                data[key] = value ? parseFloat(value) : null;
            } else if (key === 'industria_id' || key === 'distribuidora_id' || key === 'corporativo_id') {
                data[key] = value || null;
            } else if (key === 'parceiro') {
                // Processar seleção de parceiro para cotas
                const [tipo, parceiroId] = value.split('_');
                if (tipo === 'industria') {
                    data.industria_id = parseInt(parceiroId);
                    data.distribuidora_id = null;
                    data.corporativo_id = null;
                } else if (tipo === 'distribuidora') {
                    data.distribuidora_id = parseInt(parceiroId);
                    data.industria_id = null;
                    data.corporativo_id = null;
                }
            } else if (value !== '') {
                data[key] = value;
            }
        }

        try {
            // Upload de logo se houver
            if (logoFile && logoFile.size > 0 && (this.entityType === 'industrias' || this.entityType === 'distribuidoras')) {
                const partnerId = id || 'temp';
                const partnerType = this.entityType === 'industrias' ? 'industrias' : 'distribuidoras';
                const logoUrl = await this.handleLogoUpload(logoFile, partnerId, partnerType);
                if (logoUrl) {
                    data.logo_url = logoUrl;
                }
            }

            if (id) {
                // Atualizar
                const { error } = await this.supabase
                    .from(this.tableName)
                    .update(data)
                    .eq('id', id);
                
                if (error) throw error;
            } else {
                // Criar - adicionar campos padrão se necessário
                if (this.entityType === 'participantes' && !data.email_confirmado) {
                    data.email_confirmado = false;
                }
                if (this.entityType === 'cnpjs' && data.ativo === undefined) {
                    data.ativo = true;
                }
                if (this.entityType === 'cotas' && !data.status_pagamento) {
                    data.status_pagamento = 'pendente';
                }
                
                const { result, error } = await this.supabase
                    .from(this.tableName)
                    .insert([data])
                    .select();
                
                if (error) throw error;

                // Se criou novo registro e tem logo, atualizar com ID real
                if (logoFile && logoFile.size > 0 && result && result[0] && (this.entityType === 'industrias' || this.entityType === 'distribuidoras')) {
                    const newId = result[0].id;
                    const partnerType = this.entityType === 'industrias' ? 'industrias' : 'distribuidoras';
                    const logoUrl = await this.handleLogoUpload(logoFile, newId, partnerType);
                    if (logoUrl) {
                        await this.supabase
                            .from(this.tableName)
                            .update({ logo_url: logoUrl })
                            .eq('id', newId);
                    }
                }
            }

            this.closeModal();
            await this.loadData();
            this.showSuccess(`${this.entityType} ${id ? 'atualizado' : 'criado'} com sucesso!`);
        } catch (error) {
            console.error('Erro ao salvar:', error);
            this.showError(`Erro ao salvar: ${error.message}`);
        }
    }

    async deleteItem(id) {
        if (!confirm(`Deseja realmente excluir este ${this.entityType}?`)) {
            return;
        }

        try {
            const { error } = await this.supabase
                .from(this.tableName)
                .delete()
                .eq('id', id);
            
            if (error) throw error;
            
            await this.loadData();
            this.showSuccess(`${this.entityType} excluído com sucesso!`);
        } catch (error) {
            console.error('Erro ao excluir:', error);
            this.showError(`Erro ao excluir: ${error.message}`);
        }
    }

    closeModal() {
        const modal = document.getElementById('crudModal');
        if (modal) {
            modal.remove();
        }
    }

    showSuccess(message) {
        // Implementar notificação de sucesso
        alert(message); // Por enquanto, usar alert
    }

    showError(message) {
        // Implementar notificação de erro
        alert(message); // Por enquanto, usar alert
    }

    async handleLogoPreview(event, containerId) {
        const file = event.target.files[0];
        if (!file) return;

        try {
            await this.logoUploadManager.createPreviewElement(file, containerId);
        } catch (error) {
            alert(`Erro ao criar preview: ${error.message}`);
            event.target.value = '';
        }
    }

    async handleLogoUpload(file, partnerId, partnerType) {
        if (!file) return null;

        const result = await this.logoUploadManager.uploadLogo(file, partnerId, partnerType);
        if (!result.success) {
            throw new Error(result.error);
        }
        return result.url;
    }

    async marcarComoPago(id) {
        if (!confirm('Deseja marcar esta cota como paga?')) {
            return;
        }

        try {
            const { error } = await this.supabase
                .from(this.tableName)
                .update({ 
                    status_pagamento: 'pago',
                    data_pagamento: new Date().toISOString()
                })
                .eq('id', id);
            
            if (error) throw error;
            
            await this.loadData();
            this.showSuccess('Cota marcada como paga com sucesso!');
        } catch (error) {
            console.error('Erro ao marcar como pago:', error);
            this.showError(`Erro: ${error.message}`);
        }
    }

    async gerarRelatorioCotas() {
        try {
            // Buscar cotas e depois buscar parceiros separadamente
            const { data: cotas, error } = await this.supabase
                .from('fdf_cotas')
                .select('*')
                .order('created_at', { ascending: false });
            
            if (error) throw error;

            // Buscar nomes dos parceiros
            const cotasComParceiros = await Promise.all(cotas.map(async (cota) => {
                if (cota.industria_id) {
                    const { data } = await this.supabase.from('fdf_industrias').select('nome').eq('id', cota.industria_id).single();
                    return { ...cota, parceiroNome: data?.nome || '-' };
                } else if (cota.distribuidora_id) {
                    const { data } = await this.supabase.from('fdf_distribuidoras').select('nome').eq('id', cota.distribuidora_id).single();
                    return { ...cota, parceiroNome: data?.nome || '-' };
                }
                return { ...cota, parceiroNome: '-' };
            }));

            const data = cotasComParceiros;
            
            if (error) throw error;

            // Processar dados para CSV
            const csvRows = [];
            csvRows.push(['Tipo', 'Parceiro', 'Valor Cota', 'Status Pagamento', 'Data Pagamento', 'Data Criação']);

            data.forEach(cota => {
                const tipo = cota.industria_id ? 'Indústria' : cota.distribuidora_id ? 'Distribuidora' : '-';
                const parceiro = cota.parceiroNome || '-';
                const valor = cota.status_pagamento === 'isento' ? 'Isento' : this.formatCurrency(cota.valor_cota);
                const status = cota.status_pagamento === 'pago' ? 'Pago' : cota.status_pagamento === 'isento' ? 'Isento' : 'Pendente';
                const dataPagamento = cota.data_pagamento ? new Date(cota.data_pagamento).toLocaleDateString('pt-BR') : '-';
                const dataCriacao = cota.created_at ? new Date(cota.created_at).toLocaleDateString('pt-BR') : '-';

                csvRows.push([tipo, parceiro, valor, status, dataPagamento, dataCriacao]);
            });

            // Converter para CSV
            const csvContent = csvRows.map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            
            link.setAttribute('href', url);
            link.setAttribute('download', `relatorio_cotas_${new Date().toISOString().split('T')[0]}.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            this.showSuccess('Relatório gerado com sucesso!');
        } catch (error) {
            console.error('Erro ao gerar relatório:', error);
            this.showError(`Erro ao gerar relatório: ${error.message}`);
        }
    }
}
