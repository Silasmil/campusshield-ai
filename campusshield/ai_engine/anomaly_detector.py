import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os
from .utils import extract_features_from_incident

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.2,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = 'ai_engine/models/anomaly_detector.pkl'
        
    def prepare_features(self, incidents):
        """Convert incidents to feature matrix"""
        features_list = []
        for incident in incidents:
            try:
                features = extract_features_from_incident(incident)
                features_list.append(list(features.values()))
            except Exception as e:
                print(f"Error preparing features for incident {incident.id}: {e}")
                continue
        
        if not features_list:
            return np.array([])
        
        return np.array(features_list)
    
    def train(self, incidents):
        """Train the anomaly detection model"""
        if len(incidents) < 5:
            print(f"Not enough incidents for training. Have {len(incidents)}, need at least 5.")
            return False
        
        X = self.prepare_features(incidents)
        if len(X) == 0:
            print("No valid features extracted for training")
            return False
        
        try:
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled)
            self.is_trained = True
            
            # Save model
            os.makedirs('ai_engine/models', exist_ok=True)
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler
            }, self.model_path)
            
            print(f"Model trained successfully on {len(X)} incidents")
            return True
            
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def predict(self, incident):
        """Predict if an incident is anomalous"""
        try:
            if not self.is_trained:
                try:
                    if os.path.exists(self.model_path):
                        saved = joblib.load(self.model_path)
                        self.model = saved['model']
                        self.scaler = saved['scaler']
                        self.is_trained = True
                    else:
                        return 0.3  # Default score
                except Exception as e:
                    print(f"Error loading saved model: {e}")
                    return 0.3  # Default score
            
            X = self.prepare_features([incident])
            if len(X) == 0:
                return 0.3
            
            X_scaled = self.scaler.transform(X)
            
            # Get anomaly score
            score = self.model.score_samples(X_scaled)[0]
            
            # Convert to 0-1 scale (more negative = more anomalous)
            # Isolation Forest scores are typically between -0.5 and 0.5
            anomaly_score = 1 - ((score + 0.5) / 1.0)
            anomaly_score = max(0.0, min(1.0, anomaly_score))
            
            return float(anomaly_score)
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return 0.3
