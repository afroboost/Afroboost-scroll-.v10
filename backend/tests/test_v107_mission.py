"""
Test Mission v10.7: Icônes Premium et Réduction de Taille
Tests for:
- API /api/partners/active endpoint
- Boutons compacts w-20 h-20 (80x80) sur la vitrine partenaire
- Icône Calendrier pour Réserver
- Icône Enveloppe pour Contact/Chat
- Bouton Retour en icône ronde w-10 h-10
- Header icons gap 16px
- Like button violet glow
"""

import pytest
import requests
import os
import re

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestMissionV107API:
    """API Tests for Mission v10.7"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        print("✅ Health endpoint working")
    
    def test_partners_active_endpoint(self):
        """Test /api/partners/active returns partners"""
        response = requests.get(f"{BASE_URL}/api/partners/active")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1, "Should have at least one active partner"
        print(f"✅ Partners active endpoint returns {len(data)} partners")
    
    def test_coach_vitrine_endpoint(self):
        """Test /api/coach/vitrine/{username} returns coach data"""
        response = requests.get(f"{BASE_URL}/api/coach/vitrine/contact.artboost@gmail.com")
        assert response.status_code == 200
        data = response.json()
        assert 'coach' in data
        print("✅ Coach vitrine endpoint working")


class TestMissionV107CodeAnalysis:
    """Code Analysis Tests for Mission v10.7"""
    
    @pytest.fixture(scope="class")
    def coach_vitrine_code(self):
        """Load CoachVitrine.js code"""
        with open('/app/frontend/src/components/CoachVitrine.js', 'r') as f:
            return f.read()
    
    @pytest.fixture(scope="class") 
    def partners_carousel_code(self):
        """Load PartnersCarousel.js code"""
        with open('/app/frontend/src/components/PartnersCarousel.js', 'r') as f:
            return f.read()
    
    def test_back_button_w10_h10_rounded(self, coach_vitrine_code):
        """Verify Retour button is w-10 h-10 rounded-full"""
        # Check for w-10 h-10 rounded-full pattern near vitrine-back-btn
        pattern = r'className="w-10 h-10 rounded-full.*?".*?data-testid="vitrine-back-btn"'
        match = re.search(pattern, coach_vitrine_code, re.DOTALL)
        assert match, "Bouton Retour should have w-10 h-10 rounded-full classes"
        print("✅ Bouton Retour has correct classes: w-10 h-10 rounded-full")
    
    def test_reserver_button_w20_h20(self, coach_vitrine_code):
        """Verify Réserver button is w-20 h-20"""
        # Check for w-20 h-20 pattern near vitrine-cta-btn
        pattern = r'className="w-20 h-20.*?".*?data-testid="vitrine-cta-btn"'
        match = re.search(pattern, coach_vitrine_code, re.DOTALL)
        assert match, "Bouton Réserver should have w-20 h-20 classes"
        print("✅ Bouton Réserver has correct classes: w-20 h-20 (80x80)")
    
    def test_contact_button_w20_h20(self, coach_vitrine_code):
        """Verify Contact button is w-20 h-20"""
        # Check for w-20 h-20 pattern near vitrine-chat-btn
        pattern = r'className="w-20 h-20.*?".*?data-testid="vitrine-chat-btn"'
        match = re.search(pattern, coach_vitrine_code, re.DOTALL)
        assert match, "Bouton Contact should have w-20 h-20 classes"
        print("✅ Bouton Contact has correct classes: w-20 h-20 (80x80)")
    
    def test_calendar_svg_icon(self, coach_vitrine_code):
        """Verify Calendar SVG icon in Réserver button"""
        # Check for SVG calendar icon pattern (rect, line for calendar)
        pattern = r'<svg.*?width="24".*?height="24".*?>.*?<rect x="3" y="4".*?</svg>'
        match = re.search(pattern, coach_vitrine_code, re.DOTALL)
        assert match, "Réserver button should have calendar SVG icon"
        print("✅ Icône Calendrier SVG présente dans Réserver")
    
    def test_envelope_svg_icon(self, coach_vitrine_code):
        """Verify Envelope SVG icon in Contact button"""
        # Check for SVG envelope icon pattern (polyline for envelope)
        pattern = r'<svg.*?width="24".*?height="24".*?>.*?<polyline points="22,6 12,13 2,6".*?</svg>'
        match = re.search(pattern, coach_vitrine_code, re.DOTALL)
        assert match, "Contact button should have envelope SVG icon"
        print("✅ Icône Enveloppe SVG présente dans Contact")
    
    def test_buttons_in_flex_gap_4(self, coach_vitrine_code):
        """Verify buttons are in flex container with gap-4 (16px)"""
        # Check for flex gap-4 container around the buttons
        pattern = r'<div className="flex gap-4">'
        assert pattern in coach_vitrine_code, "Buttons should be in flex container with gap-4"
        print("✅ Boutons dans container flex gap-4 (16px)")
    
    def test_header_icons_gap_16px(self, partners_carousel_code):
        """Verify header icons have gap-4 (16px)"""
        # Check for flex items-center gap-4 in PartnersCarousel
        pattern = r'<div className="flex items-center gap-4">'
        assert pattern in partners_carousel_code, "Header icons should have gap-4 (16px)"
        print("✅ Header icons gap = 16px (gap-4)")
    
    def test_like_button_violet_glow(self, partners_carousel_code):
        """Verify Like button has violet glow when liked"""
        # Check for D91CD2 in boxShadow for liked state
        pattern = r"boxShadow: isLiked \? '0 0 20px rgba\(217, 28, 210"
        match = re.search(pattern, partners_carousel_code)
        assert match, "Like button should have violet glow (rgba(217, 28, 210))"
        print("✅ Like button a un glow violet (#D91CD2) quand liké")
    
    def test_buttons_have_glow_effect(self, coach_vitrine_code):
        """Verify CTA buttons have glow effect"""
        # Check for D91CD2 glow in vitrine buttons
        pattern = r"boxShadow: '0 0 20px rgba\(217, 28, 210"
        match = re.search(pattern, coach_vitrine_code)
        assert match, "Vitrine buttons should have violet glow"
        print("✅ Boutons vitrine ont un glow violet")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
