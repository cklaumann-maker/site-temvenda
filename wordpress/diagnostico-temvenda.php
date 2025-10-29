<?php
// Arquivo para forçar a exibição do diagnóstico
// Acesse via: http://localhost:8080/diagnostico-temvenda.php

// Incluir o WordPress
require_once('wp-config.php');
require_once('wp-load.php');

// Verificar se é a página de diagnóstico
if (isset($_GET['page']) && $_GET['page'] === 'diagnostico') {
    // Incluir o template personalizado
    include('wp-content/themes/temvenda-child/page-diagnostico.php');
    exit;
}

// Se não for a página de diagnóstico, mostrar erro
http_response_code(404);
echo "Página não encontrada. Use: ?page=diagnostico";
?>
