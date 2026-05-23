<?php
/**
 * Plugin Name:       BPO Firm Design System
 * Plugin URI:        https://bpofirm.com/
 * Description:       BPO Firm brand design tokens (fonts, light theme, red + blue accents, custom keyframes) for Home, About and Contact. All rules scoped under .bpo-page so service pages keep their lighter design.
 * Version:           0.1.0
 * Requires at least: 6.4
 * Requires PHP:      7.4
 * Author:            BPO Firm
 * License:           GPL-2.0-or-later
 * Text Domain:       bpofirm-design-system
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'BPOFIRM_DS_URL', plugin_dir_url( __FILE__ ) );
define( 'BPOFIRM_DS_VER', '0.1.0' );

add_action(
	'wp_enqueue_scripts',
	static function () {
		wp_enqueue_style(
			'bpofirm-design-system',
			BPOFIRM_DS_URL . 'assets/tokens.css',
			array(),
			BPOFIRM_DS_VER
		);
	}
);

/**
 * Auto-apply the .bpo-page body class on Home, About, Contact. Pages in
 * `bpofirm_dark_page_slugs` (filterable) get the dark theme without any
 * per-page edits.
 */
add_filter(
	'body_class',
	static function ( $classes ) {
		$dark_slugs = apply_filters(
			'bpofirm_dark_page_slugs',
			array( 'home', 'front-page', 'about', 'about-us', 'contact', 'contact-us' )
		);

		if ( is_front_page() || is_home() ) {
			$classes[] = 'bpo-page';
			return $classes;
		}

		if ( is_page() ) {
			$slug = get_post_field( 'post_name', get_queried_object_id() );
			if ( in_array( $slug, $dark_slugs, true ) ) {
				$classes[] = 'bpo-page';
			}
		}

		return $classes;
	}
);

/**
 * Opt-in shortcode for pages not covered by the auto-list. Drop
 * [bpofirm_dark_theme] anywhere on the page to force dark theme.
 */
add_shortcode(
	'bpofirm_brand_theme',
	static function () {
		return '<script>document.documentElement.classList.add("bpo-page");document.body&&document.body.classList.add("bpo-page");</script>';
	}
);
