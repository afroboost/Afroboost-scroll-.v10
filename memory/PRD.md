# Afroboost - Product Requirements Document

## Original Problem Statement
Multi-partner SaaS platform for fitness coaching with a mobile-first, "Instagram Reels" style vertical video feed. Super Admin (Bassi) manages partners who can customize their own storefronts.

## Core Features Implemented

### ✅ Mission v13.4 (March 2026) - COMPLETED
**Refactoring Final & Pré-Déploiement**
1. **CoachDashboard.js** réduit de 6537 → **5432 lignes** (-1105 lignes, -16.9%)
2. **6 Composants Extraits** vers `/components/dashboard/` :
   - `ConceptEditor.js` (488 lignes) - Personnalisation couleurs, paramètres
   - `CoursesManager.js` (285 lignes) - Gestion des cours
   - `OffersManager.js` (332 lignes) - Gestion des offres
   - `CreditsGate.js` (44 lignes) - Écran blocage crédits
   - `CreditBoutique.js` (111 lignes) - Boutique de packs
   - `StripeConnectTab.js` (127 lignes) - Stripe Connect
3. **Backend Routes Extraites** :
   - `stripe_routes.py` (442 lignes) - Paiements Stripe
4. **Anti-régression validée** : 22 réservations, 7 contacts intacts
5. **Tests** : 100% (18/18 tests backend passés)

### ✅ Mission v13.2 (March 2026) - COMPLETED
**Validation Sécurité & Nettoyage du Code**
- Verrouillage crédits validé (CreditsGate)
- Super Admin bypass confirmé
- Premier découpage CoachDashboard.js

### ✅ Missions v13.0-v13.1 - COMPLETED
- Stripe intégré pour vente de packs crédits
- Webhook pour crédits automatiques
- Verrouillage services si crédits insuffisants

### ✅ Missions v11.x-v12.x - COMPLETED
- Prix services dynamiques (Super Admin)
- Design "Zéro Cadre" premium
- Vidéo Full-Width
- PWA installable

## Architecture v13.4

```
/app/
├── backend/
│   ├── server.py              # 6976 lignes (routes principales)
│   └── routes/
│       ├── admin_routes.py
│       ├── auth_routes.py     # 345 lignes
│       ├── campaign_routes.py # 134 lignes
│       ├── coach_routes.py    # 438 lignes
│       ├── promo_routes.py    # 325 lignes
│       ├── reservation_routes.py # 209 lignes
│       ├── stripe_routes.py   # 442 lignes (NEW v13.4)
│       └── shared.py          # 26 lignes
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── components/
│   │       ├── CoachDashboard.js  # 5432 lignes (OPTIMISÉ v13.4)
│   │       ├── dashboard/         # 1398 lignes total (NEW v13.4)
│   │       │   ├── ConceptEditor.js    # 488 lignes
│   │       │   ├── CoursesManager.js   # 285 lignes
│   │       │   ├── OffersManager.js    # 332 lignes
│   │       │   ├── CreditsGate.js      # 44 lignes
│   │       │   ├── CreditBoutique.js   # 111 lignes
│   │       │   ├── StripeConnectTab.js # 127 lignes
│   │       │   └── index.js
│   │       └── coach/
│   │           ├── CampaignManager.js
│   │           ├── CRMSection.js
│   │           └── ReservationTab.js
│   └── public/
│       ├── manifest.json
│       └── sw.js
└── memory/PRD.md
```

## Data Status (Anti-Régression)
- ✅ **22 réservations** intactes
- ✅ **7 contacts** intactes
- ✅ **4 packs crédits** (Starter, Pro, Business, Enterprise)
- ✅ **Service prices**: campaign=2, ai_conversation=1, promo_code=3
- ✅ **Video**: Full-Width (pas de bordures noires)

## Pending Tasks (P0/P1)
1. **P0**: Continuer refactoring CoachDashboard.js (objectif <3000 lignes)
2. **P0**: Implémenter Stripe Connect complet pour paiements partenaires
3. **P1**: Continuer refactoring server.py (extraire routes restantes)
4. **P1**: Production deployment (backend preview seulement)
5. **P2**: Déduction crédits pour Chat actions

## Super Admin Access
- Emails: `contact.artboost@gmail.com`, `afroboost.bassi@gmail.com`
- Crédits: -1 (illimité)
- Triple-click sur "© Afroboost 2026" pour login admin

## Testing Status
- Mission v13.4: **100%** (18/18 backend tests)
- Report: `/app/test_reports/iteration_143.json`

---
Last Updated: March 2026 - Mission v13.4 VALIDATED
