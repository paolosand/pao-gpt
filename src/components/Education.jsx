import { motion } from 'framer-motion';
import portfolioData from '../data/portfolio.json';
import './Education.css';

const Education = () => {
  const { education } = portfolioData;

  return (
    <section className="education" id="education">
      <div className="container">
        <div className="section-number">05</div>
        <h2 className="section-title">Education</h2>

        <div className="education-grid">
          {education.map((edu, index) => (
            <motion.div
              key={index}
              className="education-card"
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <div className="education-header">
                <div className="education-icon">🎓</div>
                <div className="education-gpa">{edu.gpa} GPA</div>
              </div>

              <h3 className="education-degree">{edu.degree}</h3>
              <div className="education-school">{edu.school}</div>
              <div className="education-dates">{edu.dates}</div>

              {edu.bullets && edu.bullets.length > 0 && (
                <ul className="education-bullets">
                  {edu.bullets.map((bullet, i) => (
                    <li key={i} className="education-bullet">
                      {bullet}
                    </li>
                  ))}
                </ul>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Education;
