import shap, numpy as np

class SHAPExplainer:
    def __init__(self, model, feature_names: list[str]):
        self.feature_names = feature_names
        self.explainer = (shap.TreeExplainer(model)
            if hasattr(model, 'feature_importances_')
            else shap.KernelExplainer(model.predict, shap.sample(np.zeros((1, len(feature_names))))))

    def explain(self, X) -> np.ndarray:
        return self.explainer.shap_values(X)

    def top_contributors(self, X, n: int = 3) -> list[tuple]:
        vals = self.explain(X)
        if isinstance(vals, list):
            vals = vals[1]  # binary classification class=1
        flat = vals.flatten() if vals.ndim > 1 else vals
        idx = np.argsort(np.abs(flat))[-n:][::-1]
        return [(self.feature_names[i], float(flat[i])) for i in idx]
