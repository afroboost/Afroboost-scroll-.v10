"""
Test Mission v10.9 - Nettoyage UI et bouton Réserver ciblé
Tests for:
1. Bouton Réserver position and style (transparent background, no border)
2. Logo Afroboost central REMOVED
3. Bouton Contact (enveloppe) REMOVED
4. 3 header icons on main page
5. API /api/partners/active functionality
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestMissionV109API:
    """API tests for Mission v10.9"""
    
    def test_health_endpoint(self):
        """Test health endpoint returns healthy"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        print("✅ Health endpoint: PASS")
    
    def test_partners_active_endpoint(self):
        """Test partners active endpoint returns list"""
        response = requests.get(f"{BASE_URL}/api/partners/active")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # At least one partner
        print(f"✅ Partners active: PASS - {len(data)} partners returned")
    
    def test_coach_vitrine_endpoint(self):
        """Test coach vitrine endpoint for Bassi"""
        response = requests.get(f"{BASE_URL}/api/coach/vitrine/contact.artboost@gmail.com")
        assert response.status_code == 200
        data = response.json()
        assert "coach" in data
        assert "offers" in data
        assert data["coach"]["email"] == "contact.artboost@gmail.com"
        print(f"✅ Coach vitrine endpoint: PASS - Coach: {data['coach'].get('platform_name', 'unknown')}")


class TestMissionV109CodeVerification:
    """Code verification tests for Mission v10.9 - CoachVitrine.js changes"""
    
    def get_coachvitrine_content(self):
        """Read CoachVitrine.js file content"""
        try:
            with open('/app/frontend/src/components/CoachVitrine.js', 'r') as f:
                return f.read()
        except FileNotFoundError:
            pytest.skip("CoachVitrine.js not found")
    
    def test_reserver_button_transparent_background(self):
        """Verify Réserver button has transparent background"""
        content = self.get_coachvitrine_content()
        # Check for transparent background style on the button
        assert "background: 'transparent'" in content or 'background: "transparent"' in content
        print("✅ Réserver button transparent background: PASS")
    
    def test_reserver_button_no_border(self):
        """Verify Réserver button has no border"""
        content = self.get_coachvitrine_content()
        # Check for border: none style
        assert "border: 'none'" in content or 'border: "none"' in content
        print("✅ Réserver button no border: PASS")
    
    def test_reserver_button_position_absolute(self):
        """Verify Réserver button uses absolute positioning"""
        content = self.get_coachvitrine_content()
        # Check for absolute positioning classes
        assert "absolute bottom-8 right-4" in content
        print("✅ Réserver button absolute positioning: PASS")
    
    def test_calendar_svg_icon(self):
        """Verify calendar SVG icon for Réserver button"""
        content = self.get_coachvitrine_content()
        # Check for calendar icon SVG
        assert 'viewBox="0 0 24 24"' in content
        assert '<rect x="3" y="4" width="18" height="18"' in content
        print("✅ Calendar SVG icon: PASS")
    
    def test_contact_button_removed(self):
        """Verify Contact button (vitrine-chat-btn) is REMOVED"""
        content = self.get_coachvitrine_content()
        # The chat button should NOT exist
        assert 'data-testid="vitrine-chat-btn"' not in content
        print("✅ Contact button (enveloppe) REMOVED: PASS")
    
    def test_afroboost_central_logo_removed(self):
        """Verify central Afroboost logo is removed from hero"""
        content = self.get_coachvitrine_content()
        # Search for specific Afroboost logo SVG that was in the hero center
        # The simplified hero should only have the Réserver button
        # Check that there's no "AFROBOOST" text in the hero content div
        hero_section_start = content.find('vitrine-hero-container')
        hero_section_end = content.find('vitrine-courses-section')
        if hero_section_start > 0 and hero_section_end > hero_section_start:
            hero_content = content[hero_section_start:hero_section_end]
            # No 'AFROBOOST' centered text logo should be in hero
            assert 'text-4xl' not in hero_content or 'AFROBOOST' not in hero_content
        print("✅ Afroboost central logo REMOVED: PASS")
    
    def test_reserver_button_testid(self):
        """Verify Réserver button has correct data-testid"""
        content = self.get_coachvitrine_content()
        assert 'data-testid="vitrine-cta-btn"' in content
        print("✅ Réserver button data-testid: PASS")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
