import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  template: `
    <nav class="navbar">
      <div class="container nav-content">
        <a routerLink="/" class="logo">
          <span class="logo-bracket">&lt;</span>
          <span class="logo-text">AD</span>
          <span class="logo-bracket">/&gt;</span>
        </a>

        <button class="mobile-toggle" (click)="toggleMenu()">
          <span></span>
          <span></span>
          <span></span>
        </button>

        <div class="nav-links" [class.active]="isOpen()">
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">Home</a>
          <a routerLink="/about" routerLinkActive="active">About</a>
          <a routerLink="/projects" routerLinkActive="active">Projects</a>
          <a routerLink="/contact" routerLinkActive="active">Contact</a>
        </div>
      </div>
    </nav>
  `,
  styles: [`
    .navbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      z-index: 1000;
      background: rgba(10, 10, 15, 0.8);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--glass-border);
      height: 80px;
      display: flex;
      align-items: center;
    }

    .nav-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
    }

    .logo {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.5rem;
      font-weight: 700;
    }

    .logo-bracket {
      color: var(--accent);
    }

    .logo-text {
      background: var(--gradient-1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .nav-links {
      display: flex;
      gap: 40px;
    }

    .nav-links a {
      color: var(--text-secondary);
      font-weight: 500;
      transition: var(--transition);
      position: relative;
    }

    .nav-links a:hover,
    .nav-links a.active {
      color: var(--text-primary);
    }

    .nav-links a::after {
      content: '';
      position: absolute;
      bottom: -8px;
      left: 0;
      width: 0;
      height: 2px;
      background: var(--gradient-1);
      transition: var(--transition);
    }

    .nav-links a:hover::after,
    .nav-links a.active::after {
      width: 100%;
    }

    .mobile-toggle {
      display: none;
      flex-direction: column;
      gap: 5px;
      padding: 5px;
    }

    .mobile-toggle span {
      width: 25px;
      height: 2px;
      background: var(--text-primary);
      transition: var(--transition);
    }

    @media (max-width: 768px) {
      .mobile-toggle {
        display: flex;
      }

      .nav-links {
        position: fixed;
        top: 80px;
        left: 0;
        right: 0;
        background: var(--bg-secondary);
        flex-direction: column;
        align-items: center;
        padding: 40px;
        gap: 30px;
        transform: translateY(-100%);
        opacity: 0;
        pointer-events: none;
        transition: var(--transition);
      }

      .nav-links.active {
        transform: translateY(0);
        opacity: 1;
        pointer-events: all;
      }
    }
  `]
})
export class NavbarComponent {
  isOpen = signal(false);

  toggleMenu() {
    this.isOpen.update(v => !v);
  }
}
