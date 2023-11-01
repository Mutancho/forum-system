import unittest
from unittest.mock import Mock, create_autospec, patch
from schemas.user import User, EmailLogin, UsernameLogin, Member, RevokeMemberAccess, UpdateUser
from services import user_service
from asyncio import run


class UserService_Should(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @patch('services.user_service.read_query', autospec=True)
    def test_all_createsListOfUsers_when_dataIsPresent(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = [(1, 'Test_username', 'Test_email@test.ts', 'Test_role', '2023-04-14')
                , (2, 'Test_username', 'Test_email@test.ts', 'Test_role', '2023-04-14')]
            result = await list(user_service.all())
            self.assertEqual(2, len(result))
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_all_returnsEmptyListOfUsers_when_dataIsNotPresent(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = []
            result = await list(user_service.all())
            self.assertEqual([], result)
            run(async_test())

    @patch('services.user_service.insert_query', autospec=True)
    def test_create_createsUser(self, mock_insert_query):
        async def async_test():
            user = User(id=None, username='Testing', email='test@gmasil.com', password='123456', role='user')

            with patch('services.user_service.read_query') as mock_read_query:
                mock_insert_query.return_value = 1
                mock_read_query.return_value = [('2023-04-14',)]
                result = await user_service.create(user)
            self.assertEqual(User, type(result))
            self.assertEqual(1, result.id)
            self.assertEqual('2023-04-14', result.created_at)
            run(async_test())

    def test_update_returnsUpdateUser(self):
        async def async_test():
            user = UpdateUser(username='Testing', email='test@gmasil.com', password='123456')
            user_service.update_query = Mock()

            result = await user_service.update(1, user)
            user_service.update_query.assert_called_once()
            self.assertEqual(user, result)
            user_service.update_query.reset_mock()
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_checkUniqueUpdateEmailPassword_returnsFalse_when_dataIsNotPresent(self, mock_read_query):
        async def async_test():
            user = UpdateUser(username='Testing', email='test@gmasil.com', password='123456')
            mock_read_query.return_value = []

            result = await user_service.check_unique_update_email_password(1, user)
            self.assertEqual(False, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_checkUniqueUpdateEmailPassword_returnsTrue_when_dataIsPresent(self, mock_read_query):
        async def async_test():
            user = UpdateUser(username='Testing', email='test@gmasil.com', password='123456')
            mock_read_query.return_value = [(user,)]

            result = await user_service.check_unique_update_email_password(1, user)
            self.assertEqual(True, result)
            run(async_test())

    def test_delete(self):
        async def async_test():
            user_service.update_query = Mock()
            await user_service.delete(1)
            user_service.update_query.assert_called_once()
            user_service.update_query.reset_mock()
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_getById_returnsUser_when_dataIsPresent(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = [(1, 'Test_username', 'Test_email@test.ts', 'Test_role', '2023-04-14')]
            result = await user_service.get_by_id(1)
            expected = User(id=1, username='Test_username', email='Test_email@test.ts', password='*********',
                            role='Test_role', created_at='2023-04-14')
            self.assertEqual(expected, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_existsByUsernameEmail_returnsTrue_when_dataIsPresent(self, mock_read_query):
        async def async_test():
            user = User(id=1, username='Test_username', email='Test_email@test.ts', password='*********',
                        role='Test_role',
                        created_at='2023-04-14')
            mock_read_query.return_value = [(user,)]

            result = await user_service.exists_by_username_email(user)
            self.assertEqual(True, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_existsByUsernameEmail_returnsFalse_when_dataIsNotPresent(self, mock_read_query):
        async def async_test():
            user = User(id=1, username='Test_username', email='Test_email@test.ts', password='*********',
                        role='Test_role',
                        created_at='2023-04-14')
            mock_read_query.return_value = []

            result = await user_service.exists_by_username_email(user)
            self.assertEqual(False, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_existsById_returnsTrue_when_dataIsPresent(self, mock_read_query):
        async def async_test():
            user = User(id=1, username='Test_username', email='Test_email@test.ts', password='*********',
                        role='Test_role',
                        created_at='2023-04-14')
            mock_read_query.return_value = [(user,)]

            result = await user_service.exists_by_id(1)
            self.assertEqual(True, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_existsById_returnsFalse_when_dataIsNotPresent(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = []

            result = await user_service.exists_by_id(1)
            self.assertEqual(False, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_login_returnsToken_when_EmailLogin(self, mock_read_query):
        async def async_test():
            email_login = EmailLogin(email='Test_email@test.ts', password='*********')
            mock_read_query.return_value = [(1, 'Test_username', 'Test_email@test.ts')]

            result = await user_service.login(email_login)
            self.assertIsNotNone(result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_login_returnsToken_when_UsernameLogin(self, mock_read_query):
        async def async_test():
            username_login = UsernameLogin(username='Test_username', password='*********')
            mock_read_query.return_value = [(1, 'Test_username', 'Test_email@test.ts')]

            result = await user_service.login(username_login)
            self.assertIsNotNone(result)
            run(async_test())

    def test_giveAccess_when_userHasPermissionsForCategory(self):
        async def async_test():
            with patch(
                    'services.user_service.user_has_permissions_for_category') as mock_user_has_permissions_for_category:
                member_access = Member(user_id=1, category_id=1, read_access=True, write_access=True)
                mock_user_has_permissions_for_category = True
                user_service.update_query = Mock()

                await user_service.give_access(member_access)
                user_service.update_query.assert_called_once()
            run(async_test())

    def test_giveAccess_when_userHasNoPermissionsForCategory(self):
        async def async_test():
            with patch(
                    'services.user_service.user_has_permissions_for_category') as mock_user_has_permissions_for_category:
                member_access = Member(user_id=1, category_id=1, read_access=True, write_access=True)
                mock_user_has_permissions_for_category.return_value = False
                user_service.insert_query = Mock()

                await user_service.give_access(member_access)
                user_service.insert_query.assert_called_once()
            run(async_test())

    def test_revokeAccess(self):
        async def async_test():
            member_access = Member(user_id=1, category_id=1, read_access=False, write_access=False)
            user_service.update_query = Mock()

            await user_service.revoke_access(member_access)
            user_service.update_query.assert_called_once()
            user_service.update_query.reset_mock()
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_userHasPermissionsForCategory_returnsTrue_when_dataIsPresent(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = [('categorymembers data',)]

            result = await user_service.user_has_permissions_for_category(1, 2)
            self.assertEqual(True, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_userHasPermissionsForCategory_returnsFalse_when_dataIsNotPresent(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = []

            result = await user_service.user_has_permissions_for_category(1, 2)
            self.assertEqual(False, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyCredentials_returnsTrue_when_EmailLogin_exists(self, mock_read_query):
        async def async_test():
            email_login = EmailLogin(email='Test_email@test.ts', password='*********')
            mock_read_query.return_value = [(1, 'Test_username', 'Test_email@test.ts')]

            result = await user_service.verify_credentials(email_login)
            self.assertEqual(True, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyCredentials_returnsTrue_when_UsernameLogin_exists(self, mock_read_query):
        async def async_test():
            username_login = UsernameLogin(username='Test_username', password='*********')
            mock_read_query.return_value = [(1, 'Test_username', 'Test_email@test.ts')]

            result = await user_service.verify_credentials(username_login)
            self.assertEqual(True, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyCredentials_returnsFalse_when_EmailLogin_exists(self, mock_read_query):
        async def async_test():
            email_login = EmailLogin(email='Test_email@test.ts', password='*********')
            mock_read_query.return_value = []

            result = await user_service.verify_credentials(email_login)
            self.assertEqual(False, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyCredentials_returnsFalse_when_UsernameLogin_exists(self, mock_read_query):
        async def async_test():
            username_login = UsernameLogin(username='Test_username', password='*********')
            mock_read_query.return_value = []

            result = await user_service.verify_credentials(username_login)
            self.assertEqual(False, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_isUserAuthorizedToGetDelete_returnsTrue_when_userIsHimself(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = [('not admin',)]
            user_service.oauth2.get_current_user = lambda token: 1

            result = await user_service.is_user_authorized_to_get_delete('token', 1)
            self.assertEqual(True, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_isUserAuthorizedToGetDelete_returnsTrue_when_userIsAdmin(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = [('admin',)]
            user_service.oauth2.get_current_user = lambda token: 0

            result = await user_service.is_user_authorized_to_get_delete('token', 1)
            self.assertEqual(True, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_isUserAuthorizedToGetDelete_returnsFalse_when_userIsNotAdminOrHimself(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = [('not admin',)]
            user_service.oauth2.get_current_user = lambda token: 0

            result = await user_service.is_user_authorized_to_get_delete('token', 1)
            self.assertEqual(False, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_isAdmin_returnsTrue_when_userIsAdmin(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = [('admin',)]
            user_service.oauth2.get_current_user = lambda token: 1

            result = await user_service.is_admin('token')
            self.assertEqual(True, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_isAdmin_returnsFalse_when_userIsNotAdmin(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = [('not admin',)]
            user_service.oauth2.get_current_user = lambda token: 1

            result = await user_service.is_admin('token')
            self.assertEqual(False, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyPassword_returnsTrue_when_EmailLogin_passwordIsEqualToDecoded(self, mock_read_query):
        async def async_test():
            email_login = EmailLogin(email='Test_email@test.ts', password='123456')
            mock_read_query.return_value = [('$2b$12$V0NmXBYEU2o0x3nbxOPouu9EMhcKhYH5k3lBS49XlSoUbKrTxM0Pa',)]

            result = await user_service.valid_password(email_login)
            self.assertEqual(True, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyPassword_returnsTrue_when_UsernameLogin_passwordIsEqualToDecoded(self, mock_read_query):
        async def async_test():
            username_login = UsernameLogin(username='Test_username', password='123456')
            mock_read_query.return_value = [('$2b$12$V0NmXBYEU2o0x3nbxOPouu9EMhcKhYH5k3lBS49XlSoUbKrTxM0Pa',)]

            result = await user_service.valid_password(username_login)
            self.assertEqual(True, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyPassword_returnsFalse_when_EmailLogin_passwordIsNotEqualToDecoded(self, mock_read_query):
        async def async_test():
            email_login = EmailLogin(email='Test_email@test.ts', password='123456')
            mock_read_query.return_value = [('notHashFor:123456',)]

            result = await user_service.valid_password(email_login)
            self.assertEqual(False, result)
            run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyPassword_returnsFalse_when_UsernameLogin_passwordIsNotEqualToDecoded(self, mock_read_query):
        async def async_test():
            username_login = UsernameLogin(username='Test_username', password='123456')
            mock_read_query.return_value = [('notHashFor:123456',)]

            result = await user_service.valid_password(username_login)
            self.assertEqual(False, result)
            run(async_test())
