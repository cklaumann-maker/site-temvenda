<?php
// Arquivo para forçar a exibição da página de palestras
// Acesse via: http://localhost:8080/palestras

// Carregar o conteúdo do arquivo HTML das palestras
$palestras_html_path = '/var/www/html/palestras-corporativo.html';

if (file_exists($palestras_html_path)) {
    echo file_get_contents($palestras_html_path);
} else {
    echo "<h1>Erro: Arquivo das palestras não encontrado.</h1>";
}
?>
