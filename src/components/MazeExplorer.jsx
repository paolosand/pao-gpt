import { motion } from 'framer-motion';
import './MazeExplorer.css';

const MazeExplorer = ({ onExit }) => {
  return (
    <motion.div
      className="maze-explorer"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="maze-header">
        <button className="maze-exit" onClick={onExit}>
          ← Exit Maze
        </button>
        <div className="maze-title">Interactive Portfolio Explorer</div>
        <div className="maze-controls">
          <span>Controls: WASD or Arrow Keys</span>
        </div>
      </div>

      <div className="maze-canvas-container">
        <div className="maze-placeholder">
          <h2>🎮 Maze Explorer Coming Soon</h2>
          <p>
            This interactive p5.js maze experience is currently under construction.
            <br />
            It will feature:
          </p>
          <ul>
            <li>Top-down dungeon-style navigation</li>
            <li>Rooms for each project and experience</li>
            <li>Interactive content discovery</li>
            <li>Smooth animations with GSAP</li>
          </ul>
          <button className="maze-return-btn" onClick={onExit}>
            Return to Portfolio
          </button>
        </div>
      </div>

      <div className="maze-minimap">
        <div className="minimap-title">Map</div>
        <div className="minimap-placeholder">
          [Minimap will appear here]
        </div>
      </div>
    </motion.div>
  );
};

export default MazeExplorer;
