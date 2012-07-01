import math
from five import grok
from zope import schema
from Acquisition import aq_inner

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from Products.CMFCore.utils import getToolByName
from plone.app.contentlisting.interfaces import IContentListing

from poleworkx.shopcontent.productcategory import IProductCategory
from poleworkx.shopcontent.product import IProduct

from poleworkx.shopcontent import MessageFactory as _


# Interface class; used to define content-type schema.

class IShopFolder(form.Schema):
    """
    A sfolderish shop type
    """
    headline = schema.TextLine(
        title=_(u"Headline"),
        description=_(u"Enter optional headline for the shop landing page "),
        required=False,
    )
    text = RichText(
        title=_(u"Main Text"),
        description=_(u"Enter an optional welcome text for this shop"),
        required=False,
    )
    featuredProducts = RelationList(
        title=_(u"Featured Products"),
        description=_(u"Optional selection for featured products These "
                      u"items will be presented above the product listing"),
        default=[],
        value_type=RelationChoice(
            title=_(u"Product"),
            source=ObjPathSourceBinder(object_provides=IProduct.__identifier__)
            ),
        required=False,
    )


class ShopFolder(dexterity.Container):
    grok.implements(IShopFolder)


class View(grok.View):
    grok.context(IShopFolder)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_categories = len(self.categories()) > 0
        self.has_products = len(self.products()) > 0

    def listing_matrix(self):
        if self.has_products:
            items = self.products()
        else:
            items = self.categories()
        matrix = self._build_matrix(items)
        return matrix

    def categories(self):
        query = self._base_query()
        obj_provides = IProductCategory.__identifier__
        query['object_provides'] = obj_provides
        results = self._get_data(query)
        return results

    def products(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IProduct.__identifier__,
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1),
                          sort_on='getObjPositionInParent',
                          review_state='published')
        resultlist = IContentListing(results)
        return resultlist

    def _base_query(self):
        context = aq_inner(self.context)
        path = '/'.join(context.getPhysicalPath())
        return dict(path={'query': path, 'depth': 1},
                    sort_on='getObjPositionInParent',
                    review_state='published')

    def _get_data(self, query):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(**query)
        return IContentListing(results)

    def _build_matrix(self, items):
        """ Contruct a row/cell matrix that returns all items
            in a nice grid containing 3 items each.
        """
        count = len(items)
        rowcount = count / 2.0
        rows = math.ceil(rowcount)
        matrix = []
        for i in range(int(rows)):
            row = []
            for j in range(2):
                index = 2 * i + j
                if index <= int(count - 1):
                    cell = {}
                    cell['item'] = items[index]
                    row.append(cell)
            matrix.append(row)
        return matrix
