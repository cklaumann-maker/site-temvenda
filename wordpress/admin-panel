<?php
// Arquivo para forçar a exibição do painel administrativo de notícias
// Acesse via: http://localhost:8080/admin-panel

// Carregar o conteúdo do arquivo HTML do painel administrativo
$admin_panel_html_path = '/var/www/html/admin-panel-corporativo.html';

if (file_exists($admin_panel_html_path)) {
    echo file_get_contents($admin_panel_html_path);
} else {
    echo "<h1>Erro: Arquivo do painel administrativo não encontrado.</h1>";
}
?>
