# Afroboost - Product Requirements Document

## Original Problem Statement
Multi-partner SaaS platform for fitness coaching with a mobile-first, "Instagram Reels" style vertical video feed. Super Admin (Bassi) manages partners who can customize their own storefronts.

## Core Features Implemented

### ✅ Mission v13.0 (March 2026) - COMPLETED
**Stripe Connect & Vente de Packs Crédits**
1. **Paiement par Carte** - Endpoint `/api/stripe/create-credit-checkout`
2. **Crédits Automatiques** - Webhook Stripe ajoute crédits instantanément
3. **Boutique Premium** - Onglet "💎 Boutique" dans dashboard partenaire
4. **Transaction Logs** - Collection `credit_transactions` pour historique
5. **Notifications** - Email au coach + notification à Bassi

**Endpoints v13.0:**
- `GET /api/credit-packs` - Liste des packs visibles
- `POST /api/stripe/create-credit-checkout` - Crée session Stripe
- `POST /api/webhook/stripe` - Gère `credit_purchase`
- `GET /api/credit-transactions` - Historique transactions

### ✅ Mission v12.1 (March 2026) - COMPLETED
**Contrôle Admin & Design Premium**
- Prix services dynamiques
- Design sans cadre

### ✅ Mission v11.9 (March 2026) - COMPLETED
**Vidéo Full-Width**
- Bordures supprimées, width=100%

### ✅ Missions v11.2-v11.8 - COMPLETED
- Système codes & crédits, Scroll réserver, PWA

## Architecture

```
/app/
├── backend/
│   ├── server.py              # v13.0: Stripe credit checkout + webhook
│   └── routes/
│       ├── promo_routes.py
│       └── reservation_routes.py
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── components/
│   │       ├── CoachDashboard.js  # v13.0: Boutique tab
│   │       └── SuperAdminPanel.js # v12.1: Tarifs services
│   └── public/
│       ├── manifest.json
│       └── sw.js
└── memory/PRD.md
```

## Key Flow - Credit Purchase (v13.0)

```
1. Coach clique "Acheter" dans Boutique
2. Frontend: POST /api/stripe/create-credit-checkout
3. Backend: Crée session Stripe avec metadata
4. Coach redirigé vers page Stripe
5. Après paiement: Webhook /api/webhook/stripe
6. Backend: Ajoute crédits + log transaction + emails
7. Coach voit nouveau solde
```

## Data Status
- ✅ 22 réservations
- ✅ 14 contacts
- ✅ BOSS: 41/47 séances
- ✅ 4 packs crédits (Starter 49 CHF, Pro 99 CHF...)
- ✅ Video: full-width

## Pending Tasks (P0/P1)
1. **P1**: Production deployment
2. **P1**: Add more credit packs (500, 1000 credits)
3. **P2**: Dashboard stats for credit consumption

## Super Admin Access
- Emails: `contact.artboost@gmail.com`, `afroboost.bassi@gmail.com`
- Stripe: Clés LIVE configurées

## Testing Status
- Mission v13.0: 100% (20/20 backend tests)
- Report: `/app/test_reports/iteration_140.json`

---
Last Updated: March 2026 - Mission v13.0 VALIDATED
