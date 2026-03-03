# Afroboost - Product Requirements Document

## Original Problem Statement
Multi-partner SaaS platform for fitness coaching with a mobile-first, "Instagram Reels" style vertical video feed. Super Admin (Bassi) manages partners who can customize their own storefronts.

## Core Features Implemented

### ✅ Mission v13.7 (March 2026) - COMPLETED - BUG FIXES URGENTS
**Réparations d'urgence - Codes Promos & Conversations**
1. **Fix toggleCodeActive** : Renommé en `toggleCode` dans prop passing (ligne 4544)
2. **Fix code.isActive** : Changé en `code.active` pour correspondre au backend
3. **Fix messages vides** : Fallback `msg.content || msg.text || msg.message`
4. **Fix Invalid Date** : try/catch avec fallback `'—'` pour dates invalides
5. **Anti-régression** : 22 réservations, 7 contacts intacts
6. **Tests** : 100% (8/8 backend tests)

**Fichiers modifiés :**
- `/app/frontend/src/components/CoachDashboard.js` (ligne 4544)
- `/app/frontend/src/components/dashboard/PromoCodesTab.js` (lignes 276, 303, 306)
- `/app/frontend/src/components/coach/CRMSection.js` (lignes 277, 393, 636, 644)

### ✅ Mission v13.6 (March 2026) - COMPLETED
- Design "Zéro Cadre" appliqué (fond transparent)
- DashboardHeader.js créé (230 lignes)

### ✅ Missions v13.0-v13.5 - COMPLETED
- Stripe, verrouillage crédits, refactoring composants

## Bug Fixes v13.7 Details

### Bug 1: toggleCodeActive not defined
```javascript
// CoachDashboard.js ligne 4544
// AVANT: toggleCodeActive={toggleCodeActive}  // ERREUR
// APRÈS: toggleCodeActive={toggleCode}        // CORRIGÉ
```

### Bug 2: code.isActive vs code.active
```javascript
// PromoCodesTab.js
// AVANT: code.isActive (undefined)
// APRÈS: code.active (correspond au backend)
```

### Bug 3: Messages vides
```javascript
// CRMSection.js ligne 636
<p>{msg.content || msg.text || msg.message || '[Message vide]'}</p>
```

### Bug 4: Invalid Date
```javascript
// CRMSection.js avec try/catch
try {
  const d = new Date(dateVal);
  return isNaN(d.getTime()) ? '—' : d.toLocaleDateString('fr-FR');
} catch { return '—'; }
```

## Data Status (Anti-Régression)
- ✅ **22 réservations** intactes
- ✅ **7 contacts** intactes
- ✅ Video: Full-Width
- ✅ Design: "Zéro Cadre"

## Pending Tasks (P0/P1)
1. **P0**: Intégrer DashboardHeader.js dans CoachDashboard.js
2. **P0**: Continuer refactoring (4795 → objectif <3000 lignes)
3. **P0**: Cliquer sur "Deploy" Emergent pour URL production
4. **P1**: Implémenter Stripe Connect complet
5. **P2**: Nettoyer UI Chat (paramètres anormaux mentionnés par Bassi)

## Super Admin Access
- Emails: `contact.artboost@gmail.com`, `afroboost.bassi@gmail.com`
- Triple-click sur "© Afroboost 2026" pour login admin

## Testing Status
- Mission v13.7: **100%** (8/8 tests)
- Report: `/app/test_reports/iteration_146.json`

---
Last Updated: March 2026 - Mission v13.7 BUG FIXES VALIDATED
