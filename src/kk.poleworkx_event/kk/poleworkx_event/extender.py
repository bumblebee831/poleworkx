# -*- coding: utf-8 -*-
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender, IOrderableSchemaExtender, IBrowserLayerAwareExtender
from Products.Archetypes.public import ReferenceField, BooleanField, TextField, BooleanWidget, TextAreaWidget, StringField, SelectionWidget, RichWidget, StringWidget
from Products.ATContentTypes.interface import IATEvent
from archetypes.schemaextender.field import ExtensionField
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
                                         ReferenceBrowserWidget
from kk.poleworkx_event.interfaces import IAddOnInstalled
     
class CourseBlockField(ExtensionField, BooleanField):
    """ course block """
    
    def getCourseBock(self, instance):
        return instance.Schema().getField('courseblock').get(instance)
         
class CourseBlockDetailsField(ExtensionField, TextField):
    """ course block details"""

class TotalSeatsField(ExtensionField, StringField):
    """ total seats"""  
    def getValue(self, instance):
        return instance.Schema().getField('totalseats').get(instance)
class BookedSeatsField(ExtensionField, StringField):
    """ total seats""" 
    def getValue(self, instance):
        return instance.Schema().getField('bookedseats').get(instance)
class PriceField(ExtensionField, StringField)   :
    """ price """
    def getValue(self, instance):
        return instance.Schema().getField('price').get(instance) 
class DiscountedPriceField(ExtensionField, StringField)   :
    """ discounted price """
    def getValue(self, instance):
        return instance.Schema().getField('discountedprice').get(instance)  
class AvaliableField(ExtensionField, BooleanField)   :
    """ is registration avaliable """ 
    def getValue(self, instance):
        return instance.Schema().getField('avaliable').get(instance)      
class EventExtender(object):
    adapts(IATEvent)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = IAddOnInstalled
    fields = [
       CourseBlockField("courseblock",
       		languageIndependent = True,
			default = 0, 
       		widget = BooleanWidget( label="Kursblock")
       	),
       CourseBlockDetailsField("courseblockdetails",
       		languageIndependent = False,
       		default_output_type = 'text/x-html-safe',

       		widget = RichWidget( label="Kursblock details" )
       	), 
       	TotalSeatsField("totalseats", 
       		languageIndependent = True,
       		widget = StringWidget(label = "Teilnehmeranzahl max."),),
       	BookedSeatsField("bookedseats", 
       		languageIndependent = True,
       		widget = StringWidget(label = "Freie Plätze"),),   
       	PriceField("price", 
       		languageIndependent = True,
       		widget = StringWidget(label = "Preis"),),    
        DiscountedPriceField("discountedprice", 
       		languageIndependent = True,
       		widget = StringWidget(label = "Preis discount"),),      
        AvaliableField("avaliable", 
       		languageIndependent = True,
       		default = 0,
       		widget = BooleanWidget(label = "Anmeldung"), ),         		    		      
       ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields 
    def getOrder(self, schematas):
        schematas['default'] = ['id', 'title', 'description', 'courseblock', 'courseblockdetails', 'location', 'startDate', 'endDate', 'totalseats', 'bookedseats', 'price', 'discountedprice', 'avaliable', 'text', 'attendees', 'eventUrl', 'contactName', 'contactEmail', 'contactPhone']
        return schematas
