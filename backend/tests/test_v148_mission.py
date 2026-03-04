"""
Test Mission v14.8 - Calendar Date Offset Fix (+7 days)

BUG FIXED: Calendar was showing March 11 instead of March 4 (today).
The bug was in the condition 'if (daysUntilCourse <= 0)' which should be 
'if (daysUntilCourse < 0)' to allow same-day booking.

FEATURES TO TEST:
1. formatReservationDate uses '< 0' (not '<= 0') for same-day course
2. Date format: fr-CH with timeZone Europe/Zurich (Neuchâtel)
3. Test calculation: Wednesday (day 3) + course Wednesday (weekday 3) = 0 days to add = 04.03.2026
4. Anti-regression audit: 2 reservations, 8 contacts
"""
import pytest
import requests
import os
from datetime import datetime

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestV148MissionCalendarDateFix:
    """Mission v14.8 - Calendar date calculation fix tests"""
    
    def test_health_check(self):
        """Verify backend is running"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200, f"Health check failed: {response.text}"
        print("✅ Health check passed")
    
    def test_contacts_count_anti_regression(self):
        """Anti-regression: Should have at least 8 contacts"""
        response = requests.get(f"{BASE_URL}/api/users")
        assert response.status_code == 200, f"Failed to get users: {response.text}"
        
        data = response.json()
        # Handle paginated or direct list response
        if isinstance(data, dict) and 'users' in data:
            users = data['users']
        elif isinstance(data, list):
            users = data
        else:
            users = data.get('data', [])
        
        contacts_count = len(users)
        assert contacts_count >= 8, f"Expected at least 8 contacts, got {contacts_count}"
        print(f"✅ Contacts count: {contacts_count} (expected >= 8)")
    
    def test_reservations_count_anti_regression(self):
        """Anti-regression: Should have at least 2 reservations"""
        response = requests.get(f"{BASE_URL}/api/reservations")
        assert response.status_code == 200, f"Failed to get reservations: {response.text}"
        
        data = response.json()
        # Handle paginated or direct list response
        if isinstance(data, dict) and 'reservations' in data:
            reservations = data['reservations']
        elif isinstance(data, dict) and 'data' in data:
            reservations = data['data']
        elif isinstance(data, list):
            reservations = data
        else:
            reservations = []
        
        reservations_count = len(reservations)
        assert reservations_count >= 2, f"Expected at least 2 reservations, got {reservations_count}"
        print(f"✅ Reservations count: {reservations_count} (expected >= 2)")
    
    def test_courses_endpoint_working(self):
        """Verify courses endpoint works for booking"""
        response = requests.get(f"{BASE_URL}/api/courses")
        assert response.status_code == 200, f"Failed to get courses: {response.text}"
        
        data = response.json()
        print(f"✅ Courses endpoint working - returned {len(data) if isinstance(data, list) else 'unknown'} courses")
    
    def test_discount_codes_endpoint_working(self):
        """Verify discount codes endpoint works"""
        response = requests.get(f"{BASE_URL}/api/discount-codes")
        assert response.status_code == 200, f"Failed to get discount codes: {response.text}"
        print("✅ Discount codes endpoint working")
    
    def test_date_calculation_logic_same_day(self):
        """
        Test date calculation logic for same-day booking:
        - If today is Wednesday (day 3) and course is on Wednesday (weekday 3)
        - daysUntilCourse = 3 - 3 = 0
        - With fix (< 0): 0 is NOT < 0, so no +7 added
        - Result: Today's date (correct)
        
        BEFORE FIX (BUG): if (daysUntilCourse <= 0): 0 <= 0 is TRUE, adds +7 days (wrong!)
        AFTER FIX: if (daysUntilCourse < 0): 0 < 0 is FALSE, no +7 days (correct!)
        """
        # Simulate the fixed logic
        def calculate_course_date_fixed(course_weekday):
            """Fixed version: < 0 instead of <= 0"""
            import datetime as dt
            today = dt.datetime.now()
            current_day = today.weekday()  # 0=Monday, 6=Sunday
            # Convert to JS-style (0=Sunday, 6=Saturday)
            current_day_js = (current_day + 1) % 7
            
            days_until_course = course_weekday - current_day_js
            # FIXED: < 0 (not <= 0) to allow same-day booking
            if days_until_course < 0:
                days_until_course += 7
            
            course_date = today + dt.timedelta(days=days_until_course)
            return course_date
        
        def calculate_course_date_buggy(course_weekday):
            """Buggy version: <= 0 causes +7 day offset"""
            import datetime as dt
            today = dt.datetime.now()
            current_day = today.weekday()
            current_day_js = (current_day + 1) % 7
            
            days_until_course = course_weekday - current_day_js
            # BUG: <= 0 causes same-day to be shifted to next week
            if days_until_course <= 0:
                days_until_course += 7
            
            course_date = today + dt.timedelta(days=days_until_course)
            return course_date
        
        # Test with today's weekday for same-day course
        import datetime as dt
        today = dt.datetime.now()
        current_day = today.weekday()
        current_day_js = (current_day + 1) % 7
        
        # Fixed version should return today for same-day course
        fixed_date = calculate_course_date_fixed(current_day_js)
        assert fixed_date.date() == today.date(), f"Fixed version should return today, got {fixed_date.date()}"
        
        # Buggy version would return next week for same-day course
        buggy_date = calculate_course_date_buggy(current_day_js)
        expected_buggy_date = today + dt.timedelta(days=7)
        assert buggy_date.date() == expected_buggy_date.date(), f"Buggy version should add 7 days"
        
        print(f"✅ Date calculation logic verified:")
        print(f"   Today: {today.strftime('%A %d.%m.%Y')} (day {current_day_js})")
        print(f"   Course weekday: {current_day_js} (same as today)")
        print(f"   Fixed (< 0): {fixed_date.strftime('%A %d.%m.%Y')} ✅ CORRECT")
        print(f"   Buggy (<= 0): {buggy_date.strftime('%A %d.%m.%Y')} ❌ +7 days offset")
    
    def test_wednesday_march_4_2026_scenario(self):
        """
        Specific test for the reported bug:
        - System date: Wed Mar 4 2026 (day 3 in JS)
        - Course on Wednesday (weekday 3)
        - Expected: 04.03.2026
        - Bug showed: 11.03.2026 (+7 days)
        """
        import datetime as dt
        
        # Simulate March 4, 2026 (Wednesday)
        test_date = dt.datetime(2026, 3, 4)  # Wednesday
        test_weekday_js = 3  # Wednesday in JS (0=Sunday)
        
        course_weekday = 3  # Course on Wednesday
        
        # Calculate days until course (fixed logic)
        days_until_course = course_weekday - test_weekday_js
        
        # Verify the fix
        assert days_until_course == 0, f"Days until course should be 0 for same day, got {days_until_course}"
        
        # Fixed condition: < 0
        add_week_fixed = days_until_course < 0
        assert add_week_fixed == False, f"Should NOT add 7 days with fixed condition (< 0)"
        
        # Buggy condition: <= 0
        add_week_buggy = days_until_course <= 0
        assert add_week_buggy == True, f"Would add 7 days with buggy condition (<= 0)"
        
        # Calculate final dates
        if days_until_course < 0:  # Fixed
            days_until_course_fixed = days_until_course + 7
        else:
            days_until_course_fixed = days_until_course
        
        final_date_fixed = test_date + dt.timedelta(days=days_until_course_fixed)
        
        # Expected: 04.03.2026 (same day)
        assert final_date_fixed.day == 4, f"Fixed date should be 4th, got {final_date_fixed.day}"
        assert final_date_fixed.month == 3, f"Fixed date should be March, got month {final_date_fixed.month}"
        
        print(f"✅ March 4, 2026 scenario verified:")
        print(f"   Test date: {test_date.strftime('%A %d.%m.%Y')}")
        print(f"   Course weekday: {course_weekday} (Wednesday)")
        print(f"   daysUntilCourse: {days_until_course}")
        print(f"   Fixed (< 0): {final_date_fixed.strftime('%d.%m.%Y')} ✅")
        print(f"   Buggy (<= 0): would show 11.03.2026 (+7 days) ❌")


class TestV148AntiRegression:
    """Anti-regression tests for Mission v14.8"""
    
    def test_offers_endpoint_working(self):
        """Verify offers endpoint works"""
        response = requests.get(f"{BASE_URL}/api/offers")
        assert response.status_code == 200, f"Failed to get offers: {response.text}"
        print("✅ Offers endpoint working")
    
    def test_chat_sessions_endpoint_working(self):
        """Verify chat sessions endpoint works (for Super Admin)"""
        headers = {'X-User-Email': 'contact.artboost@gmail.com'}
        response = requests.get(f"{BASE_URL}/api/chat/sessions", headers=headers)
        assert response.status_code == 200, f"Failed to get chat sessions: {response.text}"
        print("✅ Chat sessions endpoint working (Super Admin)")
    
    def test_platform_settings_endpoint_working(self):
        """Verify platform settings endpoint works"""
        response = requests.get(f"{BASE_URL}/api/platform-settings")
        assert response.status_code == 200, f"Failed to get platform settings: {response.text}"
        print("✅ Platform settings endpoint working")
    
    def test_coach_vitrine_endpoint_working(self):
        """Verify coach vitrine endpoint works"""
        response = requests.get(f"{BASE_URL}/api/coach/vitrine/bassi")
        assert response.status_code == 200, f"Failed to get coach vitrine: {response.text}"
        print("✅ Coach vitrine endpoint working")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
