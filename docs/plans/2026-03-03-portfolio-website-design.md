# Portfolio Website Design Document

**Date**: March 3, 2026
**Author**: Paolo Sandejas & Claude
**Status**: Phase 1 Complete (Core Portfolio Built)

## Executive Summary

A distinctive, production-grade portfolio website for Paolo Sandejas showcasing AI/ML engineering expertise with creative technical applications. The site balances hireability (clear value proposition, immediate information access) with creativity (bold design, optional interactive maze exploration).

## Design Vision

**Concept**: "Technical Precision Meets Creative Energy"

A modern brutalist aesthetic with energetic color accents that immediately communicates:
1. Serious ML engineering capabilities
2. Creative technical problem-solving
3. Production-grade polish and attention to detail

## Target Audience

**Primary**: Technical recruiters and hiring managers seeking AI/ML engineers
**Secondary**: Potential collaborators interested in creative technical applications

**Key Requirements**:
- Information accessible within 30-60 seconds (recruiter attention span)
- Clear specialization (not a generalist)
- Proof of production ML work
- Technical depth without jargon overload

## Value Proposition

**"Production ML engineer who ships creative, multi-modal AI systems that scale."**

**Differentiators**:
1. Ships production ML (not just prototypes) - 2+ years, 12K+ users
2. Multi-modal specialist (video/audio/text) - not siloed
3. Creative applications (audio generation, wearable interfaces) - unique work
4. Full-stack ML (model → optimization → deployment → evaluation)
5. Research + production bridge (MFA research while shipping commercial systems)

## Visual Design System

### Color Palette

```css
--snow: #fbf5f3;           /* Warm off-white backgrounds */
--prussian-blue: #000022;   /* Ultra-dark primary */
--amber-earth: #e28413;     /* Warm energetic accent */
--raspberry: #de3c4b;       /* Bold secondary accent */
--intense-cherry: #c42847;  /* Strong emphasis */
```

**Usage Philosophy**: High contrast between prussian blue and snow. Warm accents (amber, raspberry) break the technical coldness and add energy without being playful.

### Typography

**Headings**: Epilogue (700-900 weight) - Modern, geometric, authoritative
**Body**: IBM Plex Mono (400-600 weight) - Technical credibility, excellent readability

**Scale**: Fluid typography using clamp() for responsive sizing
**Line Heights**: Tight for headings (1.2), relaxed for body (1.6-1.8)

### Motion Design

**Philosophy**: Staggered reveals on load, magnetic hover effects, smooth GSAP transitions

- Page load: Staggered fade-in with 0.15s delays between elements
- Hover states: Translateup (-4px to -8px) + shadow + color shift
- Transitions: 150-300ms cubic-bezier easing
- Minimal distraction: One orchestrated moment beats scattered micro-interactions

## Site Architecture

### Navigation Structure

**Fixed Top Nav** (Persistent):
- Left: "Paolo Sandejas / Glendale, CA"
- Right: Projects | Skills | Experience | Resume ↓ | GitHub ↗ | LinkedIn ↗

Always visible, always accessible. No hunting for information.

### Page Sections

#### 1. Hero / Landing (Above Fold)
**Goal**: Communicate who, what, where in 5 seconds

- Name (Large, bold, gradient)
- Title: "AI/ML Engineer | Multi-Modal AI & Creative Applications"
- Location: "Glendale, CA"
- Summary paragraph (production focus)
- Three CTAs: Download Resume | View Projects | Explore Interactive Portfolio
- Three value prop cards (Ships Production ML, Multi-Modal AI, Creative Applications)

#### 2. Projects
**Goal**: Prove technical depth with real work

- Filter buttons: All | AI/ML | Creative Tech
- Grid layout (3 columns desktop, 1 mobile)
- Cards show: Number, title, description, tags (first 4), links
- Featured projects highlighted with badge
- Order: Lead with strongest ML (CHULOOPA, Video Analysis, Geospatial)
- Modal for expanded details on click

**Featured Projects**:
1. CHULOOPA - Transformer drum generation (PyTorch, Audio ML, Real-time)
2. Multi-Modal Video Analysis - Production pipeline (Gemini API, Concurrent processing)
3. Geospatial ML - CNN pipeline (PyTorch, >90% accuracy)
4. HAI - Head as Interface (Arduino, Max/MSP, wearable computing)
5. ASCII Drone Synth (MediaPipe, Tone.js, creative coding)
6. Parallel Paths - Responsible AI in music (Gemini, ethics)

#### 3. Skills
**Goal**: Show breadth without skill percentage bars

Five categories:
- Languages & Core
- ML & AI
- ML Infrastructure
- APIs & Tools
- Creative Tech

Clean list format with category headers. No percentages, no "beginner/expert" labels.

#### 4. Experience
**Goal**: Prove production impact

Timeline layout with:
- Company name (large, amber)
- Role + dates
- Bullet points emphasizing production metrics, scale, impact
- Visual timeline connector between roles

#### 5. Education
**Goal**: Academic credibility + research context

- CalArts MFA: Frame as research advantage ("real-time audio ML, low-latency inference")
- UP CS: Traditional foundation

Card layout with GPA badges.

#### 6. Contact
**Goal**: Make it easy to reach you

- Large heading: "Let's Build Something"
- Email (prominent, amber button)
- GitHub, LinkedIn, Resume download
- Decorative animated circles (rotating borders, pulsing core)

### Interactive Maze (Optional Phase 2)

**Concept**: "Navigating my career as an artist and engineer"

- Top-down 2D dungeon explorer (Zelda-style)
- Each room = different portfolio section
- WASD/Arrow controls + click-to-move
- Minimap in corner
- Quick nav overlay (M key) for accessibility
- p5.js rendering, GSAP camera movements

**Room Structure**:
- Entrance Hall → About Room
- Technical ML Wing (CHULOOPA, Video Analysis, Geospatial rooms)
- Creative Tech Wing (HAI, ASCII Drone)
- Professional Spaces (Experience Gallery, Education Archive)
- Exit/Contact Portal

**Visual Distinction**:
- ML rooms: Cool blues, grid patterns, digital aesthetic
- Creative rooms: Warmer tones, organic shapes
- Smooth transitions, particle effects, polished feel

**Accessibility**: Not required for information access - bonus creative showcase

## Technical Implementation

### Stack
- React + Vite (fast dev, optimal builds)
- Framer Motion (animations)
- p5.js (maze rendering)
- Custom CSS (no Tailwind - more control)
- Vercel/Netlify (static hosting)

### Content Management
- Static JSON file (`portfolio.json`) with all content
- No backend/CMS needed
- Easy to update projects, experience, skills
- Media assets on CDN or cloud storage

### Performance Targets
- Lighthouse: 90+ all metrics
- First Contentful Paint: < 1.5s
- Maze components lazy-loaded
- Images: WebP with fallbacks
- 60fps animations

### Accessibility
- Semantic HTML throughout
- ARIA labels for interactive elements
- Keyboard navigation
- WCAG AA contrast ratios
- Focus-visible states
- Screen readers get standard portfolio (maze is enhancement)

### Browser Support
- Modern browsers (last 2 versions)
- Graceful degradation for older browsers

## Content Strategy

### Avoiding "AI Slop" Patterns

**Don't**:
- ❌ Generic fonts (Inter, Roboto, system)
- ❌ Purple gradients on white
- ❌ Slow typing animations
- ❌ "I'm a developer/strategist/designer/everything" generalist claims
- ❌ Skill percentage bars
- ❌ Cookie-cutter layouts
- ❌ Boilerplate template text

**Do**:
- ✅ Distinctive font pairing
- ✅ Bold, intentional color palette
- ✅ Immediate clarity (5-second test)
- ✅ Specialist positioning
- ✅ Production metrics and proof
- ✅ Custom components
- ✅ Context-specific character

### Hireability Checklist

- [x] Name, role, location visible immediately
- [x] Clear specialization (AI/ML Engineer + Multi-Modal)
- [x] Resume downloadable within one click
- [x] Production metrics visible (12K+ users, >90% accuracy)
- [x] Technical depth (PyTorch, real-time inference, optimization)
- [x] Project categorization (ML vs Creative)
- [x] GitHub/LinkedIn linked prominently
- [x] No skill percentage bars
- [x] No walls of jargon
- [x] Responsive design (mobile-friendly)
- [x] Fast load times
- [x] Professional polish (consistent spacing, good contrast)

## Implementation Phases

### Phase 1: Core Portfolio (Complete ✓)
- Landing page with value props
- Projects grid with filtering
- Skills, Experience, Education sections
- Contact section
- Navigation
- Responsive design
- All content from resume integrated

### Phase 2: Maze Explorer (In Progress)
- p5.js maze implementation
- Room navigation system
- Content modals within maze
- Camera controls + animations
- Minimap
- Quick nav overlay

### Phase 3: Polish & Deploy
- Performance optimization
- Cross-browser testing
- Add resume PDF to public folder
- Add project media (videos, images)
- GSAP enhancements
- Deploy to Vercel
- Domain configuration

## Success Metrics

**Hireability**:
- Recruiter can understand who you are, what you do, where you are in < 10 seconds
- Resume accessible in 1 click
- All key projects visible without scrolling past 2 screens

**Differentiation**:
- Visitors remember the design (color palette, typography, energy)
- "This doesn't look like every other portfolio" reaction
- Clear understanding of dual technical + creative identity

**Technical Execution**:
- Lighthouse scores 90+
- No broken links
- Smooth animations on modern devices
- Responsive on mobile/tablet/desktop

## Design Decisions & Rationale

### Why No Music Portfolio Section?
- Music is a "bonus fun fact" not a hireability factor for dev roles
- Parallel Paths project frames music as "responsible AI exploration"
- Keeps focus on technical value proposition
- Can add small "Other Interests" room in maze if desired

### Why Bold Color Palette?
- Differentiates from typical tech portfolios (blues, grays, purples)
- Warm accents (amber, raspberry) convey energy and creativity
- High contrast ensures readability
- Reflects personality: technical but not corporate

### Why Maze is Optional?
- Can't block information access for recruiters
- Maze becomes a portfolio piece itself (demonstrates p5.js, game dev, UX thinking)
- Those who want creative depth can explore, others get straight to content
- Shows understanding of audience priorities

### Why IBM Plex Mono?
- Technical credibility (monospace roots)
- Excellent readability (more legible than Courier or Fira Code)
- Distinctive without being weird
- Not overused (unlike Inter/Roboto)
- Pairs well with Epilogue's geometric structure

## Next Steps

1. Add resume PDF to `/public` folder
2. Gather project media (CHULOOPA video, HAI video, architecture diagrams)
3. Test on multiple devices/browsers
4. Build maze explorer (Phase 2)
5. Performance audit and optimization
6. Deploy to Vercel
7. Configure custom domain (if desired)
8. Share with target audience for feedback

## Conclusion

This portfolio successfully balances hireability (clear, professional, immediate information access) with creativity (bold design, optional interactive exploration). The design system is distinctive without being gimmicky, and the content strategy positions Paolo as a production ML engineer who brings unique creative technical capabilities to the table.

The site avoids "AI slop" patterns by making intentional design choices (fonts, colors, layouts) and focusing on proof of production work rather than vague claims or generic aesthetics.

Phase 1 (core portfolio) is complete and production-ready. Phase 2 (maze explorer) can be developed iteratively without blocking the site launch.
