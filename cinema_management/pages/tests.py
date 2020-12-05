from django.test import TestCase

class PagesTests(TestCase):
    """
    Kiểm tra status của:
    - Trang đăng nhập
    """
    def test_login_page_status_code(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    """
    Kiểm tra status nếu chưa được đăng nhập sẽ bị redirect:
    - Trang đăng xuất
    - Trang quản lý phim
    - Trang quản lý rạp chiếu
    - Trang quản lý lịch chiếu
    - Trang quản lý thành viên
    - Trang quản lý nhân viên
    """
    def test_logout_page_status_code(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_adminmovie_page_status_code(self):
        response = self.client.get('/admin/movie')
        self.assertEqual(response.status_code, 302)

    def test_adminauditorium_page_status_code(self):
        response = self.client.get('/admin/auditorium')
        self.assertEqual(response.status_code, 302)

    def test_adminschedule_page_status_code(self):
        response = self.client.get('/admin/schedule')
        self.assertEqual(response.status_code, 302)

    def test_adminmember_page_status_code(self):
        response = self.client.get('/admin/member')
        self.assertEqual(response.status_code, 302)

    def test_adminstaff_page_status_code(self):
        response = self.client.get('/admin/staff')
        self.assertEqual(response.status_code, 302)