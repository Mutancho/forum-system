
import unittest
from unittest.mock import Mock, create_autospec, patch
from schemas.user import User, EmailLogin, UsernameLogin, Member, RevokeMemberAccess, UpdateUser
from services import user_service

class UserService_Should(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @patch('services.user_service.read_query', autospec=True)
    def test_all_createsListOfUsers_when_dataIsPresent(self, mock_read_query):
        mock_read_query.return_value = [(1, 'Test_username', 'Test_email@test.ts', 'Test_role','2023-04-14')
            , (2, 'Test_username', 'Test_email@test.ts', 'Test_role','2023-04-14')]
        result = list(user_service.all())
        self.assertEqual(2, len(result))

    @patch('services.user_service.read_query', autospec=True)
    def test_all_returnsEmptyListOfUsers_when_dataIsNotPresent(self, mock_read_query):
        mock_read_query.return_value = []
        result = list(user_service.all())
        self.assertEqual([], result)

    @patch('services.user_service.insert_query', autospec=True)
    def test_create_createsUser(self, mock_insert_query):
        user = User(id=None,username='Testing',email='test@gmasil.com',password='123456',role='user')

        with patch('services.user_service.read_query') as mock_read_query:
            mock_insert_query.return_value = 1
            mock_read_query.return_value = [('2023-04-14',)]
            result = user_service.create(user)
        self.assertEqual(User, type(result))
        self.assertEqual(1,result.id)
        self.assertEqual('2023-04-14',result.created_at)


    def test_update_returnsUpdateUser(self):
        user = UpdateUser(username='Testing', email='test@gmasil.com', password='123456')
        user_service.update_query = Mock()

        result = user_service.update(1, user)
        user_service.update_query.assert_called_once()
        self.assertEqual(user, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_checkUniqueUpdateEmailPassword_returnsFalse_when_dataIsNotPresent(self,mock_read_query):
        user = UpdateUser(username='Testing', email='test@gmasil.com', password='123456')
        mock_read_query.return_value = []

        result = user_service.check_unique_update_email_password(1, user)
        self.assertEqual(False, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_checkUniqueUpdateEmailPassword_returnsTrue_when_dataIsPresent(self, mock_read_query):
        user = UpdateUser(username='Testing', email='test@gmasil.com', password='123456')
        mock_read_query.return_value = [(user,)]

        result = user_service.check_unique_update_email_password(1, user)
        self.assertEqual(True, result)

    def test_delete(self):
        user_service.update_query = Mock()
        user_service.delete(1)
        user_service.update_query.assert_called_once()

    @patch('services.user_service.read_query', autospec=True)
    def test_getById_returnsUser_when_dataIsPresent(self, mock_read_query):
        mock_read_query.return_value = [(1, 'Test_username', 'Test_email@test.ts', 'Test_role', '2023-04-14')]
        result = user_service.get_by_id(1)
        expected = User(id=1,username='Test_username',email='Test_email@test.ts',password='*********',role='Test_role',created_at='2023-04-14')
        self.assertEqual(expected, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_existsByUsernameEmail_returnsTrue_when_dataIsPresent(self, mock_read_query):
        user = User(id=1,username='Test_username',email='Test_email@test.ts',password='*********',role='Test_role',created_at='2023-04-14')
        mock_read_query.return_value = [(user,)]

        result = user_service.exists_by_username_email(user)
        self.assertEqual(True, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_existsByUsernameEmail_returnsFalse_when_dataIsNotPresent(self, mock_read_query):
        user = User(id=1, username='Test_username', email='Test_email@test.ts', password='*********', role='Test_role',
                    created_at='2023-04-14')
        mock_read_query.return_value = []

        result = user_service.exists_by_username_email(user)
        self.assertEqual(False, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_existsById_returnsTrue_when_dataIsPresent(self, mock_read_query):
        user = User(id=1, username='Test_username', email='Test_email@test.ts', password='*********', role='Test_role',
                    created_at='2023-04-14')
        mock_read_query.return_value = [(user,)]

        result = user_service.exists_by_id(1)
        self.assertEqual(True, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_existsById_returnsFalse_when_dataIsNotPresent(self, mock_read_query):
        user = User(id=1, username='Test_username', email='Test_email@test.ts', password='*********', role='Test_role',
                    created_at='2023-04-14')
        mock_read_query.return_value = []

        result = user_service.exists_by_id(1)
        self.assertEqual(False, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_login_returnsToken_when_EmailLogin(self, mock_read_query):
        email_login = EmailLogin(email='Test_email@test.ts',password='*********')
        mock_read_query.return_value = [(1,'Test_username','Test_email@test.ts')]

        result = user_service.login(email_login)
        self.assertIsNotNone(result)

    @patch('services.user_service.read_query', autospec=True)
    def test_login_returnsToken_when_UsernameLogin(self, mock_read_query):
        username_login = UsernameLogin(username='Test_username', password='*********')
        mock_read_query.return_value = [(1, 'Test_username', 'Test_email@test.ts')]

        result = user_service.login(username_login)
        self.assertIsNotNone(result)



    def test_giveAccess_when_userHasPermissionsForCategory(self):
        member_access = Member(user_id=1,category_id=1,read_access=True,write_access=True)
        user_service.user_has_permissions_for_category = lambda a,s : True
        user_service.update_query = Mock()

        user_service.give_access(member_access)
        user_service.update_query.assert_called_once()

    def test_giveAccess_when_userHasNoPermissionsForCategory(self):
        member_access = Member(user_id=1,category_id=1,read_access=True,write_access=True)
        user_service.user_has_permissions_for_category = lambda a,s : False
        user_service.insert_query = Mock()

        user_service.give_access(member_access)
        user_service.insert_query.assert_called_once()

    def test_revokeAccess(self):
        member_access = Member(user_id=1,category_id=1,read_access=False,write_access=False)
        user_service.update_query = Mock()

        user_service.revoke_access(member_access)
        user_service.update_query.assert_called_once()

    @patch('services.user_service.read_query', autospec=True)
    def test_userHasPermissionsForCategory_returnsTrue_when_dataIsPresent(self, mock_read_query):

        mock_read_query.return_value = [('categorymembers data',)]

        result = user_service.user_has_permissions_for_category(1,2)
        self.assertEqual(True, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_userHasPermissionsForCategory_returnsFalse_when_dataIsNotPresent(self, mock_read_query):
        mock_read_query.return_value = []

        result = user_service.user_has_permissions_for_category(1,2)
        self.assertEqual(False, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyCredentials_returnsTrue_when_EmailLogin_exists(self, mock_read_query):
        email_login = EmailLogin(email='Test_email@test.ts', password='*********')
        mock_read_query.return_value = [(1, 'Test_username', 'Test_email@test.ts')]

        result = user_service.verify_credentials(email_login)
        self.assertEqual(True,result)

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyCredentials_returnsTrue_when_UsernameLogin_exists(self, mock_read_query):
        username_login = UsernameLogin(username='Test_username', password='*********')
        mock_read_query.return_value = [(1, 'Test_username', 'Test_email@test.ts')]

        result = user_service.verify_credentials(username_login)
        self.assertEqual(True,result)

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyCredentials_returnsFalse_when_EmailLogin_exists(self, mock_read_query):
        email_login = EmailLogin(email='Test_email@test.ts', password='*********')
        mock_read_query.return_value = []

        result = user_service.verify_credentials(email_login)
        self.assertEqual(False, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyCredentials_returnsFalse_when_UsernameLogin_exists(self, mock_read_query):
        username_login = UsernameLogin(username='Test_username', password='*********')
        mock_read_query.return_value = []

        result = user_service.verify_credentials(username_login)
        self.assertEqual(False, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_isUserAuthorizedToGetDelete_returnsTrue_when_userIsHimself(self, mock_read_query):
        mock_read_query.return_value = [('not admin',)]
        user_service.oauth2.get_current_user = lambda token: 1

        result = user_service.is_user_authorized_to_get_delete('token', 1)
        self.assertEqual(True, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_isUserAuthorizedToGetDelete_returnsTrue_when_userIsAdmin(self, mock_read_query):
        mock_read_query.return_value = [('admin',)]
        user_service.oauth2.get_current_user = lambda token: 0

        result = user_service.is_user_authorized_to_get_delete('token',1)
        self.assertEqual(True, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_isUserAuthorizedToGetDelete_returnsFalse_when_userIsNotAdminOrHimself(self, mock_read_query):
        mock_read_query.return_value = [('not admin',)]
        user_service.oauth2.get_current_user = lambda token: 0

        result = user_service.is_user_authorized_to_get_delete('token', 1)
        self.assertEqual(False, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_isAdmin_returnsTrue_when_userIsAdmin(self, mock_read_query):
        mock_read_query.return_value = [('admin',)]
        user_service.oauth2.get_current_user = lambda token: 1

        result = user_service.is_admin('token')
        self.assertEqual(True, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_isAdmin_returnsFalse_when_userIsNotAdmin(self, mock_read_query):
        mock_read_query.return_value = [('not admin',)]
        user_service.oauth2.get_current_user = lambda token: 1

        result = user_service.is_admin('token')
        self.assertEqual(False, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyPassword_returnsTrue_when_EmailLogin_passwordIsEqualToDecoded(self, mock_read_query):
        email_login = EmailLogin(email='Test_email@test.ts', password='123456')
        mock_read_query.return_value = [('$2b$12$V0NmXBYEU2o0x3nbxOPouu9EMhcKhYH5k3lBS49XlSoUbKrTxM0Pa',)]

        result = user_service.valid_password(email_login)
        self.assertEqual(True, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyPassword_returnsTrue_when_UsernameLogin_passwordIsEqualToDecoded(self, mock_read_query):
        username_login = UsernameLogin(username='Test_username', password='123456')
        mock_read_query.return_value = [('$2b$12$V0NmXBYEU2o0x3nbxOPouu9EMhcKhYH5k3lBS49XlSoUbKrTxM0Pa',)]

        result = user_service.valid_password(username_login)
        self.assertEqual(True, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyPassword_returnsFalse_when_EmailLogin_passwordIsNotEqualToDecoded(self, mock_read_query):
        email_login = EmailLogin(email='Test_email@test.ts', password='123456')
        mock_read_query.return_value = [('notHashFor:123456',)]

        result = user_service.valid_password(email_login)
        self.assertEqual(False, result)

    @patch('services.user_service.read_query', autospec=True)
    def test_verifyPassword_returnsFalse_when_UsernameLogin_passwordIsNotEqualToDecoded(self, mock_read_query):
        username_login = UsernameLogin(username='Test_username', password='123456')
        mock_read_query.return_value = [('notHashFor:123456',)]

        result = user_service.valid_password(username_login)
        self.assertEqual(False, result)



















