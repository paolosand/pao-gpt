import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import TopBar from './components/layout/TopBar';
import ChatInterface from './components/chat/ChatInterface';
import KnowledgeGraph from './components/graph/KnowledgeGraph';
import Navigation from './components/Navigation';
import Hero from './components/Hero';
import Projects from './components/Projects';
import Skills from './components/Skills';
import Experience from './components/Experience';
import Education from './components/Education';
import Contact from './components/Contact';
import MazeExplorer from './components/MazeExplorer';
import './styles/chatgpt-theme.css';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('chat');
  const [showMaze, setShowMaze] = useState(false);
  const [showContactModal, setShowContactModal] = useState(false);

  return (
    <div className="app">
      <TopBar
        currentView={currentView}
        onViewChange={setCurrentView}
        onContactClick={() => setShowContactModal(true)}
      />

      {currentView === 'chat' && <ChatInterface />}

      {currentView === 'portfolio' && (
        <AnimatePresence mode="wait">
          {showMaze ? (
            <MazeExplorer key="maze" onExit={() => setShowMaze(false)} />
          ) : (
            <motion.div
              key="portfolio"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5 }}
              style={{ marginTop: '60px' }}
            >
              <Navigation />
              <main>
                <Hero onExploreMaze={() => setShowMaze(true)} />
                <Projects />
                <Skills />
                <Experience />
                <Education />
                <Contact />
              </main>
            </motion.div>
          )}
        </AnimatePresence>
      )}

      {currentView === 'graph' && <KnowledgeGraph />}

      {showContactModal && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 34, 0.95)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            padding: '20px',
          }}
          onClick={() => setShowContactModal(false)}
        >
          <div
            style={{
              background: '#000022',
              padding: '40px',
              borderRadius: '12px',
              border: '1px solid rgba(251, 245, 243, 0.1)',
              maxWidth: '500px',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h3 style={{ marginBottom: '20px', color: '#e28413' }}>Contact Paolo</h3>
            <p style={{ marginBottom: '10px' }}>Email: pjsandejas@gmail.com</p>
            <p style={{ marginBottom: '10px' }}>GitHub: github.com/paolosandejas</p>
            <p style={{ marginBottom: '20px' }}>LinkedIn: linkedin.com/in/paolosandejas</p>
            <button
              onClick={() => setShowContactModal(false)}
              style={{
                padding: '10px 20px',
                background: '#e28413',
                border: 'none',
                borderRadius: '8px',
                color: '#000022',
                fontWeight: '600',
                cursor: 'pointer',
              }}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
