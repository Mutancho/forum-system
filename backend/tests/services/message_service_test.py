import datetime
import unittest
from unittest.mock import Mock, create_autospec, patch
from schemas.message import Message
from schemas.user import User,DisplayUser

from services import message_service

class UserService_Should(unittest.TestCase):
    def setUp(self) -> None:
        pass
    @patch('services.message_service.insert_query', autospec=True)
    def test_create_returnsCreatedMessage(self,mock_insert_query):
        test_message = Message(id=None, content='I said testt', created_at=None, sender_id=1, reciever_id=2)
        with patch('services.message_service.read_query') as mock_read_query:
            mock_insert_query.return_value = 1
            mock_read_query.return_value = [('2023-04-14',)]

            result = message_service.create(test_message)
            self.assertEqual(1,result.id)
            self.assertEqual(('2023-04-14',),result.created_at)

    @patch('services.message_service.read_query', autospec=True)
    def test_getAllMyConversations_returnsListOfDisplayUser(self, mock_read_query):
        message_service.oauth2.get_current_user = lambda token: 1
        mock_read_query.side_effect = [[(1,),(1,)],[(2,),(2,)],[(1, 'username1', 'email@us1.com','password1', 'user', datetime.datetime.strptime('04/14/2023, 13:58:43',"%m/%d/%Y, %H:%M:%S")),
                                                                (2, 'username2', 'email@us2.com','password2','user', datetime.datetime.strptime('04/14/2023, 14:30:43',"%m/%d/%Y, %H:%M:%S"))]]

        result = message_service.get_all_my_conversations('token')
        expected = [DisplayUser(id=1, username='username1', email='email@us1.com'),
                    DisplayUser(id=2, username='username2', email='email@us2.com')]
        self.assertEqual(expected,list(result))

    @patch('services.message_service.read_query', autospec=True)
    def test_getAllMyConversationsWith_returnsDictOfMessages(self, mock_read_query):
        message_service.oauth2.get_current_user = lambda token: 1
        mock_read_query.return_value = [(1,'my message',datetime.datetime.strptime('04/14/2023, 13:58:43',"%m/%d/%Y, %H:%M:%S"),2),
                                        (2,'his message',datetime.datetime.strptime('04/14/2023, 13:59:43',"%m/%d/%Y, %H:%M:%S"),1),
                                        (1,'my message',datetime.datetime.strptime('04/14/2023, 14:58:43',"%m/%d/%Y, %H:%M:%S"),2)]


        result = message_service.get_all_my_conversations_with('token',2)
        expected = {'04/14/2023, 13:58:43': 'my message',
                    '04/14/2023, 13:59:43': '         his message',
                    '04/14/2023, 14:58:43': 'my message'}

        self.assertEqual(expected,result)











