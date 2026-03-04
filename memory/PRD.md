# Afroboost - Product Requirements Document

## Original Problem Statement
Multi-partner SaaS platform for fitness coaching with a mobile-first, "Instagram Reels" style vertical video feed. Super Admin (Bassi) manages partners who can customize their own storefronts.

## Core Features Implemented

### Mission v15.0 (March 2026) - COMPLETED - SYSTÈME CONNECTÉ
**Connexion chat, campagnes et liens dédiés - Vérification complète**

#### Fonctionnalités vérifiées:
1. **Le Pont Lien → Chat** (server.py lignes 5311-5460):
   - `POST /chat/smart-entry` met à jour `participantName` et `participantEmail` dans la session
   - `link_token` passé → session du lien utilisée
   - Nouveau: lignes 5433-5443 mettent à jour participantName pour l'affichage CRM

2. **Synchronisation Campagnes → Chat**:
   - Messages de campagne insérés dans `chat_messages` (lignes 1717-1727)
   - Scheduler insère messages via `poser_message_en_base` (ligne 103)
   - Socket.IO émet signal en temps réel

3. **Calendrier** (fix v14.8):
   - `daysUntilCourse < 0` (pas `<= 0`) vérifié
   - ChatWidget.js ligne 1807 ✅
   - BookingPanel.js ligne 23 ✅

4. **Couleurs Chat** (v14.3):
   - Client: `bg-gray-700/80` GAUCHE ✅
   - Coach/IA: `#D91CD2` DROITE ✅

5. **Étanchéité** (v14.7):
   - Super Admin voit TOUT
   - Partenaires filtrés par `coach_id` ✅

### Missions v14.x - COMPLETED
- v14.8: Calendrier réaligné
- v14.7: Étanchéité contacts
- v14.6: Recherche mots-clés
- v14.5: Document.title, badge Session Active
- v14.3: Bulles colorées, Source lien
- v14.0: Bouton Copier, participantName enrichi

## Data Status (Anti-Régression v15.0)
- 20 réservations ✅
- 8 contacts ✅
- 17 sessions chat ✅
- 12 chat links ✅

## Testing Status
- Mission v15.0: **100% backend** (18/18), **100% frontend**
- Report: `/app/test_reports/iteration_154.json`

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

## Architecture

### Flux Lien → Chat (v15.0)
```
1. Client clique sur lien: /chat/bavard
2. ChatWidget.js détecte linkToken via getLinkTokenFromUrl()
3. Client saisit Nom/Email
4. POST /chat/smart-entry avec link_token
5. Backend:
   - Trouve/crée participant
   - Trouve session du lien
   - Met à jour participantName et participantEmail
   - Retourne session enrichie
6. Dashboard Coach voit "Source: bavard"
```

### Flux Campagne → Chat
```
1. Coach lance campagne via POST /campaigns/{id}/launch
2. Pour chaque destinataire:
   - Trouve/crée session
   - INSERT message dans chat_messages (lignes 1717-1727)
   - Socket.IO signal si client connecté
3. Client voit message dans son chat
4. Client peut répondre
```

---
Last Updated: March 2026 - Mission v15.0 SYSTÈME CONNECTÉ
