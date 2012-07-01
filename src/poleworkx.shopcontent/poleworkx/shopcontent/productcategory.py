import math
from five import grok
from Acquisition import aq_inner
from plone.directives import dexterity, form

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText

from Products.CMFCore.utils import getToolByName

from plone.app.contentlisting.interfaces import IContentListing

from poleworkx.shopcontent.product import IProduct

from poleworkx.shopcontent import MessageFactory as _


class IProductCategory(form.Schema, IImageScaleTraversable):
    """
    A folderish product category type
    """
    image = NamedBlobImage(
        title=_(u"Category Image"),
        description=_(u"Upload image usable in the preview of the category"),
        required=True,
    )
    text = RichText(
        title=_(u"Main Text"),
        description=_(u"Enter an optional welcome text for this shop"),
        required=False,
    )


class ProductCategory(dexterity.Container):
    grok.implements(IProductCategory)


class View(grok.View):
    grok.context(IProductCategory)
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
        query = self._base_query()
        obj_provides = IProduct.__identifier__
        query['object_provides'] = obj_provides
        results = self._get_data(query)
        return results

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
            in a nice grid containing 2 items each.
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
