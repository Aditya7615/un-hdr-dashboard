import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { HeroComponent } from '../../components/hero/hero.component';
import { ProjectCardComponent } from '../../components/project-card/project-card.component';
import { ProjectService } from '../../services/project.service';
import { Project } from '../../models/project.model';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink, HeroComponent, ProjectCardComponent],
  template: `
    <app-hero></app-hero>

    <section class="featured section">
      <div class="container">
        <div class="section-header">
          <span class="section-label">Portfolio</span>
          <h2 class="section-title">Featured Projects</h2>
          <p class="section-subtitle">Showcasing my best work in AI, ML, and Full-Stack Development</p>
        </div>

        <div class="projects-grid">
          @for (project of featuredProjects; track project.id) {
            <app-project-card [project]="project"></app-project-card>
          }
        </div>

        <div class="section-cta">
          <a routerLink="/projects" class="btn btn-outline">
            View All Projects
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
        </div>
      </div>
    </section>

    <section class="skills-preview section">
      <div class="container">
        <div class="skills-grid">
          <div class="skill-category glass-card">
            <div class="skill-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            </div>
            <h3>AI / Machine Learning</h3>
            <ul>
              <li>Deep Learning (PyTorch, TensorFlow)</li>
              <li>NLP & Computer Vision</li>
              <li>LLMs & RAG Systems</li>
              <li>MLOps & Model Deployment</li>
            </ul>
          </div>
          <div class="skill-category glass-card">
            <div class="skill-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
            </div>
            <h3>Full-Stack Development</h3>
            <ul>
              <li>Angular, React, Node.js</li>
              <li>Python, PHP, TypeScript</li>
              <li>PostgreSQL, MongoDB</li>
              <li>REST APIs & GraphQL</li>
            </ul>
          </div>
          <div class="skill-category glass-card">
            <div class="skill-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
            </div>
            <h3>Data Engineering</h3>
            <ul>
              <li>Data Pipeline Design</li>
              <li>Big Data Processing</li>
              <li>ETL/ELT Pipelines</li>
              <li>Cloud Data Services</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="cta-section">
      <div class="container">
        <div class="cta-content glass-card">
          <h2>Ready to bring your ideas to life?</h2>
          <p>Let's collaborate and build something extraordinary together.</p>
          <a routerLink="/contact" class="btn btn-primary">
            Start a Conversation
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
        </div>
      </div>
    </section>
  `,
  styles: [`
    .section-header {
      text-align: center;
      margin-bottom: 60px;
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
      margin-bottom: 16px;
    }

    .projects-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: 30px;
    }

    .section-cta {
      text-align: center;
      margin-top: 50px;
    }

    .skills-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 30px;
    }

    .skill-category {
      padding: 40px;
    }

    .skill-icon {
      width: 60px;
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--gradient-1);
      border-radius: 16px;
      margin-bottom: 24px;
    }

    .skill-icon svg {
      width: 28px;
      height: 28px;
      color: white;
    }

    .skill-category h3 {
      font-size: 1.25rem;
      margin-bottom: 20px;
      background: var(--gradient-1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .skill-category ul {
      list-style: none;
    }

    .skill-category li {
      color: var(--text-secondary);
      padding: 8px 0;
      border-bottom: 1px solid var(--glass-border);
      font-size: 0.95rem;
    }

    .skill-category li:last-child {
      border-bottom: none;
    }

    .cta-section {
      padding: 80px 0;
    }

    .cta-content {
      text-align: center;
      padding: 80px 40px;
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    }

    .cta-content h2 {
      font-size: 2.5rem;
      margin-bottom: 16px;
    }

    .cta-content p {
      color: var(--text-secondary);
      font-size: 1.125rem;
      margin-bottom: 32px;
    }

    @media (max-width: 768px) {
      .cta-content {
        padding: 50px 24px;
      }

      .cta-content h2 {
        font-size: 1.75rem;
      }
    }
  `]
})
export class HomeComponent implements OnInit {
  featuredProjects: Project[] = [];

  constructor(private projectService: ProjectService) {}

  ngOnInit() {
    this.projectService.getProjects().subscribe({
      next: (projects) => this.featuredProjects = projects.slice(0, 3),
      error: () => this.loadFallbackProjects()
    });
  }

  private loadFallbackProjects() {
    this.featuredProjects = [
      {
        id: 1,
        title: 'RAG Knowledge System',
        description: 'Retrieval-Augmented Generation system for intelligent document Q&A with vector embeddings and semantic search.',
        image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80',
        github_link: 'https://github.com',
        live_link: '',
        tags: ['RAG', 'LLM', 'Python', 'Vector DB']
      },
      {
        id: 2,
        title: 'Real-time Data Pipeline',
        description: 'Scalable ETL pipeline processing millions of events daily with Apache Kafka and Spark streaming.',
        image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80',
        github_link: 'https://github.com',
        live_link: '',
        tags: ['Kafka', 'Spark', 'Python', 'AWS']
      },
      {
        id: 3,
        title: 'Computer Vision Platform',
        description: 'Deep learning platform for image classification and object detection with custom model training.',
        image: 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&q=80',
        github_link: 'https://github.com',
        live_link: '',
        tags: ['PyTorch', 'CV', 'Angular', 'FastAPI']
      }
    ];
  }
}
