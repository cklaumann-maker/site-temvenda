/**
 * Script de Diagnóstico para Upload de Imagens no Supabase
 * Execute no console do navegador (F12) na página admin-stats.html
 */

async function diagnosticarUpload() {
    console.log('🔍 Iniciando diagnóstico de upload...\n');
    
    const resultados = {
        config: false,
        serviceKey: false,
        bucket: false,
        permissao: false,
        teste: false
    };
    
    // 1. Verificar configuração do Supabase
    console.log('1️⃣ Verificando configuração do Supabase...');
    if (typeof window.SUPABASE_CONFIG === 'undefined') {
        console.error('❌ window.SUPABASE_CONFIG não está definido!');
        console.log('💡 Solução: Verifique se o script do Supabase está carregado');
        return resultados;
    }
    
    console.log('✅ SUPABASE_CONFIG encontrado');
    console.log('   URL:', window.SUPABASE_CONFIG.url);
    console.log('   anonKey:', window.SUPABASE_CONFIG.anonKey ? '✅ Configurado' : '❌ Não configurado');
    console.log('   serviceKey:', window.SUPABASE_CONFIG.serviceKey ? '✅ Configurado' : '❌ NÃO CONFIGURADO');
    resultados.config = true;
    
    if (!window.SUPABASE_CONFIG.serviceKey) {
        console.error('\n❌ PROBLEMA ENCONTRADO: serviceKey não está configurada!');
        console.log('💡 Solução: Adicione serviceKey no window.SUPABASE_CONFIG');
        console.log('   Exemplo:');
        console.log('   window.SUPABASE_CONFIG.serviceKey = "sua-service-key-aqui";');
        return resultados;
    }
    resultados.serviceKey = true;
    
    // 2. Verificar se Supabase está disponível
    console.log('\n2️⃣ Verificando biblioteca Supabase...');
    if (typeof supabase === 'undefined') {
        console.error('❌ Biblioteca supabase não está carregada!');
        console.log('💡 Solução: Verifique se o script está incluído:');
        console.log('   <script src="https://unpkg.com/@supabase/supabase-js@2"></script>');
        return resultados;
    }
    console.log('✅ Biblioteca Supabase carregada');
    
    // 3. Tentar conectar e verificar bucket
    console.log('\n3️⃣ Verificando bucket page-images...');
    try {
        const { createClient } = supabase;
        const client = createClient(
            window.SUPABASE_CONFIG.url,
            window.SUPABASE_CONFIG.serviceKey
        );
        
        // Listar buckets
        const { data: buckets, error: bucketsError } = await client.storage.listBuckets();
        
        if (bucketsError) {
            console.error('❌ Erro ao listar buckets:', bucketsError);
            console.log('💡 Possíveis causas:');
            console.log('   - serviceKey incorreta');
            console.log('   - Problema de conexão');
            return resultados;
        }
        
        console.log('✅ Conexão com Supabase estabelecida');
        console.log('   Buckets encontrados:', buckets?.map(b => b.name).join(', ') || 'Nenhum');
        
        const bucketExists = buckets?.some(b => b.name === 'page-images');
        
        if (!bucketExists) {
            console.warn('⚠️ Bucket "page-images" não existe!');
            console.log('💡 Tentando criar bucket...');
            
            try {
                const { data: newBucket, error: createError } = await client.storage.createBucket('page-images', {
                    public: true
                });
                
                if (createError) {
                    console.error('❌ Erro ao criar bucket:', createError);
                    console.log('💡 Solução: Crie o bucket manualmente no Supabase Dashboard');
                    return resultados;
                }
                
                console.log('✅ Bucket "page-images" criado com sucesso!');
                resultados.bucket = true;
            } catch (e) {
                console.error('❌ Erro ao criar bucket:', e);
                return resultados;
            }
        } else {
            console.log('✅ Bucket "page-images" existe');
            resultados.bucket = true;
        }
        
        // Verificar permissões do bucket
        console.log('\n4️⃣ Verificando permissões do bucket...');
        const bucket = buckets?.find(b => b.name === 'page-images');
        if (bucket) {
            console.log('   Público:', bucket.public ? '✅ Sim' : '❌ Não (deve ser público!)');
            if (!bucket.public) {
                console.warn('⚠️ Bucket não está público!');
                console.log('💡 Solução: No Supabase Dashboard, marque o bucket como público');
            } else {
                resultados.permissao = true;
            }
        }
        
        // 5. Teste de upload
        console.log('\n5️⃣ Testando upload...');
        try {
            const testBlob = new Blob(['test'], { type: 'text/plain' });
            const testPath = 'test/diagnostico.txt';
            
            const { error: uploadError } = await client.storage
                .from('page-images')
                .upload(testPath, testBlob, { upsert: true });
            
            if (uploadError) {
                console.error('❌ Erro no teste de upload:', uploadError);
                console.log('💡 Detalhes:', JSON.stringify(uploadError, null, 2));
                return resultados;
            }
            
            console.log('✅ Teste de upload bem-sucedido!');
            
            // Limpar arquivo de teste
            await client.storage.from('page-images').remove([testPath]);
            console.log('✅ Arquivo de teste removido');
            
            resultados.teste = true;
        } catch (e) {
            console.error('❌ Erro no teste de upload:', e);
            return resultados;
        }
        
    } catch (error) {
        console.error('❌ Erro geral:', error);
        return resultados;
    }
    
    // Resumo
    console.log('\n' + '='.repeat(50));
    console.log('📊 RESUMO DO DIAGNÓSTICO');
    console.log('='.repeat(50));
    console.log('Configuração:', resultados.config ? '✅' : '❌');
    console.log('Service Key:', resultados.serviceKey ? '✅' : '❌');
    console.log('Bucket existe:', resultados.bucket ? '✅' : '❌');
    console.log('Permissões:', resultados.permissao ? '✅' : '❌');
    console.log('Teste upload:', resultados.teste ? '✅' : '❌');
    console.log('='.repeat(50));
    
    if (resultados.config && resultados.serviceKey && resultados.bucket && resultados.permissao && resultados.teste) {
        console.log('✅ TUDO OK! O upload deve funcionar.');
    } else {
        console.log('❌ PROBLEMAS ENCONTRADOS. Veja os detalhes acima.');
    }
    
    return resultados;
}

// Executar automaticamente se estiver no admin-stats
if (window.location.pathname.includes('admin-stats')) {
    console.log('💡 Para executar diagnóstico, digite: diagnosticarUpload()');
    console.log('   Ou execute automaticamente aguardando 2 segundos...');
    setTimeout(() => {
        diagnosticarUpload();
    }, 2000);
}

// Exportar função globalmente
window.diagnosticarUpload = diagnosticarUpload;

