from zope.interface import Interface


class IAddOnInstalled(Interface):
    """A layer specific for this add-on product.

    This interface is referred in browserlayers.xml.

    All views and viewlets register against this layer will appear on your Plone site
    only 
    """