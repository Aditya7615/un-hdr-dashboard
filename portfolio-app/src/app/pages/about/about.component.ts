import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [CommonModule],
  template: `
    <section class="about section">
      <div class="container">
        <div class="about-grid">
          <div class="about-image">
            <div class="image-wrapper glass-card">
              <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=80" alt="Aditya Goyal">
              <div class="image-overlay"></div>
            </div>
            <div class="experience-badge glass-card">
              <span class="badge-number">3+</span>
              <span class="badge-text">Years of Experience</span>
            </div>
          </div>

          <div class="about-content">
            <span class="section-label">About Me</span>
            <h1 class="section-title">Crafting Intelligent Solutions Through Data & Code</h1>
            <p class="about-text">
              I'm a passionate Data Scientist and Full-Stack Developer with expertise in building
              end-to-end AI-powered applications. My journey spans from training deep learning
              models to deploying production-ready web applications.
            </p>
            <p class="about-text">
              I thrive on solving complex problems with elegant solutions, whether it's
              implementing RAG systems for intelligent document retrieval, building real-time
              data pipelines, or creating intuitive user interfaces that make technology
              accessible to everyone.
            </p>

            <div class="skills-bars">
              <div class="skill-bar">
                <div class="skill-bar-header">
                  <span>Python / Machine Learning</span>
                  <span>95%</span>
                </div>
                <div class="skill-bar-track">
                  <div class="skill-bar-fill" style="--width: 95%"></div>
                </div>
              </div>
              <div class="skill-bar">
                <div class="skill-bar-header">
                  <span>Angular / TypeScript</span>
                  <span>90%</span>
                </div>
                <div class="skill-bar-track">
                  <div class="skill-bar-fill" style="--width: 90%"></div>
                </div>
              </div>
              <div class="skill-bar">
                <div class="skill-bar-header">
                  <span>Node.js / PHP</span>
                  <span>85%</span>
                </div>
                <div class="skill-bar-track">
                  <div class="skill-bar-fill" style="--width: 85%"></div>
                </div>
              </div>
              <div class="skill-bar">
                <div class="skill-bar-header">
                  <span>Data Engineering</span>
                  <span>88%</span>
                </div>
                <div class="skill-bar-track">
                  <div class="skill-bar-fill" style="--width: 88%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="timeline-section">
          <h2 class="section-title">My Journey</h2>
          <div class="timeline">
            <div class="timeline-item glass-card">
              <div class="timeline-marker"></div>
              <div class="timeline-content">
                <span class="timeline-date">2024 - Present</span>
                <h3>Senior Data Science Developer</h3>
                <p>Building AI-powered applications and data pipelines at scale</p>
              </div>
            </div>
            <div class="timeline-item glass-card">
              <div class="timeline-marker"></div>
              <div class="timeline-content">
                <span class="timeline-date">2022 - 2024</span>
                <h3>Full-Stack Developer</h3>
                <p>Developed web applications using Angular, Node.js, and Python</p>
              </div>
            </div>
            <div class="timeline-item glass-card">
              <div class="timeline-marker"></div>
              <div class="timeline-content">
                <span class="timeline-date">2021 - 2022</span>
                <h3>Data Analyst Intern</h3>
                <p>Performed data analysis and visualization for business insights</p>
              </div>
            </div>
          </div>
        </div>

        <div class="tech-stack">
          <h2 class="section-title">Tech Stack</h2>
          <div class="tech-grid">
            @for (tech of techStack; track tech.name) {
              <div class="tech-item glass-card">
                <div class="tech-icon">{{ tech.icon }}</div>
                <span class="tech-name">{{ tech.name }}</span>
                <span class="tech-category">{{ tech.category }}</span>
              </div>
            }
          </div>
        </div>
      </div>
    </section>
  `,
  styles: [`
    .about-grid {
      display: grid;
      grid-template-columns: 1fr 1.2fr;
      gap: 80px;
      margin-bottom: 100px;
    }

    .about-image {
      position: relative;
    }

    .image-wrapper {
      position: relative;
      overflow: hidden;
    }

    .image-wrapper img {
      width: 100%;
      height: 500px;
      object-fit: cover;
    }

    .image-overlay {
      position: absolute;
      inset: 0;
      background: linear-gradient(to top, var(--bg-primary) 0%, transparent 50%);
    }

    .experience-badge {
      position: absolute;
      bottom: 30px;
      right: -30px;
      padding: 24px 32px;
      text-align: center;
    }

    .badge-number {
      display: block;
      font-size: 3rem;
      font-weight: 800;
      background: var(--gradient-1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .badge-text {
      font-size: 0.875rem;
      color: var(--text-secondary);
    }

    .section-label {
      display: inline-block;
      padding: 6px 14px;
      background: var(--glass);
      border: 1px solid var(--glass-border);
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: var(--accent);
      margin-bottom: 20px;
    }

    .about-content .section-title {
      font-size: 2.5rem;
      margin-bottom: 24px;
    }

    .about-text {
      color: var(--text-secondary);
      font-size: 1.1rem;
      line-height: 1.8;
      margin-bottom: 20px;
    }

    .skills-bars {
      margin-top: 40px;
    }

    .skill-bar {
      margin-bottom: 24px;
    }

    .skill-bar-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
      font-size: 0.95rem;
    }

    .skill-bar-track {
      height: 8px;
      background: var(--glass);
      border-radius: 4px;
      overflow: hidden;
    }

    .skill-bar-fill {
      height: 100%;
      width: var(--width);
      background: var(--gradient-1);
      border-radius: 4px;
      transition: width 1s ease-out;
    }

    .timeline-section {
      margin-bottom: 100px;
    }

    .timeline {
      position: relative;
      padding-left: 40px;
    }

    .timeline::before {
      content: '';
      position: absolute;
      left: 7px;
      top: 0;
      bottom: 0;
      width: 2px;
      background: var(--glass-border);
    }

    .timeline-item {
      position: relative;
      padding: 24px;
      margin-bottom: 24px;
    }

    .timeline-marker {
      position: absolute;
      left: -40px;
      top: 30px;
      width: 16px;
      height: 16px;
      background: var(--accent);
      border-radius: 50%;
      box-shadow: 0 0 20px var(--accent-glow);
    }

    .timeline-date {
      font-size: 0.75rem;
      color: var(--accent);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    .timeline-content h3 {
      font-size: 1.25rem;
      margin: 8px 0;
    }

    .timeline-content p {
      color: var(--text-secondary);
    }

    .tech-stack {
      text-align: center;
    }

    .tech-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 20px;
      margin-top: 40px;
    }

    .tech-item {
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
    }

    .tech-icon {
      font-size: 2rem;
    }

    .tech-name {
      font-weight: 600;
      font-size: 0.95rem;
    }

    .tech-category {
      font-size: 0.75rem;
      color: var(--text-secondary);
    }

    @media (max-width: 1024px) {
      .about-grid {
        grid-template-columns: 1fr;
        gap: 40px;
      }

      .experience-badge {
        right: 20px;
      }

      .about-image {
        max-width: 400px;
        margin: 0 auto;
      }
    }
  `]
})
export class AboutComponent {
  techStack = [
    { name: 'Python', icon: '🐍', category: 'Backend' },
    { name: 'Angular', icon: '🅰️', category: 'Frontend' },
    { name: 'TypeScript', icon: '📘', category: 'Language' },
    { name: 'PyTorch', icon: '🔥', category: 'ML Framework' },
    { name: 'TensorFlow', icon: '🧠', category: 'ML Framework' },
    { name: 'Node.js', icon: '💚', category: 'Backend' },
    { name: 'PostgreSQL', icon: '🐘', category: 'Database' },
    { name: 'MongoDB', icon: '🍃', category: 'Database' },
    { name: 'Docker', icon: '🐳', category: 'DevOps' },
    { name: 'AWS', icon: '☁️', category: 'Cloud' },
    { name: 'FastAPI', icon: '⚡', category: 'API' },
    { name: 'Three.js', icon: '🎮', category: '3D Graphics' }
  ];
}
