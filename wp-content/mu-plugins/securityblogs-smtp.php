<?php
/**
 * Plugin Name: Security Blogs SMTP
 * Description: Routes all wp_mail() through the cPanel mailbox for info@securityblogs.com.au so contact-form notifications actually deliver. BCCs the same address so a copy of every site email is retained.
 * Version: 1.0.0
 * Author: securityblogs.com.au
 *
 * Deployment:
 *   Add the following constants to wp-config.php (above the "stop editing" line):
 *
 *     define( 'SECURITYBLOGS_SMTP_HOST',      'mail.securityblogs.com.au' );
 *     define( 'SECURITYBLOGS_SMTP_PORT',      465 );          // 465 for SSL, 587 for STARTTLS
 *     define( 'SECURITYBLOGS_SMTP_SECURE',    'ssl' );        // 'ssl' or 'tls'
 *     define( 'SECURITYBLOGS_SMTP_USER',      'info@securityblogs.com.au' );
 *     define( 'SECURITYBLOGS_SMTP_PASS',      'YOUR_MAILBOX_PASSWORD_HERE' );
 *     define( 'SECURITYBLOGS_SMTP_FROM',      'info@securityblogs.com.au' );
 *     define( 'SECURITYBLOGS_SMTP_FROM_NAME', 'Security Blogs' );
 *     define( 'SECURITYBLOGS_SMTP_BCC',       'info@securityblogs.com.au' );
 *     define( 'SECURITYBLOGS_SMTP_DEBUG',     false );        // set true temporarily to log errors
 *
 *   Then upload this file to /wp-content/mu-plugins/ (create the folder if missing).
 *   Must-use plugins auto-activate; nothing to enable in wp-admin.
 *
 * Verify after deploy:
 *   wp-admin → Tools → Site Health → Info → "wp_mail" sends through SMTP, or
 *   install "Check & Log Email" plugin and send a test, or
 *   submit the live contact form and watch info@securityblogs.com.au.
 */

defined( 'ABSPATH' ) || exit;

if ( ! defined( 'SECURITYBLOGS_SMTP_HOST' ) ) {
	define( 'SECURITYBLOGS_SMTP_HOST', 'mail.securityblogs.com.au' );
}
if ( ! defined( 'SECURITYBLOGS_SMTP_PORT' ) ) {
	define( 'SECURITYBLOGS_SMTP_PORT', 465 );
}
if ( ! defined( 'SECURITYBLOGS_SMTP_SECURE' ) ) {
	define( 'SECURITYBLOGS_SMTP_SECURE', 'ssl' );
}
if ( ! defined( 'SECURITYBLOGS_SMTP_USER' ) ) {
	define( 'SECURITYBLOGS_SMTP_USER', 'info@securityblogs.com.au' );
}
if ( ! defined( 'SECURITYBLOGS_SMTP_FROM' ) ) {
	define( 'SECURITYBLOGS_SMTP_FROM', 'info@securityblogs.com.au' );
}
if ( ! defined( 'SECURITYBLOGS_SMTP_FROM_NAME' ) ) {
	define( 'SECURITYBLOGS_SMTP_FROM_NAME', 'Security Blogs' );
}
if ( ! defined( 'SECURITYBLOGS_SMTP_BCC' ) ) {
	define( 'SECURITYBLOGS_SMTP_BCC', 'info@securityblogs.com.au' );
}
if ( ! defined( 'SECURITYBLOGS_SMTP_DEBUG' ) ) {
	define( 'SECURITYBLOGS_SMTP_DEBUG', false );
}

add_action(
	'phpmailer_init',
	function ( $phpmailer ) {
		if ( ! defined( 'SECURITYBLOGS_SMTP_PASS' ) || '' === SECURITYBLOGS_SMTP_PASS ) {
			error_log( 'SECURITYBLOGS_SMTP: SECURITYBLOGS_SMTP_PASS is not defined in wp-config.php; falling back to PHP mail().' );
			return;
		}

		$phpmailer->isSMTP();
		$phpmailer->Host        = SECURITYBLOGS_SMTP_HOST;
		$phpmailer->Port        = (int) SECURITYBLOGS_SMTP_PORT;
		$phpmailer->SMTPAuth    = true;
		$phpmailer->SMTPSecure  = SECURITYBLOGS_SMTP_SECURE;
		$phpmailer->SMTPAutoTLS = true;
		$phpmailer->Username    = SECURITYBLOGS_SMTP_USER;
		$phpmailer->Password    = SECURITYBLOGS_SMTP_PASS;
		$phpmailer->CharSet     = 'UTF-8';

		$phpmailer->setFrom( SECURITYBLOGS_SMTP_FROM, SECURITYBLOGS_SMTP_FROM_NAME, false );

		$bcc = SECURITYBLOGS_SMTP_BCC;
		if ( $bcc && is_email( $bcc ) ) {
			$already_bcc = false;
			foreach ( $phpmailer->getBccAddresses() as $existing ) {
				if ( strcasecmp( $existing[0], $bcc ) === 0 ) {
					$already_bcc = true;
					break;
				}
			}
			$primary_to = '';
			$to_addrs   = $phpmailer->getToAddresses();
			if ( ! empty( $to_addrs ) ) {
				$primary_to = $to_addrs[0][0];
			}
			if ( ! $already_bcc && strcasecmp( $primary_to, $bcc ) !== 0 ) {
				$phpmailer->addBCC( $bcc );
			}
		}

		if ( SECURITYBLOGS_SMTP_DEBUG ) {
			$phpmailer->SMTPDebug = 2;
			$phpmailer->Debugoutput = function ( $str, $level ) {
				error_log( 'SECURITYBLOGS_SMTP[' . $level . ']: ' . trim( $str ) );
			};
		}
	}
);

add_filter(
	'wp_mail_from',
	function ( $from ) {
		return SECURITYBLOGS_SMTP_FROM ? SECURITYBLOGS_SMTP_FROM : $from;
	},
	99
);

add_filter(
	'wp_mail_from_name',
	function ( $name ) {
		return SECURITYBLOGS_SMTP_FROM_NAME ? SECURITYBLOGS_SMTP_FROM_NAME : $name;
	},
	99
);

add_action(
	'wp_mail_failed',
	function ( $error ) {
		if ( is_wp_error( $error ) ) {
			error_log( 'SECURITYBLOGS_SMTP wp_mail_failed: ' . $error->get_error_message() );
		}
	}
);
