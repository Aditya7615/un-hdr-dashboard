import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProjectCardComponent } from '../../components/project-card/project-card.component';
import { ProjectService } from '../../services/project.service';
import { Project } from '../../models/project.model';

@Component({
  selector: 'app-projects',
  standalone: true,
  imports: [CommonModule, ProjectCardComponent],
  template: `
    <section class="projects-page section">
      <div class="container">
        <div class="page-header">
          <span class="section-label">My Work</span>
          <h1 class="section-title">Featured Projects</h1>
          <p class="section-subtitle">
            A collection of AI/ML models, data pipelines, and full-stack applications
            that showcase my skills and passion for technology.
          </p>
        </div>

        <div class="filter-tabs">
          @for (filter of filters; track filter) {
            <button
              class="filter-btn"
              [class.active]="activeFilter === filter"
              (click)="setFilter(filter)"
            >
              {{ filter }}
            </button>
          }
        </div>

        @if (isLoading) {
          <div class="loading-state">
            <div class="spinner"></div>
            <p>Loading projects...</p>
          </div>
        } @else if (filteredProjects.length === 0) {
          <div class="empty-state glass-card">
            <p>No projects found in this category.</p>
          </div>
        } @else {
          <div class="projects-grid">
            @for (project of filteredProjects; track project.id) {
              <app-project-card [project]="project"></app-project-card>
            }
          </div>
        }
      </div>
    </section>
  `,
  styles: [`
    .page-header {
      text-align: center;
      max-width: 700px;
      margin: 0 auto 60px;
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

    .section-title {
      font-size: 3rem;
      margin-bottom: 16px;
    }

    .section-subtitle {
      color: var(--text-secondary);
      font-size: 1.125rem;
      line-height: 1.7;
    }

    .filter-tabs {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px;
      margin-bottom: 50px;
    }

    .filter-btn {
      padding: 10px 24px;
      background: var(--glass);
      border: 1px solid var(--glass-border);
      border-radius: 30px;
      color: var(--text-secondary);
      font-size: 0.9rem;
      font-weight: 500;
      transition: var(--transition);
    }

    .filter-btn:hover {
      border-color: var(--accent);
      color: var(--text-primary);
    }

    .filter-btn.active {
      background: var(--gradient-1);
      border-color: transparent;
      color: white;
    }

    .projects-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 30px;
    }

    .loading-state {
      text-align: center;
      padding: 80px 0;
      color: var(--text-secondary);
    }

    .spinner {
      width: 50px;
      height: 50px;
      border: 3px solid var(--glass-border);
      border-top-color: var(--accent);
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 20px;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    .empty-state {
      text-align: center;
      padding: 60px;
      color: var(--text-secondary);
    }

    @media (max-width: 640px) {
      .projects-grid {
        grid-template-columns: 1fr;
      }

      .section-title {
        font-size: 2rem;
      }
    }
  `]
})
export class ProjectsComponent implements OnInit {
  projects: Project[] = [];
  filteredProjects: Project[] = [];
  isLoading = true;
  activeFilter = 'All';
  filters = ['All', 'AI/ML', 'Full-Stack', 'Data Engineering', 'Web App'];

  constructor(private projectService: ProjectService) {}

  ngOnInit() {
    this.loadProjects();
  }

  loadProjects() {
    this.projectService.getProjects().subscribe({
      next: (projects) => {
        this.projects = projects;
        this.applyFilter();
        this.isLoading = false;
      },
      error: () => {
        this.loadFallbackProjects();
        this.isLoading = false;
      }
    });
  }

  loadFallbackProjects() {
    this.projects = [
      {
        id: 1,
        title: 'RAG Knowledge System',
        description: 'Retrieval-Augmented Generation system for intelligent document Q&A with vector embeddings.',
        image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80',
        github_link: 'https://github.com',
        live_link: '',
        tags: ['RAG', 'LLM', 'Python', 'Vector DB']
      },
      {
        id: 2,
        title: 'Real-time Data Pipeline',
        description: 'Scalable ETL pipeline processing millions of events daily with Apache Kafka and Spark.',
        image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80',
        github_link: 'https://github.com',
        live_link: '',
        tags: ['Kafka', 'Spark', 'Python', 'AWS']
      },
      {
        id: 3,
        title: 'Computer Vision Platform',
        description: 'Deep learning platform for image classification and object detection.',
        image: 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&q=80',
        github_link: 'https://github.com',
        live_link: '',
        tags: ['PyTorch', 'CV', 'Angular', 'FastAPI']
      },
      {
        id: 4,
        title: 'E-commerce Platform',
        description: 'Full-stack e-commerce solution with Angular, Node.js, and PostgreSQL.',
        image: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&q=80',
        github_link: 'https://github.com',
        live_link: '',
        tags: ['Angular', 'Node.js', 'PostgreSQL', 'Stripe']
      },
      {
        id: 5,
        title: 'Sentiment Analysis API',
        description: 'REST API for real-time sentiment analysis using transformer models.',
        image: 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80',
        github_link: 'https://github.com',
        live_link: '',
        tags: ['NLP', 'FastAPI', 'BERT', 'Docker']
      },
      {
        id: 6,
        title: 'Analytics Dashboard',
        description: 'Interactive dashboard for visualizing business metrics in real-time.',
        image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80',
        github_link: 'https://github.com',
        live_link: '',
        tags: ['React', 'D3.js', 'Node.js', 'MongoDB']
      }
    ];
    this.applyFilter();
  }

  setFilter(filter: string) {
    this.activeFilter = filter;
    this.applyFilter();
  }

  applyFilter() {
    if (this.activeFilter === 'All') {
      this.filteredProjects = [...this.projects];
    } else {
      this.filteredProjects = this.projects.filter(p =>
        p.tags?.some(tag => {
          const category = tag.toLowerCase();
          if (this.activeFilter === 'AI/ML') return category.includes('ml') || category.includes('ai') || category.includes('nlp') || category.includes('cv') || category.includes('pytorch') || category.includes('rag');
          if (this.activeFilter === 'Full-Stack') return category.includes('angular') || category.includes('node') || category.includes('react');
          if (this.activeFilter === 'Data Engineering') return category.includes('kafka') || category.includes('spark') || category.includes('pipeline') || category.includes('etl');
          if (this.activeFilter === 'Web App') return true;
          return false;
        })
      );
    }
  }
}
