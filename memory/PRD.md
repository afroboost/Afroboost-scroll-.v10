# Afroboost - Product Requirements Document

## Original Problem Statement
Multi-partner SaaS platform for fitness coaching with a mobile-first, "Instagram Reels" style vertical video feed. Super Admin (Bassi) manages partners who can customize their own storefronts.

## Core Features Implemented

### ✅ Mission v12.1 (March 2026) - COMPLETED
**Contrôle Admin & Design Premium Minimalist**
1. **Prix Services Dynamiques** - Super Admin définit le coût en crédits:
   - Campagne: 2 crédits
   - Conversation IA: 1 crédit
   - Code Promo: 3 crédits
2. **Design Premium Sans Cadre** - Fond #000000, icônes nues, violet #D91CD2 glow uniquement
3. **Nouvel onglet "Tarifs Services"** dans le panneau Super Admin

**Endpoints:**
- `GET /api/platform-settings` - Retourne service_prices
- `PUT /api/platform-settings` - Modifie service_prices (Admin only)

### ✅ Mission v11.9 (March 2026) - COMPLETED
**Vidéo Full-Width**
- Bordures supprimées, width=100% viewport

### ✅ Mission v11.8 (March 2026) - COMPLETED
**Scroll Réserver**
- +412px vers sessions-section

### ✅ Missions v11.2-v11.7 - COMPLETED
- Système codes & crédits
- Logique multi-partenaires
- PWA installable

## Architecture

```
/app/
├── backend/
│   ├── server.py              # v12.1: service_prices in platform-settings
│   └── routes/
│       ├── promo_routes.py
│       └── reservation_routes.py
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── components/
│   │       ├── SuperAdminPanel.js  # v12.1: Tab Tarifs Services
│   │       └── PartnersCarousel.js
│   └── public/
│       ├── manifest.json
│       └── sw.js
└── memory/PRD.md
```

## Key API - Service Prices (v12.1)

```json
// GET /api/platform-settings
{
  "service_prices": {
    "campaign": 2,
    "ai_conversation": 1,
    "promo_code": 3
  }
}
```

## Data Status
- ✅ 22 réservations
- ✅ 14 contacts
- ✅ BOSS: 41/47 séances
- ✅ Video: full-width

## Pending Tasks (P0/P1)
1. **P0**: Stripe Connect for partner payouts
2. **P1**: Production deployment
3. **P1**: Implement credit check before services (verrouillage)

## Super Admin Access
- Emails: `contact.artboost@gmail.com`, `afroboost.bassi@gmail.com`
- Access: Triple-click footer "© Afroboost 2026"

## Testing Status
- Mission v12.1: 100% validated (9/9 backend tests)
- Report: `/app/test_reports/iteration_139.json`

---
Last Updated: March 2026 - Mission v12.1 VALIDATED
