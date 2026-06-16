/* BPO Firm — Cinematic Hero (v2)
 * Scroll-driven zoom + interactive password entry.
 *
 * Behaviour:
 *  1. On page load, .bpo-cine sections register. Each one locks page
 *     scroll while it's the active hero and drives a 0..1 zoom value
 *     from wheel / touch deltas (same pattern as bpofirm-scroll-hero).
 *  2. Once zoom hits 1.0, the keypad becomes interactive. Hint text
 *     swaps from "Scroll to enter" -> "Enter the code".
 *  3. Clicking the keypad buttons fills the 4-digit display.
 *  4. When 4 digits are entered:
 *       correct  -> .is-granted -> interior reveal + scroll unlocked
 *       wrong    -> .is-error -> shake + clear, allow retry
 *  5. Once granted, scroll behaves normally and the user proceeds to
 *     the rest of the page.
 *
 * The expected password is read from data-bpo-password on the root
 * (set by the PHP shortcode). Defaults to "1234".
 */
(function () {
	'use strict';

	var WHEEL_SENS    = 0.0012;
	var TOUCH_SENS    = 0.006;
	var ERROR_HOLD_MS = 700;

	function clamp01(n) { return n < 0 ? 0 : n > 1 ? 1 : n; }

	function init(root) {
		if (root.__bpoCineInit) return;
		root.__bpoCineInit = true;

		var password = (root.getAttribute('data-bpo-password') || '1234').replace(/\D/g, '');
		if (password.length !== 4) password = '1234';

		var keys     = root.querySelectorAll('.bpo-cine__key');
		var digits   = root.querySelectorAll('.bpo-cine__display .digit');
		var state = {
			zoom: 0,
			zoomed: false,
			granted: false,
			entered: '',
			touchStartY: 0,
		};

		function render() {
			root.style.setProperty('--bpo-cine-zoom', state.zoom);
			root.classList.toggle('is-zoomed', state.zoomed);
			root.classList.toggle('is-granted', state.granted);
		}

		function setZoom(z) {
			state.zoom = clamp01(z);
			var wasZoomed = state.zoomed;
			state.zoomed = state.zoom >= 1;
			if (state.zoomed && !wasZoomed) {
				resetEntered();
			}
			render();
		}

		function resetEntered() {
			state.entered = '';
			for (var i = 0; i < digits.length; i++) {
				digits[i].classList.remove('is-filled');
				digits[i].textContent = '·';
			}
		}

		function pressKey(value) {
			if (state.granted || !state.zoomed) return;
			if (state.entered.length >= 4) return;
			var idx = state.entered.length;
			state.entered += value;
			if (digits[idx]) {
				digits[idx].classList.add('is-filled');
				digits[idx].textContent = value;
			}
			if (state.entered.length === 4) {
				if (state.entered === password) {
					setTimeout(grant, 220);
				} else {
					flashError();
				}
			}
		}

		function grant() {
			state.granted = true;
			render();
		}

		function flashError() {
			root.classList.add('is-error');
			setTimeout(function () {
				root.classList.remove('is-error');
				resetEntered();
			}, ERROR_HOLD_MS);
		}

		// --- Scroll-hijack: wheel + touch drive zoom while not granted
		function onWheel(e) {
			if (state.granted) return;
			if (state.zoomed && e.deltaY < 0 && window.scrollY <= 5) {
				// Scrolling up while at zoom=1 reverses out (rare; matches scroll-hero UX).
				setZoom(0.95);
				e.preventDefault();
				return;
			}
			if (!state.zoomed) {
				e.preventDefault();
				setZoom(state.zoom + e.deltaY * WHEEL_SENS);
			}
			// At zoomed && deltaY > 0: do not preventDefault — allow page scroll past
			// once granted. Until granted we still block to keep them at the keypad.
			if (state.zoomed && !state.granted) {
				e.preventDefault();
			}
		}

		function onTouchStart(e) { state.touchStartY = e.touches[0].clientY; }
		function onTouchMove(e) {
			if (state.granted || !state.touchStartY) return;
			var y = e.touches[0].clientY;
			var dy = state.touchStartY - y;
			if (state.zoomed && dy < -20 && window.scrollY <= 5) {
				setZoom(0.95);
				e.preventDefault();
				return;
			}
			if (!state.zoomed) {
				e.preventDefault();
				setZoom(state.zoom + dy * TOUCH_SENS);
				state.touchStartY = y;
			} else {
				e.preventDefault();
			}
		}
		function onTouchEnd() { state.touchStartY = 0; }

		function onScroll() {
			if (!state.granted) window.scrollTo(0, 0);
		}

		// Wire up keypad clicks (always listening; pressKey gates on state).
		for (var i = 0; i < keys.length; i++) {
			(function (k) {
				k.addEventListener('click', function () {
					var v = k.getAttribute('data-value') || k.textContent.trim();
					if (/^\d$/.test(v)) pressKey(v);
				});
			})(keys[i]);
		}

		window.addEventListener('wheel',      onWheel,      { passive: false });
		window.addEventListener('touchstart', onTouchStart, { passive: false });
		window.addEventListener('touchmove',  onTouchMove,  { passive: false });
		window.addEventListener('touchend',   onTouchEnd);
		window.addEventListener('scroll',     onScroll);

		resetEntered();
		render();

		// Honour prefers-reduced-motion: skip the keypad gate entirely.
		if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
			state.zoomed = true;
			state.granted = true;
			render();
		}
	}

	function bootstrap() {
		var nodes = document.querySelectorAll('.bpo-cine');
		for (var i = 0; i < nodes.length; i++) init(nodes[i]);
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', bootstrap);
	} else {
		bootstrap();
	}
})();
