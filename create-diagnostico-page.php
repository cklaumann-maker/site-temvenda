<?php
// Script para criar a página de diagnóstico no WordPress
require_once('wp-config.php');

// Conectar ao banco de dados
$mysqli = new mysqli(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);

if ($mysqli->connect_error) {
    die('Erro de conexão: ' . $mysqli->connect_error);
}

// Verificar se a página já existe
$check_query = "SELECT ID FROM wp_posts WHERE post_name = 'diagnostico' AND post_type = 'page'";
$result = $mysqli->query($check_query);

if ($result->num_rows > 0) {
    echo "Página 'diagnostico' já existe.\n";
} else {
    // Criar a página
    $insert_query = "INSERT INTO wp_posts (
        post_title, 
        post_name, 
        post_content, 
        post_excerpt, 
        post_status, 
        post_type, 
        post_author, 
        post_date, 
        post_date_gmt, 
        post_modified, 
        post_modified_gmt, 
        comment_status, 
        ping_status, 
        post_parent, 
        menu_order, 
        post_mime_type, 
        comment_count,
        to_ping,
        pinged,
        post_content_filtered
    ) VALUES (
        'Diagnóstico TemVenda',
        'diagnostico',
        '',
        '',
        'publish',
        'page',
        1,
        NOW(),
        NOW(),
        NOW(),
        NOW(),
        'closed',
        'closed',
        0,
        0,
        '',
        0,
        '',
        '',
        ''
    )";
    
    if ($mysqli->query($insert_query)) {
        $page_id = $mysqli->insert_id;
        echo "Página 'diagnostico' criada com sucesso! ID: $page_id\n";
        echo "Acesse: http://localhost:8080/diagnostico\n";
    } else {
        echo "Erro ao criar página: " . $mysqli->error . "\n";
    }
}

$mysqli->close();
?>
