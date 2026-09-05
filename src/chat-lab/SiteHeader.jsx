// Copied 1:1 from src/components/layout/TopBar.jsx. In the real app this
// switches between the portfolio and chat views; here "chat" is the only
// view that exists, so it's permanently active. "portfolio" hands off to
// the real site instead of trying to reproduce it, and the music button
// is left inert — porting the ArtistModal is out of scope for this lab.
export default function SiteHeader() {
  return (
    <header className="topbar">
      <div className="tb-mark">
        <span className="glyph">P/</span>
        <div>
          <div className="name">paolo sandejas</div>
          <div className="sub">ai · ml · creative tech</div>
        </div>
      </div>
      <nav className="tb-nav">
        <button className="is-active">
          <span className="dot"></span>
          <span className="tb-label-full">chat / pao-gpt</span>
          <span className="tb-label-short">chat</span>
        </button>
        <button onClick={() => { window.location.href = '/'; }}>
          <span className="dot"></span>
          <span className="tb-label-full">portfolio</span>
          <span className="tb-label-short">portfolio</span>
        </button>
        <button className="tb-nav-music" title="not wired up in this lab">
          <span className="tb-label-full">♪ listen</span>
          <span className="tb-label-short">♪</span>
        </button>
      </nav>
      <div className="tb-meta">
        <div><b>v0.4.1</b> · march 2026</div>
        <div>printed in los angeles, ca</div>
      </div>
    </header>
  );
}
