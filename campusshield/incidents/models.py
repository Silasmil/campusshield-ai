from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json

class Incident(models.Model):
    INCIDENT_TYPES = [
        ('phishing', 'Phishing'),
        ('malware', 'Malware'),
        ('ddos', 'DDoS'),
        ('unauthorized_access', 'Unauthorized Access'),
        ('data_breach', 'Data Breach'),
        ('ransomware', 'Ransomware'),
        ('insider_threat', 'Insider Threat'),
    ]
    
    # Fix: Severity should be 1-5, not 6 (I see you added severity 6)
    SEVERITY_LEVELS = [
        (1, 'Critical'),
        (2, 'High'),
        (3, 'Medium'),
        (4, 'Low'),
        (5, 'Info'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('investigating', 'Investigating'),
        ('contained', 'Contained'),
        ('resolved', 'Resolved'),
        ('false_positive', 'False Positive'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    incident_type = models.CharField(max_length=50, choices=INCIDENT_TYPES)
    
    # Severity and Impact
    severity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    impact_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])  # AI-calculated impact
    confidence_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])  # AI confidence
    
    # Temporal Data
    detected_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    resolved = models.BooleanField(default=False)
    
    # Technical Details (new fields for AI)
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    target_system = models.CharField(max_length=100, blank=True)
    affected_assets = models.TextField(blank=True)  # JSON field
    indicators = models.TextField(blank=True)  # JSON field for IOCs
    
    # AI/ML Fields
    anomaly_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])  # Anomaly detection score
    risk_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])  # Calculated risk
    predicted_type = models.CharField(max_length=50, blank=True)  # AI prediction
    prediction_confidence = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    
    # Audit
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"{self.title} - Severity: {self.severity}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate risk score before saving
        if not self.risk_score:
            self.risk_score = self.calculate_risk()
        super().save(*args, **kwargs)
    
    def calculate_risk(self):
        """Basic risk calculation"""
        risk = self.severity / 5.0  # Normalize severity to 0-1
        if not self.resolved:
            risk += 0.2  # Unresolved incidents are riskier
        return min(risk, 1.0)