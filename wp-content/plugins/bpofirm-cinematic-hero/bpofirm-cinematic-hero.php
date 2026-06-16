<?php
/**
 * Plugin Name:       BPO Firm Cinematic Hero
 * Plugin URI:        https://bpofirm.com/
 * Description:       Scroll-driven zoom hero with an interactive 4-digit keypad. Visitor scrolls to zoom in on the keypad, enters the code, sees the interior reveal. Per-office colour theming via shortcode attributes. Shortcode: [bpofirm_cinematic_hero ...].
 * Version:           0.2.0
 * Requires at least: 6.4
 * Requires PHP:      7.4
 * Author:            BPO Firm
 * License:           GPL-2.0-or-later
 * Text Domain:       bpofirm-cinematic-hero
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'BPOFIRM_CINE_URL', plugin_dir_url( __FILE__ ) );
define( 'BPOFIRM_CINE_VER', '0.2.0' );

add_action(
	'wp_enqueue_scripts',
	static function () {
		wp_register_style(
			'bpofirm-cinematic-hero',
			BPOFIRM_CINE_URL . 'assets/cinematic-hero.css',
			array(),
			BPOFIRM_CINE_VER
		);
		wp_register_script(
			'bpofirm-cinematic-hero',
			BPOFIRM_CINE_URL . 'assets/cinematic-hero.js',
			array(),
			BPOFIRM_CINE_VER,
			true
		);
	}
);

/**
 * Per-office colour theme presets — maps a friendly name to the
 * `--bpo-cine-accent-rgb` triplet (used for keypad glow, vignette
 * tint, hint text, granted badge).
 */
function bpofirm_cine_theme_preset( $name ) {
	$presets = array(
		'warm'    => '255, 195, 100',  // default golden — luxury, hospitality
		'orange'  => '255, 140, 50',   // matches office #5 (orange creative studio)
		'blue'    => '120, 170, 255',  // matches office #2 (blue corporate)
		'sketch'  => '200, 210, 230',  // matches office #3 (sketch render — cool neutral)
		'social'  => '255, 80, 130',   // matches office #1 (social-media office)
		'modern'  => '160, 130, 200',  // matches office #4 (modern pods)
		'red'     => '239, 73, 75',    // brand red itself
	);
	$name = strtolower( (string) $name );
	return isset( $presets[ $name ] ) ? $presets[ $name ] : '';
}

/**
 * Render an inline-coloured title: words wrapped in pipes become the
 * brand-red italic highlight, e.g. "Welcome inside |BPO Firm|."
 */
function bpofirm_cine_render_title( $raw ) {
	$out = '';
	$parts = preg_split( '/(\|[^|]+\|)/u', (string) $raw, -1, PREG_SPLIT_DELIM_CAPTURE | PREG_SPLIT_NO_EMPTY );
	foreach ( $parts as $p ) {
		if ( strlen( $p ) >= 2 && $p[0] === '|' && substr( $p, -1 ) === '|' ) {
			$out .= '<em>' . esc_html( substr( $p, 1, -1 ) ) . '</em>';
		} else {
			$out .= esc_html( $p );
		}
	}
	return $out;
}

add_shortcode(
	'bpofirm_cinematic_hero',
	static function ( $atts ) {
		$atts = shortcode_atts(
			array(
				'title'                => 'Welcome inside |BPO Firm|.',
				'eyebrow'              => 'A partnership unlocked',
				'lede'                 => 'Calls. Chats. Social. AI assists. Every channel — orchestrated under one roof. Plug your stack in once; ship outcomes from day one.',
				'cta_primary_label'    => 'Book a discovery call',
				'cta_primary_url'      => '/contact-us/',
				'cta_secondary_label'  => 'See our work',
				'cta_secondary_url'    => '/services/',
				'password'             => '1234',
				'access_label'         => 'Access Granted',
				'hint_scroll'          => 'Scroll to approach',
				'hint_enter'           => 'Enter the code',
				'bg_exterior'          => '',
				'bg_interior'          => '',
				'theme'                => '',
				'accent_rgb'           => '',
			),
			$atts,
			'bpofirm_cinematic_hero'
		);

		wp_enqueue_style( 'bpofirm-cinematic-hero' );
		wp_enqueue_script( 'bpofirm-cinematic-hero' );

		$password = preg_replace( '/\D/', '', (string) $atts['password'] );
		if ( strlen( $password ) !== 4 ) {
			$password = '1234';
		}

		// Resolve colour theme — explicit accent_rgb wins, then theme preset, then default.
		$accent = trim( (string) $atts['accent_rgb'] );
		if ( ! $accent && $atts['theme'] ) {
			$accent = bpofirm_cine_theme_preset( $atts['theme'] );
		}

		$inline_vars = '';
		if ( $accent ) {
			$inline_vars .= '--bpo-cine-accent-rgb:' . esc_attr( $accent ) . ';';
		}
		if ( $atts['bg_exterior'] ) {
			$inline_vars .= '--bpo-cine-exterior:url(' . esc_url_raw( $atts['bg_exterior'] ) . ');';
		}
		if ( $atts['bg_interior'] ) {
			$inline_vars .= '--bpo-cine-interior:url(' . esc_url_raw( $atts['bg_interior'] ) . ');';
		}

		$keys = array( '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#' );

		ob_start();
		?>
		<section
			class="bpo-cine"
			data-bpo-password="<?php echo esc_attr( $password ); ?>"
			<?php if ( $inline_vars ) : ?>style="<?php echo esc_attr( $inline_vars ); ?>"<?php endif; ?>
		>
			<div class="bpo-cine__bg bpo-cine__bg--exterior" aria-hidden="true"></div>
			<div class="bpo-cine__bg bpo-cine__bg--interior" aria-hidden="true"></div>
			<div class="bpo-cine__vignette" aria-hidden="true"></div>

			<div class="bpo-cine__stage">
				<div class="bpo-cine__keypad">
					<div class="bpo-cine__display" aria-label="<?php esc_attr_e( 'Code entry' ); ?>">
						<span class="digit">·</span>
						<span class="digit">·</span>
						<span class="digit">·</span>
						<span class="digit">·</span>
					</div>
					<div class="bpo-cine__keys" role="group" aria-label="<?php esc_attr_e( 'Keypad' ); ?>">
						<?php foreach ( $keys as $k ) : ?>
							<button
								type="button"
								class="bpo-cine__key"
								data-value="<?php echo esc_attr( $k ); ?>"
								tabindex="-1"
							><?php echo esc_html( $k ); ?></button>
						<?php endforeach; ?>
					</div>
				</div>
				<div class="bpo-cine__granted" aria-live="polite"><?php echo esc_html( $atts['access_label'] ); ?></div>
			</div>

			<?php if ( $atts['hint_scroll'] ) : ?>
				<div class="bpo-cine__hint"><?php echo esc_html( $atts['hint_scroll'] ); ?></div>
			<?php endif; ?>
			<?php if ( $atts['hint_enter'] ) : ?>
				<div class="bpo-cine__hint-2"><?php echo esc_html( $atts['hint_enter'] ); ?></div>
			<?php endif; ?>

			<div class="bpo-cine__content">
				<?php if ( $atts['eyebrow'] ) : ?>
					<p class="bpo-cine__eyebrow"><?php echo esc_html( $atts['eyebrow'] ); ?></p>
				<?php endif; ?>
				<h1 class="bpo-cine__title"><?php echo bpofirm_cine_render_title( $atts['title'] ); ?></h1>
				<?php if ( $atts['lede'] ) : ?>
					<p class="bpo-cine__lede"><?php echo esc_html( $atts['lede'] ); ?></p>
				<?php endif; ?>
				<?php if ( $atts['cta_primary_label'] || $atts['cta_secondary_label'] ) : ?>
					<div class="bpo-cine__ctas">
						<?php if ( $atts['cta_primary_label'] ) : ?>
							<a href="<?php echo esc_url( $atts['cta_primary_url'] ); ?>" class="bpo-cine__btn bpo-cine__btn--solid"><?php echo esc_html( $atts['cta_primary_label'] ); ?></a>
						<?php endif; ?>
						<?php if ( $atts['cta_secondary_label'] ) : ?>
							<a href="<?php echo esc_url( $atts['cta_secondary_url'] ); ?>" class="bpo-cine__btn bpo-cine__btn--outline"><?php echo esc_html( $atts['cta_secondary_label'] ); ?></a>
						<?php endif; ?>
					</div>
				<?php endif; ?>
			</div>
		</section>
		<?php
		return ob_get_clean();
	}
);
