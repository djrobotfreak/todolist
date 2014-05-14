import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import json
from google.appengine.ext import ndb
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


class listItem:
    id = 0

    def __init__(self, title):
        self.title = title
        self.id = listItem.id
        listItem.id += 1


ITEMLIST = [listItem('take out the trash'), listItem('buy groceries')]


def itemListToJSON():
    itemlist = []
    for item in ITEMLIST:
        d = collections.OrderedDict()
        d['title'] = item.title
        d['id'] = item.id
        itemlist.append(d)
    return json.dumps(itemlist)


@endpoints.api(name='todolist', version='v1',allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class RESTApi(remote.Service):
    @endpoints.method(message_types.VoidMessage, Response, path='getlist', http_method='GET', name='listItem.getList')
    def greeting_get(self, request):
        try:
            return Response(message=itemListToJSON())
        except:
            return Response(message='Error with stupid json')

    ADD_ITEM = endpoints.ResourceContainer(Response)

    @endpoints.method(ADD_ITEM, Response,path='addItem', http_method='POST', name='listItem.addItem')
    def add_item(self, request):
        item = listItem(request.message)
        ITEMLIST.append(item)
        return Response(message=itemListToJSON())

    ID_RESOURCE = endpoints.ResourceContainer(message_types.VoidMessage, id=messages.IntegerField(1,
                                              variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Response, path='removeItem/{id}', http_method='DELETE', name='listItem.removeItem')
    def remove_item(self, request):
        for item in ITEMLIST:
            if item.id == request.id:
                ITEMLIST.remove(item)
                break
        return Response(message=itemListToJSON())


APPLICATION = endpoints.api_server([RESTApi])
