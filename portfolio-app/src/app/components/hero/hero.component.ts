import { Component, ElementRef, ViewChild, AfterViewInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import * as THREE from 'three';

@Component({
  selector: 'app-hero',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <section class="hero">
      <canvas #canvasRef class="hero-canvas"></canvas>
      <div class="hero-content">
        <div class="hero-text">
          <span class="hero-label">Welcome to my portfolio</span>
          <h1 class="hero-title">
            Hi, I'm <span class="gradient-text">Aditya Goyal</span>
          </h1>
          <p class="hero-subtitle">
            Data Science & Full-Stack Developer crafting intelligent solutions
            with cutting-edge technologies. Turning data into insights and ideas
            into reality.
          </p>
          <div class="hero-cta">
            <a routerLink="/projects" class="btn btn-primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
              View Projects
            </a>
            <a routerLink="/contact" class="btn btn-outline">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
              Get in Touch
            </a>
          </div>
          <div class="hero-stats">
            <div class="stat">
              <span class="stat-value">50+</span>
              <span class="stat-label">Projects</span>
            </div>
            <div class="stat">
              <span class="stat-value">3+</span>
              <span class="stat-label">Years Experience</span>
            </div>
            <div class="stat">
              <span class="stat-value">20+</span>
              <span class="stat-label">AI/ML Models</span>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-card glass-card">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="url(#grad1)" stroke-width="1.5">
                <defs>
                  <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#667eea"/>
                    <stop offset="100%" stop-color="#764ba2"/>
                  </linearGradient>
                </defs>
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
            </div>
            <span class="card-label">AI/ML Engineer</span>
          </div>
          <div class="floating-card glass-card" style="--delay: 1">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="url(#grad2)" stroke-width="1.5">
                <defs>
                  <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#4facfe"/>
                    <stop offset="100%" stop-color="#00f2fe"/>
                  </linearGradient>
                </defs>
                <polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>
              </svg>
            </div>
            <span class="card-label">Full-Stack Dev</span>
          </div>
          <div class="floating-card glass-card" style="--delay: 2">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="url(#grad3)" stroke-width="1.5">
                <defs>
                  <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#f093fb"/>
                    <stop offset="100%" stop-color="#f5576c"/>
                  </linearGradient>
                </defs>
                <circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/>
              </svg>
            </div>
            <span class="card-label">Data Enthusiast</span>
          </div>
        </div>
      </div>
      <div class="scroll-indicator">
        <div class="mouse">
          <div class="wheel"></div>
        </div>
        <span>Scroll to explore</span>
      </div>
    </section>
  `,
  styles: [`
    .hero {
      min-height: 100vh;
      display: flex;
      align-items: center;
      position: relative;
      overflow: hidden;
    }

    .hero-canvas {
      position: absolute;
      inset: 0;
      z-index: 0;
    }

    .hero-content {
      position: relative;
      z-index: 1;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 80px;
      align-items: center;
      width: 100%;
      max-width: 1280px;
      margin: 0 auto;
      padding: 0 24px;
    }

    .hero-label {
      display: inline-block;
      padding: 8px 16px;
      background: var(--glass);
      border: 1px solid var(--glass-border);
      border-radius: 20px;
      font-size: 0.875rem;
      color: var(--accent);
      margin-bottom: 24px;
    }

    .hero-title {
      font-size: 4rem;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 24px;
    }

    .gradient-text {
      background: var(--gradient-1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
      font-size: 1.25rem;
      color: var(--text-secondary);
      line-height: 1.8;
      margin-bottom: 40px;
      max-width: 540px;
    }

    .hero-cta {
      display: flex;
      gap: 16px;
      margin-bottom: 60px;
    }

    .hero-stats {
      display: flex;
      gap: 60px;
    }

    .stat {
      text-align: left;
    }

    .stat-value {
      display: block;
      font-size: 2.5rem;
      font-weight: 800;
      background: var(--gradient-1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .stat-label {
      font-size: 0.875rem;
      color: var(--text-secondary);
    }

    .hero-visual {
      position: relative;
      height: 400px;
    }

    .floating-card {
      position: absolute;
      padding: 20px 30px;
      display: flex;
      align-items: center;
      gap: 16px;
      animation: float 6s ease-in-out infinite;
      animation-delay: calc(var(--delay) * -2s);
    }

    .floating-card:nth-child(1) {
      top: 20%;
      left: 10%;
    }

    .floating-card:nth-child(2) {
      top: 50%;
      right: 5%;
    }

    .floating-card:nth-child(3) {
      bottom: 10%;
      left: 20%;
    }

    .card-icon svg {
      width: 32px;
      height: 32px;
    }

    .card-label {
      font-weight: 600;
      font-size: 0.95rem;
    }

    @keyframes float {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(-20px); }
    }

    .scroll-indicator {
      position: absolute;
      bottom: 40px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
      color: var(--text-secondary);
      font-size: 0.875rem;
      z-index: 1;
    }

    .mouse {
      width: 26px;
      height: 40px;
      border: 2px solid var(--text-secondary);
      border-radius: 13px;
      position: relative;
    }

    .wheel {
      width: 4px;
      height: 8px;
      background: var(--accent);
      border-radius: 2px;
      position: absolute;
      top: 8px;
      left: 50%;
      transform: translateX(-50%);
      animation: scroll 2s ease-in-out infinite;
    }

    @keyframes scroll {
      0% { opacity: 1; transform: translateX(-50%) translateY(0); }
      100% { opacity: 0; transform: translateX(-50%) translateY(15px); }
    }

    @media (max-width: 1024px) {
      .hero-content {
        grid-template-columns: 1fr;
        text-align: center;
      }

      .hero-subtitle {
        margin: 0 auto 40px;
      }

      .hero-cta {
        justify-content: center;
      }

      .hero-stats {
        justify-content: center;
      }

      .hero-visual {
        display: none;
      }

      .hero-title {
        font-size: 3rem;
      }
    }

    @media (max-width: 640px) {
      .hero-title {
        font-size: 2.5rem;
      }

      .hero-cta {
        flex-direction: column;
      }

      .hero-stats {
        flex-direction: column;
        gap: 20px;
        align-items: center;
      }
    }
  `]
})
export class HeroComponent implements AfterViewInit, OnDestroy {
  @ViewChild('canvasRef') canvasRef!: ElementRef<HTMLCanvasElement>;

  private scene!: THREE.Scene;
  private camera!: THREE.PerspectiveCamera;
  private renderer!: THREE.WebGLRenderer;
  private particles!: THREE.Points;
  private animationId!: number;

  ngAfterViewInit() {
    this.initThreeJS();
    this.animate();
    window.addEventListener('resize', this.onResize.bind(this));
  }

  ngOnDestroy() {
    window.removeEventListener('resize', this.onResize.bind(this));
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    this.renderer?.dispose();
  }

  private initThreeJS() {
    const canvas = this.canvasRef.nativeElement;
    const width = window.innerWidth;
    const height = window.innerHeight;

    this.scene = new THREE.Scene();
    this.scene.background = null;

    this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    this.camera.position.z = 50;

    this.renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true
    });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    this.createParticles();
    this.createGlowSphere();
  }

  private createParticles() {
    const geometry = new THREE.BufferGeometry();
    const count = 2000;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    for (let i = 0; i < count * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 100;
      positions[i + 1] = (Math.random() - 0.5) * 100;
      positions[i + 2] = (Math.random() - 0.5) * 100;

      const color = new THREE.Color();
      color.setHSL(Math.random() * 0.3 + 0.6, 0.8, 0.6);
      colors[i] = color.r;
      colors[i + 1] = color.g;
      colors[i + 2] = color.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.5,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending
    });

    this.particles = new THREE.Points(geometry, material);
    this.scene.add(this.particles);
  }

  private createGlowSphere() {
    const geometry = new THREE.SphereGeometry(8, 32, 32);
    const material = new THREE.MeshBasicMaterial({
      color: 0x6366f1,
      transparent: true,
      opacity: 0.1,
      wireframe: true
    });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.set(30, -10, -20);
    this.scene.add(sphere);
  }

  private animate() {
    this.animationId = requestAnimationFrame(this.animate.bind(this));

    if (this.particles) {
      this.particles.rotation.x += 0.0003;
      this.particles.rotation.y += 0.0005;
    }

    this.renderer.render(this.scene, this.camera);
  }

  private onResize() {
    const width = window.innerWidth;
    const height = window.innerHeight;

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }
}
