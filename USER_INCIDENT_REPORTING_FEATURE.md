# 🚨 User Incident Reporting Feature - Documentation

## Overview
Added a complete incident reporting system that allows normal (non-admin) users to:
- ✅ Report security incidents in real-time
- ✅ Track incident status from report to resolution
- ✅ View detailed incident information with AI analysis
- ✅ Manage their own incident reports
- ✅ Receive automatic timestamping and date tracking

## New Features

### 1. Report Incident Page (`/report/`)
**For**: Any authenticated user

**Features**:
- Beautiful form to report new incidents
- Required fields:
  - **Title**: Brief summary of the incident
  - **Description**: Detailed description of what happened
  - **Incident Type**: Select from categories (phishing, malware, ddos, etc.)
  - **Severity Level**: 1-5 scale (1=Critical, 5=Info)
- Optional fields:
  - **Source IP**: IP address of the attacker/source
  - **Target System**: Server or system affected
  - **Affected Assets**: List of impacted resources

**Auto-Features**:
- ✅ Automatic timestamp and date capture
- ✅ Linked to the reporting user's account
- ✅ Status automatically set to "New"
- ✅ Ready for AI analysis

### 2. My Incidents Page (`/my-incidents/`)
**For**: Any authenticated user

**Features**:
- View all incidents YOU have reported
- Quick statistics:
  - Total Incidents Reported
  - Resolved Count
  - Pending Count
- Sortable incident list with:
  - Incident title
  - Brief description
  - Severity badge (color-coded)
  - Status badge
  - Report date and time
- Click any incident to view full details

### 3. Incident Detail Page (`/incidents/<id>/`)
**For**: Reporter or staff members

**Features**:
- **Full Incident Information**:
  - Title, description, type, severity
  - All technical details (source IP, target system, affected assets)
  - Automatic timestamps (reported, last updated, resolved)
  
- **AI Analysis Section**:
  - Predicted incident type
  - Confidence score
  - Anomaly score (0-100%)
  - Risk score (0-100%)
  - Risk level indicator
  
- **Status Tracking**:
  - Current status (New, Investigating, Contained, Resolved, False Positive)
  - Updated by staff with notes
  - Users can see progress notes from security team
  
- **Update Capability** (for staff or reporter):
  - Change status
  - Add notes/updates
  - Mark as resolved

### 4. Incident Tracking Dashboard (`/tracking/`)
**For**: Any authenticated user (staff sees all, users see theirs)

**Features**:
- Advanced filtering:
  - By incident type
  - By status
  - By severity
  - By resolution status (pending/resolved)
  
- Quick statistics:
  - Total incidents in system
  - Your total reports
  - Your resolved incidents
  - Your pending incidents
  
- Detailed incident list with sorting
- Responsive design for mobile

## URL Routes

### New Routes Added:
```
/report/                          - Report a new incident
/my-incidents/                    - View your reported incidents
/incidents/<id>/                  - View incident details
/tracking/                        - Advanced tracking dashboard
```

### Existing Routes Updated:
```
/ (dashboard)                     - Added navigation links to new features
```

## Data Model Updates

### Incident Model Enhanced With:
- `reported_by`: ForeignKey to User (tracks who reported it)
- `detected_at`: Auto-set on creation (timestamp)
- `last_updated`: Auto-updated (tracking changes)
- `resolved_at`: Set when incident is resolved
- `status`: Tracks incident progress (new → investigating → contained → resolved)

## User Permissions

### Regular Users Can:
✅ Report incidents (no admin required)
✅ View their own reported incidents
✅ View full details of incidents they reported
✅ See staff notes and status updates
✅ Edit notes on incidents they reported

### Admin/Staff Can:
✅ View ALL incidents in the system
✅ Edit any incident's status
✅ Add/update notes on any incident
✅ Mark incidents as resolved
✅ Run AI analysis on incidents

## Admin Interface Improvements

Enhanced Django admin with:
- 🎨 Color-coded severity badges
- 📊 Status indicators
- ⚙️ Rich admin customization
- 🔍 Advanced search and filtering
- 🎯 Risk level indicators
- 👤 Reporter tracking

## Forms Created

1. **IncidentReportForm** (`forms.py`):
   - User-friendly form for reporting incidents
   - Validates required fields
   - Clean UI with Bootstrap classes

2. **IncidentUpdateForm** (`forms.py`):
   - For updating incident status and notes
   - Staff can mark as resolved
   - Add progress updates

## Templates Created

1. **report.html** - Beautiful incident reporting form
2. **my_incidents.html** - User's incident list with stats
3. **detail.html** - Detailed incident view with updates
4. **tracking.html** - Advanced tracking dashboard

## How to Use

### For Regular Users:

1. **Report an Incident**:
   ```
   Click "🚨 Report Incident" button on dashboard
   Fill in the incident details
   Click "📤 Submit Report"
   System automatically timestamps it
   ```

2. **Track Your Report**:
   ```
   Click "📋 My Reports" to see all your incidents
   Click any incident to view details and updates
   Check status changes made by security team
   ```

3. **View Real-time Updates**:
   ```
   The security team can add notes and change status
   You'll see all updates on your incident's detail page
   Know exactly where your incident stands
   ```

### For Admin/Staff:

1. **Review User Reports**:
   ```
   Click "📊 Track All" or go to /tracking/
   Filter by type, severity, status
   Click any incident to see full details
   ```

2. **Update Incidents**:
   ```
   Open incident detail page
   Change status (Investigating → Contained → Resolved)
   Add notes for the user
   Save changes
   ```

3. **Admin Interface**:
   ```
   Go to /admin/incidents/
   See color-coded incidents
   Advanced search and filtering
   Bulk management options
   ```

## Security Features Implemented

✅ **Login Required**: All incident pages require authentication
✅ **Permission Checks**: Users can only see/edit their own incidents (unless staff)
✅ **Automatic Attribution**: Incidents are automatically linked to the reporter
✅ **Timestamp Tracking**: All actions are timestamped
✅ **Status Workflow**: Prevents invalid status transitions
✅ **AI Analysis**: Automatic anomaly and risk scoring

## Views Implementation

### Key Views Added:

1. **report_incident()** - Handles incident creation
2. **my_incidents()** - Shows user's incidents
3. **incident_detail()** - Displays full incident info with update form
4. **incident_tracking()** - Advanced filtering and search

All views are decorated with:
- `@login_required` - Authentication check
- Permission checks for viewing/editing

## Testing the Feature

### Test Scenarios:

1. **Create Incident as Regular User**:
   ```
   Login as: testuser / TestUser123!
   Go to /report/
   Fill form with sample data
   Check if timestamp is automatic
   Verify listed in "My Reports"
   ```

2. **View Incident Details**:
   ```
   Click on incident in "My Reports"
   Verify all data displays correctly
   See AI analysis scores
   ```

3. **Track Progress**:
   ```
   Login as admin
   Go to /admin/incidents/
   Update incident status to "Investigating"
   Add a note
   Login as regular user
   See updated status and notes
   ```

4. **Filter Incidents**:
   ```
   Go to /tracking/
   Use filters (type, status, severity)
   Verify results match criteria
   ```

## Files Created/Modified

### New Files:
- `campusshield/incidents/forms.py` - User forms
- `campusshield/incidents/templates/incidents/report.html` - Report form
- `campusshield/incidents/templates/incidents/my_incidents.html` - User's list
- `campusshield/incidents/templates/incidents/detail.html` - Incident details
- `campusshield/incidents/templates/incidents/tracking.html` - Tracking dashboard

### Modified Files:
- `campusshield/incidents/views.py` - Added new views
- `campusshield/campusshield/urls.py` - Added new routes
- `campusshield/incidents/admin.py` - Enhanced admin interface
- `campusshield/incidents/templates/incidents/list.html` - Added navigation links

## Next Steps / Future Enhancements

Potential future features to consider:
- 📧 Email notifications when incidents are updated
- 🔔 Real-time push notifications
- 📈 Analytics dashboard showing incident trends
- 🏷️ Incident tagging and categorization
- 💬 Comments/discussion thread per incident
- 📎 File attachments for evidence
- 🔐 Audit log of all incident changes
- 🤖 Automated incident response
- 📱 Mobile app notifications
- 🔗 Integration with external ticketing systems

## Deployment Notes

✅ All code committed to GitHub
✅ System checks pass (0 issues)
✅ All migrations applied
✅ Admin interface enhanced
✅ Ready for production

Test users created:
- **testuser** (regular user) / TestUser123!
- **admin** (superuser) / CampusShield123!

---

**Status**: ✅ FEATURE COMPLETE AND DEPLOYED
**Last Updated**: March 12, 2026
**Version**: 1.0
