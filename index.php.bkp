<?php
// Fallback para garantir que o host sirva a home
if (file_exists(__DIR__ . '/index.html')) {
	readfile(__DIR__ . '/index.html');
	exit;
}
http_response_code(404);
echo 'Arquivo index.html não encontrado.';
