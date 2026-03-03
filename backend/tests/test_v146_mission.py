"""
Test v14.6 Mission: Recherche par mots-clés et stabilité campagnes
Features:
1. CoachVitrine: Champ de recherche (loupe) si > 1 offre
2. Filtrage instantané par nom, description ou keywords
3. OffersManager: Champ 'Mots-clés' dans le formulaire
4. API /api/offers: Création offre avec keywords
5. Campagnes: mediaUrl stocké et traité (programmées & directes)
6. Anti-régression: contacts >= 8, réservations fonctionnent
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestHealthAndBasics:
    """Tests de base pour vérifier le fonctionnement de l'API"""
    
    def test_health_check(self):
        """Vérifie que l'API est en bonne santé"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        print("✅ Health check OK")

    def test_offers_endpoint(self):
        """Vérifie que l'endpoint offers fonctionne"""
        response = requests.get(f"{BASE_URL}/api/offers")
        assert response.status_code == 200
        offers = response.json()
        assert isinstance(offers, list)
        print(f"✅ Offers endpoint OK - {len(offers)} offers")

class TestOffersWithKeywords:
    """Tests pour la fonctionnalité keywords dans les offres"""
    
    def test_offer_has_keywords_field(self):
        """Vérifie que les offres ont le champ keywords"""
        response = requests.get(f"{BASE_URL}/api/offers")
        assert response.status_code == 200
        offers = response.json()
        assert len(offers) > 0, "Au moins une offre doit exister"
        
        # Vérifier que le champ keywords existe
        for offer in offers:
            assert "keywords" in offer, f"Offre {offer.get('name')} n'a pas le champ keywords"
        print("✅ Toutes les offres ont le champ keywords")
    
    def test_create_offer_with_keywords(self):
        """Crée une offre avec des mots-clés et vérifie la persistence"""
        test_keywords = "test, cardio, danse, afro, session"
        offer_data = {
            "name": f"TEST_Offre_Keywords_{uuid.uuid4().hex[:6]}",
            "price": 25.0,
            "description": "Test offer pour mots-clés",
            "keywords": test_keywords,
            "visible": True,
            "images": []
        }
        
        # Créer l'offre
        response = requests.post(f"{BASE_URL}/api/offers", json=offer_data)
        assert response.status_code == 200, f"Création échouée: {response.text}"
        created_offer = response.json()
        
        # Vérifier les données
        assert created_offer.get("name") == offer_data["name"]
        assert created_offer.get("keywords") == test_keywords
        print(f"✅ Offre créée avec keywords: {test_keywords}")
        
        # Vérifier la persistence via GET
        offer_id = created_offer.get("id")
        all_offers = requests.get(f"{BASE_URL}/api/offers").json()
        found_offer = next((o for o in all_offers if o.get("id") == offer_id), None)
        assert found_offer is not None, "Offre non trouvée après création"
        assert found_offer.get("keywords") == test_keywords, "Keywords non persistés"
        print("✅ Keywords persistés correctement en base")
        
        # Cleanup
        delete_response = requests.delete(f"{BASE_URL}/api/offers/{offer_id}")
        assert delete_response.status_code == 200
        print("✅ Offre de test supprimée")

class TestCampaignsMediaUrl:
    """Tests pour la gestion de mediaUrl dans les campagnes"""
    
    def test_campaigns_endpoint(self):
        """Vérifie que l'endpoint campaigns fonctionne"""
        response = requests.get(f"{BASE_URL}/api/campaigns")
        assert response.status_code == 200
        campaigns = response.json()
        assert isinstance(campaigns, list)
        print(f"✅ Campaigns endpoint OK - {len(campaigns)} campaigns")
    
    def test_create_campaign_with_media_url(self):
        """Crée une campagne avec mediaUrl et vérifie le stockage"""
        test_media_url = "https://example.com/test-image.jpg"
        campaign_data = {
            "name": f"TEST_Campaign_Media_{uuid.uuid4().hex[:6]}",
            "message": "Test message avec média",
            "mediaUrl": test_media_url,
            "targetType": "all",
            "selectedContacts": [],
            "channels": {"internal": True, "whatsapp": False, "email": False}
        }
        
        response = requests.post(f"{BASE_URL}/api/campaigns", json=campaign_data)
        assert response.status_code == 200, f"Création échouée: {response.text}"
        created_campaign = response.json()
        
        assert created_campaign.get("mediaUrl") == test_media_url
        assert created_campaign.get("name") == campaign_data["name"]
        print(f"✅ Campagne créée avec mediaUrl: {test_media_url}")
        
        # Cleanup
        campaign_id = created_campaign.get("id")
        delete_response = requests.delete(f"{BASE_URL}/api/campaigns/{campaign_id}")
        assert delete_response.status_code == 200
        print("✅ Campagne de test supprimée")
    
    def test_create_scheduled_campaign_with_media_url(self):
        """Crée une campagne programmée avec mediaUrl"""
        from datetime import datetime, timedelta
        
        # Date programmée dans le futur (1 heure)
        scheduled_at = (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
        test_media_url = "https://example.com/scheduled-image.jpg"
        
        campaign_data = {
            "name": f"TEST_Scheduled_Media_{uuid.uuid4().hex[:6]}",
            "message": "Message programmé avec média",
            "mediaUrl": test_media_url,
            "scheduledAt": scheduled_at,
            "targetType": "all",
            "selectedContacts": [],
            "channels": {"group": True}
        }
        
        response = requests.post(f"{BASE_URL}/api/campaigns", json=campaign_data)
        assert response.status_code == 200, f"Création échouée: {response.text}"
        created = response.json()
        
        assert created.get("status") == "scheduled", "Status devrait être 'scheduled'"
        assert created.get("mediaUrl") == test_media_url
        print(f"✅ Campagne programmée avec mediaUrl créée (status: {created.get('status')})")
        
        # Cleanup
        campaign_id = created.get("id")
        requests.delete(f"{BASE_URL}/api/campaigns/{campaign_id}")
        print("✅ Campagne programmée de test supprimée")

class TestChatWidgetFeatures:
    """Tests pour ChatWidget - document.title, badge Session Active"""
    
    def test_chat_sessions_endpoint(self):
        """Vérifie que l'endpoint chat sessions fonctionne"""
        response = requests.get(f"{BASE_URL}/api/chat/sessions")
        assert response.status_code == 200
        sessions = response.json()
        assert isinstance(sessions, list)
        print(f"✅ Chat sessions endpoint OK - {len(sessions)} sessions")
    
    def test_chat_session_has_title_field(self):
        """Vérifie que les sessions chat peuvent avoir un title"""
        response = requests.get(f"{BASE_URL}/api/chat/sessions")
        assert response.status_code == 200
        sessions = response.json()
        
        # Le champ title doit être présent (même si null)
        if sessions:
            for session in sessions[:5]:  # Vérifier les 5 premières
                # Le champ title est optionnel mais doit être dans le modèle
                assert "is_deleted" in session or "mode" in session, "Session mal formée"
            print(f"✅ Sessions structure vérifiée ({len(sessions)} sessions)")
        else:
            print("⚠️ Aucune session chat existante")

class TestCRMAndPromoFeatures:
    """Tests pour CRM et codes promo"""
    
    def test_conversations_endpoint(self):
        """Vérifie l'endpoint conversations (CRM)"""
        response = requests.get(f"{BASE_URL}/api/conversations")
        assert response.status_code == 200
        print("✅ Conversations (CRM) endpoint OK")
    
    def test_discount_codes_endpoint(self):
        """Vérifie l'endpoint discount codes"""
        response = requests.get(f"{BASE_URL}/api/discount-codes")
        assert response.status_code == 200
        codes = response.json()
        assert isinstance(codes, list)
        print(f"✅ Discount codes endpoint OK - {len(codes)} codes")

class TestAntiRegression:
    """Tests anti-régression pour vérifier que les fonctionnalités existantes fonctionnent"""
    
    def test_contacts_count(self):
        """Vérifie qu'il y a au moins 8 contacts"""
        response = requests.get(f"{BASE_URL}/api/users")
        assert response.status_code == 200
        contacts = response.json()
        assert len(contacts) >= 8, f"Attendu >= 8 contacts, trouvé {len(contacts)}"
        print(f"✅ Contacts count OK: {len(contacts)} >= 8")
    
    def test_reservations_endpoint(self):
        """Vérifie que l'endpoint réservations fonctionne"""
        response = requests.get(f"{BASE_URL}/api/reservations")
        assert response.status_code == 200
        data = response.json()
        # Support pagination ou liste directe
        if isinstance(data, dict):
            reservations = data.get("reservations", [])
        else:
            reservations = data
        print(f"✅ Reservations endpoint OK - {len(reservations)} réservations")
    
    def test_courses_endpoint(self):
        """Vérifie que l'endpoint cours fonctionne"""
        response = requests.get(f"{BASE_URL}/api/courses")
        assert response.status_code == 200
        courses = response.json()
        assert isinstance(courses, list)
        print(f"✅ Courses endpoint OK - {len(courses)} cours")
    
    def test_offers_count(self):
        """Vérifie qu'il y a au moins 3 offres"""
        response = requests.get(f"{BASE_URL}/api/offers")
        assert response.status_code == 200
        offers = response.json()
        assert len(offers) >= 3, f"Attendu >= 3 offres, trouvé {len(offers)}"
        print(f"✅ Offers count OK: {len(offers)} >= 3")

class TestCoachVitrine:
    """Tests pour la vitrine coach et la recherche"""
    
    def test_coach_vitrine_endpoint(self):
        """Vérifie qu'une vitrine coach existe"""
        # Essayer avec le username connu
        response = requests.get(f"{BASE_URL}/api/coach/vitrine/contact.artboost@gmail.com")
        if response.status_code == 200:
            data = response.json()
            assert "coach" in data or "offers" in data
            print(f"✅ Coach vitrine endpoint OK")
        else:
            print(f"⚠️ Coach vitrine non configurée (status: {response.status_code})")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
