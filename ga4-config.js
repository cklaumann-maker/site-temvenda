// Configuração do Google Analytics 4 (GA4)
// Measurement ID configurado: G-DR5X1GNCXV
window.GA4_MEASUREMENT_ID = 'G-DR5X1GNCXV';

// Função para inicializar o Google Analytics 4
(function() {
    if (!window.GA4_MEASUREMENT_ID) {
        console.warn('⚠️ Google Analytics 4 Measurement ID não configurado');
        console.info('💡 Configure o GA4_MEASUREMENT_ID no arquivo ga4-config.js');
        return;
    }

    // Carregar o script do Google Analytics
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${window.GA4_MEASUREMENT_ID}`;
    document.head.appendChild(script);

    // Configurar gtag
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    window.gtag = gtag;
    
    gtag('js', new Date());
    gtag('config', window.GA4_MEASUREMENT_ID, {
        'page_path': window.location.pathname + window.location.search,
        'page_title': document.title,
        'page_location': window.location.href
    });
    
    console.log('✅ Google Analytics 4 inicializado com ID:', window.GA4_MEASUREMENT_ID);
    
    // Salvar page_view automaticamente no Supabase
    if (window.SUPABASE_CONFIG) {
        saveGA4Event('page_view', {
            page_path: window.location.pathname + window.location.search,
            page_title: document.title,
            page_location: window.location.href
        }).catch(err => {
            console.log('ℹ️ Evento page_view registrado apenas no GA4');
        });
    }
})();

// Funções auxiliares para rastrear eventos customizados
window.trackGA4Event = function(eventName, eventParams = {}) {
    if (!window.gtag) {
        console.warn('⚠️ Google Analytics não está carregado');
        return;
    }
    
    // Registrar evento no GA4
    window.gtag('event', eventName, eventParams);
    console.log('📊 Evento GA4 rastreado:', eventName, eventParams);
    
    // Salvar evento no Supabase também (para acompanhamento no admin)
    if (window.SUPABASE_CONFIG) {
        saveGA4Event(eventName, eventParams).catch(err => {
            console.warn('⚠️ Erro ao salvar evento no Supabase:', err);
        });
    }
};

// Salvar evento no Supabase para análise interna
async function saveGA4Event(eventName, eventParams) {
    try {
        const supabaseUrl = window.SUPABASE_CONFIG?.url || 'https://mgcoyeohqelystqmytah.supabase.co';
        // Usar anonKey para inserção (conforme política RLS criada)
        const supabaseKey = window.SUPABASE_CONFIG?.anonKey;
        
        if (!supabaseKey) {
            // Silenciosamente falhar se não houver configuração
            return;
        }
        
        const payload = {
            event_name: eventName,
            event_source: 'ga4',
            page_url: window.location.href,
            page_path: window.location.pathname || '/',
            page_title: document.title || 'Sem título',
            event_params: eventParams || {},
            user_agent: navigator.userAgent || 'unknown',
            timestamp: new Date().toISOString()
        };
        
        // Salvar evento no Supabase (usando anonKey conforme política RLS)
        const response = await fetch(`${supabaseUrl}/rest/v1/analytics_events`, {
            method: 'POST',
            headers: {
                'apikey': supabaseKey,
                'Authorization': `Bearer ${supabaseKey}`,
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            // Sucesso silencioso (não logar para não poluir console)
        } else if (response.status === 404) {
            // Tabela não existe ainda - esperado até o SQL ser executado
            console.log('ℹ️ Tabela analytics_events não criada ainda. Execute o SQL: criar-tabela-analytics-events.sql');
        } else {
            // Outros erros são silenciosos para não impactar performance
        }
    } catch (error) {
        // Erro silencioso - não impactar experiência do usuário
    }
}

// Rastrear eventos automáticos comuns
document.addEventListener('DOMContentLoaded', function() {
    // Rastrear cliques em links externos
    document.querySelectorAll('a[href^="http"]').forEach(link => {
        if (!link.href.includes(window.location.hostname)) {
            link.addEventListener('click', function() {
                window.trackGA4Event('click_external_link', {
                    link_url: this.href,
                    link_text: this.textContent.trim()
                });
            });
        }
    });
    
    // Rastrear downloads de PDFs
    document.querySelectorAll('a[href$=".pdf"], a[href*=".pdf"]').forEach(link => {
        link.addEventListener('click', function() {
            window.trackGA4Event('file_download', {
                file_name: this.href.split('/').pop(),
                file_extension: 'pdf',
                link_url: this.href
            });
        });
    });
    
    // Rastrear envio de formulários
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const formId = this.id || this.name || 'unknown_form';
            window.trackGA4Event('form_submit', {
                form_id: formId,
                form_action: this.action || window.location.href
            });
        });
    });
});

