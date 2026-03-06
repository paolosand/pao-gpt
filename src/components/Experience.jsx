import { motion } from 'framer-motion';
import portfolioData from '../data/portfolio.json';
import './Experience.css';

const Experience = () => {
  const { experience } = portfolioData;

  return (
    <section className="experience" id="experience">
      <div className="container">
        <div className="section-number">04</div>
        <h2 className="section-title">Experience</h2>

        <div className="experience-timeline">
          {experience.map((exp, index) => (
            <motion.div
              key={index}
              className="experience-item"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <div className="experience-marker">
                <div className="marker-dot"></div>
                <div className="marker-line"></div>
              </div>

              <div className="experience-content">
                <div className="experience-header">
                  <div>
                    <h3 className="experience-company">{exp.company}</h3>
                    <h4 className="experience-role">{exp.role}</h4>
                  </div>
                  <div className="experience-dates">{exp.dates}</div>
                </div>

                <ul className="experience-bullets">
                  {exp.bullets.map((bullet, i) => (
                    <li key={i} className="experience-bullet">
                      {bullet}
                    </li>
                  ))}
                </ul>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Experience;
