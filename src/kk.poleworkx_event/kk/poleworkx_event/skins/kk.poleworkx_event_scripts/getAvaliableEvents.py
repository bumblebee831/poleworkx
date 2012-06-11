# Example code:

# Import a standard function, and get the HTML request and response objects.
events = context.portal_catalog(portal_type="Event", event_avaliable=True, sort_on="sortable_title")
toLocalizedTime = context.restrictedTraverse("@@plone").toLocalizedTime
options = []
for event in events:
    obj = event.getObject()
    option = "%s | %s - %s | %s " % (unicode(event.Title, 'utf-8'), toLocalizedTime(event.start, long_format=1), toLocalizedTime(event.end, long_format=1), unicode(obj.getLocation(), 'utf-8'))
    options.append((event.UID, option))
return options