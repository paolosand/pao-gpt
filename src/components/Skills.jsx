import { motion } from 'framer-motion';
import portfolioData from '../data/portfolio.json';
import './Skills.css';

const Skills = () => {
  const { skills } = portfolioData;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: {
      opacity: 1,
      x: 0,
      transition: {
        duration: 0.5,
      },
    },
  };

  return (
    <section className="skills" id="skills">
      <div className="container">
        <div className="section-number">03</div>
        <h2 className="section-title">Technical Stack</h2>

        <motion.div
          className="skills-grid"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
        >
          {Object.entries(skills).map(([category, skillList], index) => (
            <motion.div
              key={category}
              className="skill-category"
              variants={itemVariants}
            >
              <div className="skill-category-header">
                <div className="skill-category-number">
                  {String(index + 1).padStart(2, '0')}
                </div>
                <h3 className="skill-category-title">{category}</h3>
              </div>

              <div className="skill-list">
                {skillList.map((skill, i) => (
                  <motion.div
                    key={i}
                    className="skill-item"
                    whileHover={{ scale: 1.05, x: 4 }}
                    transition={{ duration: 0.2 }}
                  >
                    <span className="skill-bullet">▸</span>
                    <span className="skill-name">{skill}</span>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default Skills;
