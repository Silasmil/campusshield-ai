import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from .utils import extract_features_from_incident

class ThreatClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=50,
            max_depth=5,
            random_state=42
        )
        self.is_trained = False
        self.model_path = 'ai_engine/models/threat_classifier.pkl'
        self.incident_types = [
            'phishing', 'malware', 'ddos', 'unauthorized_access', 
            'data_breach', 'ransomware', 'insider_threat'
        ]
        
    def prepare_data(self, incidents):
        """Prepare features and labels for training"""
        X = []
        y = []
        
        # Get unique incident types from data
        unique_types = list(set([i.incident_type for i in incidents if i.incident_type]))
        if unique_types:
            self.incident_types = unique_types
        
        for incident in incidents:
            try:
                features = extract_features_from_incident(incident)
                X.append(list(features.values()))
                
                # Find the index of the incident type
                if incident.incident_type in self.incident_types:
                    y.append(self.incident_types.index(incident.incident_type))
                else:
                    # Skip incidents with unknown types
                    continue
                    
            except Exception as e:
                print(f"Error preparing data for incident {incident.id}: {e}")
                continue
        
        if not X or not y:
            return np.array([]), np.array([])
        
        return np.array(X), np.array(y)
    
    def train(self, incidents):
        """Train the threat classifier"""
        if len(incidents) < 10:
            print(f"Need at least 10 incidents for training, have {len(incidents)}")
            return False
        
        X, y = self.prepare_data(incidents)
        if len(X) == 0 or len(y) == 0:
            print("No valid training data available")
            return False
        
        try:
            # Train model
            self.model.fit(X, y)
            self.is_trained = True
            
            # Save model
            os.makedirs('ai_engine/models', exist_ok=True)
            joblib.dump({
                'model': self.model,
                'incident_types': self.incident_types
            }, self.model_path)
            
            print(f"Classifier trained successfully on {len(X)} incidents")
            return True
            
        except Exception as e:
            print(f"Error training classifier: {e}")
            return False
    
    def predict(self, incident):
        """Predict incident type"""
        try:
            if not self.is_trained:
                try:
                    if os.path.exists(self.model_path):
                        saved = joblib.load(self.model_path)
                        self.model = saved['model']
                        self.incident_types = saved['incident_types']
                        self.is_trained = True
                    else:
                        return incident.incident_type, 0.5
                except Exception as e:
                    print(f"Error loading saved model: {e}")
                    return incident.incident_type, 0.5
            
            features = extract_features_from_incident(incident)
            X = np.array([list(features.values())])
            
            # Get prediction
            prediction_idx = self.model.predict(X)[0]
            
            # Get confidence (probability)
            proba = self.model.predict_proba(X)[0]
            confidence = float(np.max(proba)) if len(proba) > 0 else 0.5
            
            # Ensure prediction_idx is within range
            if 0 <= prediction_idx < len(self.incident_types):
                predicted_type = self.incident_types[prediction_idx]
            else:
                predicted_type = incident.incident_type
                confidence = 0.5
            
            return predicted_type, confidence
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return incident.incident_type, 0.5
