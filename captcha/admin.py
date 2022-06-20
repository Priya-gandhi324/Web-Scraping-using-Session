from django.contrib import admin
from .models import Cases, CaseStatus

# Register your models here.
admin.site.register(Cases)
admin.site.register(CaseStatus)