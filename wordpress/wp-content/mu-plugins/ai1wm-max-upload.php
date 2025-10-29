<?php
/*
Plugin Name: AIOWPM - Max Upload
Description: Aumenta limites para importação do All-in-One WP Migration.
Author: TemVenda
Version: 1.0
*/

if (!defined('ABSPATH')) { exit; }

@ini_set('upload_max_filesize', '2048M');
@ini_set('post_max_size', '2048M');
@ini_set('memory_limit', '1024M');
@ini_set('max_execution_time', '0');
@ini_set('max_input_time', '0');

add_filter('ai1wm_max_file_size', function () { return 2 * 1024 * 1024 * 1024; });

