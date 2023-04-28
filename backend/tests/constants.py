from schemas.category import Category

READ_QUERY_RETURN_VALUE_CATEGORY_WITH_TOPICS = [(1, 'TestTopic1'),
                                                (2, 'TestTopic2'),
                                                ]
CATEGORY_EXISTS_RETURN_VALUE = {"id": 1, "name": "TestCategory", "private": False, "locked": False}
CURRENT_USER_ID = 1
CATEGORY_ID_1 = 1
CATEGORY_ID_2 = 2
CATEGORY_1 = Category(id=1, name="Category 1")
CATEGORY_2 = Category(id=2, name="Category 2")
CATEGORY_NAME_1 = "TestCategory"
CATEGORY_NAME_2 = "TestCategory2"
ALL_CATEGORIES = [CATEGORY_1, CATEGORY_2]
INVALID_CATEGORY_ID = 999
PRIVATE_CATEGORY = ((1,),)
NOT_PRIVATE_CATEGORY = ((0,),)
READ_ACCESS_GRANTED = ((1,),)
READ_ACCESS_DENIED = ((0,),)
WRITE_ACCESS_GRANTED = ((1,),)
WRITE_ACCESS_DENIED = ((0,),)

TOKEN = "dummy_token"
TOPIC_ID_1 = 1
TOPIC_NAME_1 = 'TestTopic1'
TOPIC_NAME_2 = 'TestTopic2'
TOPIC_TITLE = 'Test topic'
TOPIC_CONTENT = 'Test topic content'
REPLY_ID_1 = 1
REPLY_CONTENT = 'Test reply content'
REPLY_ID_2 = 2
BEST_REPLY_ID = 1

USER_ID_1 = 1
USER_ID_2 = 1
