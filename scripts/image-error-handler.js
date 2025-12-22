/**
 * Image Error Handler - TEM VENDA
 * Trata imagens que falham ao carregar em todas as páginas
 */

(function() {
    'use strict';

    // Função para tratar erro em imagens
    function handleImageError(img) {
        console.warn('⚠️ Imagem não carregou:', img.src);
        
        // Ocultar imagem quebrada
        img.style.display = 'none';
        
        // Adicionar classe para identificação
        img.classList.add('image-error');
        
        // Tentar carregar placeholder se disponível
        const placeholder = img.dataset.placeholder || '/logo-temvenda.png';
        if (placeholder && placeholder !== img.src) {
            const fallbackImg = new Image();
            fallbackImg.onload = function() {
                img.src = placeholder;
                img.style.display = '';
                img.classList.remove('image-error');
                img.classList.add('image-fallback');
            };
            fallbackImg.onerror = function() {
                // Se placeholder também falhar, manter oculto
                console.warn('⚠️ Placeholder também falhou:', placeholder);
            };
            fallbackImg.src = placeholder;
        }
    }

    // Aplicar tratamento a todas as imagens existentes
    function initImageErrorHandling() {
        const images = document.querySelectorAll('img');
        
        images.forEach(function(img) {
            // Se já tem handler, não adicionar novamente
            if (img.dataset.errorHandled) return;
            
            img.dataset.errorHandled = 'true';
            
            // Se imagem já falhou (src vazio ou erro)
            if (!img.complete || img.naturalHeight === 0) {
                // Aguardar um pouco para ver se carrega
                setTimeout(function() {
                    if (!img.complete || img.naturalHeight === 0) {
                        handleImageError(img);
                    }
                }, 1000);
            }
            
            // Adicionar handler de erro
            img.addEventListener('error', function() {
                handleImageError(this);
            });
            
            // Log de sucesso (opcional, apenas em dev)
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                img.addEventListener('load', function() {
                    console.log('✅ Imagem carregada:', this.src);
                });
            }
        });
    }

    // Observar novas imagens adicionadas dinamicamente
    function observeNewImages() {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        if (node.tagName === 'IMG') {
                            const img = node;
                            if (!img.dataset.errorHandled) {
                                img.dataset.errorHandled = 'true';
                                img.addEventListener('error', function() {
                                    handleImageError(this);
                                });
                            }
                        } else {
                            // Verificar imagens dentro do elemento
                            const images = node.querySelectorAll && node.querySelectorAll('img');
                            if (images) {
                                images.forEach(function(img) {
                                    if (!img.dataset.errorHandled) {
                                        img.dataset.errorHandled = 'true';
                                        img.addEventListener('error', function() {
                                            handleImageError(this);
                                        });
                                    }
                                });
                            }
                        }
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Inicializar quando DOM estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initImageErrorHandling();
            observeNewImages();
        });
    } else {
        initImageErrorHandling();
        observeNewImages();
    }

    // Exportar função para uso manual se necessário
    window.handleImageError = handleImageError;
})();

