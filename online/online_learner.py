from river import linear_model, preprocessing, metrics

class OnlineLearner:
    """Incremental logistic regression - updates every trade."""
    def __init__(self):
        self.scaler = preprocessing.StandardScaler()
        self.model = linear_model.LogisticRegression()
        self.metric = metrics.ROCAUC()

    def predict(self, features: dict) -> float:
        """Returns probability of price going up."""
        x = self.scaler.transform_one(features)
        return self.model.predict_proba_one(x).get(1, 0.5)

    def update(self, features: dict, outcome: int) -> None:
        """outcome: 1=up, 0=down."""
        self.scaler.learn_one(features)
        x = self.scaler.transform_one(features)
        self.model.learn_one(x, outcome)
        self.metric.update(outcome, self.predict(features))

    @property
    def auc(self) -> float:
        return self.metric.get()
