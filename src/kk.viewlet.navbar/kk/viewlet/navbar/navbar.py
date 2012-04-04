from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements, alsoProvides

from Products.CMFPlone import utils
from Acquisition import aq_inner, aq_base, aq_parent

from zope.viewlet.interfaces import IViewlet
from Products.CMFPlone.interfaces import INonStructuralFolder, IBrowserDefault

from zope.app.component.hooks import getSite
from Products.CMFPlone.Portal import PloneSite
from Products.CMFCore.interfaces import ISiteRoot

class NavBarViewlet(ViewletBase):
    implements(IViewlet)

    render = ViewPageTemplateFile('navbar.pt')
    
    navitems = None
    
    def available(self):
        """Returns true or false depending on of the nav has any results
        """
        return len(self.navitems)
    
    def update(self):
        """Needed to use the build-in script for finding the selectedTab.
        This script is the one used by the Portal Tabs. 
        """
        
        self.navitems = self.update_items()
        
        selectable_tabs = []
        for item in self.navitems:
            selectable_tabs.append({'id': item.id,
                                    'url': item.getURL(),
                                    })
        
        selectedTabs = self.context.restrictedTraverse('selectedTabs')
        self.selected_tabs = selectedTabs('default',
                                          self.context,
                                          selectable_tabs)
        self.selected_tab = self.selected_tabs['portal']
        
    # FIXME: @memoize
    def update_items(self):
        """Find the items that are to be part of the navigation. 
        This is basically just a catalog search and then remove the items that are to be 
        excluded from navigation.
        """
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')

        #build query
        query = {}
        query['portal_type'] = utils.typesToList(context)
        # display viewlet only on 4th level and deeper (1st - zope itself, 2nd - plone site, 3d - root lingua plone folders (ru, de, etc.) )
        path = context.getPhysicalPath()
        if len(path)<4:        	
            return []
        else:
            # 4th level container 
            path = path[0:4]


        query['path'] = {'query':"/".join(path), 'depth':1}

        # Make sure the sorting is correct.
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute

            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder

        # Do not include the default pages
        query['is_default_page'] = False
        
        results = catalog.searchResults(query)
        
        # Only add the items that are not excluded from navigation. 
        brains = []
        for result in results:
            if not result.exclude_from_nav:
                brains.append(result)
                    
        return brains
        
