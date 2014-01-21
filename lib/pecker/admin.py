from django.contrib import admin
from django.db.models  import  get_app,get_models

from models import *

for model in get_models( get_app("pecker")) :  
    if model.__name__ in ['Link','LinkResult',]:    
        continue
    admin_class = type( "%sAdmin" % model.__name__,
                        (admin.ModelAdmin,),
                        dict(
                         list_display=tuple([f.name for f in model._meta.fields ]),
                        )
                    )

    admin.site.register(model,admin_class) 


class LinkResultInline(admin.StackedInline):
    model = LinkResult
    extra = 0

### Link 
class LinkAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Link._meta.fields ])
    list_filter=('available','site',)
    search_fields = ['url',]
    inlines =[
        LinkResultInline,
    ]
admin.site.register(Link,LinkAdmin)

### LinkResult
class LinkResultAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in LinkResult._meta.fields ])
    list_filter=('status',)
    search_fields = ['link__url',]
admin.site.register(LinkResult,LinkResultAdmin)
