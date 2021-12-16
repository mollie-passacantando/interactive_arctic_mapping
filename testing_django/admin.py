from django.contrib import admin
from django.shortcuts import render
from django.http import Http404
from mainapp.models import DataModel

class PageAdmin(admin.ModelAdmin):

    def get_urls(self):
        """
        Add additional view to ModelAdmin urls
        """
        urls = super(PageAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r'^(?P<instance_id>\d+)/view_mpld3_chart/$',
                               self.view_chart, name='view_chart'),
                           )
        return my_urls + urls

    # ==============================
    # Model Admin custom view method
    # ==============================

                                  
admin.site.register(DataModel)  # Register the Model in the AdminSite
