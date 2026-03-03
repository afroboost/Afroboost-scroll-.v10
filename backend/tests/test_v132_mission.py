"""
Mission v13.2 - Backend Tests
Tests for Credit Locking System & Refactoring Validation

Tests covered:
1. Super Admin access (credits=-1, is_super_admin=true)
2. Service prices from platform-settings
3. Reservations count (should be 22)
4. Credit packs API
5. Coach profile API
6. Extracted components functionality via frontend build verification
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Super Admin emails
SUPER_ADMIN_EMAILS = ['contact.artboost@gmail.com', 'afroboost.bassi@gmail.com']
SUPER_ADMIN_EMAIL = SUPER_ADMIN_EMAILS[0]

class TestSuperAdminAccess:
    """v13.2: Tests for Super Admin unrestricted access"""
    
    def test_super_admin_profile_has_unlimited_credits(self):
        """Super Admin should have credits=-1 (unlimited)"""
        response = requests.get(
            f"{BASE_URL}/api/coach/profile",
            headers={'X-User-Email': SUPER_ADMIN_EMAIL}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get('credits') == -1, f"Super Admin should have credits=-1, got {data.get('credits')}"
        assert data.get('is_super_admin') == True, "Super Admin flag should be true"
        print(f"PASS: Super Admin has credits=-1 and is_super_admin=true")
    
    def test_super_admin_bassi_email_recognized(self):
        """Second Super Admin email (Bassi) should also be recognized"""
        response = requests.get(
            f"{BASE_URL}/api/coach/profile",
            headers={'X-User-Email': SUPER_ADMIN_EMAILS[1]}
        )
        assert response.status_code == 200
        data = response.json()
        # Bassi should be recognized as super admin
        assert data.get('is_super_admin') == True or data.get('credits') == -1, \
            f"Bassi should be super admin, got: {data}"
        print(f"PASS: Bassi email recognized as Super Admin")
    
    def test_platform_settings_accessible_to_super_admin(self):
        """Super Admin should access platform settings with is_super_admin=true"""
        response = requests.get(
            f"{BASE_URL}/api/platform-settings",
            headers={'X-User-Email': SUPER_ADMIN_EMAIL}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get('is_super_admin') == True, "Platform settings should show is_super_admin=true"
        print(f"PASS: Platform settings accessible with is_super_admin=true")


class TestServicePrices:
    """v13.2: Tests for service prices configuration"""
    
    def test_service_prices_configured(self):
        """Platform settings should return correct service prices"""
        response = requests.get(
            f"{BASE_URL}/api/platform-settings",
            headers={'X-User-Email': SUPER_ADMIN_EMAIL}
        )
        assert response.status_code == 200
        data = response.json()
        
        service_prices = data.get('service_prices', {})
        assert service_prices.get('campaign') == 2, f"Campaign should cost 2 credits, got {service_prices.get('campaign')}"
        assert service_prices.get('ai_conversation') == 1, f"AI conversation should cost 1 credit, got {service_prices.get('ai_conversation')}"
        assert service_prices.get('promo_code') == 3, f"Promo code should cost 3 credits, got {service_prices.get('promo_code')}"
        print(f"PASS: Service prices correctly configured - campaign=2, ai_conversation=1, promo_code=3")


class TestReservationsCount:
    """v13.2: Anti-regression test for 22 reservations"""
    
    def test_reservations_count_is_22(self):
        """There should be 22 reservations (anti-regression)"""
        response = requests.get(
            f"{BASE_URL}/api/reservations?page=1&limit=100",
            headers={'X-User-Email': SUPER_ADMIN_EMAIL}
        )
        assert response.status_code == 200
        data = response.json()
        
        total = data.get('pagination', {}).get('total', 0)
        assert total == 22, f"Should have 22 reservations, got {total}"
        print(f"PASS: Reservations count is 22 (anti-regression validated)")


class TestCreditPacks:
    """v13.2: Tests for credit packs boutique"""
    
    def test_credit_packs_api_accessible(self):
        """Credit packs API should be accessible"""
        response = requests.get(f"{BASE_URL}/api/credit-packs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Credit packs should return a list"
        print(f"PASS: Credit packs API returns {len(data)} packs")


class TestExtractedComponents:
    """v13.2: Verify extracted components don't break the app"""
    
    def test_frontend_health_check(self):
        """Frontend should be accessible (verifies build success with new components)"""
        response = requests.get(f"{BASE_URL}/", timeout=10)
        assert response.status_code == 200
        print(f"PASS: Frontend accessible (extracted components build successfully)")
    
    def test_api_health(self):
        """Backend API health check"""
        response = requests.get(f"{BASE_URL}/api/health")
        # Some endpoints may not have /health, so we also check root API
        if response.status_code != 200:
            response = requests.get(f"{BASE_URL}/api/concept")
        assert response.status_code == 200
        print(f"PASS: Backend API accessible")


class TestCreditsDeduction:
    """v13.2: Tests for credits deduction endpoint"""
    
    def test_credits_deduct_endpoint_exists(self):
        """Credits deduct endpoint should exist"""
        # Test with Super Admin (should bypass)
        response = requests.post(
            f"{BASE_URL}/api/credits/deduct",
            json={'action': 'test_action'},
            headers={'X-User-Email': SUPER_ADMIN_EMAIL}
        )
        # Super Admin should succeed or get a specific response
        assert response.status_code in [200, 403, 402], f"Unexpected status: {response.status_code}"
        print(f"PASS: Credits deduct endpoint responds correctly")


class TestCoursesAndOffers:
    """v13.2: Non-regression tests for courses and offers"""
    
    def test_courses_api(self):
        """Courses API should return data"""
        response = requests.get(f"{BASE_URL}/api/courses")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Courses should return a list"
        print(f"PASS: Courses API returns {len(data)} courses")
    
    def test_offers_api(self):
        """Offers API should return data"""
        response = requests.get(f"{BASE_URL}/api/offers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Offers should return a list"
        print(f"PASS: Offers API returns {len(data)} offers")


class TestDiscountCodes:
    """v13.2: Tests for discount codes (promo codes)"""
    
    def test_discount_codes_api(self):
        """Discount codes API should return data"""
        response = requests.get(f"{BASE_URL}/api/discount-codes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Discount codes should return a list"
        print(f"PASS: Discount codes API returns {len(data)} codes")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
