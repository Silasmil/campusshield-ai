from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Incident
from .forms import IncidentReportForm, IncidentUpdateForm
import json
import traceback

# Import AI modules with error handling
try:
    from ai_engine.anomaly_detector import AnomalyDetector
    from ai_engine.threat_classifier import ThreatClassifier
    AI_AVAILABLE = True
    print("✅ AI modules loaded successfully")
except ImportError as e:
    print(f"⚠️ AI modules not available: {e}")
    AI_AVAILABLE = False
    AnomalyDetector = None
    ThreatClassifier = None

# Initialize AI models if available
if AI_AVAILABLE:
    try:
        anomaly_detector = AnomalyDetector()
        threat_classifier = ThreatClassifier()
        print("✅ AI models initialized successfully")
    except Exception as e:
        print(f"⚠️ Error initializing AI models: {e}")
        AI_AVAILABLE = False
        anomaly_detector = None
        threat_classifier = None

@login_required
@require_http_methods(["GET", "HEAD", "OPTIONS"])
def incidents_list(request):
    incidents = Incident.objects.all()
    data = []
    for incident in incidents:
        data.append({
            'id': incident.id,
            'title': incident.title,
            'description': incident.description,
            'incident_type': incident.incident_type,
            'severity': incident.severity,
            'detected_at': incident.detected_at,
            'resolved': incident.resolved,
            'anomaly_score': getattr(incident, 'anomaly_score', 0.0),
            'risk_score': getattr(incident, 'risk_score', 0.0)
        })
    return JsonResponse(data, safe=False)

@login_required
@require_http_methods(["GET", "HEAD", "OPTIONS"])
def incidents_dashboard(request):
    try:
        incidents = Incident.objects.all().order_by('-detected_at')
        
        # Calculate statistics
        total_incidents = incidents.count()
        critical_incidents = incidents.filter(severity__lte=2, resolved=False).count()
        
        # Safely calculate average risk score
        if total_incidents > 0:
            avg_risk = sum(getattr(i, 'risk_score', 0) for i in incidents) / total_incidents
        else:
            avg_risk = 0
    except Exception as e:
        print(f"Database error in incidents_dashboard: {e}")
        incidents = []
        total_incidents = 0
        critical_incidents = 0
        avg_risk = 0
    
    context = {
        'incidents': incidents,
        'total_incidents': total_incidents,
        'critical_incidents': critical_incidents,
        'avg_risk': round(avg_risk * 100, 1)  # Convert to percentage
    }
    return render(request, 'incidents/list.html', context)

@login_required
@require_http_methods(["POST"])
def analyze_incident(request, incident_id):
    """AI analysis endpoint"""
    incident = get_object_or_404(Incident, id=incident_id)
    
    if not AI_AVAILABLE:
        return JsonResponse({
            'id': incident.id,
            'anomaly_score': 0.3,
            'risk_score': incident.calculate_risk(),
            'message': 'AI not available - using default scores'
        })
    
    try:
        # Run AI analysis
        anomaly_score = anomaly_detector.predict(incident)
        
        # Update incident with AI scores
        incident.anomaly_score = anomaly_score
        incident.risk_score = min(incident.calculate_risk() * (1 + anomaly_score), 1.0)
        incident.save()
        
        return JsonResponse({
            'id': incident.id,
            'anomaly_score': anomaly_score,
            'risk_score': incident.risk_score,
            'message': 'AI analysis complete'
        })
    except Exception as e:
        return JsonResponse({
            'id': incident.id,
            'error': str(e),
            'anomaly_score': 0.3,
            'risk_score': incident.calculate_risk(),
            'message': 'AI analysis failed - using default scores'
        })

@login_required
@require_http_methods(["POST"])
def train_ai_models(request):
    """Train AI models with existing incidents"""
    if not AI_AVAILABLE:
        return JsonResponse({
            'error': 'AI modules not available'
        }, status=400)
    
    incidents = list(Incident.objects.all())
    
    if len(incidents) < 5:
        return JsonResponse({
            'error': f'Need at least 5 incidents for training. Current: {len(incidents)}'
        }, status=400)
    
    try:
        # Train anomaly detector
        anomaly_result = anomaly_detector.train(incidents)
        
        # Train classifier if enough incidents
        classifier_result = False
        if len(incidents) >= 10:
            classifier_result = threat_classifier.train(incidents)
        
        return JsonResponse({
            'success': True,
            'anomaly_detector_trained': anomaly_result,
            'threat_classifier_trained': classifier_result,
            'incidents_used': len(incidents)
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=500)

@login_required
@require_http_methods(["GET", "HEAD", "OPTIONS"])
def incident_analysis(request, incident_id):
    """Get AI analysis for a specific incident"""
    incident = get_object_or_404(Incident, id=incident_id)
    
    if not AI_AVAILABLE:
        return JsonResponse({
            'id': incident.id,
            'title': incident.title,
            'current_type': incident.incident_type,
            'predicted_type': incident.incident_type,
            'prediction_confidence': 0.5,
            'anomaly_score': getattr(incident, 'anomaly_score', 0.0),
            'risk_score': getattr(incident, 'risk_score', incident.calculate_risk()),
            'analysis': {
                'is_anomalous': False,
                'risk_level': 'High' if incident.severity <= 2 else 'Medium' if incident.severity == 3 else 'Low',
                'needs_attention': incident.severity <= 2 and not incident.resolved
            }
        })
    
    try:
        # Get AI predictions
        predicted_type, confidence = threat_classifier.predict(incident)
        
        return JsonResponse({
            'id': incident.id,
            'title': incident.title,
            'current_type': incident.incident_type,
            'predicted_type': predicted_type,
            'prediction_confidence': confidence,
            'anomaly_score': incident.anomaly_score,
            'risk_score': incident.risk_score,
            'analysis': {
                'is_anomalous': incident.anomaly_score > 0.7,
                'risk_level': 'High' if incident.risk_score > 0.7 else 'Medium' if incident.risk_score > 0.4 else 'Low',
                'needs_attention': incident.anomaly_score > 0.6 and not incident.resolved
            }
        })
    except Exception as e:
        return JsonResponse({
            'id': incident.id,
            'error': str(e),
            'current_type': incident.incident_type,
            'predicted_type': incident.incident_type,
            'prediction_confidence': 0.5,
            'anomaly_score': getattr(incident, 'anomaly_score', 0.0),
            'risk_score': getattr(incident, 'risk_score', incident.calculate_risk())
        })


# User-facing incident reporting views

@login_required
def report_incident(request):
    """Allow users to report a new incident"""
    if request.method == 'POST':
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user
            incident.status = 'new'
            incident.save()
            
            messages.success(
                request,
                f"✅ Incident '{incident.title}' reported successfully! Incident ID: {incident.id}"
            )
            return redirect('incident_detail', incident_id=incident.id)
    else:
        form = IncidentReportForm()
    
    context = {
        'form': form,
        'title': 'Report an Incident'
    }
    return render(request, 'incidents/report.html', context)


@login_required
def my_incidents(request):
    """Show incidents reported by the current user"""
    # Get all incidents reported by this user
    user_incidents = Incident.objects.filter(
        reported_by=request.user
    ).order_by('-detected_at')
    
    # Get statistics for this user's incidents
    total_reported = user_incidents.count()
    resolved_count = user_incidents.filter(resolved=True).count()
    pending_count = user_incidents.filter(resolved=False).count()
    
    context = {
        'incidents': user_incidents,
        'total_reported': total_reported,
        'resolved_count': resolved_count,
        'pending_count': pending_count,
        'page_title': 'My Reported Incidents'
    }
    return render(request, 'incidents/my_incidents.html', context)


@login_required
def incident_detail(request, incident_id):
    """Show detailed view of a single incident"""
    incident = get_object_or_404(Incident, id=incident_id)
    
    # Check if user can view this incident (reporter or admin)
    if incident.reported_by != request.user and not request.user.is_staff:
        messages.error(request, '❌ You do not have permission to view this incident.')
        return redirect('my_incidents')
    
    # Handle status updates
    if request.method == 'POST' and (request.user.is_staff or incident.reported_by == request.user):
        form = IncidentUpdateForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Incident updated successfully!')
            return redirect('incident_detail', incident_id=incident.id)
    else:
        form = IncidentUpdateForm(instance=incident)
    
    # Get AI analysis if available
    ai_analysis = None
    if AI_AVAILABLE:
        try:
            predicted_type, confidence = threat_classifier.predict(incident)
            ai_analysis = {
                'predicted_type': predicted_type,
                'prediction_confidence': round(confidence * 100, 1),
                'anomaly_score': round(incident.anomaly_score * 100, 1),
                'risk_score': round(incident.risk_score * 100, 1),
                'is_anomalous': incident.anomaly_score > 0.7,
                'risk_level': 'High' if incident.risk_score > 0.7 else 'Medium' if incident.risk_score > 0.4 else 'Low',
            }
        except Exception as e:
            print(f"Error in AI analysis: {e}")
    
    context = {
        'incident': incident,
        'form': form,
        'is_reporter': incident.reported_by == request.user,
        'is_staff': request.user.is_staff,
        'ai_analysis': ai_analysis,
        'status_choices': Incident.STATUS_CHOICES,
    }
    return render(request, 'incidents/detail.html', context)


@login_required
def incident_tracking(request):
    """Dashboard showing all incidents with filtering and tracking"""
    # Start with incidents the user can see
    if request.user.is_staff:
        # Admin sees all incidents
        incidents = Incident.objects.all()
    else:
        # Regular users see only their reported incidents
        incidents = Incident.objects.filter(reported_by=request.user)
    
    # Apply filters
    incident_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    severity = request.GET.get('severity', '')
    resolved = request.GET.get('resolved', '')
    
    if incident_type:
        incidents = incidents.filter(incident_type=incident_type)
    if status:
        incidents = incidents.filter(status=status)
    if severity:
        incidents = incidents.filter(severity=int(severity))
    if resolved == 'true':
        incidents = incidents.filter(resolved=True)
    elif resolved == 'false':
        incidents = incidents.filter(resolved=False)
    
    # Order by most recent
    incidents = incidents.order_by('-detected_at')
    
    # Calculate statistics
    total_incidents = Incident.objects.all().count() if request.user.is_staff else incidents.count()
    user_total = Incident.objects.filter(reported_by=request.user).count()
    user_resolved = Incident.objects.filter(reported_by=request.user, resolved=True).count()
    user_pending = Incident.objects.filter(reported_by=request.user, resolved=False).count()
    
    # Get unique values for filter dropdowns
    incident_types = Incident.objects.values_list('incident_type', flat=True).distinct()
    statuses = Incident.STATUS_CHOICES
    severities = Incident.SEVERITY_LEVELS
    
    context = {
        'incidents': incidents,
        'total_incidents': total_incidents,
        'user_total': user_total,
        'user_resolved': user_resolved,
        'user_pending': user_pending,
        'incident_types': incident_types,
        'statuses': statuses,
        'severities': severities,
        'is_staff': request.user.is_staff,
        'selected_type': incident_type,
        'selected_status': status,
        'selected_severity': severity,
        'selected_resolved': resolved,
    }
    return render(request, 'incidents/tracking.html', context)