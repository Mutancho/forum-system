from unittest import TestCase
from unittest.mock import patch
import services.category_service as cat_service
from schemas.category import CategoryWithTopics, Category, CategoryOut
from services.validations import UpdateStatus
import tests.constants as C


class TestCategoryService(TestCase):
    @patch("services.category_service.read_query")
    def test_get_all(self, mock_read_query):
        mock_read_query.return_value = [
            (1, "Category 1", False, False),
            (2, "Category 2", True, False),
            (3, "Category 3", False, True),
        ]

        result = cat_service.get_all()

        expected_result = [
            CategoryOut(id=1, name="Category 1", private=False, locked=False),
            CategoryOut(id=2, name="Category 2", private=True, locked=False),
            CategoryOut(id=3, name="Category 3", private=False, locked=True),
        ]

        self.assertEqual(result, expected_result)
        mock_read_query.assert_called_once_with("SELECT * FROM categories")


class TestGetCategoryByID_Should(TestCase):
    @patch("services.category_service.get_current_user")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    @patch("services.category_service.is_category_private")
    @patch("services.category_service.category_read_restriction_applies")
    @patch("services.category_service.read_query")
    def test_not_admin_no_constraints(self, mock_read_query, mock_category_read_restriction_applies,
                                      mock_is_category_private, mock_is_admin, mock_category_exists,
                                      mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_category_exists.return_value = C.CATEGORY_EXISTS_RETURN_VALUE
        mock_is_admin.return_value = False
        mock_is_category_private.return_value = C.NOT_PRIVATE_CATEGORY
        mock_category_read_restriction_applies.return_value = C.READ_ACCESS_DENIED
        mock_read_query.return_value = C.READ_QUERY_RETURN_VALUE_CATEGORY_WITH_TOPICS

        result = cat_service.get_category_by_id_with_topics(C.TOKEN, C.CATEGORY_ID_1)
        self.assertIsInstance(result, CategoryWithTopics)
        self.assertEqual(result.category.name, C.CATEGORY_NAME_1)
        self.assertEqual(len(result.topics), 2)
        self.assertEqual(result.topics[0].title, C.TOPIC_NAME_1)
        self.assertEqual(result.topics[1].title, C.TOPIC_NAME_2)

    @patch("services.category_service.get_current_user")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    @patch("services.category_service.is_category_private")
    @patch("services.category_service.category_read_restriction_applies")
    @patch("services.category_service.read_query")
    def test_not_admin_private_no_read_access(self, mock_read_query, mock_category_read_restriction_applies,
                                              mock_is_category_private, mock_is_admin, mock_category_exists,
                                              mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_category_exists.return_value = C.CATEGORY_EXISTS_RETURN_VALUE
        mock_is_admin.return_value = False
        mock_is_category_private.return_value = C.PRIVATE_CATEGORY
        mock_category_read_restriction_applies.return_value = C.READ_ACCESS_DENIED
        mock_read_query.return_value = C.READ_QUERY_RETURN_VALUE_CATEGORY_WITH_TOPICS

        result = cat_service.get_category_by_id_with_topics(C.TOKEN, C.CATEGORY_ID_1)
        self.assertEqual(result, UpdateStatus.NO_READ_ACCESS)

    @patch("services.category_service.get_current_user")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    @patch("services.category_service.is_category_private")
    @patch("services.category_service.category_read_restriction_applies")
    @patch("services.category_service.read_query")
    def test_not_admin_private_with_read_access(self, mock_read_query, mock_category_read_restriction_applies,
                                                mock_is_category_private, mock_is_admin, mock_category_exists,
                                                mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_category_exists.return_value = C.CATEGORY_EXISTS_RETURN_VALUE
        mock_is_admin.return_value = False
        mock_is_category_private.return_value = C.PRIVATE_CATEGORY
        mock_category_read_restriction_applies.return_value = C.READ_ACCESS_GRANTED
        mock_read_query.return_value = C.READ_QUERY_RETURN_VALUE_CATEGORY_WITH_TOPICS

        result = cat_service.get_category_by_id_with_topics(C.TOKEN, C.CATEGORY_ID_1)
        self.assertIsInstance(result, CategoryWithTopics)
        self.assertEqual(result.category.name, C.CATEGORY_NAME_1)
        self.assertEqual(len(result.topics), 2)
        self.assertEqual(result.topics[0].title, C.TOPIC_NAME_1)
        self.assertEqual(result.topics[1].title, C.TOPIC_NAME_2)

    @patch("services.category_service.get_current_user")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    @patch("services.category_service.is_category_private")
    @patch("services.category_service.category_read_restriction_applies")
    @patch("services.category_service.read_query")
    def test_admin_private_with_no_read_access(self, mock_read_query, mock_category_read_restriction_applies,
                                               mock_is_category_private, mock_is_admin, mock_category_exists,
                                               mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_category_exists.return_value = C.CATEGORY_EXISTS_RETURN_VALUE
        mock_is_admin.return_value = True
        mock_is_category_private.return_value = C.PRIVATE_CATEGORY
        mock_category_read_restriction_applies.return_value = C.READ_ACCESS_DENIED
        mock_read_query.return_value = C.READ_QUERY_RETURN_VALUE_CATEGORY_WITH_TOPICS

        result = cat_service.get_category_by_id_with_topics(C.TOKEN, C.CATEGORY_ID_1)
        self.assertIsInstance(result, CategoryWithTopics)
        self.assertEqual(result.category.name, C.CATEGORY_NAME_1)
        self.assertEqual(len(result.topics), 2)
        self.assertEqual(result.topics[0].title, C.TOPIC_NAME_1)
        self.assertEqual(result.topics[1].title, C.TOPIC_NAME_2)

    @patch("services.category_service.get_current_user")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    @patch("services.category_service.is_category_private")
    @patch("services.category_service.category_read_restriction_applies")
    @patch("services.category_service.read_query")
    def test_not_found(self, mock_read_query, mock_category_read_restriction_applies,
                       mock_is_category_private, mock_is_admin, mock_category_exists,
                       mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_category_exists.return_value = None
        mock_is_admin.return_value = True
        mock_is_category_private.return_value = C.PRIVATE_CATEGORY
        mock_category_read_restriction_applies.return_value = C.READ_ACCESS_DENIED
        mock_read_query.return_value = C.READ_QUERY_RETURN_VALUE_CATEGORY_WITH_TOPICS

        result = cat_service.get_category_by_id_with_topics(C.TOKEN, C.INVALID_CATEGORY_ID)
        self.assertEqual(result, UpdateStatus.NOT_FOUND)


class TestCreate_Should(TestCase):

    def setUp(self):
        self.sample_category = Category(id=None, name=C.CATEGORY_NAME_1)

    @patch("services.category_service.is_admin")
    @patch("services.category_service.insert_query")
    def test_create_success(self, mock_insert_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_insert_query.return_value = 1

        token = C.TOKEN
        created_category = cat_service.create(token, self.sample_category)

        self.assertEqual(created_category.id, C.CATEGORY_ID_1)
        self.assertEqual(created_category.name, C.CATEGORY_NAME_1)

    @patch("services.category_service.is_admin")
    def test_create_no_permission(self, mock_is_admin):
        mock_is_admin.return_value = False

        token = C.TOKEN
        created_category = cat_service.create(token, self.sample_category)

        self.assertIsNone(created_category)
        mock_is_admin.assert_called_once_with(token)


class TestDelete_Should(TestCase):
    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_delete_success(self, mock_update_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_update_query.return_value = 1

        token = C.TOKEN
        category_id = C.CATEGORY_ID_1
        result = cat_service.delete(token, category_id)

        self.assertTrue(result)
        mock_is_admin.assert_called_once_with(token)

    @patch("services.category_service.is_admin")
    def test_delete_no_permission(self, mock_is_admin):
        mock_is_admin.return_value = False

        token = C.TOKEN
        category_id = C.CATEGORY_ID_1
        result = cat_service.delete(token, category_id)

        self.assertFalse(result)
        mock_is_admin.assert_called_once_with(token)

    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_delete_not_found(self, mock_update_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_update_query.return_value = 0

        token = C.TOKEN
        category_id = C.CATEGORY_ID_1
        result = cat_service.delete(token, category_id)

        self.assertFalse(result)
        mock_is_admin.assert_called_once_with(token)


class TestCategoryUpdate_Should(TestCase):
    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_update_success(self, mock_update_query, mock_is_admin):
        token = C.TOKEN
        category_id = C.CATEGORY_ID_1
        category = Category(id=category_id, name="Updated Category")
        mock_is_admin.return_value = True
        mock_update_query.return_value = 1

        result = cat_service.update(token, category_id, category)

        self.assertEqual(result, UpdateStatus.SUCCESS)
        mock_is_admin.assert_called_once_with(token)


class TestCategoryLock_Should(TestCase):
    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_lock_success(self, mock_update_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_update_query.return_value = 1

        result = cat_service.lock(C.TOKEN, C.CATEGORY_ID_1)
        self.assertEqual(result, UpdateStatus.SUCCESS)

    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_lock_not_found(self, mock_update_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_update_query.return_value = 0

        result = cat_service.lock(C.TOKEN, C.INVALID_CATEGORY_ID)
        self.assertEqual(result, UpdateStatus.NOT_FOUND)

    @patch("services.category_service.is_admin")
    def test_lock_not_admin(self, mock_is_admin):
        mock_is_admin.return_value = False

        result = cat_service.lock(C.TOKEN, C.CATEGORY_ID_1)
        self.assertIsNone(result)


class TestUnlockCategory_Should(TestCase):
    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_unlock_success(self, mock_update_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_update_query.return_value = 1

        result = cat_service.unlock(C.TOKEN, C.CATEGORY_ID_1)
        self.assertEqual(result, UpdateStatus.SUCCESS)

    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_unlock_not_found(self, mock_update_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_update_query.return_value = 0

        result = cat_service.unlock(C.TOKEN, C.INVALID_CATEGORY_ID)
        self.assertEqual(result, UpdateStatus.NOT_FOUND)

    @patch("services.category_service.is_admin")
    def test_unlock_not_admin(self, mock_is_admin):
        mock_is_admin.return_value = False

        result = cat_service.unlock(C.TOKEN, C.CATEGORY_ID_1)
        self.assertIsNone(result)


class TestMakePrivateCategory_Should(TestCase):
    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_make_private_success(self, mock_update_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_update_query.return_value = 1

        result = cat_service.make_private(C.TOKEN, C.CATEGORY_ID_1)
        self.assertEqual(result, UpdateStatus.SUCCESS)

    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_make_private_not_found(self, mock_update_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_update_query.return_value = 0

        result = cat_service.make_private(C.TOKEN, C.INVALID_CATEGORY_ID)
        self.assertEqual(result, UpdateStatus.NOT_FOUND)

    @patch("services.category_service.is_admin")
    def test_make_private_not_admin(self, mock_is_admin):
        mock_is_admin.return_value = False

        result = cat_service.make_private(C.TOKEN, C.CATEGORY_ID_1)
        self.assertIsNone(result)


class TestMakeNonPrivateCategory_Should(TestCase):
    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_make_non_private_success(self, mock_update_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_update_query.return_value = 1

        result = cat_service.make_non_private(C.TOKEN, C.CATEGORY_ID_1)
        self.assertEqual(result, UpdateStatus.SUCCESS)

    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_make_non_private_not_found(self, mock_update_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_update_query.return_value = 0

        result = cat_service.make_non_private(C.TOKEN, C.INVALID_CATEGORY_ID)
        self.assertEqual(result, UpdateStatus.NOT_FOUND)

    @patch("services.category_service.is_admin")
    def test_make_non_private_not_admin(self, mock_is_admin):
        mock_is_admin.return_value = False

        result = cat_service.make_non_private(C.TOKEN, C.CATEGORY_ID_1)
        self.assertIsNone(result)


class TestViewPrivilegedUsers_Should(TestCase):
    @patch("services.category_service.is_admin")
    @patch("services.category_service.read_query")
    def test_view_privileged_users_no_users(self, mock_read_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_read_query.return_value = []

        result = cat_service.view_privileged_users(C.TOKEN, C.CATEGORY_ID_1)
        self.assertEqual(len(result), 0)

    @patch("services.category_service.is_admin")
    def test_view_privileged_users_not_admin(self, mock_is_admin):
        mock_is_admin.return_value = False

        result = cat_service.view_privileged_users(C.TOKEN, C.CATEGORY_ID_1)
        self.assertIsNone(result)


class TestAddUserAsPrivateMember_Should(TestCase):
    @patch("services.category_service.exists_by_id")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    @patch("services.category_service.read_query")
    @patch("services.category_service.insert_query")
    def test_add_user_as_private_member_success(self, mock_insert_query, mock_read_query, mock_is_admin,
                                                mock_category_exists, mock_exists_by_id):
        mock_is_admin.return_value = True
        mock_category_exists.return_value = True
        mock_exists_by_id.return_value = True
        mock_read_query.return_value = []

        result = cat_service.add_user_as_private_member(C.TOKEN, C.CATEGORY_ID_1, C.USER_ID_1)
        self.assertEqual(result, UpdateStatus.SUCCESS)

    @patch("services.category_service.exists_by_id")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    @patch("services.category_service.read_query")
    def test_add_user_as_private_member_duplicate_entry(self, mock_read_query, mock_is_admin,
                                                        mock_category_exists, mock_exists_by_id):
        mock_is_admin.return_value = True
        mock_category_exists.return_value = True
        mock_exists_by_id.return_value = True
        mock_read_query.return_value = [(C.USER_ID_1, C.CATEGORY_ID_1, 1)]

        result = cat_service.add_user_as_private_member(C.TOKEN, C.CATEGORY_ID_1, C.USER_ID_1)
        self.assertEqual(result, UpdateStatus.DUPLICATE_ENTRY)

    @patch("services.category_service.exists_by_id")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    def test_add_user_as_private_member_not_found(self, mock_is_admin, mock_category_exists, mock_exists_by_id):
        mock_is_admin.return_value = True
        mock_category_exists.return_value = False
        mock_exists_by_id.return_value = True

        result = cat_service.add_user_as_private_member(C.TOKEN, C.CATEGORY_ID_1, C.USER_ID_1)
        self.assertEqual(result, UpdateStatus.NOT_FOUND)

    @patch("services.category_service.exists_by_id")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    def test_add_user_as_private_member_admin_required(self, mock_is_admin, mock_category_exists, mock_exists_by_id):
        mock_is_admin.return_value = False
        mock_category_exists.return_value = True
        mock_exists_by_id.return_value = True

        result = cat_service.add_user_as_private_member(C.TOKEN, C.CATEGORY_ID_1, C.USER_ID_1)
        self.assertEqual(result, UpdateStatus.ADMIN_REQUIRED)


class TestRemoveUserAsPrivateMember_Should(TestCase):
    @patch("services.category_service.exists_by_id")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_remove_user_as_private_member_success(self, mock_update_query, mock_is_admin,
                                                   mock_category_exists, mock_exists_by_id):
        mock_is_admin.return_value = True
        mock_category_exists.return_value = True
        mock_exists_by_id.return_value = True
        mock_update_query.return_value = 1

        result = cat_service.remove_user_as_private_member(C.TOKEN, C.CATEGORY_ID_1, C.USER_ID_1)
        self.assertEqual(result, UpdateStatus.SUCCESS)

    @patch("services.category_service.exists_by_id")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    @patch("services.category_service.update_query")
    def test_remove_user_as_private_member_not_found(self, mock_update_query, mock_is_admin,
                                                     mock_category_exists, mock_exists_by_id):
        mock_is_admin.return_value = True
        mock_category_exists.return_value = True
        mock_exists_by_id.return_value = True
        mock_update_query.return_value = 0

        result = cat_service.remove_user_as_private_member(C.TOKEN, C.CATEGORY_ID_1, C.USER_ID_1)
        self.assertEqual(result, UpdateStatus.NOT_FOUND)

    @patch("services.category_service.exists_by_id")
    @patch("services.category_service.category_exists")
    @patch("services.category_service.is_admin")
    def test_remove_user_as_private_member_admin_required(self, mock_is_admin, mock_category_exists, mock_exists_by_id):
        mock_is_admin.return_value = False
        mock_category_exists.return_value = True
        mock_exists_by_id.return_value = True

        result = cat_service.remove_user_as_private_member(C.TOKEN, C.CATEGORY_ID_1, C.USER_ID_1)
        self.assertEqual(result, UpdateStatus.ADMIN_REQUIRED)
