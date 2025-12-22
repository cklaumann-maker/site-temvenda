// Configuração do Meta Pixel (Facebook Pixel)
// Pixel ID configurado: 1356287742600569
window.META_PIXEL_ID = '1356287742600569';

// Função para inicializar o Pixel Meta
(function() {
    if (!window.META_PIXEL_ID) {
        console.warn('⚠️ Meta Pixel ID não configurado');
        return;
    }

    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    
    fbq('init', window.META_PIXEL_ID);
    fbq('track', 'PageView');
    
    console.log('✅ Meta Pixel inicializado com ID:', window.META_PIXEL_ID);
})();

// Funções auxiliares para rastrear eventos
window.trackMetaEvent = function(eventName, eventData = {}) {
    if (!window.fbq) {
        console.warn('⚠️ Meta Pixel não está carregado');
        return;
    }
    
    // Registrar evento no Pixel
    fbq('track', eventName, eventData);
    console.log('📊 Evento Meta Pixel rastreado:', eventName, eventData);
    
    // Salvar evento no Supabase também (para acompanhamento no admin)
    if (window.SUPABASE_CONFIG) {
        saveCampaignEvent(eventName, eventData).catch(err => {
            console.warn('⚠️ Erro ao salvar evento no Supabase:', err);
        });
    }
};

// Salvar evento no Supabase
async function saveCampaignEvent(eventName, eventData) {
    try {
        const supabaseUrl = window.SUPABASE_CONFIG?.url || 'https://mgcoyeohqelystqmytah.supabase.co';
        const supabaseKey = window.SUPABASE_CONFIG?.serviceKey || window.SUPABASE_CONFIG?.anonKey;
        
        if (!supabaseKey) {
            console.warn('⚠️ Chave Supabase não encontrada');
            return;
        }
        
        const payload = {
            event_name: eventName,
            user_email: eventData.email || eventData.user_email || null,
            user_phone: eventData.phone || eventData.user_phone || null,
            user_name: eventData.name || eventData.user_name || null,
            event_source: eventData.source || window.location.pathname || 'unknown',
            page_url: window.location.href,
            pdf_downloaded: eventName === 'CompleteRegistration' || eventName === 'Lead',
            lead_created: eventName === 'Lead' || eventName === 'CompleteRegistration',
            pixel_id: window.META_PIXEL_ID,
            event_id: `${eventName}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            metadata: eventData
        };
        
        const response = await fetch(`${supabaseUrl}/rest/v1/campaign_events`, {
            method: 'POST',
            headers: {
                'apikey': supabaseKey,
                'Authorization': `Bearer ${supabaseKey}`,
                'Content-Type': 'application/json',
                'Prefer': 'return=representation'
            },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            console.log('✅ Evento salvo no Supabase:', eventName);
        } else {
            console.warn('⚠️ Erro ao salvar evento:', response.status, await response.text());
        }
    } catch (error) {
        console.warn('⚠️ Erro ao salvar evento no Supabase:', error);
    }
}

