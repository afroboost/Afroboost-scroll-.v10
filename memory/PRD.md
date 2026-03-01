# Afroboost - Product Requirements Document

## Original Problem Statement
Multi-partner SaaS platform for fitness coaching with a mobile-first, "Instagram Reels" style vertical video feed. Super Admin (Bassi) manages partners who can customize their own storefronts.

## Core Features Implemented

### ✅ Mission v11.2 (March 2026) - COMPLETED
1. **Prompt Isolation** - Each conversation link has isolated `custom_prompt` that replaces base AI instructions
2. **PWA Installation** - `manifest.json` display:standalone + `sw.js` service worker for fullscreen app
3. **Réserver Button** - Frameless, transparent background, positioned bottom-right on video overlay
4. **Campaign Media** - Full support for images/videos in email campaigns with notifications

### ✅ Previous Missions Completed
- v10.9: Clean vitrine UI, redesigned Réserver button
- v10.7: Dashboard icon-based cards (Envelope, Calendar)
- v10.6: Minimalist 2-column grid dashboard
- v10.5: Harmonized dashboard buttons
- v10.4: Chat persistence with localStorage
- v10.3: Glow Violet effect on Like button
- v10.2: Full-screen 16:9 video support
- v10.0: Instagram Reels style UI overhaul
- v9.x: Partner login flow, video deduplication, unique showcase logic

## Architecture

```
/app/
├── backend/
│   ├── server.py           # FastAPI main (6731 lines)
│   ├── routes/             # Modular routes (in progress)
│   └── shared.py
├── frontend/
│   ├── src/
│   │   ├── App.js          # Main routing
│   │   ├── components/
│   │   │   ├── CoachVitrine.js    # Partner storefront (1190 lines)
│   │   │   ├── CoachDashboard.js  # Partner management (large)
│   │   │   ├── PartnersCarousel.js # Main Reels feed
│   │   │   └── ChatWidget.js       # Chat with AI (5174 lines)
│   │   └── services/
│   │       ├── SoundManager.js     # Notification sounds
│   │       └── notificationService.js
│   └── public/
│       ├── manifest.json   # PWA config
│       └── sw.js           # Service Worker
└── memory/PRD.md
```

## Key Technical Concepts
- **Custom Prompt Isolation**: `custom_prompt` field on chat sessions replaces base AI prompt
- **PWA**: `display: standalone` + service worker for fullscreen experience
- **UI Style**: Violet glow (#D91CD2), transparent backgrounds, absolute positioning

## Pending Tasks (P0/P1)
1. **P0**: Stripe Connect for partner payouts
2. **P1**: Complete credit deduction for Chat actions
3. **P1**: Continue modularizing server.py
4. **P1**: Continue modularizing CoachDashboard.js
5. **P1**: Production deployment (currently preview-only)

## Super Admin Access
- Emails: `contact.artboost@gmail.com`, `afroboost.bassi@gmail.com`
- Login: Triple-click footer "© Afroboost 2026"

## Testing Status
- Mission v11.2: 10/10 backend tests PASS, 7/7 frontend UI tests PASS
- Test file: `/app/backend/tests/test_v112_mission.py`
- Report: `/app/test_reports/iteration_133.json`

---
Last Updated: March 2026 - Mission v11.2 VALIDATED
