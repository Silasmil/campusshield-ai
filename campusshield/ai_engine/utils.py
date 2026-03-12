import numpy as np
from django.utils import timezone  # ✅ use Django's timezone-aware datetime
import re

def extract_features_from_incident(incident):
    """Extract numerical features from an incident for ML models"""
    features = {}
    
    try:
        # Temporal features
        now = timezone.now()
        detected_at = incident.detected_at
        
        features['hour_of_day'] = detected_at.hour
        features['day_of_week'] = detected_at.weekday()
        features['days_ago'] = (now - detected_at).days
        
        # Text features
        features['title_length'] = len(incident.title) if incident.title else 0
        features['description_length'] = len(incident.description) if incident.description else 0
        
        # Count suspicious keywords in description
        suspicious_words = ['hack', 'breach', 'unauthorized', 'suspicious', 
                           'stolen', 'malware', 'phishing', 'attack', 'ransomware', 'ddos']
        description_lower = incident.description.lower() if incident.description else ""
        features['suspicious_word_count'] = sum(
            1 for word in suspicious_words if word in description_lower
        )
        
        # Incident type encoding (one-hot)
        incident_types = ['phishing', 'malware', 'ddos', 'unauthorized_access', 
                         'data_breach', 'ransomware', 'insider_threat']
        for it in incident_types:
            features[f'type_{it}'] = 1 if incident.incident_type == it else 0
        
        # Severity (normalized to 0-1)
        features['severity_normalized'] = min(float(incident.severity) / 5.0, 1.0)
        
        # Status features
        features['is_resolved'] = 1 if incident.resolved else 0
        features['hours_since_detected'] = (now - detected_at).total_seconds() / 3600
        
    except Exception as e:
        print(f"Error extracting features: {e}")
        # Return default features if extraction fails
        features = {
            'hour_of_day': 0,
            'day_of_week': 0,
            'days_ago': 0,
            'title_length': 0,
            'description_length': 0,
            'suspicious_word_count': 0,
            'severity_normalized': 0.5,
            'is_resolved': 0,
            'hours_since_detected': 0
        }
        # Add type encodings
        for it in ['phishing', 'malware', 'ddos', 'unauthorized_access', 
                   'data_breach', 'ransomware', 'insider_threat']:
            features[f'type_{it}'] = 0
    
    return features

def validate_ip(ip):
    """Simple IP validation"""
    if not ip:
        return False
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return bool(re.match(pattern, ip))
