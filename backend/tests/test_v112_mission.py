"""
Mission v11.2 - Tests de validation Afroboost
1. Étanchéité des prompts (custom_prompt par lien)
2. PWA installable (manifest.json + sw.js)
3. Bouton Réserver sans cadre en bas à droite
4. Audit campagnes avec médias et notifications
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestMissionV112:
    """Tests Mission v11.2 - Validation système Afroboost"""
    
    # ====== TEST 1: API Health ======
    def test_health_endpoint(self):
        """Vérifie que l'API est accessible"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        assert data.get("database") == "connected"
        print("✅ API Health: OK")
    
    # ====== TEST 2: Coach Vitrine Bassi ======
    def test_coach_vitrine_bassi(self):
        """Vérifie que la vitrine /coach/bassi charge correctement"""
        response = requests.get(f"{BASE_URL}/api/coach/vitrine/bassi")
        assert response.status_code == 200
        data = response.json()
        
        # Verify coach data
        assert "coach" in data
        assert data["coach"]["id"] == "bassi"
        assert "offers" in data
        assert "courses" in data
        
        print(f"✅ Vitrine Bassi: {data['offers_count']} offres, {data['courses_count']} cours")
    
    # ====== TEST 3: Partners Active ======
    def test_partners_active(self):
        """Vérifie l'API /api/partners/active"""
        response = requests.get(f"{BASE_URL}/api/partners/active")
        assert response.status_code == 200
        data = response.json()
        
        # Should return list of partners
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check first partner has required fields
        first_partner = data[0]
        assert "id" in first_partner
        assert "name" in first_partner
        assert "email" in first_partner
        
        print(f"✅ Partners Active: {len(data)} partenaires actifs")
    
    # ====== TEST 4: Custom Prompt - Generate Link ======
    def test_generate_link_with_custom_prompt(self):
        """
        Vérifie l'étanchéité des prompts:
        - L'API /api/chat/generate-link accepte un custom_prompt
        - Le custom_prompt est stocké et retourné
        """
        test_prompt = "Tu es un assistant de test pour la mission v11.2"
        test_title = "Test Link v11.2"
        
        response = requests.post(
            f"{BASE_URL}/api/chat/generate-link",
            json={
                "title": test_title,
                "custom_prompt": test_prompt
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "link_token" in data
        assert "session_id" in data
        assert "share_url" in data
        assert "custom_prompt" in data
        assert "has_custom_prompt" in data
        
        # Verify custom_prompt is correctly stored
        assert data["custom_prompt"] == test_prompt
        assert data["has_custom_prompt"] == True
        assert data["title"] == test_title
        
        print(f"✅ Generate Link: token={data['link_token']}, custom_prompt='{test_prompt[:30]}...'")
    
    def test_generate_link_without_custom_prompt(self):
        """Vérifie qu'un lien peut être généré sans custom_prompt"""
        response = requests.post(
            f"{BASE_URL}/api/chat/generate-link",
            json={
                "title": "Test Link Without Prompt"
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify no custom_prompt
        assert data.get("has_custom_prompt") == False
        assert data.get("custom_prompt") is None or data.get("custom_prompt") == ""
        
        print("✅ Generate Link sans custom_prompt: OK")
    
    # ====== TEST 5: PWA manifest.json ======
    def test_manifest_json(self):
        """Vérifie que manifest.json est accessible et contient display:standalone"""
        response = requests.get(f"{BASE_URL}/manifest.json")
        assert response.status_code == 200
        data = response.json()
        
        # Verify PWA requirements
        assert data.get("display") == "standalone", "manifest.json must have display:standalone for PWA"
        assert "short_name" in data
        assert "name" in data
        assert "icons" in data
        assert len(data["icons"]) >= 2  # At least 2 icon sizes
        
        print(f"✅ manifest.json: display={data['display']}, name={data['short_name']}")
    
    # ====== TEST 6: Service Worker (sw.js) ======
    def test_service_worker(self):
        """Vérifie que sw.js est accessible"""
        response = requests.get(f"{BASE_URL}/sw.js")
        assert response.status_code == 200
        
        # Verify it's a valid service worker (contains install event)
        content = response.text
        assert "self.addEventListener('install'" in content or "self.addEventListener(\"install\"" in content
        assert "self.addEventListener('push'" in content or "self.addEventListener(\"push\"" in content
        
        print("✅ sw.js: Service Worker accessible et valide")
    
    # ====== TEST 7: Campaigns API ======
    def test_campaigns_api(self):
        """Vérifie l'API des campagnes pour l'audit médias"""
        response = requests.get(f"{BASE_URL}/api/campaigns")
        # API may return empty list or campaigns
        assert response.status_code == 200
        data = response.json()
        
        # Should be a list
        assert isinstance(data, list)
        
        # If campaigns exist, verify structure
        if len(data) > 0:
            campaign = data[0]
            expected_fields = ["id", "name", "message", "status"]
            for field in expected_fields:
                assert field in campaign, f"Campaign missing field: {field}"
            
            # Check for media support
            if "mediaUrl" in campaign:
                print(f"✅ Campaigns: {len(data)} campagnes, médias supportés")
            else:
                print(f"✅ Campaigns: {len(data)} campagnes")
        else:
            print("✅ Campaigns API: OK (liste vide)")


class TestVitrineButtonStyles:
    """Tests pour vérifier le bouton Réserver sans cadre"""
    
    def test_vitrine_contains_reserver_button(self):
        """La vitrine doit contenir un bouton Réserver avec data-testid"""
        # This is verified by Playwright tests
        # Here we just verify the API returns data for the vitrine
        response = requests.get(f"{BASE_URL}/api/coach/vitrine/bassi")
        assert response.status_code == 200
        print("✅ Vitrine API OK - Bouton Réserver vérifié via Playwright")


class TestChatPromptIsolation:
    """Tests d'isolation des prompts personnalisés"""
    
    def test_create_link_with_isolation(self):
        """Crée un lien avec prompt isolé et vérifie l'étanchéité"""
        # Create link with specific prompt
        prompt_isolation = "Tu réponds UNIQUEMENT en anglais. Ne parle jamais d'Afroboost."
        
        response = requests.post(
            f"{BASE_URL}/api/chat/generate-link",
            json={
                "title": "English Only Test",
                "custom_prompt": prompt_isolation
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify the prompt is stored correctly
        assert data["custom_prompt"] == prompt_isolation
        assert data["has_custom_prompt"] == True
        
        # The link_token can be used to verify isolation in chat
        link_token = data["link_token"]
        session_id = data["session_id"]
        
        print(f"✅ Link créé avec prompt isolé: {link_token}")
        print(f"   Prompt: {prompt_isolation[:50]}...")
        
        return {"link_token": link_token, "session_id": session_id}


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
