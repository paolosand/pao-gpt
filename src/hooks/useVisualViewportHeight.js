import { useEffect } from 'react';

// KEYBOARD_THRESHOLD_PX must clear iOS 26's known ~24px visualViewport/
// innerHeight residual gap after the keyboard closes, so a closed keyboard
// never gets misread as open.
const KEYBOARD_THRESHOLD_PX = 100;

// iOS Safari resizes window.visualViewport when the on-screen keyboard opens
// but doesn't sync 100dvh in the same tick, leaving a stray gap under the
// chat input while the keyboard is up. Only override height with the real
// visible height while a keyboard is actually compressing the viewport;
// otherwise defer to 100dvh, which already handles Safari's toolbar
// show/hide reliably and natively. Overriding unconditionally fights that
// native behavior — visualViewport doesn't reliably fire a resize event for
// every toolbar transition, so an always-on override can get stuck on a
// stale (too-short) value and push the input off-screen with nothing to
// scroll it back into view.
export function useVisualViewportHeight() {
  useEffect(() => {
    const vv = window.visualViewport;
    if (!vv) return;

    const sync = () => {
      const keyboardOpen = window.innerHeight - vv.height > KEYBOARD_THRESHOLD_PX;
      if (keyboardOpen) {
        document.documentElement.style.setProperty('--vvh', `${vv.height}px`);
      } else {
        document.documentElement.style.removeProperty('--vvh');
      }
    };

    sync();
    vv.addEventListener('resize', sync);
    vv.addEventListener('scroll', sync);
    return () => {
      vv.removeEventListener('resize', sync);
      vv.removeEventListener('scroll', sync);
      document.documentElement.style.removeProperty('--vvh');
    };
  }, []);
}
