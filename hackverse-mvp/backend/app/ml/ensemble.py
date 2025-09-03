from typing import Dict, Any
from backend.app.ml.agents import ALL_AGENTS
from backend.app.database import SessionLocal
from sqlalchemy import Column, String, Float
from backend.app.models.user import Base


class AgentWeight(Base):
    __tablename__ = 'agent_weights'
    technique = Column(String, primary_key=True)
    weight = Column(Float, default=1.0)


class EnsembleAnalyzer:
    def __init__(self, agents=None):
        self.agents = agents or ALL_AGENTS
        # load weights from DB or default to 1.0
        self.weights = self._load_weights()

    def analyze(self, event: Dict[str, Any]):
        results = []
        # dispatch to all agents
        for a in self.agents:
            try:
                r = a.analyze(event)
                results.append(r)
            except Exception as e:
                results.append({'technique': a.technique, 'is_threat': False, 'score': 0.0, 'details': {'error': str(e)}})

        # aggregate: apply per-technique weights
        weighted_sum = 0.0
        total_weight = 0.0
        for r in results:
            w = self.weights.get(r.get('technique'), 1.0)
            weighted_sum += r.get('score', 0.0) * w
            total_weight += w
        agg_score = (weighted_sum / total_weight) if total_weight > 0 else 0.0

        # choose highest-confidence technique
        best = max(results, key=lambda r: r.get('score', 0.0)) if results else None
        return {
            'aggregate_score': agg_score,
            'is_threat': agg_score > 0.5,
            'per_technique': results,
            'top_technique': best
        }

    def _load_weights(self):
        weights = {}
        # default weights
        for a in (self.agents or ALL_AGENTS):
            weights[a.technique] = 1.0
        try:
            db = SessionLocal()
            # ensure table exists and query
            for aw in db.query(AgentWeight).all():
                weights[aw.technique] = aw.weight
            db.close()
        except Exception:
            # DB might not exist yet; keep defaults
            pass
        return weights
