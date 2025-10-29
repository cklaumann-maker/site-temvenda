<?php
/**
 * Template para páginas - compatível com Elementor
 */

get_header(); ?>

<main id="main" class="site-main">
    <?php
    while ( have_posts() ) :
        the_post();
        
        // Verifica se a página foi criada com Elementor
        if ( \Elementor\Plugin::$instance->documents->get( get_the_ID() )->is_built_with_elementor() ) {
            // Renderiza o conteúdo do Elementor
            the_content();
        } else {
            // Fallback para conteúdo normal
            ?>
            <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                <header class="entry-header">
                    <?php the_title( "<h1 class=\"entry-title\">", "</h1>" ); ?>
                </header>
                <div class="entry-content">
                    <?php the_content(); ?>
                </div>
            </article>
            <?php
        }
    endwhile;
    ?>
</main>

<?php
get_footer();
