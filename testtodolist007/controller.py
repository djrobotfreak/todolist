import endpoints
import logging
import datetime
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import json
from google.appengine.ext import ndb
import time
from endpoints_proto_datastore.ndb import EndpointsModel
import collections

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'testtodolist007'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


class Response(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)


class ListItem(ndb.Model):
    title = ndb.StringProperty()
    checked = ndb.BooleanProperty(default=False)
    timestamp = ndb.DateTimeProperty(default=datetime.datetime.now())


def itemListToJSON():
    dthandler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, datetime.datetime)
        or isinstance(obj, datetime.date)
        else None)
    logging.error('hey im actually in the freaking function')
    itemlist = ListItem.query().fetch(projection=[ListItem.title, ListItem.checked, ListItem.timestamp])
    printlist = []
    for item in itemlist:
        printlist.append({'id': item.key.urlsafe(), 'title': item.title, 'checked': item.checked,
                          'timestamp': item.timestamp})
    logging.error('I made it')
    logging.error(printlist)
    return json.dumps(printlist, default=dthandler)


@endpoints.api(name='todolist', version='v1', allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class RESTApi(remote.Service):
    @endpoints.method(message_types.VoidMessage, Response, path='getlist', http_method='GET', name='listItem.getList')
    def greeting_get(self, request):
        try:
            return Response(message=itemListToJSON())
        except:
            return Response(message='Error with stupid json')

    ADD_ITEM = endpoints.ResourceContainer(Response)

    @endpoints.method(ADD_ITEM, Response, path='addItem', http_method='POST', name='listItem.addItem')
    def add_item(self, request):
        newitem = ListItem(title=request.message)
        newitem.put()
        return Response(message=newitem.key.urlsafe())

    ID_RESOURCE = endpoints.ResourceContainer(message_types.VoidMessage, id=messages.StringField(1,
                                              variant=messages.Variant.STRING))

    @endpoints.method(ID_RESOURCE, Response, path='checkItem/{id}', http_method='POST', name='listItem.checkItem')
    def check_item(self, request):
        key = ndb.Key(urlsafe=request.id)
        item = key.get()
        if item.checked:
            item.checked = False
        else:
            item.checked = True
        item.put()
        return Response(message='ok')

    @endpoints.method(ID_RESOURCE, Response, path='removeItem/{id}', http_method='DELETE', name='listItem.removeItem')
    def remove_item(self, request):
        try:
            key = ndb.Key(urlsafe=request.id)
            item = key.get()
            item.key.delete()
            return Response(message='ok')
        except:
            return Response(message='error')


APPLICATION = endpoints.api_server([RESTApi])
