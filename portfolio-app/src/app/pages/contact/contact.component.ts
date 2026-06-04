import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <section class="contact section">
      <div class="container">
        <div class="contact-grid">
          <div class="contact-info">
            <span class="section-label">Get in Touch</span>
            <h1 class="section-title">Let's Build Something Amazing Together</h1>
            <p class="contact-description">
              Have a project in mind or want to collaborate? I'd love to hear from you.
              Drop me a message and I'll get back to you as soon as possible.
            </p>

            <div class="contact-details">
              <div class="detail-item glass-card">
                <div class="detail-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                </div>
                <div class="detail-content">
                  <span class="detail-label">Email</span>
                  <span class="detail-value">hello&#64;adityagoyal.dev</span>
                </div>
              </div>
              <div class="detail-item glass-card">
                <div class="detail-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
                </div>
                <div class="detail-content">
                  <span class="detail-label">Location</span>
                  <span class="detail-value">San Francisco, CA</span>
                </div>
              </div>
              <div class="detail-item glass-card">
                <div class="detail-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
                </div>
                <div class="detail-content">
                  <span class="detail-label">Availability</span>
                  <span class="detail-value">Open for opportunities</span>
                </div>
              </div>
            </div>

            <div class="social-links">
              <h3>Connect with me</h3>
              <div class="social-icons">
                <a href="https://github.com" target="_blank" rel="noopener" class="social-icon glass-card">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
                </a>
                <a href="https://linkedin.com" target="_blank" rel="noopener" class="social-icon glass-card">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                </a>
                <a href="https://twitter.com" target="_blank" rel="noopener" class="social-icon glass-card">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/></svg>
                </a>
                <a href="https://kaggle.com" target="_blank" rel="noopener" class="social-icon glass-card">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.504 0c-.155 0-.315.008.48.06 4.924.294 8.235 2.688 9.535 5.52.6-.72.945-1.5.945-2.34 0-.78-.345-1.56-.945-2.34-1.125-2.46-3.6-4.28-7.065-4.8.48.06.96.36.96.96 0 .6-.48.96-1.005.96-.36 0-.72-.18-1.005-.54-.42-.54-.945-1.02-1.62-1.08-.48-.06-.96.3-1.26.78-.21.339-.45.72-.78 1.02-.3.24-.75.42-1.23.42-.36 0-.69-.12-.96-.3-.39-.33-.9-.75-1.35-.75-.24 0-.48.12-.72.39-.21.24-.3.51-.3.84.03.6.45 1.11 1.2 1.47.03.06.06.03.06.09-.21.42-.39.84-.36 1.29.03.6.33 1.11.75 1.5.09.09.21.15.33.21.39.18.9.27 1.35.33.27.03.54.06.78.12.06 0 .09-.03.09-.09v-.42c-.09-.12-.15-.15-.18-.27-.03-.06.03-.12.06-.18.12-.18.18-.36.18-.6 0-.21-.09-.39-.3-.6-.15-.12-.36-.24-.6-.3-.12-.03-.24-.06-.39-.06-.48-.06-1.14-.18-1.38-.6-.12-.24-.18-.63-.18-.87 0-.33.12-.63.36-.9.45-.51 1.26-.78 2.16-.87 1.29-.12 2.85-.12 4.41 0 1.08.09 1.92.36 2.37.87.24.27.36.57.36.9 0 .24-.06.63-.18.87-.24.42-.9.54-1.38.6-.15 0-.27.03-.39.06-.24.06-.45.18-.6.3-.21.21-.3.39-.3.6 0 .24.06.42.18.6.03.06.09.12.06.18-.03.12-.09.15-.18.27v.42c0 .06.03.09.09.09.24-.06.51-.09.78-.12.45-.06.96-.15 1.35-.33.12-.06.24-.12.33-.21.42-.39.72-.9.75-1.5.03-.45-.15-.87-.36-1.29 0-.06.03-.03.06-.09.75-.36 1.17-.87 1.2-1.47 0-.33-.09-.6-.3-.84-.24-.27-.48-.39-.72-.39-.45 0-.96.42-1.35.75-.27.18-.6.3-.96.3-.48 0-.93-.18-1.23-.42-.33-.3-.57-.72-.78-1.02-.3-.48-.78-.84-1.26-.78-.675.06-1.2.54-1.62 1.08-.285.36-.645.54-1.005.54-.525 0-1.005-.36-1.005-.96 0-.6.48-.9.96-.96-3.465.52-5.94 2.34-7.065 4.8-.6.78-.945 1.56-.945 2.34 0 .84.345 1.62.945 2.34 1.305-2.832 4.62-5.226 9.54-5.52.795-.06.63-.06.48-.06h.06z"/></svg>
                </a>
              </div>
            </div>
          </div>

          <div class="contact-form-wrapper">
            <form class="contact-form glass-card" (ngSubmit)="onSubmit()">
              @if (submitted()) {
                <div class="success-message">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                  <h3>Message Sent!</h3>
                  <p>Thank you for reaching out. I'll get back to you soon.</p>
                </div>
              } @else {
                <h2>Send a Message</h2>
                <div class="form-group">
                  <label for="name">Name</label>
                  <input type="text" id="name" [(ngModel)]="formData.name" name="name" required placeholder="Your name">
                </div>
                <div class="form-group">
                  <label for="email">Email</label>
                  <input type="email" id="email" [(ngModel)]="formData.email" name="email" required placeholder="your&#64;email.com">
                </div>
                <div class="form-group">
                  <label for="subject">Subject</label>
                  <input type="text" id="subject" [(ngModel)]="formData.subject" name="subject" required placeholder="Project inquiry">
                </div>
                <div class="form-group">
                  <label for="message">Message</label>
                  <textarea id="message" [(ngModel)]="formData.message" name="message" rows="5" required placeholder="Tell me about your project..."></textarea>
                </div>
                <button type="submit" class="btn btn-primary btn-full" [disabled]="isSubmitting()">
                  @if (isSubmitting()) {
                    <span class="spinner-small"></span>
                    Sending...
                  } @else {
                    Send Message
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
                  }
                </button>
              }
            </form>
          </div>
        </div>
      </div>
    </section>
  `,
  styles: [`
    .contact-grid {
      display: grid;
      grid-template-columns: 1fr 1.2fr;
      gap: 80px;
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
      font-size: 2.5rem;
      margin-bottom: 24px;
    }

    .contact-description {
      color: var(--text-secondary);
      font-size: 1.1rem;
      line-height: 1.8;
      margin-bottom: 40px;
    }

    .contact-details {
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-bottom: 40px;
    }

    .detail-item {
      display: flex;
      align-items: center;
      gap: 20px;
      padding: 20px;
    }

    .detail-icon {
      width: 50px;
      height: 50px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--gradient-1);
      border-radius: 12px;
    }

    .detail-icon svg {
      width: 22px;
      height: 22px;
      color: white;
    }

    .detail-label {
      display: block;
      font-size: 0.75rem;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    .detail-value {
      font-weight: 600;
      font-size: 1rem;
    }

    .social-links h3 {
      font-size: 1rem;
      margin-bottom: 16px;
      color: var(--text-secondary);
    }

    .social-icons {
      display: flex;
      gap: 12px;
    }

    .social-icon {
      width: 50px;
      height: 50px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 12px;
      transition: var(--transition);
    }

    .social-icon:hover {
      background: var(--accent);
      transform: translateY(-4px);
    }

    .social-icon svg {
      width: 22px;
      height: 22px;
    }

    .contact-form {
      padding: 40px;
    }

    .contact-form h2 {
      font-size: 1.5rem;
      margin-bottom: 30px;
    }

    .form-group {
      margin-bottom: 24px;
    }

    .form-group label {
      display: block;
      font-size: 0.875rem;
      font-weight: 500;
      margin-bottom: 8px;
      color: var(--text-secondary);
    }

    .form-group input,
    .form-group textarea {
      width: 100%;
      padding: 14px 18px;
      background: var(--glass);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-sm);
      color: var(--text-primary);
      font-size: 1rem;
      font-family: inherit;
      transition: var(--transition);
    }

    .form-group input:focus,
    .form-group textarea:focus {
      outline: none;
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-glow);
    }

    .form-group textarea {
      resize: vertical;
      min-height: 120px;
    }

    .btn-full {
      width: 100%;
      justify-content: center;
    }

    .spinner-small {
      width: 18px;
      height: 18px;
      border: 2px solid rgba(255,255,255,0.3);
      border-top-color: white;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    .success-message {
      text-align: center;
      padding: 40px 20px;
    }

    .success-message svg {
      width: 60px;
      height: 60px;
      color: #10b981;
      margin-bottom: 20px;
    }

    .success-message h3 {
      font-size: 1.5rem;
      margin-bottom: 12px;
    }

    .success-message p {
      color: var(--text-secondary);
    }

    @media (max-width: 1024px) {
      .contact-grid {
        grid-template-columns: 1fr;
        gap: 50px;
      }

      .section-title {
        font-size: 2rem;
      }
    }
  `]
})
export class ContactComponent {
  submitted = signal(false);
  isSubmitting = signal(false);

  formData = {
    name: '',
    email: '',
    subject: '',
    message: ''
  };

  onSubmit() {
    if (!this.formData.name || !this.formData.email || !this.formData.subject || !this.formData.message) {
      return;
    }

    this.isSubmitting.set(true);

    setTimeout(() => {
      this.isSubmitting.set(false);
      this.submitted.set(true);
      this.formData = { name: '', email: '', subject: '', message: '' };

      setTimeout(() => this.submitted.set(false), 5000);
    }, 1500);
  }
}
