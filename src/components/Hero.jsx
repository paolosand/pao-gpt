import { motion } from 'framer-motion';
import portfolioData from '../data/portfolio.json';
import './Hero.css';

const Hero = ({ onChatClick }) => {
  const { personal, summary, valueProps } = portfolioData;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.3,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.8,
        ease: [0.6, 0.05, 0.01, 0.9],
      },
    },
  };

  return (
    <section className="hero" id="hero">
      <div className="hero-background">
        <div className="grid-pattern"></div>
        <div className="hero-gradient"></div>
      </div>

      <div className="container">
        <motion.div
          className="hero-content"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.h1 className="hero-title" variants={itemVariants}>
            {personal.name}
          </motion.h1>

          <motion.div className="hero-label" variants={itemVariants}>
            <span className="hero-bracket">{'['}</span>
            <span className="hero-label-text">AI/ML Engineer</span>
            <span className="hero-bracket">{']'}</span>
          </motion.div>

          <motion.p className="hero-description" variants={itemVariants}>
            {summary}
          </motion.p>

          <motion.div className="hero-actions" variants={itemVariants}>
            <a
              href="/Paolo_Sandejas_Resume.pdf"
              download
              className="btn btn-primary"
            >
              Download Resume
              <span className="btn-icon">↓</span>
            </a>
            <a href="#projects" className="btn btn-secondary">
              View Projects
              <span className="btn-icon">→</span>
            </a>
            <button onClick={onChatClick} className="btn btn-secondary">
              Chat with pao-gpt
              <span className="btn-icon">💬</span>
            </button>
          </motion.div>

          <motion.div className="value-props" variants={itemVariants}>
            {valueProps.map((prop, index) => (
              <div key={index} className="value-prop">
                <div className="value-prop-number">{String(index + 1).padStart(2, '0')}</div>
                <div className="value-prop-content">
                  <h3 className="value-prop-title">{prop.title}</h3>
                  <p className="value-prop-description">{prop.description}</p>
                </div>
              </div>
            ))}
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
};

export default Hero;
