// Dashboard - Feira Digital Farma
// Carrega métricas reais do banco de dados

class DashboardManager {
    constructor() {
        this.supabase = null;
        this.init();
    }

    async init() {
        // Inicializar Supabase
        const config = window.SUPABASE_CONFIG;
        this.supabase = supabase.createClient(config.url, config.anonKey);
    }

    async loadSummaryStats(containerId) {
        // Resumo minimalista para página inicial
        try {
            const container = document.getElementById(containerId);
            if (!container) return;

            container.innerHTML = '<div class="summary-card"><div class="summary-label">Carregando...</div><div class="summary-value">-</div></div>';

            const [
                industriasAtivas,
                totalDistribuidoras,
                totalCorporativos,
                totalParticipantes,
                cotasPagas,
                receitaEstimada
            ] = await Promise.all([
                this.countIndustrias('ativo'),
                this.countDistribuidoras(),
                this.countCorporativos(),
                this.countParticipantes(),
                this.countCotasPagas(),
                this.calcularReceitaEstimada()
            ]);

            const summary = [
                { label: 'Indústrias Ativas', value: industriasAtivas, icon: '🏭' },
                { label: 'Distribuidoras', value: totalDistribuidoras, icon: '🚚' },
                { label: 'Corporativos', value: totalCorporativos, icon: '🏢' },
                { label: 'Participantes', value: totalParticipantes, icon: '👥' },
                { label: 'Cotas Pagas', value: cotasPagas, icon: '💰' },
                { label: 'Receita Estimada', value: this.formatCurrency(receitaEstimada), icon: '💵' }
            ];

            container.innerHTML = summary.map(stat => `
                <div class="summary-card">
                    <div class="summary-icon">${stat.icon}</div>
                    <div class="summary-content">
                        <div class="summary-label">${stat.label}</div>
                        <div class="summary-value">${stat.value}</div>
                    </div>
                </div>
            `).join('');

        } catch (error) {
            console.error('Erro ao carregar resumo:', error);
            const container = document.getElementById(containerId);
            if (container) {
                container.innerHTML = '<div class="summary-card"><div class="summary-label">Erro ao carregar</div></div>';
            }
        }
    }

    async loadFullStats(containerId) {
        // Dashboard detalhado completo
        try {
            const container = document.getElementById(containerId);
            if (!container) return;

            container.innerHTML = '<div class="stat-card"><div class="stat-label">Carregando...</div><div class="stat-value">-</div></div>';

            const [
                industriasAtivas,
                industriasAguardando,
                industriasInativas,
                totalDistribuidoras,
                totalCorporativos,
                totalParticipantes,
                participantesConfirmados,
                participantesPendentes,
                cotasPagas,
                cotasPendentes,
                receitaEstimada
            ] = await Promise.all([
                this.countIndustrias('ativo'),
                this.countIndustrias('aguardando'),
                this.countIndustrias('inativo'),
                this.countDistribuidoras(),
                this.countCorporativos(),
                this.countParticipantes(),
                this.countParticipantesConfirmados(),
                this.countParticipantesPendentes(),
                this.countCotasPagas(),
                this.countCotasPendentes(),
                this.calcularReceitaEstimada()
            ]);

            const stats = [
                { label: 'Indústrias Ativas', value: industriasAtivas, icon: '🏭' },
                { label: 'Indústrias Aguardando', value: industriasAguardando, icon: '⏳' },
                { label: 'Indústrias Inativas', value: industriasInativas, icon: '🚫' },
                { label: 'Total Distribuidoras', value: totalDistribuidoras, icon: '🚚' },
                { label: 'Total Corporativos', value: totalCorporativos, icon: '🏢' },
                { label: 'Total Participantes', value: totalParticipantes, icon: '👥' },
                { label: 'Participantes Confirmados', value: participantesConfirmados, icon: '✅' },
                { label: 'Participantes Pendentes', value: participantesPendentes, icon: '📧' },
                { label: 'Cotas Pagas', value: cotasPagas, icon: '💰' },
                { label: 'Cotas Pendentes', value: cotasPendentes, icon: '⏰' },
                { label: 'Receita Estimada', value: this.formatCurrency(receitaEstimada), icon: '💵' }
            ];

            container.innerHTML = stats.map(stat => `
                <div class="stat-card">
                    <div class="stat-label">${stat.icon} ${stat.label}</div>
                    <div class="stat-value">${stat.value}</div>
                </div>
            `).join('');

        } catch (error) {
            console.error('Erro ao carregar dashboard:', error);
            const container = document.getElementById(containerId);
            if (container) {
                container.innerHTML = '<div class="stat-card"><div class="stat-label">Erro ao carregar</div><div class="stat-value" style="color: #ff4d4d;">Erro</div></div>';
            }
        }
    }

    async loadStats() {
        try {
            const statsGrid = document.getElementById('statsGrid');
            if (!statsGrid) return;

            // Mostrar loading
            statsGrid.innerHTML = '<div class="stat-card"><div class="stat-label">Carregando...</div><div class="stat-value">-</div></div>';

            // Buscar métricas do banco
            const [
                industriasAtivas,
                industriasAguardando,
                industriasInativas,
                totalDistribuidoras,
                totalCorporativos,
                totalParticipantes,
                participantesConfirmados,
                participantesPendentes,
                cotasPagas,
                cotasPendentes,
                receitaEstimada
            ] = await Promise.all([
                this.countIndustrias('ativo'),
                this.countIndustrias('aguardando'),
                this.countIndustrias('inativo'),
                this.countDistribuidoras(),
                this.countCorporativos(),
                this.countParticipantes(),
                this.countParticipantesConfirmados(),
                this.countParticipantesPendentes(),
                this.countCotasPagas(),
                this.countCotasPendentes(),
                this.calcularReceitaEstimada()
            ]);

            // Calcular participantes por parceiro
            const participantesPorParceiro = await this.getParticipantesPorParceiro();

            // Renderizar cards de estatísticas
            const stats = [
                { label: 'Indústrias Ativas', value: industriasAtivas, icon: '🏭' },
                { label: 'Indústrias Aguardando', value: industriasAguardando, icon: '⏳' },
                { label: 'Indústrias Inativas', value: industriasInativas, icon: '🚫' },
                { label: 'Total Distribuidoras', value: totalDistribuidoras, icon: '🚚' },
                { label: 'Total Corporativos', value: totalCorporativos, icon: '🏢' },
                { label: 'Total Participantes', value: totalParticipantes, icon: '👥' },
                { label: 'Participantes Confirmados', value: participantesConfirmados, icon: '✅' },
                { label: 'Participantes Pendentes', value: participantesPendentes, icon: '📧' },
                { label: 'Cotas Pagas', value: cotasPagas, icon: '💰' },
                { label: 'Cotas Pendentes', value: cotasPendentes, icon: '⏰' },
                { label: 'Receita Estimada', value: this.formatCurrency(receitaEstimada), icon: '💵' }
            ];

            statsGrid.innerHTML = stats.map(stat => `
                <div class="stat-card">
                    <div class="stat-label">${stat.icon} ${stat.label}</div>
                    <div class="stat-value">${stat.value}</div>
                </div>
            `).join('');

        } catch (error) {
            console.error('Erro ao carregar estatísticas:', error);
            document.getElementById('statsGrid').innerHTML = `
                <div class="stat-card">
                    <div class="stat-label">Erro ao carregar</div>
                    <div class="stat-value" style="color: #ff4d4d;">Erro</div>
                </div>
            `;
        }
    }

    async countIndustrias(status) {
        try {
            const { count, error } = await this.supabase
                .from('fdf_industrias')
                .select('*', { count: 'exact', head: true })
                .eq('status', status);
            
            if (error) throw error;
            return count || 0;
        } catch (error) {
            console.error(`Erro ao contar indústrias ${status}:`, error);
            return 0;
        }
    }

    async countDistribuidoras() {
        try {
            const { count, error } = await this.supabase
                .from('fdf_distribuidoras')
                .select('*', { count: 'exact', head: true });
            
            if (error) throw error;
            return count || 0;
        } catch (error) {
            console.error('Erro ao contar distribuidoras:', error);
            return 0;
        }
    }

    async countCorporativos() {
        try {
            const { count, error } = await this.supabase
                .from('fdf_corporativos')
                .select('*', { count: 'exact', head: true });
            
            if (error) throw error;
            return count || 0;
        } catch (error) {
            console.error('Erro ao contar corporativos:', error);
            return 0;
        }
    }

    async countParticipantes() {
        try {
            const { count, error } = await this.supabase
                .from('fdf_participantes')
                .select('*', { count: 'exact', head: true });
            
            if (error) throw error;
            return count || 0;
        } catch (error) {
            console.error('Erro ao contar participantes:', error);
            return 0;
        }
    }

    async countParticipantesConfirmados() {
        try {
            const { count, error } = await this.supabase
                .from('fdf_participantes')
                .select('*', { count: 'exact', head: true })
                .eq('email_confirmado', true);
            
            if (error) throw error;
            return count || 0;
        } catch (error) {
            console.error('Erro ao contar participantes confirmados:', error);
            return 0;
        }
    }

    async countParticipantesPendentes() {
        try {
            const { count, error } = await this.supabase
                .from('fdf_participantes')
                .select('*', { count: 'exact', head: true })
                .eq('email_confirmado', false);
            
            if (error) throw error;
            return count || 0;
        } catch (error) {
            console.error('Erro ao contar participantes pendentes:', error);
            return 0;
        }
    }

    async countCotasPagas() {
        try {
            const { count, error } = await this.supabase
                .from('fdf_cotas')
                .select('*', { count: 'exact', head: true })
                .eq('status_pagamento', 'pago');
            
            if (error) throw error;
            return count || 0;
        } catch (error) {
            console.error('Erro ao contar cotas pagas:', error);
            return 0;
        }
    }

    async countCotasPendentes() {
        try {
            const { count, error } = await this.supabase
                .from('fdf_cotas')
                .select('*', { count: 'exact', head: true })
                .eq('status_pagamento', 'pendente');
            
            if (error) throw error;
            return count || 0;
        } catch (error) {
            console.error('Erro ao contar cotas pendentes:', error);
            return 0;
        }
    }

    async calcularReceitaEstimada() {
        try {
            const { data, error } = await this.supabase
                .from('fdf_cotas')
                .select('valor_cota, status_pagamento');
            
            if (error) throw error;
            
            if (!data || data.length === 0) return 0;
            
            // Somar todas as cotas pagas
            const receita = data
                .filter(cota => cota.status_pagamento === 'pago')
                .reduce((sum, cota) => sum + (parseFloat(cota.valor_cota) || 0), 0);
            
            return receita;
        } catch (error) {
            console.error('Erro ao calcular receita:', error);
            return 0;
        }
    }

    async getParticipantesPorParceiro() {
        try {
            // Buscar participantes com seus parceiros vinculados
            const { data, error } = await this.supabase
                .from('fdf_participantes')
                .select('industria_id, distribuidora_id, corporativo_id');
            
            if (error) throw error;
            
            const porParceiro = {
                industrias: 0,
                distribuidoras: 0,
                corporativos: 0,
                semVinculo: 0
            };
            
            data.forEach(p => {
                if (p.industria_id) porParceiro.industrias++;
                else if (p.distribuidora_id) porParceiro.distribuidoras++;
                else if (p.corporativo_id) porParceiro.corporativos++;
                else porParceiro.semVinculo++;
            });
            
            return porParceiro;
        } catch (error) {
            console.error('Erro ao buscar participantes por parceiro:', error);
            return { industrias: 0, distribuidoras: 0, corporativos: 0, semVinculo: 0 };
        }
    }

    formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    }
}

// Inicializar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.dashboardManager = new DashboardManager();
    });
} else {
    window.dashboardManager = new DashboardManager();
}
