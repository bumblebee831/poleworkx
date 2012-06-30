from zope.interface import Interface
from zope.interface import alsoProvides
from zope import schema
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider

from poleworkx.shopcontent import MessageFactory as _


class IBuyable(Interface):
    """A general interface to mark content as buyable """


class IBuyableInformation(form.Schema):
    """
       Marker/Form interface for Recipients
    """
    form.fieldset(
        'buyable',
        label=u"Buyable Details",
        fields=['price', 'sales_price', 'sales_info', 'packaging'
                'weight'],
    )
    price = schema.Float(
        title=_(u"Price"),
        required=True,
    )
    sales_price = schema.Float(
        title=_(u"Sales Price"),
        description=_(u"Add sales or special offer price. This will override "
                      u"the actual price which will display lined-through"),
        required=False,
    )
    sales_info = schema.Text(
        title=_(u"Special Offer Details"),
        description=_(u"Include optional marketing- or infotext describing "
                      u"the sales price, e.g. valid through date"),
        required=False,
    )
    packaging = schema.TextLine(
        title=_(u"Packaging"),
        description=_(u"Specify packaging details, e.g. sizes"),
        required=False,
    )
    weight = schema.TextLine(
        title=_(u"Weight"),
        description=-(u"Enter weight information to warn for potential higher "
                      u"shipping costs."),
        required=False,
    )


alsoProvides(IBuyableInformation, IFormFieldProvider)
