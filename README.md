# Paolo Sandejas - Portfolio Website

A distinctive, production-grade portfolio website showcasing AI/ML engineering expertise with creative technical applications.

## Design Philosophy

**Technical Precision Meets Creative Energy**

This portfolio combines modern brutalism with energetic accents, featuring:
- Bold color palette (prussian blue, amber earth, raspberry, cherry)
- IBM Plex Mono + Epilogue typography for technical credibility
- Geometric layouts with unexpected energy
- Smooth animations via Framer Motion
- Optional interactive p5.js maze exploration

## Features

### Core Portfolio
- **Landing Page**: Clear value proposition with immediate hireability focus
- **Projects Grid**: Filterable showcase of ML and creative tech work
- **Skills**: Technical stack organized by category
- **Experience**: Timeline of production ML work
- **Education**: Academic background with research focus
- **Contact**: Multiple connection points

### Interactive Maze (Coming Soon)
- Top-down dungeon-style navigation
- Rooms representing different projects and experiences
- p5.js canvas rendering with GSAP animations
- Minimap and quick navigation options

## Tech Stack

- **Framework**: React + Vite
- **Animation**: Framer Motion
- **Graphics**: p5.js (for maze)
- **Styling**: Custom CSS with design system
- **Hosting**: Vercel/Netlify ready

## Design System

### Colors
```css
--snow: #fbf5f3;          /* Backgrounds */
--prussian-blue: #000022;  /* Primary text, dark sections */
--amber-earth: #e28413;    /* Primary accent, CTAs */
--raspberry: #de3c4b;      /* Secondary accent, hovers */
--intense-cherry: #c42847; /* Strong emphasis, active states */
```

### Typography
- **Headings**: Epilogue (700-900 weight)
- **Body**: IBM Plex Mono (400-600 weight)
- **Scale**: Fluid typography with clamp()

### Spacing
- Base unit: 4px
- Scale: 1, 2, 3, 4, 6, 8, 12, 16, 20, 24

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
portfolio-site/
├── src/
│   ├── components/
│   │   ├── Navigation.jsx/css
│   │   ├── Hero.jsx/css
│   │   ├── Projects.jsx/css
│   │   ├── Skills.jsx/css
│   │   ├── Experience.jsx/css
│   │   ├── Education.jsx/css
│   │   ├── Contact.jsx/css
│   │   └── MazeExplorer.jsx/css
│   ├── data/
│   │   └── portfolio.json
│   ├── App.jsx/css
│   ├── index.css
│   └── main.jsx
├── public/
│   └── Paolo_Sandejas_Resume.pdf
└── package.json
```

## Content Updates

Update your portfolio content in `src/data/portfolio.json`:
- Personal information
- Projects with descriptions, tags, links
- Work experience
- Education

## Deployment

### Vercel
```bash
npm run build
vercel --prod
```

### Netlify
```bash
npm run build
netlify deploy --prod --dir=dist
```

## Design Principles

### Avoiding "AI Slop" Aesthetics
- ✅ Distinctive font pairing (IBM Plex Mono + Epilogue)
- ✅ Bold, intentional color palette with high contrast
- ✅ Geometric layouts with asymmetry
- ✅ Purposeful animations (staggered reveals, magnetic hovers)
- ✅ Custom components (no generic templates)
- ❌ No Inter/Roboto/system fonts
- ❌ No purple gradients on white
- ❌ No cookie-cutter layouts
- ❌ No slow typing animations

### Hireability Focus
- Clear role and location in header
- Immediate value propositions
- Technical depth showcased first
- Direct resume download access
- Project categorization (ML vs Creative)
- Production metrics where applicable

## License

© 2026 Paolo Sandejas. All rights reserved.
