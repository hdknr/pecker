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



### Link 
class LinkAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Link._meta.fields ])
    list_filter=('available',)
    search_fields = ['url',]
admin.site.register(Link,LinkAdmin)

### LinkResult
class LinkResultAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in LinkResult._meta.fields ])
    list_filter=('status',)
    search_fields = ['link__url',]
admin.site.register(LinkResult,LinkResultAdmin)
