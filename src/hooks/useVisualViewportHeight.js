import { useEffect } from 'react';

// iOS Safari resizes window.visualViewport when the on-screen keyboard opens
// but doesn't sync 100dvh in the same tick, leaving a stray gap under the
// chat input. Mirror the real visible height into a CSS var so the chat
// shell can track it directly instead of trusting dvh alone.
export function useVisualViewportHeight() {
  useEffect(() => {
    const vv = window.visualViewport;
    if (!vv) return;

    const sync = () => {
      document.documentElement.style.setProperty('--vvh', `${vv.height}px`);
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
