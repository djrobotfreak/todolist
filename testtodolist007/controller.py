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

class RESTfulPart(remote.Service):
    @endpoints.method(message_types.VoidMessage, Response,
                     path='getlist', http_method='GET',
                     name='listItem.getList')
    def greeting_get(self, request):
       try:
           return listItem.query();
       except (IndexError, TypeError):
           raise endpoints.NotFoundException('coudnt query correctly' %
                                             (request.id,))

    """@endpoints.method(message_types.VoidMessage, Response,
                  path='hellogreeting/{times}', http_method='POST',
                  name='listItem.addItem')
    def greetings_multiply(self, request):
        newListItem = listItem(title = request.message, checked=false)
        return Response(message=request.message)"""
"""


class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
    Greeting(message='Derek says howdy'),
    Greeting(message ='Hi Jake... Meow'),
])


@endpoints.api(name='helloworld', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class HelloWorldApi(remote.Service):
    """Helloworld API v1."""

    MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
            Greeting,
            times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                        required=True))

    @endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
                      path='hellogreeting/{times}', http_method='POST',
                      name='greetings.multiply')
    def greetings_multiply(self, request):
        return Greeting(message=request.message * request.times)

    @endpoints.method(message_types.VoidMessage, Greeting,
                      path='derekgreeting', http_method='GET',
                      name='greetings.howdyDerek')
    def greetings_derek(self, request):
        return Greeting(message='howdy derek')

    @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      path='hellogreeting', http_method='GET',
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        return STORED_GREETINGS

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Greeting,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        try:
            return STORED_GREETINGS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))

    @endpoints.method(message_types.VoidMessage, Greeting,
                      path='hellogreeting/authed', http_method='POST',
                      name='greetings.authed')
    def greeting_authed(self, request):
        current_user = endpoints.get_current_user()
        email = (current_user.email() if current_user is not None
                 else 'Anonymous')
        return Greeting(message='hello %s' % (email,))
