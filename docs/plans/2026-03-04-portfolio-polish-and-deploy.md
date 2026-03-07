# Portfolio Website Polish & Deploy Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Polish the portfolio website, fix remaining issues, add project media, and deploy to production

**Architecture:** Frontend-only React application with static content, deploying to Vercel with automatic builds from GitHub

**Tech Stack:** React, Vite, Framer Motion, Custom CSS, Vercel

---

## Current Status

✅ **Completed:**
- Core portfolio structure (Hero, Projects, Skills, Experience, Education, Contact)
- Brand design system with distinctive color palette
- Responsive navigation
- Framer Motion animations
- Resume PDF added to public folder
- Fixed contrast issues (dark sections now properly styled)
- Fixed hero text hierarchy (role appears once above name)
- Updated ASCII drone link and LinkedIn URL

❌ **Remaining Work:**
- Add project media (videos, images, GitHub links)
- Test all interactive elements
- Cross-browser testing
- Performance optimization
- Deploy to Vercel
- Optional: Build p5.js maze explorer (Phase 2)

---

## Task 1: Add Project Media & Links

**Files:**
- Modify: `src/data/portfolio.json`

**Step 1: Add CHULOOPA GitHub link**

Update the CHULOOPA project entry:

```json
{
  "id": "chuloopa",
  "title": "CHULOOPA - Transformer-Based Drum Generation",
  "description": "Low-latency transformer model for real-time rhythmic generation in live performance. Researching efficient inference pipelines for generative audio systems.",
  "tags": ["PyTorch", "Audio ML", "Real-time Inference", "ChucK", "Python", "Transformers"],
  "category": "ml",
  "featured": true,
  "links": {
    "github": "https://github.com/paolosand/CHULOOPA",
    "demo": null
  },
  "media": {
    "thumbnail": null,
    "video": null
  }
}
```

**Step 2: Verify CHULOOPA repo exists**

Run: `curl -I https://github.com/paolosand/CHULOOPA`
Expected: HTTP 200 or check if repo needs to be made public

**Step 3: Test project links in browser**

1. Start dev server: `npm run dev`
2. Navigate to Projects section
3. Click on CHULOOPA card
4. Verify GitHub link opens correctly

**Step 4: Commit**

```bash
git add src/data/portfolio.json
git commit -m "feat: add CHULOOPA GitHub link"
```

---

## Task 2: Responsive Testing & Mobile Fixes

**Files:**
- Modify: `src/components/Navigation.css`
- Modify: `src/components/Hero.css`
- Modify: `src/components/Projects.css`

**Step 1: Test on mobile viewport**

1. Open browser DevTools
2. Toggle device toolbar (Cmd+Shift+M)
3. Test iPhone SE (375px) and iPad (768px)
4. Check for:
   - Text overflow
   - Button sizes (touch-friendly 44px minimum)
   - Navigation collapse
   - Card layouts

**Step 2: Fix navigation mobile layout if needed**

If navigation is cramped, update `src/components/Navigation.css`:

```css
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-4);
  }

  .nav-brand {
    font-size: 0.85rem;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
    gap: var(--space-3);
    width: 100%;
  }

  .nav-link {
    font-size: 0.75rem;
    padding: var(--space-2) 0;
  }
}
```

**Step 3: Test touch targets**

Ensure all interactive elements meet 44x44px minimum:
- Navigation links
- Buttons in Hero
- Project cards
- Contact links

**Step 4: Commit**

```bash
git add src/components/*.css
git commit -m "fix: improve mobile responsive design"
```

---

## Task 3: Performance Optimization

**Files:**
- Create: `src/components/LazyImage.jsx`
- Modify: `src/components/Projects.jsx` (if adding images)

**Step 1: Add lazy loading for future images**

Create `src/components/LazyImage.jsx`:

```jsx
import { useState, useEffect, useRef } from 'react';

const LazyImage = ({ src, alt, className, placeholder }) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(false);
  const imgRef = useRef();

  useEffect(() => {
    if (!imgRef.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { rootMargin: '50px' }
    );

    observer.observe(imgRef.current);

    return () => observer.disconnect();
  }, []);

  return (
    <div ref={imgRef} className={className}>
      {isInView && (
        <img
          src={src}
          alt={alt}
          onLoad={() => setIsLoaded(true)}
          style={{ opacity: isLoaded ? 1 : 0, transition: 'opacity 0.3s' }}
        />
      )}
      {!isLoaded && placeholder && <div className="img-placeholder">{placeholder}</div>}
    </div>
  );
};

export default LazyImage;
```

**Step 2: Test current performance**

Run Lighthouse audit:
1. Open DevTools > Lighthouse
2. Run audit for Desktop and Mobile
3. Target scores: 90+ across all metrics

**Step 3: Commit**

```bash
git add src/components/LazyImage.jsx
git commit -m "feat: add lazy loading component for images"
```

---

## Task 4: Accessibility Audit

**Files:**
- Modify: `src/components/Projects.jsx`
- Modify: `src/components/Navigation.jsx`

**Step 1: Test keyboard navigation**

1. Use Tab key to navigate through site
2. Verify focus visible on all interactive elements
3. Test Escape to close project modal
4. Ensure all actions keyboard-accessible

**Step 2: Add ARIA labels where missing**

Update Projects modal close button:

```jsx
<button
  className="modal-close"
  onClick={() => setSelectedProject(null)}
  aria-label="Close project details"
>
  ✕
</button>
```

**Step 3: Test with screen reader**

macOS VoiceOver test:
1. Enable VoiceOver (Cmd+F5)
2. Navigate through site
3. Verify all content announced correctly
4. Check heading hierarchy (H1 → H2 → H3)

**Step 4: Commit**

```bash
git add src/components/*.jsx
git commit -m "a11y: improve keyboard navigation and screen reader support"
```

---

## Task 5: Browser Compatibility Testing

**Step 1: Test in multiple browsers**

Test on:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

Check for:
- CSS Grid layout rendering
- Framer Motion animations
- Custom scrollbar styling
- Focus visible styles

**Step 2: Document any browser-specific issues**

Create issue list if bugs found, prioritize critical rendering issues

**Step 3: Add CSS fallbacks if needed**

For older browsers, ensure graceful degradation:

```css
/* Fallback for browsers without backdrop-filter */
.project-modal-overlay {
  background: rgba(0, 0, 34, 0.95);
  backdrop-filter: blur(10px);
}

@supports not (backdrop-filter: blur(10px)) {
  .project-modal-overlay {
    background: rgba(0, 0, 34, 0.98);
  }
}
```

---

## Task 6: Git Repository Setup

**Step 1: Initialize git repository**

```bash
git init
git add .
git commit -m "feat: initial portfolio website implementation

- Landing page with hero section and value props
- Projects grid with filtering (AI/ML and Creative Tech)
- Skills section organized by category
- Experience timeline with production metrics
- Education cards with GPA highlighting
- Contact section with social links
- Responsive navigation with resume download
- Brand design system (IBM Plex Mono + Epilogue)
- Custom color palette (prussian blue, amber earth, raspberry)
- Framer Motion animations throughout

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**Step 2: Create GitHub repository**

```bash
# Create repo on GitHub via gh CLI or web interface
gh repo create portfolio-site --public --source=. --remote=origin --push
```

Or manually:
1. Go to github.com/new
2. Name: `portfolio-site`
3. Visibility: Public
4. Don't initialize with README (already have one)
5. Copy the git remote URL

**Step 3: Push to GitHub**

```bash
git remote add origin https://github.com/paolosand/portfolio-site.git
git branch -M main
git push -u origin main
```

**Step 4: Verify push**

Visit: `https://github.com/paolosand/portfolio-site`
Confirm all files visible

---

## Task 7: Deploy to Vercel

**Step 1: Install Vercel CLI (if not installed)**

```bash
npm install -g vercel
```

**Step 2: Login to Vercel**

```bash
vercel login
```

Follow prompts to authenticate

**Step 3: Deploy from project directory**

```bash
vercel --prod
```

Answer prompts:
- Set up and deploy? Yes
- Which scope? (Your account)
- Link to existing project? No
- Project name? `portfolio-site` or `paolo-sandejas`
- Directory? `./` (current directory)
- Override settings? No

**Step 4: Verify deployment**

1. Note the deployment URL (e.g., `paolo-sandejas.vercel.app`)
2. Visit URL in browser
3. Test all sections, links, resume download
4. Check mobile responsive on real device if possible

**Step 5: Configure custom domain (optional)**

If you have a custom domain:

```bash
vercel domains add yourdomain.com
```

Follow DNS configuration instructions

---

## Task 8: Final QA Checklist

**Step 1: Click-through testing**

Go through each section systematically:

**Navigation:**
- [ ] All nav links scroll to correct sections
- [ ] Resume download works
- [ ] GitHub link opens in new tab
- [ ] LinkedIn link opens in new tab

**Hero:**
- [ ] Text is readable and properly hierarchical
- [ ] All 3 CTA buttons work
- [ ] Value props display correctly
- [ ] Animations play smoothly

**Projects:**
- [ ] Filter buttons work (All, AI/ML, Creative Tech)
- [ ] Project cards show correct info
- [ ] Clicking card opens modal
- [ ] Modal close button works
- [ ] External links work (GitHub, demos)
- [ ] ASCII drone demo link works

**Skills:**
- [ ] All skill categories visible
- [ ] No layout issues

**Experience:**
- [ ] Timeline displays correctly
- [ ] Dates are accurate
- [ ] Bullets are readable

**Education:**
- [ ] Both degrees show
- [ ] GPA badges display

**Contact:**
- [ ] Email link opens mail client
- [ ] All social links work
- [ ] Resume download works
- [ ] Animated circles render

**Step 2: Cross-browser check on deployed site**

Test production URL on:
- [ ] Desktop Chrome
- [ ] Desktop Safari
- [ ] Desktop Firefox
- [ ] Mobile Safari (iPhone)
- [ ] Mobile Chrome (Android if available)

**Step 3: Performance check**

Run Lighthouse on production URL:
- [ ] Performance: 90+
- [ ] Accessibility: 90+
- [ ] Best Practices: 90+
- [ ] SEO: 90+

**Step 4: Share test**

Send link to 1-2 people for feedback:
- [ ] Can they understand who you are in 5 seconds?
- [ ] Can they find your resume easily?
- [ ] Do they remember the design?
- [ ] Any broken links or bugs?

---

## Task 9: Documentation Updates

**Files:**
- Modify: `README.md`
- Create: `docs/DEPLOYMENT.md`

**Step 1: Update README with deployment info**

Add to README.md:

```markdown
## Live Site

**Production:** https://paolo-sandejas.vercel.app (or your custom domain)

## Recent Updates

- March 4, 2026: Initial launch with core portfolio sections
- Fixed contrast issues in Contact section
- Added latest resume (LLM research position)
- Corrected LinkedIn and ASCII Drone links
```

**Step 2: Create deployment guide**

Create `docs/DEPLOYMENT.md`:

```markdown
# Deployment Guide

## Vercel Deployment

The site auto-deploys on every push to `main` branch.

**Manual deployment:**
```bash
vercel --prod
```

**Deployment URL:** https://paolo-sandejas.vercel.app

## GitHub Actions (Future)

Currently using Vercel's automatic GitHub integration.
No additional CI/CD setup required.

## Environment Variables

None required - site is fully static.

## Custom Domain

If setting up custom domain:
1. `vercel domains add yourdomain.com`
2. Add DNS records as shown in Vercel dashboard
3. Wait for DNS propagation (up to 48 hours)
```

**Step 3: Commit documentation**

```bash
git add README.md docs/DEPLOYMENT.md
git commit -m "docs: add deployment information and update README"
git push origin main
```

---

## Task 10: Optional - Maze Explorer Placeholder Enhancement

**Files:**
- Modify: `src/components/MazeExplorer.jsx`
- Modify: `src/components/MazeExplorer.css`

**Step 1: Improve placeholder messaging**

Update `MazeExplorer.jsx` to make it more engaging:

```jsx
<div className="maze-placeholder">
  <h2>🎮 Interactive Portfolio Explorer</h2>
  <p className="maze-tagline">
    Navigate my career journey through an interactive 2D maze
  </p>

  <div className="maze-features">
    <div className="maze-feature">
      <span className="feature-icon">🗺️</span>
      <span>Top-down dungeon exploration</span>
    </div>
    <div className="maze-feature">
      <span className="feature-icon">🎨</span>
      <span>Rooms for each project</span>
    </div>
    <div className="maze-feature">
      <span className="feature-icon">✨</span>
      <span>Smooth p5.js animations</span>
    </div>
    <div className="maze-feature">
      <span className="feature-icon">🎯</span>
      <span>Interactive discovery</span>
    </div>
  </div>

  <p className="maze-status">Coming Soon - Phase 2</p>

  <button className="maze-return-btn" onClick={onExit}>
    ← Back to Portfolio
  </button>
</div>
```

**Step 2: Style the enhanced placeholder**

Update `MazeExplorer.css`:

```css
.maze-tagline {
  font-size: 1rem;
  opacity: 0.7;
  margin-bottom: var(--space-8);
}

.maze-features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
  margin: var(--space-8) 0;
  text-align: left;
}

.maze-feature {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  background: rgba(226, 132, 19, 0.05);
  border: 1px solid rgba(226, 132, 19, 0.2);
  border-radius: 4px;
}

.feature-icon {
  font-size: 1.5rem;
}

.maze-status {
  font-size: 0.9rem;
  color: var(--amber-earth);
  font-weight: 600;
  margin-top: var(--space-6);
}
```

**Step 3: Test the enhanced placeholder**

1. Click "Explore Interactive Portfolio"
2. Verify new layout looks good
3. Check responsiveness on mobile

**Step 4: Commit**

```bash
git add src/components/MazeExplorer.*
git commit -m "feat: enhance maze explorer placeholder with feature preview"
git push origin main
```

---

## Success Criteria

**MVP Launch Ready When:**
- [x] All sections render correctly
- [x] Resume downloads work
- [x] All external links functional
- [x] Mobile responsive
- [x] Lighthouse scores 90+
- [x] Deployed to production
- [x] GitHub repo public
- [x] No console errors

**Future Enhancements (Phase 2):**
- [ ] Build actual p5.js maze with navigation
- [ ] Add project videos and screenshots
- [ ] Blog/writing section
- [ ] Analytics integration (Vercel Analytics)
- [ ] Contact form with email integration
- [ ] Dark mode toggle

---

## Rollback Plan

If deployment has critical issues:

```bash
# Revert to previous commit
git revert HEAD
git push origin main

# Vercel will auto-deploy the reverted version
```

Or via Vercel dashboard:
1. Go to Deployments
2. Find previous working deployment
3. Click "..." → "Promote to Production"

---

## Next Steps After Launch

1. **Share with network:**
   - Update LinkedIn with portfolio link
   - Add to resume
   - Share in relevant communities

2. **Monitor performance:**
   - Check Vercel Analytics
   - Note any user-reported issues
   - Track which projects get most views

3. **Iterate:**
   - Gather feedback
   - Plan Phase 2 features
   - Keep content updated

4. **Phase 2 Planning:**
   - Design p5.js maze mechanics
   - Create room layouts and content strategy
   - Build interactive navigation system
