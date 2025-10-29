<?php
// Arquivo para forçar a exibição da página de consultoria
// Acesse via: http://localhost:8080/consultoria

// Carregar o conteúdo do arquivo HTML da consultoria
$consultoria_html_path = '/var/www/html/consultoria-corporativo.html';

if (file_exists($consultoria_html_path)) {
    echo file_get_contents($consultoria_html_path);
} else {
    echo "<h1>Erro: Arquivo da consultoria não encontrado.</h1>";
}
?>
