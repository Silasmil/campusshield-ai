from django.contrib import admin
from django.utils.html import format_html
from .models import Incident

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        'colored_title',
        'incident_type',
        'severity_badge',
        'status_badge',
        'reported_by',
        'detected_at',
        'risk_indicator'
    )
    list_filter = ('incident_type', 'severity', 'status', 'resolved', 'detected_at')
    search_fields = ('title', 'description', 'reported_by__username')
    readonly_fields = ('detected_at', 'last_updated', 'risk_score', 'calculated_risk_display')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'incident_type', 'reported_by')
        }),
        ('Severity & Status', {
            'fields': ('severity', 'status', 'resolved', 'resolved_at')
        }),
        ('Technical Details', {
            'fields': ('source_ip', 'target_system', 'affected_assets')
        }),
        ('AI Analysis', {
            'fields': ('anomaly_score', 'risk_score', 'calculated_risk_display', 'impact_score', 'confidence_score')
        }),
        ('Additional Information', {
            'fields': ('notes', 'indicators')
        }),
        ('Timestamps', {
            'fields': ('detected_at', 'last_updated'),
            'classes': ('collapse',)
        })
    )
    
    def colored_title(self, obj):
        """Display title with color coding based on severity"""
        colors = {
            1: '#c0392b',  # Critical - Red
            2: '#e74c3c',  # High - Orange-Red
            3: '#f39c12',  # Medium - Orange
            4: '#27ae60',  # Low - Green
            5: '#3498db'   # Info - Blue
        }
        color = colors.get(obj.severity, '#95a5a6')
        return format_html(
            '<span style="color: {}; font-weight: bold;">■</span> {}',
            color,
            obj.title
        )
    colored_title.short_description = 'Title'
    
    def severity_badge(self, obj):
        """Display severity as a badge"""
        colors = {
            1: '#c0392b',
            2: '#e74c3c',
            3: '#f39c12',
            4: '#27ae60',
            5: '#3498db'
        }
        color = colors.get(obj.severity, '#95a5a6')
        labels = {
            1: 'Critical',
            2: 'High',
            3: 'Medium',
            4: 'Low',
            5: 'Info'
        }
        label = labels.get(obj.severity, 'Unknown')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 20px; font-weight: bold;">{}</span>',
            color,
            label
        )
    severity_badge.short_description = 'Severity'
    
    def status_badge(self, obj):
        """Display status as a badge"""
        colors = {
            'new': '#1976d2',
            'investigating': '#f77f00',
            'contained': '#7b1fa2',
            'resolved': '#388e3c',
            'false_positive': '#c2185b'
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 20px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def risk_indicator(self, obj):
        """Display risk score visually"""
        risk = obj.risk_score * 100
        if risk > 70:
            color = '#e74c3c'
            level = 'High'
        elif risk > 40:
            color = '#f39c12'
            level = 'Medium'
        else:
            color = '#27ae60'
            level = 'Low'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 20px; font-weight: bold;">{:.0f}% Risk</span>',
            color,
            risk
        )
    risk_indicator.short_description = 'Risk Level'
    
    def calculated_risk_display(self, obj):
        """Display calculated risk score"""
        risk = obj.calculate_risk() * 100
        return f"{risk:.1f}%"
    calculated_risk_display.short_description = 'Calculated Risk'
    
    def save_model(self, request, obj, form, change):
        """Auto-set reported_by on creation"""
        if not change:  # New incident
            obj.reported_by = request.user
        super().save_model(request, obj, form, change)