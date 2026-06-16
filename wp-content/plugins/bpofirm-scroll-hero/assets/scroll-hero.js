/* BPO Firm — Scroll-Expand Hero
 * Vanilla JS port of the ScrollExpandMedia React component.
 * Hijacks wheel + touch to drive a 0..1 progress value, which inflates
 * the centered media block from 300x400 to ~1550x800 (desktop) /
 * ~950x600 (mobile), fades the background out, and reveals the inner
 * content once fully expanded.
 *
 * Reverses if the user wheels/swipes up while already expanded and
 * scrolled to the top of the page.
 */
(function () {
	'use strict';

	var WHEEL_SENSITIVITY = 0.0009;
	var TOUCH_SENSITIVITY_FWD = 0.005;
	var TOUCH_SENSITIVITY_BACK = 0.008;
	var COLLAPSE_THRESHOLD = 0.75;
	var MOBILE_BREAKPOINT = 768;

	function isMobile() {
		return window.innerWidth < MOBILE_BREAKPOINT;
	}

	function clamp01(n) {
		if (n < 0) return 0;
		if (n > 1) return 1;
		return n;
	}

	function init(root) {
		if (root.__bpoScrollHeroInit) return;
		root.__bpoScrollHeroInit = true;

		// Static mode opts out of scroll hijack entirely — the section
		// just sits there as a normal banner and the page scrolls past.
		if (root.classList.contains('bpo-scroll-hero--static')) return;

		var mediaType = root.getAttribute('data-media-type') || 'image';
		var overlayBase = mediaType === 'video' ? 0.5 : 0.7;

		var state = {
			progress: 0,
			fullyExpanded: false,
			touchStartY: 0,
		};

		function render() {
			var m = isMobile();
			var width = 300 + state.progress * (m ? 650 : 1250);
			var height = 400 + state.progress * (m ? 200 : 400);
			var tx = state.progress * (m ? 180 : 150);

			root.style.setProperty('--bpo-media-w', width + 'px');
			root.style.setProperty('--bpo-media-h', height + 'px');
			root.style.setProperty('--bpo-text-tx', tx);
			root.style.setProperty('--bpo-bg-opacity', 1 - state.progress);
			root.style.setProperty('--bpo-overlay-opacity', overlayBase - state.progress * 0.3);

			root.classList.toggle('is-expanded', state.fullyExpanded);
		}

		function updateProgress(delta) {
			state.progress = clamp01(state.progress + delta);
			if (state.progress >= 1) {
				state.fullyExpanded = true;
			} else if (state.progress < COLLAPSE_THRESHOLD) {
				state.fullyExpanded = false;
			}
			render();
		}

		function onWheel(e) {
			if (state.fullyExpanded && e.deltaY < 0 && window.scrollY <= 5) {
				state.fullyExpanded = false;
				state.progress = 0.99;
				e.preventDefault();
				render();
				return;
			}
			if (!state.fullyExpanded) {
				e.preventDefault();
				updateProgress(e.deltaY * WHEEL_SENSITIVITY);
			}
		}

		function onTouchStart(e) {
			state.touchStartY = e.touches[0].clientY;
		}

		function onTouchMove(e) {
			if (!state.touchStartY) return;
			var y = e.touches[0].clientY;
			var deltaY = state.touchStartY - y;

			if (state.fullyExpanded && deltaY < -20 && window.scrollY <= 5) {
				state.fullyExpanded = false;
				state.progress = 0.99;
				e.preventDefault();
				render();
				return;
			}
			if (!state.fullyExpanded) {
				e.preventDefault();
				var factor = deltaY < 0 ? TOUCH_SENSITIVITY_BACK : TOUCH_SENSITIVITY_FWD;
				updateProgress(deltaY * factor);
				state.touchStartY = y;
			}
		}

		function onTouchEnd() {
			state.touchStartY = 0;
		}

		function onScroll() {
			if (!state.fullyExpanded) {
				window.scrollTo(0, 0);
			}
		}

		window.addEventListener('wheel', onWheel, { passive: false });
		window.addEventListener('touchstart', onTouchStart, { passive: false });
		window.addEventListener('touchmove', onTouchMove, { passive: false });
		window.addEventListener('touchend', onTouchEnd);
		window.addEventListener('scroll', onScroll);
		window.addEventListener('resize', render);

		render();
	}

	function bootstrap() {
		var nodes = document.querySelectorAll('.bpo-scroll-hero');
		for (var i = 0; i < nodes.length; i++) {
			init(nodes[i]);
		}
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', bootstrap);
	} else {
		bootstrap();
	}
})();
