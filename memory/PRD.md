# Afroboost - Product Requirements Document

## Original Problem Statement
Multi-partner SaaS platform for fitness coaching with a mobile-first, "Instagram Reels" style vertical video feed. Super Admin (Bassi) manages partners who can customize their own storefronts.

## Core Features Implemented

### ✅ Mission v11.4 (March 2026) - COMPLETED
**Système de Codes & Crédits Chat réparé**
1. **Validation Code Promo** - Crée automatiquement un abonnement avec séances
2. **Bloc Info Abonnement** - Affiche offre, solde (ex: 41/47 séances), date expiration
3. **Multi-Réservation** - Possibilité de réserver tant qu'il reste des séances
4. **Déduction Automatique** - -1 séance à chaque réservation

**Nouveaux endpoints:**
- `POST /api/discount-codes/validate` - Valide code et crée abonnement
- `GET /api/discount-codes/subscriptions/status` - Retourne le solde
- `POST /api/discount-codes/subscriptions/deduct` - Déduit 1 séance
- `POST /api/reservations` - Auto-déduit de l'abonnement

### ✅ Mission v11.2 (March 2026) - COMPLETED
1. **Prompt Isolation** - Chaque lien a un custom_prompt isolé
2. **PWA Installation** - manifest.json + sw.js pour fullscreen
3. **Bouton Réserver** - Sans cadre, bottom-right
4. **Campaign Media** - Support images/vidéos + notifications

### ✅ Previous Missions (v10.x)
- v10.9: Clean vitrine UI, redesigned Réserver button
- v10.7: Dashboard icon-based cards
- v10.6: Minimalist 2-column grid dashboard
- v10.5: Harmonized dashboard buttons
- v10.4: Chat persistence with localStorage
- v10.3: Glow Violet effect on Like button
- v10.2: Full-screen 16:9 video support
- v10.0: Instagram Reels style UI overhaul

## Architecture

```
/app/
├── backend/
│   ├── server.py
│   ├── routes/
│   │   ├── promo_routes.py      # v11.4: Subscription system
│   │   ├── reservation_routes.py # v11.4: Auto-deduct sessions
│   │   ├── auth_routes.py
│   │   ├── coach_routes.py
│   │   └── campaign_routes.py
│   └── shared.py
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── CoachVitrine.js
│   │   │   ├── CoachDashboard.js
│   │   │   ├── PartnersCarousel.js
│   │   │   └── ChatWidget.js     # v11.4: Subscription info block
│   │   └── services/
│   │       └── SoundManager.js
│   └── public/
│       ├── manifest.json
│       └── sw.js
└── memory/PRD.md
```

## Key DB Collections

### subscriptions (v11.4 NEW)
```json
{
  "id": "uuid",
  "email": "user@email.com",
  "code": "BOSS",
  "offer_name": "Pack 10 Séances",
  "total_sessions": 47,
  "used_sessions": 6,
  "remaining_sessions": 41,
  "expires_at": "2027-04-23T23:59:59+00:00",
  "status": "active|completed",
  "created_at": "...",
  "updated_at": "..."
}
```

### discount_codes
```json
{
  "code": "BOSS",
  "maxUses": 47,  // Devient total_sessions
  "expiresAt": "...",
  "active": true
}
```

## Pending Tasks (P0/P1)
1. **P0**: Stripe Connect for partner payouts
2. **P1**: Production deployment (preview-only currently)
3. **P1**: Continue modularizing server.py
4. **P1**: Continue modularizing CoachDashboard.js

## Super Admin Access
- Emails: `contact.artboost@gmail.com`, `afroboost.bassi@gmail.com`
- Login: Triple-click footer "© Afroboost 2026"

## Testing Status
- Mission v11.4: 13/13 pytest tests PASS
- Test file: `/app/backend/tests/test_v114_mission.py`
- Report: `/app/test_reports/iteration_134.json`
- Anti-régression: 18 réservations, 14 contacts intacts

---
Last Updated: March 2026 - Mission v11.4 VALIDATED
