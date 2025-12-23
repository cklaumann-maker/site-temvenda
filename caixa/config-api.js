// Configuração da URL da API do módulo financeiro
// Este arquivo deve ser incluído ANTES do index.html carregar o script principal

// Detecção automática de ambiente
(function() {
  // Se já foi definido manualmente, usa esse valor
  if (window.FINANCE_API_URL) {
    return;
  }

  // SEMPRE usa a API de produção (backend está no Render)
  // O backend local não está sendo usado, então sempre aponta para produção
  // Para usar localhost, descomente as linhas abaixo e comente a próxima linha
  /*
  const isLocalhost = window.location.hostname === 'localhost' || 
                      window.location.hostname === '127.0.0.1' ||
                      window.location.hostname === '';

  if (isLocalhost) {
    window.FINANCE_API_URL = "http://localhost:8001";
  } else {
  */
    // PRODUÇÃO - URL da API no Render (SEMPRE HTTPS)
    // IMPORTANTE: Usar HTTPS para evitar problemas de mixed content no celular
    window.FINANCE_API_URL = "https://temvenda-finance-api.onrender.com";
  // }
  
  // Log para debug
  console.log('🔧 API URL configurada:', window.FINANCE_API_URL);
})();

// Para forçar um ambiente específico, defina antes deste script:
// window.FINANCE_API_URL = "https://temvenda-finance-api.onrender.com"; // Produção
// window.FINANCE_API_URL = "http://localhost:8001"; // Desenvolvimento local
