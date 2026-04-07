import lime.lime_tabular as lt
import numpy as np

class LIMEExplainer:
    def __init__(self, training_data: np.ndarray, feature_names: list[str]):
        self.explainer = lt.LimeTabularExplainer(
            training_data,
            feature_names=feature_names,
            mode='classification'
        )

    def explain(self, instance: np.ndarray, model_fn, n_features: int = 5) -> list:
        exp = self.explainer.explain_instance(
            instance, model_fn, num_features=n_features)
        return exp.as_list()
