# Portfolio | Data Science & Full-Stack Developer

A high-end, production-ready portfolio featuring Angular SPA, Three.js 3D graphics, and dynamic PHP/MySQL backend.

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Angular, SCSS, TypeScript |
| **3D Graphics** | Three.js |
| **Backend** | PHP |
| **Database** | MySQL |
| **Deployment** | Vercel |

## Features

- **Three.js Hero Section** - Interactive particle background with floating cards
- **Glassmorphism UI** - Dark futuristic design with blur effects
- **Dynamic Projects** - Fetched from MySQL via PHP API
- **Responsive Design** - Mobile-first approach
- **GSAP Ready** - Animation framework integrated

## Getting Started

### Prerequisites

- Node.js 18+
- PHP 7.4+
- MySQL 5.7+
- XAMPP/WAMP (for local PHP/MySQL)

### Frontend Setup

```bash
cd portfolio-app
npm install
npm start
```

Visit http://localhost:4200

### Backend Setup

1. Start Apache + MySQL in XAMPP/WAMP
2. Create database and import `portfolio-api/setup.sql`
3. Place `portfolio-api` in `htdocs` folder
4. Access: http://localhost/portfolio-api/getProjects.php

## Project Structure

```
├── portfolio-app/          # Angular SPA
│   └── src/app/
│       ├── components/     # Reusable UI components
│       │   ├── hero/      # Three.js hero section
│       │   ├── navbar/    # Navigation
│       │   ├── footer/    # Footer
│       │   └── project-card/
│       ├── pages/         # Route pages
│       │   ├── home/
│       │   ├── about/
│       │   ├── projects/
│       │   └── contact/
│       ├── services/      # API services
│       └── models/        # TypeScript interfaces
├── portfolio-api/          # PHP Backend
│   ├── db.php             # Database connection
│   ├── getProjects.php    # Projects API endpoint
│   └── setup.sql          # Database schema
```

## Pages

- **/** - Hero section with Three.js particles + featured projects
- **/about** - Timeline, skills bars, tech stack
- **/projects** - Filterable project grid
- **/contact** - Contact form + social links

## Deployment

### Frontend (Vercel)

```bash
cd portfolio-app
npx vercel --prod
```

### Backend

Deploy PHP/MySQL to:
- [Render](https://render.com)
- [Railway](https://railway.app)
- [InfinityFree](https://infinityfree.com)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/getProjects.php` | Fetch all projects |

### Response Format

```json
[
  {
    "id": 1,
    "title": "Project Title",
    "description": "Project description",
    "image": "https://image.url",
    "github_link": "https://github.com",
    "live_link": "https://demo.com",
    "tags": ["AI", "ML", "Python"]
  }
]
```

## License

MIT License - feel free to use for your own portfolio!