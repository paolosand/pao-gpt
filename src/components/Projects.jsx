import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import portfolioData from '../data/portfolio.json';
import './Projects.css';

const Projects = () => {
  const { projects } = portfolioData;
  const [filter, setFilter] = useState('all');
  const [selectedProject, setSelectedProject] = useState(null);

  const filteredProjects = projects.filter(
    (project) => filter === 'all' || project.category === filter
  );

  const categories = [
    { id: 'all', label: 'All Projects' },
    { id: 'ml', label: 'AI/ML' },
    { id: 'creative', label: 'Creative Tech' },
  ];

  return (
    <section className="projects" id="projects">
      <div className="container">
        <div className="section-number">02</div>
        <h2 className="section-title">Featured Work</h2>

        <div className="project-filters">
          {categories.map((cat) => (
            <button
              key={cat.id}
              className={`filter-btn ${filter === cat.id ? 'active' : ''}`}
              onClick={() => setFilter(cat.id)}
            >
              {cat.label}
            </button>
          ))}
        </div>

        <motion.div layout className="projects-grid">
          <AnimatePresence mode="popLayout">
            {filteredProjects.map((project, index) => (
              <motion.div
                key={project.id}
                layout
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.4 }}
                className={`project-card ${project.featured ? 'featured' : ''}`}
                onClick={() => setSelectedProject(project)}
              >
                <div className="project-header">
                  <div className="project-number">
                    {String(index + 1).padStart(2, '0')}
                  </div>
                  {project.featured && <div className="featured-badge">Featured</div>}
                </div>

                <h3 className="project-title">{project.title}</h3>
                <p className="project-description">{project.description}</p>

                <div className="project-tags">
                  {project.tags.slice(0, 4).map((tag, i) => (
                    <span key={i} className="project-tag">
                      {tag}
                    </span>
                  ))}
                  {project.tags.length > 4 && (
                    <span className="project-tag more">+{project.tags.length - 4}</span>
                  )}
                </div>

                <div className="project-links">
                  {project.links.github && (
                    <a
                      href={project.links.github}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="project-link"
                      onClick={(e) => e.stopPropagation()}
                    >
                      GitHub ↗
                    </a>
                  )}
                  {project.links.demo && (
                    <a
                      href={project.links.demo}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="project-link"
                      onClick={(e) => e.stopPropagation()}
                    >
                      Demo ↗
                    </a>
                  )}
                </div>

                <div className="project-hover-indicator">
                  <span>View Details →</span>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </motion.div>
      </div>

      {/* Project Modal */}
      <AnimatePresence>
        {selectedProject && (
          <motion.div
            className="project-modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedProject(null)}
          >
            <motion.div
              className="project-modal"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <button
                className="modal-close"
                onClick={() => setSelectedProject(null)}
              >
                ✕
              </button>

              <div className="modal-header">
                <h2 className="modal-title">{selectedProject.title}</h2>
                <div className="modal-category">
                  {selectedProject.category === 'ml' ? 'AI/ML' : 'Creative Tech'}
                </div>
              </div>

              <p className="modal-description">{selectedProject.description}</p>

              <div className="modal-tags">
                {selectedProject.tags.map((tag, i) => (
                  <span key={i} className="modal-tag">
                    {tag}
                  </span>
                ))}
              </div>

              <div className="modal-links">
                {selectedProject.links.github && (
                  <a
                    href={selectedProject.links.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="modal-link"
                  >
                    View on GitHub ↗
                  </a>
                )}
                {selectedProject.links.demo && (
                  <a
                    href={selectedProject.links.demo}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="modal-link"
                  >
                    Live Demo ↗
                  </a>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
};

export default Projects;
