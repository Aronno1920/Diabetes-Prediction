# locustfile.py
import random
from locust import HttpUser, task, between


class DiabetesAPIUser(HttpUser):
    # Simulate a short think time between requests
    wait_time = between(1, 3)

    def _payload(self):
        """Generate a realistic payload for /predict"""
        return {
            "Pregnancies": random.randint(0, 10),
            "Glucose": random.randint(70, 200),
            "BloodPressure": random.randint(50, 100),
            "SkinThickness": random.randint(10, 50),
            "Insulin": random.randint(15, 276),
            "BMI": round(random.uniform(15.0, 50.0), 1),
            "DiabetesPedigreeFunction": round(random.uniform(0.1, 2.5), 2),
            "Age": random.randint(18, 90),
        }

    @task(2)
    def health(self):
        # Will be counted as failure automatically if status >= 400
        self.client.get("/health", name="/health")

    @task(2)
    def info(self):
        self.client.get("/info", name="/info")

    @task(1)
    def metrics(self):
        # If you don’t serve /metrics yet, you can comment this out
        self.client.get("/metrics", name="/metrics")

    @task(5)
    def predict(self):
        self.client.post("/predict", json=self._payload(), name="/predict")
