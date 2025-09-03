"""Agentic model stubs for the 10 cybersecurity techniques.

Each agent implements analyze(event) -> dict with keys:
 - technique: str
 - is_threat: bool
 - score: float (0-1)
 - details: dict

These are lightweight, explainable stubs suitable for MVP. Replace with production models later.
"""
from typing import Dict, Any
import random
import hashlib
from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
from pathlib import Path

MODELS_DIR = Path(__file__).parent / 'models'
MODELS_DIR.mkdir(exist_ok=True)


class BaseAgent:
    technique = 'base'

    def analyze(self, event: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()


class SIEMAgent(BaseAgent):
    technique = 'SIEM'

    def analyze(self, event):
        # simple correlation heuristic: many fields present => lower risk; rare event types => higher
        et = event.get('event_type', '')
        score = 0.2
        if 'error' in et or 'failed' in et:
            score += 0.5
        if event.get('user') == 'root' or event.get('user') == 'Administrator':
            score += 0.2
        return self._out(score, {'event_type': et})

    def _out(self, score, details):
        return {'technique': self.technique, 'is_threat': score > 0.5, 'score': min(1.0, score), 'details': details}


class EDRAgent(BaseAgent):
    technique = 'EDR'

    def __init__(self):
        self.model_file = MODELS_DIR / 'edr_iso.joblib'
        if self.model_file.exists():
            try:
                self.model = joblib.load(self.model_file)
            except Exception:
                self.model = None
        else:
            self.model = None

    def analyze(self, event):
        # use IsolationForest on numeric features if present
        features = list(event.get('features', {}).values())
        if self.model is not None and len(features) >= 1:
            score = float(-self.model.decision_function([features])[0])
        else:
            score = random.random() * 0.6
        return {'technique': self.technique, 'is_threat': score > 0.6, 'score': min(1.0, score), 'details': {}}


class ThreatIntelAgent(BaseAgent):
    technique = 'Threat Intelligence'

    def analyze(self, event):
        # naive IOC check: hash IP and look for matches (stub)
        ip = event.get('ip', '')
        if not ip:
            return {'technique': self.technique, 'is_threat': False, 'score': 0.0, 'details': {}}
        h = int(hashlib.sha1(ip.encode()).hexdigest()[:6], 16)
        score = 0.9 if (h % 97) == 0 else 0.1 * (h % 10)
        return {'technique': self.technique, 'is_threat': score > 0.7, 'score': min(1.0, score/1.0), 'details': {'ip': ip}}


class BehavioralAgent(BaseAgent):
    technique = 'Behavioral Analysis'

    def analyze(self, event):
        # heuristic: sudden numeric spikes in features
        feats = list(event.get('features', {}).values())
        if not feats:
            return {'technique': self.technique, 'is_threat': False, 'score': 0.0, 'details': {}}
        arr = np.array(feats)
        z = (arr - arr.mean()) / (arr.std() + 1e-6)
        score = float(min(1.0, np.abs(z).max() / 3.0))
        return {'technique': self.technique, 'is_threat': score > 0.6, 'score': score, 'details': {'z_max': float(np.abs(z).max())}}


class SignatureAgent(BaseAgent):
    technique = 'Signature Detection'

    def analyze(self, event):
        # stub: look for suspicious substrings in event_type or details
        et = event.get('event_type', '')
        suspicious = ['malware', 'trojan', 'exploit', 'ransom']
        score = 0.0
        for s in suspicious:
            if s in et.lower():
                score = 0.95
                break
        return {'technique': self.technique, 'is_threat': score > 0.5, 'score': score, 'details': {'event_type': et}}


class AnomalyAgent(BaseAgent):
    technique = 'Anomaly Detection'

    def __init__(self):
        self.model_file = MODELS_DIR / 'iso_forest.joblib'
        if self.model_file.exists():
            try:
                self.model = joblib.load(self.model_file)
            except Exception:
                self.model = None
        else:
            self.model = None

    def analyze(self, event):
        feats = list(event.get('features', {}).values())
        if self.model is not None and len(feats) >= 1:
            score = float(-self.model.decision_function([feats])[0])
        else:
            score = random.random() * 0.5
        return {'technique': self.technique, 'is_threat': score > 0.5, 'score': min(1.0, score), 'details': {}}


class SOARAgent(BaseAgent):
    technique = 'SOAR'

    def analyze(self, event):
        # SOAR decides on actions based on severity hints
        base = 0.0
        if 'kill' in event.get('event_type', '') or 'isolate' in event.get('event_type', ''):
            base = 0.9
        action = 'notify'
        if base > 0.8:
            action = 'isolate'
        return {'technique': self.technique, 'is_threat': base > 0.5, 'score': base, 'details': {'recommended_action': action}}


class VulnerabilityAgent(BaseAgent):
    technique = 'Vulnerability Management'

    def analyze(self, event):
        # stub: if event_type mentions outdated software keywords, raise score
        et = event.get('event_type', '')
        keywords = ['outdated', 'unpatched', 'vuln', 'cve']
        score = 0.0
        for k in keywords:
            if k in et.lower():
                score = 0.8
                break
        return {'technique': self.technique, 'is_threat': score > 0.5, 'score': score, 'details': {}}


class NetworkAgent(BaseAgent):
    technique = 'Network Analysis'

    def analyze(self, event):
        # simple heuristic: large numeric features or certain ports => higher score
        feats = list(event.get('features', {}).values())
        score = 0.0
        if feats and max(feats) > 5:
            score = 0.7
        return {'technique': self.technique, 'is_threat': score > 0.5, 'score': score, 'details': {}}


class IAMAgent(BaseAgent):
    technique = 'Identity & Access Management'

    def analyze(self, event):
        user = event.get('user', '')
        # stub: unusual user names or admin usage flagged
        score = 0.0
        if user.lower().startswith('svc_') or user.lower() in ('root', 'administrator'):
            score = 0.6
        return {'technique': self.technique, 'is_threat': score > 0.5, 'score': score, 'details': {'user': user}}


ALL_AGENTS = [
    SIEMAgent(),
    EDRAgent(),
    ThreatIntelAgent(),
    BehavioralAgent(),
    SignatureAgent(),
    AnomalyAgent(),
    SOARAgent(),
    VulnerabilityAgent(),
    NetworkAgent(),
    IAMAgent(),
]
