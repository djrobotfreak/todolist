import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import json
from google.appengine.ext import ndb

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'testtodolist007'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


class Response(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)

class listItem(ndb.Model):
    title = ndb.StringProperty()
    checked = ndb.BoolProperty()


@endpoints.api(name='todolist', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])

class RESTApi(remote.Service):
    @endpoints.method(message_types.VoidMessage, Response,
                     path='getlist', http_method='GET',
                     name='listItem.getList')
    def greeting_get(self, request):
       try:
           return listItem.query();
       except (IndexError, TypeError):
           raise endpoints.NotFoundException('coudnt query correctly' %
                                             (request.id,))
    @endpoints.method(message_types.VoidMessage, Response,
                      path='derekgreeting', http_method='GET',
                      name='todolist.howdyDerek')
    def greetings_derek(self, request):
        return Response(message='howdy derek')


APPLICATION = endpoints.api_server([RESTApi])
