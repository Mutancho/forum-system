from datetime import datetime,date
import unittest
from unittest.mock import Mock, create_autospec, patch
from schemas.reply import ReplyWithUserAndTopic, Vote, Reply, UpdateReply
from services import reply_service

class ReplyService_Should(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @patch('services.reply_service.get_votes_for_reply', autospec=True)
    def test_getById_returnsEmptyDictionary_when_dataIsNotPresent(self,mock_get_votes_for_reply):
        with patch('services.reply_service.read_query') as mock_read_query:
            mock_read_query.return_value = []
            mock_get_votes_for_reply.return_value = {'upvote': 0,'downvote': 0}

            result = reply_service.get_by_id(1)
            self.assertEqual({},result)

    @patch('services.reply_service.get_votes_for_reply', autospec=True)
    def test_getById_returnsDictionaryFromReplyWithVotes_when_dataIsPresent(self,mock_get_votes_for_reply):
        with patch('services.reply_service.read_query') as mock_read_query:
            mock_read_query.return_value = [(1,'reply test said',datetime.strptime('04/14/2023, 13:58:43',"%m/%d/%Y, %H:%M:%S"),datetime.strptime('04/14/2023, 13:59:43',"%m/%d/%Y, %H:%M:%S"))]
            mock_get_votes_for_reply.return_value =  {'upvote': 0, 'downvote': 0}

            result = reply_service.get_by_id(1)
            expected = {'content': 'reply test said',
                        'created_at': date(2023,4,14) ,
                        'downvote': 0,
                        'id': 1,
                        'updated_at': date(2023,4,14),
                        'upvote': 0}
            self.assertEqual(expected, result)



    @patch('services.reply_service.insert_query', autospec=True)
    def test_create_returnDictionary(self,mock_insert_query):
        mock_insert_query.return_value = 1
        reply_service.oauth2.get_current_user = lambda token: 1
        test_reply = Reply(content='Test reply')

        result = reply_service.create(test_reply,1,'token')
        expected = {'content': 'Test reply', 'downvote': 0, 'id': 1, 'upvote': 0}
        self.assertEqual(expected,result)

    @patch('services.reply_service.update_query', autospec=False)
    def test_updateReply_returnDictionaryWithUpdatedReply(self, mock_update_query):
        with patch('services.reply_service.read_query') as mock_read_query:
            mock_update_query.return_value = []
            mock_read_query.return_value =[(datetime.strptime('04/14/2023, 13:58:43',"%m/%d/%Y, %H:%M:%S"),)]
            updated_reply = UpdateReply(content='new content')

            result = reply_service.update_reply(1,updated_reply)
            expected ={'content': 'new content','downvote': 0, 'id': 1,
                       'update on': '14-04-2023 13:58:43','upvote': 0}
            self.assertEqual(expected,result)


    def test_replyVote_returnVote(self):
        reply_service.insert_query = Mock()
        reply_service.oauth2.get_current_user = lambda token: 1
        test_vote = Vote(vote='upvote')

        result = reply_service.reply_vote(1,test_vote,'token')
        reply_service.insert_query.assert_called_once()
        self.assertEqual(Vote,type(result))

        reply_service.insert_query.reset_mock()

    def test_updateReplyVote_returnVote(self):
        reply_service.update_query = Mock()
        reply_service.oauth2.get_current_user = lambda token: 1
        test_vote = Vote(vote='upvote')

        result = reply_service.update_reply_vote(1,test_vote,'token')
        reply_service.update_query.assert_called_once()
        self.assertEqual(Vote,type(result))

        reply_service.update_query.reset_mock()

    def test_delete_returnVote(self):
        reply_service.update_query = Mock()

        result = reply_service.delete(1)
        reply_service.update_query.assert_called_once()

        reply_service.update_query.reset_mock()

    @patch('services.reply_service.read_query', autospec=True)
    def test_alreadyVoted_returnTrue_when_dataIsPresent(self,mock_read_query):
        mock_read_query.return_value = [('replyvote data'),]
        reply_service.oauth2.get_current_user = lambda token: 1

        result = reply_service.already_voted(1,'token')
        self.assertEqual(True, result)

    @patch('services.reply_service.read_query', autospec=True)
    def test_alreadyVoted_returnFalse_when_dataIsNotPresent(self, mock_read_query):
        mock_read_query.return_value = []
        reply_service.oauth2.get_current_user = lambda token: 1

        result = reply_service.already_voted(1, 'token')
        self.assertEqual(False, result)



    def test_getVotesForReply_returnDictionaryWithZeros_when_dataIsNotPresent(self):
        with patch('services.reply_service.read_query') as mock_read_query:
            mock_read_query.return_value = []

            result = reply_service.get_votes_for_reply(1)
            expected = {'upvote': 0,'downvote': 0}
            self.assertEqual(expected, result)


    def test_getVotesForReply_returnDictionaryCorrectCount_when_dataIsPresent(self):#
        with patch('services.reply_service.read_query') as mock_read_query:
            mock_read_query.return_value = [('upvote',),('upvote',),('upvote',),('downvote',)]

            result = reply_service.get_votes_for_reply(1)
            expected = {'upvote': 3, 'downvote': 1}
        self.assertEqual(expected,result)

    @patch('services.reply_service.read_query', autospec=True)
    def test_isReplyOwner_returnFalse_when_dataIdIsNotAuthUserId(self, mock_read_query):
        mock_read_query.return_value = [(2,)]
        reply_service.oauth2.get_current_user = lambda token: 1

        result = reply_service.is_reply_owner(1,'token')
        self.assertEqual(False,result)

    @patch('services.reply_service.read_query', autospec=True)
    def test_isReplyOwner_returnTrue_when_dataIdIsAuthUserId(self, mock_read_query):
        mock_read_query.return_value = [(1,)]
        reply_service.oauth2.get_current_user = lambda token: 1

        result = reply_service.is_reply_owner(1, 'token')
        self.assertEqual(True, result)

    @patch('services.reply_service.read_query', autospec=True)
    def test_existsById_returnFalse_when_dataIsNotPresent(self, mock_read_query):
        mock_read_query.return_value = []
        reply_service.oauth2.get_current_user = lambda token: 1

        result = reply_service.exists_by_id(1)
        self.assertEqual(False, result)

    @patch('services.reply_service.read_query', autospec=True)
    def test_existsById_returnTrue_when_dataIsPresent(self, mock_read_query):
        mock_read_query.return_value = [(1,)]
        reply_service.oauth2.get_current_user = lambda token: 1

        result = reply_service.exists_by_id(1)
        self.assertEqual(True, result)


































