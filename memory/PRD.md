# Afroboost - Product Requirements Document

## Original Problem Statement
Multi-partner SaaS platform for fitness coaching with a mobile-first, "Instagram Reels" style vertical video feed. Super Admin (Bassi) manages partners who can customize their own storefronts.

## Core Features Implemented

### ✅ Mission v11.8 (March 2026) - COMPLETED
**Réparation du Scroll Réserver & Audit Réel**
1. **Scroll Instantané** - Clic sur Réserver (vidéo SA) scrolle vers `sessions-section` (+407px)
2. **Aucune Redirection** - URL reste inchangée après clic
3. **Double-clic Désactivé** - Sur vidéo SA, fait uniquement play/pause
4. **Console Logs** - Confirmation: `[SUPER-ADMIN] ✅ Scroll effectué vers sessions-section`

### ✅ Mission v11.7 (March 2026) - COMPLETED
**Logique Multi-Partenaires**
- Identification par email unique
- Scroll Reels conditionnel (>1 partenaire)
- Protection Super Admin

### ✅ Mission v11.5 (March 2026) - COMPLETED
**Date/Heure Réservation**
- Affichage date/heure dans confirmation

### ✅ Mission v11.4 (March 2026) - COMPLETED
**Système Codes & Crédits**
- Validation code crée abonnement
- Bloc info abonnement (solde)
- Déduction automatique

### ✅ Mission v11.2 (March 2026) - COMPLETED
**Prompts Indépendants & PWA**
- Isolation custom_prompts
- PWA installable

## Architecture

```
/app/
├── backend/
│   ├── server.py
│   ├── routes/
│   │   ├── promo_routes.py      # Subscription system
│   │   ├── reservation_routes.py
│   │   └── ...
│   └── shared.py
├── frontend/
│   ├── src/
│   │   ├── App.js               # Main + sessions-section
│   │   ├── components/
│   │   │   ├── CoachVitrine.js  # Partner storefront
│   │   │   ├── PartnersCarousel.js # Reels feed (v11.8)
│   │   │   └── ChatWidget.js
│   │   └── services/
│   │       └── SoundManager.js
│   └── public/
│       ├── manifest.json
│       └── sw.js
└── memory/PRD.md
```

## Key Logic (v11.8)

### handleReserve - Scroll for Super Admin
```javascript
const handleReserve = (e) => {
  if (isSuperAdminVideo) {
    const offersSection = document.getElementById('sessions-section') || 
                         document.getElementById('offers-section');
    if (offersSection) {
      offersSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    return;
  }
  onNavigate(partner); // For other partners
};
```

## Data Status
- ✅ 21 réservations intactes
- ✅ 14 contacts intacts  
- ✅ Système BOSS: 41/47 séances
- ✅ PWA: display: standalone

## Pending Tasks (P0/P1)
1. **P0**: Stripe Connect for partner payouts
2. **P1**: Production deployment

## Super Admin Access
- Emails: `contact.artboost@gmail.com`, `afroboost.bassi@gmail.com`
- Login: Triple-click footer "© Afroboost 2026"

## Testing Status
- Mission v11.8: 100% frontend validated
- Report: `/app/test_reports/iteration_137.json`

---
Last Updated: March 2026 - Mission v11.8 VALIDATED
