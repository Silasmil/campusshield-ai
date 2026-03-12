from django.contrib import admin
from .models import Incident

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'incident_type', 'severity', 'detected_at', 'resolved')
    list_filter = ('incident_type', 'severity', 'resolved')
    search_fields = ('title', 'description')