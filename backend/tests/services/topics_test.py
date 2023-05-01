from datetime import date
from unittest import TestCase
from unittest.mock import patch
from services.validations import UpdateStatus
import tests.constants as C
from services.topic_service import get_all, delete, update, lock, unlock, set_best_reply
from schemas.topic import TopicsTimeStamps, TopicWithContent, TopicBestReply
from asyncio import run


class TestGetAll_Should(TestCase):

    @patch('services.topic_service.read_query')
    def test_get_all(self, mock_read_query):
        async def async_test():
            # Arrange
            mock_read_query.return_value = [
                (1, 'topic1', date(2023, 1, 1), date(2023, 1, 2)),
                (2, 'topic2', date(2023, 2, 1), date(2023, 2, 2)),
            ]

            # Act
            result = await get_all()

            # Assert
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], TopicsTimeStamps)
            self.assertEqual(result[0].id, 1)
            self.assertEqual(result[0].title, 'topic1')
            self.assertEqual(result[0].created_at, date(2023, 1, 1))
            self.assertEqual(result[0].updated_at, date(2023, 1, 2))

            self.assertIsInstance(result[1], TopicsTimeStamps)
            self.assertEqual(result[1].id, 2)
            self.assertEqual(result[1].title, 'topic2')
            self.assertEqual(result[1].created_at, date(2023, 2, 1))
            self.assertEqual(result[1].updated_at, date(2023, 2, 2))

            mock_read_query.assert_called_once_with("SELECT id, title, created_at, updated_at from topics")
            run(async_test())


class TestDelete_Should(TestCase):
    @patch('services.topic_service.topic_exists', return_value=True)
    @patch('services.topic_service.get_current_user', return_value=C.USER_ID_1)
    @patch('services.topic_service.update_query')
    def test_delete_success(self, mock_update_query, mock_get_current_user, mock_topic_exists):
        async def async_test():
            result = await delete(C.TOKEN, C.TOPIC_ID_1)
            self.assertEqual(result, UpdateStatus.SUCCESS)
            mock_update_query.assert_called_once_with("DELETE FROM topics WHERE id = ?", (C.TOPIC_ID_1,))
            run(async_test())

    @patch('services.topic_service.topic_exists', return_value=False)
    def test_delete_not_found(self, mock_topic_exists):
        async def async_test():
            result = await delete(C.TOKEN, C.TOPIC_ID_1)
            self.assertEqual(result, UpdateStatus.NOT_FOUND)
            run(async_test())

    @patch('services.topic_service.topic_exists', return_value=True)
    @patch('services.topic_service.get_current_user', return_value=None)
    @patch('services.topic_service.is_admin', return_value=False)
    def test_delete_bad_request(self, mock_is_admin, mock_get_current_user, mock_topic_exists):
        async def async_test():
            result = await delete(C.TOKEN, C.TOPIC_ID_1)
            self.assertEqual(result, UpdateStatus.BAD_REQUEST)
            run(async_test())

    @patch('services.topic_service.topic_exists', return_value=True)
    @patch('services.topic_service.get_current_user', return_value=None)
    @patch('services.topic_service.is_admin', return_value=True)
    @patch('services.topic_service.update_query')
    def test_delete_success_admin(self, mock_update_query, mock_is_admin, mock_get_current_user,
                                        mock_topic_exists):
        async def async_test():
            result = await delete(C.TOKEN, C.TOPIC_ID_1)
            self.assertEqual(result, UpdateStatus.SUCCESS)
            mock_update_query.assert_called_once_with("DELETE FROM topics WHERE id = ?", (C.TOPIC_ID_1,))
            run(async_test())


class TestUpdate_Should(TestCase):
    @patch('services.topic_service.get_current_user', return_value=C.USER_ID_1)
    @patch('services.topic_service.update_query', return_value=1)
    def test_update_success(self, mock_update_query, mock_get_current_user):
        async def async_test():
            topic = TopicWithContent(id=None, title=C.TOPIC_TITLE, content=C.TOPIC_CONTENT)
            result = await update(C.TOKEN, C.TOPIC_ID_1, topic)
            self.assertEqual(result, UpdateStatus.SUCCESS)
            mock_update_query.assert_called_once_with(
                "UPDATE topics SET title = ?, content = ? WHERE id = ? AND user_id = ?",
                (C.TOPIC_TITLE, C.TOPIC_CONTENT, C.TOPIC_ID_1, C.USER_ID_1))
            run(async_test())

    @patch('services.topic_service.get_current_user', return_value=C.USER_ID_1)
    @patch('services.topic_service.update_query', return_value=0)
    def test_update_not_found(self, mock_update_query, mock_get_current_user):
        async def async_test():
            topic = TopicWithContent(id=None, title=C.TOPIC_TITLE, content=C.TOPIC_CONTENT)
            result = await update(C.TOKEN, C.TOPIC_ID_1, topic)
            self.assertEqual(result, UpdateStatus.NOT_FOUND)
            run(async_test())


class TestLock_Should(TestCase):
    @patch('services.topic_service.is_admin', return_value=True)
    @patch('services.topic_service.update_query', return_value=1)
    def test_lock_success(self, mock_update_query, mock_is_admin):
        async def async_test():
            result = await lock(C.TOKEN, C.TOPIC_ID_1)
            self.assertEqual(result, UpdateStatus.SUCCESS)
            mock_update_query.assert_called_once_with("UPDATE topics SET locked = 1 WHERE id = ?", (C.TOPIC_ID_1,))
            run(async_test())

    @patch('services.topic_service.is_admin', return_value=True)
    @patch('services.topic_service.update_query', return_value=0)
    def test_lock_not_found(self, mock_update_query, mock_is_admin):
        async def async_test():
            result = await lock(C.TOKEN, C.TOPIC_ID_1)
            self.assertEqual(result, UpdateStatus.NOT_FOUND)
            run(async_test())

    @patch('services.topic_service.is_admin', return_value=False)
    def test_lock_not_admin(self, mock_is_admin):
        async def async_test():
            result = await lock(C.TOKEN, C.TOPIC_ID_1)
            self.assertIsNone(result)
            run(async_test())

    @patch('services.topic_service.is_admin', return_value=True)
    @patch('services.topic_service.update_query', return_value=1)
    def test_unlock_success(self, mock_update_query, mock_is_admin):
        async def async_test():
            result = await unlock(C.TOKEN, C.TOPIC_ID_1)
            self.assertEqual(result, UpdateStatus.SUCCESS)
            mock_update_query.assert_called_once_with("UPDATE topics SET locked = 0 WHERE id = ?", (C.TOPIC_ID_1,))
            run(async_test())

    @patch('services.topic_service.is_admin', return_value=True)
    @patch('services.topic_service.update_query', return_value=0)
    def test_unlock_not_found(self, mock_update_query, mock_is_admin):
        async def async_test():
            result = await unlock(C.TOKEN, C.TOPIC_ID_1)
            self.assertEqual(result, UpdateStatus.NOT_FOUND)
            run(async_test())

    @patch('services.topic_service.is_admin', return_value=False)
    def test_unlock_not_admin(self, mock_is_admin):
        async def async_test():
            result = await unlock(C.TOKEN, C.TOPIC_ID_1)
            self.assertIsNone(result)
            run(async_test())


class TestBestReply_Should(TestCase):
    def setUp(self):
        async def async_test():
            self.topic_best_reply = TopicBestReply(best_reply_id=C.BEST_REPLY_ID)
            run(async_test())

    @patch('services.topic_service.get_current_user', return_value=C.USER_ID_1)
    @patch('services.topic_service.update_query', return_value=0)
    @patch('services.topic_service.exists_by_id', return_value=False)
    def test_set_best_reply_not_found(self, mock_exists_by_id, mock_update_query, mock_get_current_user):
        async def async_test():
            result = await set_best_reply(C.TOKEN, C.TOPIC_ID_1, self.topic_best_reply)
            self.assertEqual(result, UpdateStatus.NOT_FOUND)
            run(async_test())

    @patch('services.topic_service.get_current_user', return_value=C.USER_ID_1)
    @patch('services.topic_service.update_query', return_value=0)
    @patch('services.topic_service.exists_by_id', return_value=True)
    def test_set_best_reply_no_permission(self, mock_exists_by_id, mock_update_query, mock_get_current_user):
        async def async_test():
            result = await set_best_reply(C.TOKEN, C.TOPIC_ID_1, self.topic_best_reply)
            self.assertEqual(result, UpdateStatus.NOT_FOUND)
            run(async_test())

    @patch('services.topic_service.get_current_user', return_value=C.USER_ID_1)
    @patch('services.topic_service.update_query', return_value=1)
    @patch('services.topic_service.exists_by_id', return_value=True)
    def test_set_best_reply_success(self, mock_exists_by_id, mock_update_query, mock_get_current_user):
        async def async_test():
            result = await set_best_reply(C.TOKEN, C.TOPIC_ID_1, self.topic_best_reply)
            self.assertEqual(result, UpdateStatus.SUCCESS)
            run(async_test())
