import { motion } from 'framer-motion';
import portfolioData from '../data/portfolio.json';
import './Contact.css';

const Contact = () => {
  const { personal } = portfolioData;

  return (
    <section className="contact" id="contact">
      <div className="container">
        <div className="contact-content">
          <motion.div
            className="contact-info"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="contact-title">Let's Build Something</h2>
            <p className="contact-subtitle">
              Interested in collaborating or discussing opportunities? Reach out.
            </p>

            <div className="contact-links">
              <a
                href={`mailto:${personal.email}`}
                className="contact-link email-link"
              >
                <span className="contact-icon">✉</span>
                <span>{personal.email}</span>
              </a>

              <a
                href={personal.github}
                target="_blank"
                rel="noopener noreferrer"
                className="contact-link"
              >
                <span className="contact-icon">→</span>
                <span>GitHub</span>
              </a>

              <a
                href={personal.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                className="contact-link"
              >
                <span className="contact-icon">→</span>
                <span>LinkedIn</span>
              </a>

              <a
                href="/Paolo_Sandejas_Resume.pdf"
                download
                className="contact-link"
              >
                <span className="contact-icon">↓</span>
                <span>Download Resume</span>
              </a>
            </div>
          </motion.div>


        </div>

        <div className="contact-footer">
          <p>© 2026 {personal.name}. Built with React + Framer Motion</p>
        </div>
      </div>
    </section>
  );
};

export default Contact;
