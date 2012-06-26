from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from poleworkx.shopcontent import MessageFactory as _


# Interface class; used to define content-type schema.

class IShopFolder(form.Schema, IImageScaleTraversable):
    """
    A sfolderish shop type
    """


class ShopFolder(dexterity.Container):
    grok.implements(IShopFolder)


class View(grok.View):
    grok.context(IShopFolder)
    grok.require('zope2.View')
    grok.name('view')
