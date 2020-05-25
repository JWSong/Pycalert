import time
import datetime
import simpleaudio as sa

from gql_query_builder import GqlQuery
from .client import Class101Client


class Alerter:
    def __init__(self, account, pwd):
        self.cc = Class101Client(account, pwd)
        self.alert_sound = sa.WaveObject.from_wave_file('./pycalert/alert.wav')

    def run(self):
        frag_attachment_file = GqlQuery().fields(['fileID', 'fileName', 'extension', '__typename']) \
            .fragment('AttachmentFile', 'PostAttachFile').generate()
        field_files = GqlQuery().fields(['...AttachmentFile', '__typename'], name='files').generate()
        field_user = GqlQuery().fields(['_id', 'name', 'nickName'], name='user').generate()
        frag_comment = GqlQuery().fields([
            '_id', 'content', 'createdAt', 'likedCount', 'missionId', 'photoUrl', 'videoUUID',
            'audioUUID', 'type', 'klassId', 'languageCode', field_files, field_user
        ]).fragment('PostCommentStackedList', 'Post').generate()

        query = GqlQuery().fields(
            ['...PostCommentStackedList']
        ).query(
            'klassPostsForCreator',
            alias='posts',
            input={"isAnswered": "$isAnswered", "klassId": "$klassId", "offset": "$offset", "limit": "$limit"}
        ).operation(
            'query', name='PostManagementListViewModelKlassPost',
            input={"$isAnswered": "Boolean!", "$klassId": "ID!", "$offset": "Int!", "$limit": "Int!"}
        ).generate()

        full_query = '\n'.join([query, frag_comment, frag_attachment_file])
        query_json = {
            "operationName": "PostManagementListViewModelKlassPost",
            "variables": {
                "isAnswered": False,
                "limit": 10,
                "offset": 0,
                "klassId": "5e2556a44ba7b950bbd46bb4"
            },
            "query": full_query
        }

        last_post_time = ''
        is_first = True
        temp_post = None

        res = self.cc.data_query(query_json).json()
        for reversed_post in reversed(res['data']['posts']):
            timestamp = datetime.datetime.strptime(reversed_post['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
            print(f"[{timestamp}] {reversed_post['user']['name']}: {reversed_post['content']}")
            last_post_time = reversed_post['createdAt']
        print('-'*20)
        while True:
            res = self.cc.data_query(query_json).json()
            for post in res['data']['posts']:
                if last_post_time < post['createdAt']:
                    timestamp = datetime.datetime.strptime(post['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    print(f"[{timestamp}] {post['user']['name']}: {post['content']}")
                    self.alert_sound.play().wait_done()

                    if is_first:
                        temp_post = post
                        is_first = False
                else:
                    if temp_post:
                        last_post_time = temp_post['createdAt']
                    temp_post = None
                    is_first = True
                    break
            time.sleep(3)
