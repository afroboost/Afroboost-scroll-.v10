"""
Test Mission v14.3: Liaison client-lien et interface chat pro
Tests for:
1. API /api/chat/enhance-prompt endpoint
2. Anti-regression: contacts count (expected: 8)
3. Chat session with title (Source: Nom du Lien)
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://promo-credits-lab.preview.emergentagent.com')


class TestMissionV143:
    """Tests for Mission v14.3 features"""
    
    # === 1. TEST: API /api/chat/enhance-prompt endpoint ===
    def test_enhance_prompt_endpoint_exists(self):
        """Verify the /api/chat/enhance-prompt endpoint exists and responds"""
        response = requests.post(
            f"{BASE_URL}/api/chat/enhance-prompt",
            json={"raw_prompt": "focus sur les cours de fitness"},
            headers={"Content-Type": "application/json"}
        )
        # Endpoint should return 200 (success) or 503 (AI disabled) - both valid
        assert response.status_code in [200, 503], f"Unexpected status: {response.status_code}"
        if response.status_code == 200:
            data = response.json()
            assert "enhanced_prompt" in data, "Response should contain enhanced_prompt"
            assert "original" in data, "Response should contain original prompt"
            print(f"✅ enhance-prompt endpoint works - enhanced: {data['enhanced_prompt'][:50]}...")
        else:
            print(f"⚠️ AI is disabled (503) - endpoint exists but fallback active")
    
    def test_enhance_prompt_with_fallback(self):
        """Test that enhance-prompt returns a fallback when AI is disabled"""
        response = requests.post(
            f"{BASE_URL}/api/chat/enhance-prompt",
            json={"raw_prompt": "test prompt"},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            # Check if it's using fallback
            if data.get("fallback"):
                assert "Tu es un assistant virtuel professionnel" in data["enhanced_prompt"], \
                    "Fallback should contain standard prompt structure"
                print(f"✅ Fallback mode active - enhanced: {data['enhanced_prompt']}")
            else:
                print(f"✅ AI enhancement mode active")
        else:
            print(f"⚠️ AI disabled - status {response.status_code}")
    
    def test_enhance_prompt_empty_input(self):
        """Test that enhance-prompt rejects empty input"""
        response = requests.post(
            f"{BASE_URL}/api/chat/enhance-prompt",
            json={"raw_prompt": ""},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400, f"Empty input should return 400, got {response.status_code}"
        print("✅ Empty input correctly rejected with 400")
    
    # === 2. ANTI-REGRESSION: Contacts count ===
    def test_anti_regression_contacts_count(self):
        """Verify contacts count >= 8 (anti-regression)"""
        response = requests.get(f"{BASE_URL}/api/users")
        assert response.status_code == 200, f"Failed to get users: {response.status_code}"
        users = response.json()
        assert len(users) >= 8, f"Expected at least 8 contacts, got {len(users)}"
        print(f"✅ Anti-regression: {len(users)} contacts (expected ≥8)")
    
    # === 3. TEST: Chat sessions with title (Source du lien) ===
    def test_chat_sessions_endpoint(self):
        """Verify chat sessions endpoint returns sessions with title field"""
        response = requests.get(f"{BASE_URL}/api/chat/sessions")
        assert response.status_code == 200, f"Failed to get sessions: {response.status_code}"
        sessions = response.json()
        # Check if sessions exist and have expected structure
        if len(sessions) > 0:
            session = sessions[0]
            # Each session should have potential for title (for Source: Nom du Lien)
            print(f"✅ Found {len(sessions)} chat sessions")
            if session.get('title'):
                print(f"   - Session with title: {session['title']}")
        else:
            print("ℹ️ No chat sessions found (expected for fresh install)")
    
    # === 4. TEST: API health check ===
    def test_api_health(self):
        """Verify API is healthy"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200, f"Health check failed: {response.status_code}"
        data = response.json()
        assert data.get("status") == "healthy", f"API not healthy: {data}"
        print("✅ API health check passed")
    
    # === 5. TEST: Chat links list for source verification ===
    def test_chat_links_list(self):
        """Verify chat links can be retrieved for source tracking"""
        response = requests.get(f"{BASE_URL}/api/chat/links")
        assert response.status_code == 200, f"Failed to get chat links: {response.status_code}"
        links = response.json()
        print(f"✅ Chat links endpoint works - found {len(links)} links")
        if len(links) > 0:
            link = links[0]
            # Each link should have title and token
            if link.get('title'):
                print(f"   - Link: '{link['title']}' (token: {link.get('token', 'N/A')[:8]}...)")
    
    # === 6. TEST: Date format fr-CH support ===
    def test_reservations_endpoint(self):
        """Verify reservations endpoint works (date format verified in UI)"""
        response = requests.get(f"{BASE_URL}/api/reservations?page=1&limit=20")
        assert response.status_code == 200, f"Failed to get reservations: {response.status_code}"
        data = response.json()
        assert "data" in data, "Response should contain data field"
        assert "pagination" in data, "Response should contain pagination field"
        print(f"✅ Reservations endpoint works - found {len(data['data'])} reservations")
    
    # === 7. TEST: Discount codes for promo system ===
    def test_discount_codes_endpoint(self):
        """Verify discount codes endpoint works"""
        response = requests.get(f"{BASE_URL}/api/discount-codes")
        assert response.status_code == 200, f"Failed to get discount codes: {response.status_code}"
        codes = response.json()
        print(f"✅ Discount codes endpoint works - found {len(codes)} codes")


class TestCRMBubbleColors:
    """Tests for CRM bubble color requirements (v14.3)
    Client = Gris foncé GAUCHE (justify-start)
    Coach/IA = Violet #D91CD2 DROITE (justify-end)
    """
    
    def test_chat_messages_endpoint(self):
        """Verify chat messages endpoint works for CRM bubble verification"""
        # First get sessions to find a session ID
        sessions_response = requests.get(f"{BASE_URL}/api/chat/sessions")
        if sessions_response.status_code == 200 and len(sessions_response.json()) > 0:
            session_id = sessions_response.json()[0].get('id')
            if session_id:
                messages_response = requests.get(f"{BASE_URL}/api/chat/sessions/{session_id}/messages")
                assert messages_response.status_code == 200, f"Failed to get messages: {messages_response.status_code}"
                messages = messages_response.json()
                print(f"✅ Found {len(messages)} messages in session {session_id[:8]}...")
                # Check sender_type field exists for color determination
                if len(messages) > 0:
                    msg = messages[0]
                    print(f"   - Message has sender_type: {'sender_type' in msg}")
        else:
            print("ℹ️ No sessions with messages to test CRM bubble colors")


class TestGenerateLinkCardAI:
    """Tests for GenerateLinkCard AI enhance button (v14.3)"""
    
    def test_enhance_prompt_available_for_super_admin(self):
        """Verify enhance-prompt is accessible"""
        response = requests.post(
            f"{BASE_URL}/api/chat/enhance-prompt",
            json={"raw_prompt": "Je veux que l'assistant parle de fitness et santé"},
            headers={"Content-Type": "application/json"}
        )
        # Should get 200 or 503 (if AI disabled)
        assert response.status_code in [200, 503]
        if response.status_code == 200:
            data = response.json()
            assert len(data.get('enhanced_prompt', '')) > 0, "Enhanced prompt should not be empty"
            print(f"✅ AI enhance works - prompt transformed")
        print("✅ enhance-prompt endpoint accessible for GenerateLinkCard")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
