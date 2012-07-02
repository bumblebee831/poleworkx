from five import grok
from Acquisition import aq_inner
from AccessControl import Unauthorized
from plone.directives import dexterity, form

from zope import schema
from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText

from Products.statusmessages.interfaces import IStatusMessage
from plone.uuid.interfaces import IUUID

from kk.shopified.interfaces import ICartUpdaterUtility

from poleworkx.shopcontent import MessageFactory as _


# Interface class; used to define content-type schema.

class IProduct(form.Schema, IImageScaleTraversable):
    """
    A simple product type
    """
    productcode = schema.TextLine(
        title=_(u"Article ID"),
        description=_(u"Please enter a unique article id / product code that "
                      u"will be passed to the payment processor"),
        required=True,
    )
    image = NamedBlobImage(
        title=_(u"Main Product Image"),
        description=_(u"Upload main produt image to be displayed in product "
                      u"listings and search result"),
        required=True,
    )
    text = RichText(
        title=_(u"Product Information"),
        required=True,
    )


class Product(dexterity.Container):
    grok.implements(IProduct)


class View(grok.View):
    grok.context(IProduct)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        context = aq_inner(self.context)
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            updater = getUtility(ICartUpdaterUtility)
            uuid = IUUID(context, None)
            quantity = self.request.get('quantity', '1')
            item = updater.add(uuid, quantity)
            if not item:
                IStatusMessage(self.request).addStatusMessage(
                    _(u"Item could not be added to the shopping cart. "
                      u"Please try again. If the error should persist, please "
                      u"contact the shop owner"),
                    type="error")
                return self.request.response.redirect(context.absolute_url())
            else:
                IStatusMessage(self.request).addStatusMessage(
                    _(u"Item has been added to the shopping cart"),
                    type="info")
                return_url = context.absolute_url() + '/@@cart'
                return self.request.response.redirect(return_url)
