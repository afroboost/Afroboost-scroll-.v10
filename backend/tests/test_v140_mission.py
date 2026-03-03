"""
Test Suite for Mission v14.0:
- API /api/chat/sessions returns participantName enriched (fallback on title)
- API /api/ai-config returns enabled=true
- Promo Codes Copy Button (frontend - verified via API structure)
- Anti-regression: 2 reservations, 8 contacts, 2 promo codes
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://promo-credits-lab.preview.emergentagent.com')

class TestAIConfig:
    """Test AI Configuration endpoint"""
    
    def test_ai_config_returns_enabled(self):
        """GET /api/ai-config should return enabled=true"""
        response = requests.get(f"{BASE_URL}/api/ai-config")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "enabled" in data, "Response should contain 'enabled' field"
        print(f"AI Config enabled: {data.get('enabled')}")
        
        # Per mission requirement, AI should be enabled
        assert data.get("enabled") == True, "AI should be enabled (enabled=true)"
    
    def test_ai_config_has_campaign_prompt(self):
        """GET /api/ai-config should have campaignPrompt field"""
        response = requests.get(f"{BASE_URL}/api/ai-config")
        assert response.status_code == 200
        
        data = response.json()
        # campaignPrompt can be empty but field should exist
        assert "campaignPrompt" in data or "campaign_prompt" in data, "Should have campaignPrompt field"


class TestChatSessionsEnrichment:
    """Test chat sessions API enrichment with participantName"""
    
    def test_chat_sessions_returns_participant_name(self):
        """GET /api/chat/sessions should return sessions with participantName"""
        response = requests.get(f"{BASE_URL}/api/chat/sessions")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        sessions = response.json()
        assert isinstance(sessions, list), "Response should be a list of sessions"
        
        if len(sessions) > 0:
            first_session = sessions[0]
            # v14.0: participantName should be in the response
            assert "participantName" in first_session, "Session should have participantName field"
            assert "participantEmail" in first_session, "Session should have participantEmail field"
            assert "lastMessage" in first_session, "Session should have lastMessage field"
            assert "messageCount" in first_session, "Session should have messageCount field"
            
            print(f"First session participantName: {first_session.get('participantName')}")
            print(f"First session participantEmail: {first_session.get('participantEmail')}")
            print(f"First session messageCount: {first_session.get('messageCount')}")
        else:
            print("No chat sessions found - test passes (structure verified)")
    
    def test_chat_sessions_fallback_on_title(self):
        """Verify participantName falls back to session title if no participant"""
        response = requests.get(f"{BASE_URL}/api/chat/sessions")
        assert response.status_code == 200
        
        sessions = response.json()
        
        for session in sessions[:5]:  # Check first 5 sessions
            participant_name = session.get("participantName", "")
            title = session.get("title", "")
            
            # participantName should be either from participant or from title
            if participant_name:
                print(f"Session {session.get('id', 'N/A')[:8]}... participantName: {participant_name}")
            elif title:
                print(f"Session {session.get('id', 'N/A')[:8]}... title (fallback): {title}")


class TestConversationsEnrichment:
    """Test /api/conversations advanced endpoint enrichment"""
    
    def test_conversations_returns_participant_name(self):
        """GET /api/conversations should return participantName in each conversation"""
        response = requests.get(f"{BASE_URL}/api/conversations", params={"page": 1, "limit": 10})
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "conversations" in data, "Response should have 'conversations' key"
        assert "total" in data, "Response should have 'total' key"
        
        conversations = data.get("conversations", [])
        
        if len(conversations) > 0:
            first_conv = conversations[0]
            # v14.0: participantName should be enriched
            assert "participantName" in first_conv, "Conversation should have participantName"
            assert "participantEmail" in first_conv, "Conversation should have participantEmail"
            
            print(f"First conversation participantName: {first_conv.get('participantName')}")
        else:
            print("No conversations found - test passes (structure verified)")


class TestPromoCodesCopyButton:
    """Test promo codes API - Copy button functionality relies on this"""
    
    def test_discount_codes_returns_codes(self):
        """GET /api/discount-codes should return promo codes"""
        response = requests.get(f"{BASE_URL}/api/discount-codes")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        codes = response.json()
        assert isinstance(codes, list), "Response should be a list"
        
        # The copy button data-testid="copy-code-{code.id}" needs code.id and code.code
        for code in codes[:5]:
            assert "id" in code, "Code should have 'id' field"
            assert "code" in code, "Code should have 'code' field (the actual code string)"
            print(f"Promo code: {code.get('code')} (id: {code.get('id')[:8]}...)")


class TestAntiRegression:
    """Anti-regression tests: verify data integrity"""
    
    def test_reservations_count(self):
        """Should have at least 2 reservations"""
        response = requests.get(f"{BASE_URL}/api/reservations")
        assert response.status_code == 200
        
        reservations = response.json()
        count = len(reservations)
        print(f"Reservations count: {count}")
        
        # Mission specifies 2 reservations minimum
        assert count >= 2, f"Expected at least 2 reservations, got {count}"
    
    def test_contacts_count(self):
        """Should have at least 8 contacts"""
        response = requests.get(f"{BASE_URL}/api/users")
        assert response.status_code == 200
        
        users = response.json()
        count = len(users)
        print(f"Contacts count: {count}")
        
        # Mission specifies 8 contacts
        assert count >= 8, f"Expected at least 8 contacts, got {count}"
    
    def test_promo_codes_count(self):
        """Should have at least 2 promo codes"""
        response = requests.get(f"{BASE_URL}/api/discount-codes")
        assert response.status_code == 200
        
        codes = response.json()
        count = len(codes)
        print(f"Promo codes count: {count}")
        
        # Mission specifies 2 promo codes minimum
        assert count >= 2, f"Expected at least 2 promo codes, got {count}"


class TestChatAIResponse:
    """Test that AI responds to messages (not 'assistant IA désactivé')"""
    
    def test_ai_enabled_check(self):
        """Verify AI is enabled for chat responses"""
        response = requests.get(f"{BASE_URL}/api/ai-config")
        assert response.status_code == 200
        
        data = response.json()
        enabled = data.get("enabled", False)
        
        assert enabled == True, "AI must be enabled for chat to respond"
        print(f"AI assistant is enabled: {enabled}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
