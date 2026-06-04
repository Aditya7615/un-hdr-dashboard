import { Component, Input, OnInit, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Project } from '../../models/project.model';

@Component({
  selector: 'app-project-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="project-card glass-card" #cardRef>
      <div class="card-image">
        <img [src]="project.image" [alt]="project.title">
        <div class="card-overlay"></div>
      </div>
      <div class="card-content">
        <div class="card-tags">
          @for (tag of project.tags; track tag) {
            <span class="tag">{{ tag }}</span>
          }
        </div>
        <h3 class="card-title">{{ project.title }}</h3>
        <p class="card-description">{{ project.description }}</p>
        <div class="card-links">
          @if (project.github_link) {
            <a [href]="project.github_link" target="_blank" rel="noopener" class="btn btn-outline">
              <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
              Code
            </a>
          }
          @if (project.live_link) {
            <a [href]="project.live_link" target="_blank" rel="noopener" class="btn btn-primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/></svg>
              Live Demo
            </a>
          }
        </div>
      </div>
    </div>
  `,
  styles: [`
    .project-card {
      overflow: hidden;
      height: 100%;
      display: flex;
      flex-direction: column;
    }

    .card-image {
      position: relative;
      height: 200px;
      overflow: hidden;
    }

    .card-image img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: var(--transition);
    }

    .project-card:hover .card-image img {
      transform: scale(1.1);
    }

    .card-overlay {
      position: absolute;
      inset: 0;
      background: linear-gradient(to top, var(--bg-card) 0%, transparent 100%);
    }

    .card-content {
      padding: 24px;
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .card-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 16px;
    }

    .card-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 12px;
      background: var(--gradient-1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .card-description {
      color: var(--text-secondary);
      font-size: 0.95rem;
      line-height: 1.7;
      flex: 1;
      margin-bottom: 20px;
    }

    .card-links {
      display: flex;
      gap: 12px;
    }

    .card-links .btn {
      padding: 10px 18px;
      font-size: 0.875rem;
    }
  `]
})
export class ProjectCardComponent {
  @Input() project!: Project;
  @ViewChild('cardRef') cardRef!: ElementRef;
}
