<?php
// Arquivo para forçar a exibição do painel de estatísticas
// Acesse via: http://localhost:8080/admin-stats

// Carregar o conteúdo do arquivo HTML do painel de estatísticas
$admin_stats_html_path = '/var/www/html/admin-stats-corporativo.html';

if (file_exists($admin_stats_html_path)) {
    echo file_get_contents($admin_stats_html_path);
} else {
    echo "<h1>Erro: Arquivo do painel de estatísticas não encontrado.</h1>";
}
?>

