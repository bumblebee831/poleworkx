from plone.indexer.decorator import indexer
from Products.ATContentTypes.interface import IATEvent

@indexer(IATEvent)
def is_event_avaliable(object, **kw):
     return object.Schema()['avaliable'].getValue(object)