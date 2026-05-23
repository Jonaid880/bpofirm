<?php
/**
 * Plugin Name:       BPO Firm Service-Page Blocks
 * Plugin URI:        https://bpofirm.com/
 * Description:       Service-page blocks for bpofirm.com — scroll-expand hero ([bpofirm_scroll_hero]) and integrations carousel ([bpofirm_integrations]). Drop into any Elementor Shortcode widget. See /reference/scroll-hero-rollout.md for per-page snippets.
 * Version:           0.2.0
 * Requires at least: 6.4
 * Requires PHP:      7.4
 * Author:            BPO Firm
 * License:           GPL-2.0-or-later
 * Text Domain:       bpofirm-scroll-hero
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'BPOFIRM_SCROLL_HERO_URL', plugin_dir_url( __FILE__ ) );
define( 'BPOFIRM_SCROLL_HERO_VER', '0.2.0' );

add_action(
	'wp_enqueue_scripts',
	static function () {
		wp_register_style(
			'bpofirm-scroll-hero',
			BPOFIRM_SCROLL_HERO_URL . 'assets/scroll-hero.css',
			array(),
			BPOFIRM_SCROLL_HERO_VER
		);
		wp_register_script(
			'bpofirm-scroll-hero',
			BPOFIRM_SCROLL_HERO_URL . 'assets/scroll-hero.js',
			array(),
			BPOFIRM_SCROLL_HERO_VER,
			true
		);
		wp_register_style(
			'bpofirm-integrations',
			BPOFIRM_SCROLL_HERO_URL . 'assets/integrations.css',
			array(),
			BPOFIRM_SCROLL_HERO_VER
		);
	}
);

/**
 * Default Flaticon icon set used by the integrations carousel. Owner can
 * override per-page via the `icons_row1` / `icons_row2` shortcode atts.
 */
function bpofirm_scroll_hero_default_icons() {
	return array(
		'row1' => array(
			'https://cdn-icons-png.flaticon.com/512/5968/5968854.png',
			'https://cdn-icons-png.flaticon.com/512/732/732221.png',
			'https://cdn-icons-png.flaticon.com/512/733/733609.png',
			'https://cdn-icons-png.flaticon.com/512/732/732084.png',
			'https://cdn-icons-png.flaticon.com/512/733/733585.png',
			'https://cdn-icons-png.flaticon.com/512/281/281763.png',
			'https://cdn-icons-png.flaticon.com/512/888/888879.png',
		),
		'row2' => array(
			'https://cdn-icons-png.flaticon.com/512/174/174857.png',
			'https://cdn-icons-png.flaticon.com/512/906/906324.png',
			'https://cdn-icons-png.flaticon.com/512/888/888841.png',
			'https://cdn-icons-png.flaticon.com/512/5968/5968875.png',
			'https://cdn-icons-png.flaticon.com/512/906/906361.png',
			'https://cdn-icons-png.flaticon.com/512/732/732190.png',
			'https://cdn-icons-png.flaticon.com/512/888/888847.png',
		),
	);
}

add_shortcode(
	'bpofirm_scroll_hero',
	static function ( $atts, $content = '' ) {
		$atts = shortcode_atts(
			array(
				'title'        => '',
				'media_type'   => 'image',
				'media_src'    => 'https://bpofirm.com/wp-content/uploads/Partner-with-BPO-Firm.webp',
				'poster'       => '',
				'bg_src'       => 'https://bpofirm.com/wp-content/uploads/2026/01/vecteezy_dotted-world-map_1198050-1024x491.png',
				'date'         => '',
				'scroll_label' => 'Scroll to Expand',
				'text_blend'   => '1',
				'static'       => '0',
			),
			$atts,
			'bpofirm_scroll_hero'
		);

		wp_enqueue_style( 'bpofirm-scroll-hero' );
		wp_enqueue_script( 'bpofirm-scroll-hero' );

		$title = trim( (string) $atts['title'] );
		$parts = preg_split( '/\s+/', $title, 2 );
		$first = $parts[0] ?? '';
		$rest  = $parts[1] ?? '';

		$blend_class  = ( '1' === (string) $atts['text_blend'] ) ? ' bpo-scroll-hero--text-blend' : '';
		$static_class = ( '1' === (string) $atts['static'] ) ? ' bpo-scroll-hero--static' : '';
		$is_youtube   = $atts['media_src'] && false !== strpos( $atts['media_src'], 'youtube.com' );

		ob_start();
		?>
		<section
			class="bpo-scroll-hero<?php echo esc_attr( $blend_class . $static_class ); ?>"
			data-media-type="<?php echo esc_attr( $atts['media_type'] ); ?>"
		>
			<?php if ( $atts['bg_src'] ) : ?>
				<img class="bpo-scroll-hero__bg" src="<?php echo esc_url( $atts['bg_src'] ); ?>" alt="" />
				<div class="bpo-scroll-hero__bg-tint" aria-hidden="true"></div>
			<?php endif; ?>

			<div class="bpo-scroll-hero__stage">
				<div class="bpo-scroll-hero__media">
					<?php if ( 'video' === $atts['media_type'] && $atts['media_src'] ) : ?>
						<?php if ( $is_youtube ) : ?>
							<iframe
								src="<?php echo esc_url( $atts['media_src'] ); ?><?php echo ( false !== strpos( $atts['media_src'], '?' ) ? '&' : '?' ); ?>autoplay=1&mute=1&loop=1&controls=0&showinfo=0&rel=0&disablekb=1&modestbranding=1"
								allow="autoplay; encrypted-media; picture-in-picture"
								frameborder="0"
								allowfullscreen
							></iframe>
						<?php else : ?>
							<video
								src="<?php echo esc_url( $atts['media_src'] ); ?>"
								<?php if ( $atts['poster'] ) : ?>poster="<?php echo esc_url( $atts['poster'] ); ?>"<?php endif; ?>
								autoplay muted loop playsinline preload="auto"
								disablepictureinpicture disableremoteplayback
							></video>
						<?php endif; ?>
					<?php elseif ( $atts['media_src'] ) : ?>
						<img src="<?php echo esc_url( $atts['media_src'] ); ?>" alt="<?php echo esc_attr( $title ); ?>" />
					<?php endif; ?>
					<div class="bpo-scroll-hero__media-overlay" aria-hidden="true"></div>
				</div>

				<?php if ( $first || $rest ) : ?>
					<div class="bpo-scroll-hero__title">
						<?php if ( $first ) : ?>
							<h1 class="bpo-scroll-hero__title-first"><?php echo esc_html( $first ); ?></h1>
						<?php endif; ?>
						<?php if ( $rest ) : ?>
							<h1 class="bpo-scroll-hero__title-rest"><?php echo esc_html( $rest ); ?></h1>
						<?php endif; ?>
					</div>
				<?php endif; ?>

				<?php if ( $atts['date'] || $atts['scroll_label'] ) : ?>
					<div class="bpo-scroll-hero__caption">
						<?php if ( $atts['date'] ) : ?>
							<p class="bpo-scroll-hero__date"><?php echo esc_html( $atts['date'] ); ?></p>
						<?php endif; ?>
						<?php if ( $atts['scroll_label'] ) : ?>
							<p class="bpo-scroll-hero__scroll-label"><?php echo esc_html( $atts['scroll_label'] ); ?></p>
						<?php endif; ?>
					</div>
				<?php endif; ?>
			</div>

			<?php if ( $content ) : ?>
				<div class="bpo-scroll-hero__content"><?php echo do_shortcode( $content ); ?></div>
			<?php endif; ?>
		</section>
		<?php
		return ob_get_clean();
	}
);

/**
 * [bpofirm_integrations] — two-row infinite icon carousel that
 * appears directly under the main banner on each service page.
 */
add_shortcode(
	'bpofirm_integrations',
	static function ( $atts ) {
		$defaults = bpofirm_scroll_hero_default_icons();

		$atts = shortcode_atts(
			array(
				'badge'       => '⚡ Integrations',
				'title'       => 'Plays well with your stack',
				'description' => 'Bring your CRM, helpdesk and telephony — we plug into your existing tools and start shipping outcomes from day one.',
				'cta_label'   => 'Talk to our team',
				'cta_url'     => '/contact-us/',
				'icons_row1'  => implode( ',', $defaults['row1'] ),
				'icons_row2'  => implode( ',', $defaults['row2'] ),
				'repeat'      => 4,
			),
			$atts,
			'bpofirm_integrations'
		);

		wp_enqueue_style( 'bpofirm-integrations' );

		$repeat = max( 2, (int) $atts['repeat'] );

		$parse_icons = static function ( $csv ) {
			return array_values(
				array_filter(
					array_map( 'trim', explode( ',', (string) $csv ) ),
					static function ( $u ) {
						return '' !== $u;
					}
				)
			);
		};

		$row1 = $parse_icons( $atts['icons_row1'] );
		$row2 = $parse_icons( $atts['icons_row2'] );

		if ( ! $row1 ) {
			$row1 = $defaults['row1'];
		}
		if ( ! $row2 ) {
			$row2 = $defaults['row2'];
		}

		$render_track = static function ( $icons, $repeat ) {
			$out = '';
			for ( $i = 0; $i < $repeat; $i++ ) {
				foreach ( $icons as $url ) {
					$out .= '<div class="bpo-integrations__chip"><img src="' . esc_url( $url ) . '" alt="" loading="lazy" /></div>';
				}
			}
			return $out;
		};

		ob_start();
		?>
		<section class="bpo-integrations">
			<div class="bpo-integrations__grid-bg" aria-hidden="true"></div>
			<div class="bpo-integrations__inner">
				<?php if ( $atts['badge'] ) : ?>
					<span class="bpo-integrations__badge"><?php echo esc_html( $atts['badge'] ); ?></span>
				<?php endif; ?>
				<?php if ( $atts['title'] ) : ?>
					<h2 class="bpo-integrations__title"><?php echo esc_html( $atts['title'] ); ?></h2>
				<?php endif; ?>
				<?php if ( $atts['description'] ) : ?>
					<p class="bpo-integrations__lede"><?php echo esc_html( $atts['description'] ); ?></p>
				<?php endif; ?>
				<?php if ( $atts['cta_label'] && $atts['cta_url'] ) : ?>
					<a class="bpo-integrations__cta" href="<?php echo esc_url( $atts['cta_url'] ); ?>"><?php echo esc_html( $atts['cta_label'] ); ?></a>
				<?php endif; ?>

				<div class="bpo-integrations__carousel" aria-label="Supported integrations">
					<div class="bpo-integrations__row bpo-integrations__row--left">
						<div class="bpo-integrations__track">
							<?php echo $render_track( $row1, $repeat ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
						</div>
					</div>
					<div class="bpo-integrations__row bpo-integrations__row--right">
						<div class="bpo-integrations__track">
							<?php echo $render_track( $row2, $repeat ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
						</div>
					</div>
					<div class="bpo-integrations__fade bpo-integrations__fade--left" aria-hidden="true"></div>
					<div class="bpo-integrations__fade bpo-integrations__fade--right" aria-hidden="true"></div>
				</div>
			</div>
		</section>
		<?php
		return ob_get_clean();
	}
);
