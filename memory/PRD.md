# Afroboost - Product Requirements Document

## Original Problem Statement
Multi-partner SaaS platform for fitness coaching with a mobile-first, "Instagram Reels" style vertical video feed. Super Admin (Bassi) manages partners who can customize their own storefronts.

## Core Features Implemented

### Mission v14.8 (March 2026) - COMPLETED - CALENDRIER RÉALIGNÉ
**Correction décalage calendrier +7 jours**

#### Bug corrigé:
- **Symptôme**: Le calendrier affichait le 11 mars au lieu du 4 mars (aujourd'hui)
- **Cause racine**: `if (daysUntilCourse <= 0)` incluait 0 (jour même) comme nécessitant +7 jours
- **Fix appliqué**: Changé en `if (daysUntilCourse < 0)` pour permettre la réservation le jour même

#### Fichiers modifiés:
1. **ChatWidget.js** (ligne 1806): `if (daysUntilCourse < 0)`
2. **BookingPanel.js** (ligne 22): `if (daysUntilCourse < 0)`

#### Format de date:
- Changé de `fr-FR / Europe/Paris` à `fr-CH / Europe/Zurich` (Neuchâtel)
- Affichage: "Mercredi 4 mars 2026" ✅

### Mission v14.7 (March 2026) - COMPLETED
- Étanchéité contacts multi-partenaires (coach_id)

### Mission v14.6 (March 2026) - COMPLETED
- Recherche offres par mots-clés

### Missions v14.0-14.5 - COMPLETED
- Activation IA, bouton Copier, document.title, bulles colorées

## Data Status (Anti-Régression v14.8)
- 2 réservations ✅
- 8 contacts ✅
- 3 offres ✅

## Testing Status
- Mission v14.8: **100% frontend** - Calendrier affiche 04.03 (correct)
- Report: `/app/test_reports/iteration_153.json`

## Bug Fix Details v14.8

### Avant le fix (BUG):
```javascript
let daysUntilCourse = weekday - currentDay;
if (daysUntilCourse <= 0) daysUntilCourse += 7;  // ❌ BUG
// Mercredi (3) - Mercredi (3) = 0
// 0 <= 0 → TRUE → +7 = 7 jours → 11 mars (FAUX)
```

### Après le fix (CORRECT):
```javascript
let daysUntilCourse = weekday - currentDay;
if (daysUntilCourse < 0) daysUntilCourse += 7;  // ✅ FIX
// Mercredi (3) - Mercredi (3) = 0
// 0 < 0 → FALSE → 0 jours → 4 mars (CORRECT)
```

## Pending Tasks

### P0 (Critical)
- Déploiement backend en production

### P1 (High Priority)
- Intégration Stripe Connect pour paiements partenaires

### P2 (Medium Priority)
- Déduction crédits pour actions Chat
- Modularisation CoachDashboard.js

## Super Admin Access
- Emails: `contact.artboost@gmail.com`, `afroboost.bassi@gmail.com`
- Triple-click "© Afroboost 2026" pour login admin

---
Last Updated: March 2026 - Mission v14.8 CALENDRIER RÉALIGNÉ
