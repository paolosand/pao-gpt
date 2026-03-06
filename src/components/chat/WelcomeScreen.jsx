import portfolioData from '../../data/portfolio.json';
import './WelcomeScreen.css';

export default function WelcomeScreen() {
  const { personal } = portfolioData;

  return (
    <div className="welcome-screen">
      <h1 className="welcome-title">Hi, I'm pao-gpt 👋</h1>

      <p className="welcome-subtitle">
        An AI clone of Paolo Sandejas<br />
        AI/ML Engineer | Creative Technologist
      </p>

      <div className="welcome-links">
        <a href={`mailto:${personal.email}`} className="welcome-link">
          📧 {personal.email}
        </a>
        <a href={personal.github} target="_blank" rel="noopener noreferrer" className="welcome-link">
          🔗 GitHub
        </a>
        <a href={personal.linkedin} target="_blank" rel="noopener noreferrer" className="welcome-link">
          💼 LinkedIn
        </a>
      </div>

      <div className="welcome-topics">
        <h3>Ask me about:</h3>
        <ul>
          <li>• My ML production experience</li>
          <li>• Creative tech projects</li>
          <li>• Music + audio AI work</li>
          <li>• Anything else!</li>
        </ul>
      </div>

      <p className="welcome-privacy">
        Conversations stored anonymously for analytics
      </p>
    </div>
  );
}
