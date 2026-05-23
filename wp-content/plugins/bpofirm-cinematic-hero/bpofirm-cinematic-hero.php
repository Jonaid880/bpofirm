<?php
/**
 * Plugin Name:       BPO Firm Cinematic Hero
 * Plugin URI:        https://bpofirm.com/
 * Description:       Cinematic intro hero with animated keypad → "Access Granted" → interior reveal, inspired by the octaboot.lb Reel and brand-adapted (red accent, golden vignette). Shortcode: [bpofirm_cinematic_hero ...].
 * Version:           0.1.0
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
define( 'BPOFIRM_CINE_VER', '0.1.0' );

add_action(
	'wp_enqueue_scripts',
	static function () {
		wp_register_style(
			'bpofirm-cinematic-hero',
			BPOFIRM_CINE_URL . 'assets/cinematic-hero.css',
			array(),
			BPOFIRM_CINE_VER
		);
	}
);

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
				'code'                 => '1300',
				'access_label'         => 'Access Granted',
				'bg_exterior'          => '',
				'bg_interior'          => '',
				'loop'                 => '0',
			),
			$atts,
			'bpofirm_cinematic_hero'
		);

		wp_enqueue_style( 'bpofirm-cinematic-hero' );

		// Build the 4-digit code as data-step keys so the choreography
		// matches whatever owner sets in the shortcode.
		$code = preg_replace( '/\D/', '', (string) $atts['code'] );
		if ( strlen( $code ) !== 4 ) {
			$code = '1300';
		}
		$code_digits = str_split( $code );

		$variant_class = ( '1' === (string) $atts['loop'] ) ? ' bpo-cine--loop' : ' bpo-cine--once';

		$inline_vars = '';
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
			class="bpo-cine<?php echo esc_attr( $variant_class ); ?>"
			<?php if ( $inline_vars ) : ?>style="<?php echo esc_attr( $inline_vars ); ?>"<?php endif; ?>
		>
			<div class="bpo-cine__bg bpo-cine__bg--exterior" aria-hidden="true"></div>
			<div class="bpo-cine__bg bpo-cine__bg--interior" aria-hidden="true"></div>
			<div class="bpo-cine__vignette" aria-hidden="true"></div>

			<div class="bpo-cine__stage" aria-hidden="true">
				<div class="bpo-cine__keypad">
					<div class="bpo-cine__display">
						<?php foreach ( $code_digits as $d ) : ?>
							<span class="digit"><?php echo esc_html( $d ); ?></span>
						<?php endforeach; ?>
					</div>
					<div class="bpo-cine__keys">
						<?php foreach ( $keys as $k ) :
							$step = array_search( $k, $code_digits, true );
							// array_search returns the first match — if a digit
							// appears twice (e.g. '0' in '1300'), step the second
							// press by detecting duplicates and assigning incrementally.
							?>
							<div class="bpo-cine__key<?php echo ( false !== $step ) ? ' is-active' : ''; ?>"<?php
								if ( false !== $step ) {
									echo ' data-step="' . ( $step + 1 ) . '"';
								}
							?>><?php echo esc_html( $k ); ?></div>
						<?php endforeach; ?>
					</div>
				</div>
				<div class="bpo-cine__granted"><?php echo esc_html( $atts['access_label'] ); ?></div>
			</div>

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
