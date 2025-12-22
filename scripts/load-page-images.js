/**
 * Carrega imagens das páginas do Supabase Storage
 * Fallback para localStorage se não encontrar no Storage
 */

// Aguardar Supabase estar disponível
function waitForSupabase(maxWait = 5000) {
    return new Promise((resolve) => {
        if (typeof supabase !== 'undefined' && window.SUPABASE_CONFIG) {
            resolve(true);
            return;
        }
        
        const startTime = Date.now();
        const checkInterval = setInterval(() => {
            if (typeof supabase !== 'undefined' && window.SUPABASE_CONFIG) {
                clearInterval(checkInterval);
                resolve(true);
            } else if (Date.now() - startTime > maxWait) {
                clearInterval(checkInterval);
                resolve(false);
            }
        }, 100);
    });
}

async function loadPageImages(imageMap) {
    /**
     * imageMap: Array de objetos { key: 'nome-imagem', el: 'id-do-elemento' }
     * Exemplo: [{ key: 'formacao-lider', el: 'formacao-lider-image' }]
     */
    
    if (!imageMap || imageMap.length === 0) return;
    
    // Aguardar Supabase estar disponível
    const supabaseAvailable = await waitForSupabase();
    
    // Função para carregar imagem do Supabase Storage
    async function loadFromSupabase(imageKey) {
        try {
            if (!supabaseAvailable) {
                console.log(`ℹ️ Supabase não disponível para ${imageKey}, usando fallback`);
                return null;
            }
            
            if (typeof supabase === 'undefined' || !window.SUPABASE_CONFIG) {
                console.log(`ℹ️ Supabase não configurado para ${imageKey}`);
                return null;
            }
            
            const { createClient } = supabase;
            const client = createClient(
                window.SUPABASE_CONFIG.url,
                window.SUPABASE_CONFIG.anonKey
            );
            
            const bucketName = 'page-images';
            
            // Tentar construir URL diretamente primeiro (mais rápido)
            // Como o bucket é público, podemos confiar na URL diretamente
            const possibleExtensions = ['jpg', 'jpeg', 'png', 'webp'];
            for (const ext of possibleExtensions) {
                const path = `images/${imageKey}.${ext}`;
                const { data: urlData } = client.storage
                    .from(bucketName)
                    .getPublicUrl(path);
                
                if (urlData?.publicUrl) {
                    // Retornar URL diretamente (bucket público, URL sempre válida)
                    console.log(`✅ URL gerada para imagem no Supabase Storage: ${imageKey}.${ext}`);
                    return urlData.publicUrl;
                }
            }
            
            // Se não encontrou com extensões conhecidas, listar arquivos
            try {
                const { data: files, error: listError } = await client.storage
                    .from(bucketName)
                    .list('images');
                
                if (listError) {
                    console.warn(`⚠️ Erro ao listar arquivos do bucket:`, listError);
                    return null;
                }
                
                if (!files || files.length === 0) {
                    console.log(`ℹ️ Nenhum arquivo encontrado no bucket ${bucketName}/images`);
                    return null;
                }
                
                // Procurar arquivo que corresponde ao imageKey
                const matchingFile = files.find(file => {
                    const fileName = file.name.toLowerCase();
                    const keyLower = imageKey.toLowerCase();
                    // Verificar se o nome do arquivo começa com o imageKey
                    return fileName.startsWith(keyLower + '.') || fileName === keyLower;
                });
                
                if (matchingFile) {
                    const path = `images/${matchingFile.name}`;
                    
                    // Obter URL pública
                    const { data: urlData } = client.storage
                        .from(bucketName)
                        .getPublicUrl(path);
                    
                    if (urlData?.publicUrl) {
                        console.log(`✅ Imagem encontrada no Supabase Storage: ${imageKey} (${matchingFile.name})`);
                        return urlData.publicUrl;
                    }
                }
            } catch (listError) {
                console.warn(`⚠️ Erro ao listar arquivos:`, listError);
            }
            
            return null;
        } catch (error) {
            console.warn(`⚠️ Erro ao carregar ${imageKey} do Supabase:`, error);
            return null;
        }
    }
    
    // Função para carregar do localStorage
    function loadFromLocalStorage(imageKey) {
        try {
            const images = JSON.parse(localStorage.getItem('temvenda_images') || '{}');
            return images[imageKey] || null;
        } catch (e) {
            return null;
        }
    }
    
    // Função para renderizar imagem
    function renderImage(elementId, imageUrl, alt) {
        const container = document.getElementById(elementId);
        if (!container) {
            console.warn(`⚠️ Container não encontrado: ${elementId}`);
            return;
        }
        
        if (imageUrl) {
            // Verificar se é URL válida (http/https) ou base64
            if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://') || imageUrl.startsWith('data:')) {
                const img = document.createElement('img');
                img.src = imageUrl;
                img.alt = alt || elementId;
                img.style.cssText = 'width:100%;height:400px;object-fit:cover;display:block;';
                img.loading = 'lazy';
                
                // Tratamento de erro mais robusto
                img.onerror = function() {
                    console.error(`❌ Erro ao carregar imagem ${alt}:`, imageUrl);
                    this.style.display = 'none';
                    // Tentar fallback do localStorage se for URL do Supabase
                    if (imageUrl.includes('supabase.co')) {
                        const fallback = loadFromLocalStorage(alt);
                        if (fallback && fallback !== imageUrl) {
                            console.log(`🔄 Tentando fallback do localStorage para ${alt}`);
                            img.src = fallback;
                        }
                    }
                };
                
                img.onload = function() {
                    console.log(`✅ Imagem renderizada com sucesso: ${alt}`);
                };
                
                container.innerHTML = '';
                container.appendChild(img);
            } else {
                console.warn(`⚠️ URL inválida para ${elementId}:`, imageUrl);
            }
        }
    }
    
    // Carregar cada imagem
    for (const { key, el } of imageMap) {
        try {
            // Tentar carregar do Supabase primeiro
            let imageUrl = await loadFromSupabase(key);
            
            // Se não encontrou no Supabase, tentar localStorage
            if (!imageUrl) {
                imageUrl = loadFromLocalStorage(key);
                if (imageUrl) {
                    console.log(`📦 Imagem carregada do localStorage: ${key}`);
                    // Se for URL do Supabase no localStorage, usar diretamente
                    if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
                        // URL já está pronta
                    } else if (imageUrl.startsWith('data:')) {
                        // Base64, usar diretamente
                    } else {
                        console.warn(`⚠️ Formato de imagem inválido no localStorage para ${key}`);
                        imageUrl = null;
                    }
                }
            }
            
            // Renderizar imagem se encontrada
            if (imageUrl) {
                renderImage(el, imageUrl, key);
            } else {
                console.log(`ℹ️ Imagem não encontrada (nem no Storage nem no localStorage): ${key}`);
            }
        } catch (error) {
            console.error(`❌ Erro ao carregar imagem ${key}:`, error);
            // Tentar fallback do localStorage em caso de erro
            try {
                const fallbackUrl = loadFromLocalStorage(key);
                if (fallbackUrl) {
                    console.log(`🔄 Usando fallback do localStorage para ${key}`);
                    renderImage(el, fallbackUrl, key);
                }
            } catch (fallbackError) {
                console.error(`❌ Erro no fallback para ${key}:`, fallbackError);
            }
        }
    }
}

// Exportar globalmente
window.loadPageImages = loadPageImages;

