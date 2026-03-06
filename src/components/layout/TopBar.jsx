import './TopBar.css';

export default function TopBar({ currentView, onViewChange, onContactClick }) {
  return (
    <div className="top-bar">
      <div className="top-bar-left">
        <div className="brand">pao-gpt</div>
      </div>

      <div className="top-bar-center">
        <button
          className={`view-toggle ${currentView === 'chat' ? 'active' : ''}`}
          onClick={() => onViewChange('chat')}
        >
          💬 Chat
        </button>
        <button
          className={`view-toggle ${currentView === 'portfolio' ? 'active' : ''}`}
          onClick={() => onViewChange('portfolio')}
        >
          📋 Portfolio
        </button>
        <button
          className={`view-toggle ${currentView === 'graph' ? 'active' : ''}`}
          onClick={() => onViewChange('graph')}
        >
          🕸️ Graph
        </button>
      </div>

      <div className="top-bar-right">
        <button className="icon-btn" onClick={onContactClick} aria-label="Contact info">
          ℹ️
        </button>
      </div>
    </div>
  );
}
