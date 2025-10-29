<?php
/**
 * Funções do child theme TEM VENDA.
 * Mantemos leve e deixamos o template controlar Tailwind via CDN.
 */

/**
 * Opcional: força largura total nas páginas que usarem nosso template.
 */
add_filter('body_class', function($classes){
    $classes[] = 'temvenda-child';
    return $classes;
