from django.contrib import admin
from .models import Source, Standard, Site, Pedon, Synonym, Dataset
admin.site.register(Source)
admin.site.register(Standard)
admin.site.register(Site)
admin.site.register(Pedon)
admin.site.register(Dataset)
admin.site.register(Synonym)