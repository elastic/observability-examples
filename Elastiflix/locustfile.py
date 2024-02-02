from locust import HttpUser, task, between

from time import sleep
import random

class NodeServerElasticApm(HttpUser):
    host = "http://node-server-elastic-apm:3001"
    wait_time = between(1, 3)

    @task
    def favorites_and_login(self):
        self.client.get("/api/favorites")

        if random.random() < 0.5:
            self.client.post("/api/favorites", json={"id": random.randint(1, 100)})

        # in 50% of the cases, call the login endpoint
        if random.random() < 0.5:
            self.client.get("/api/login")

class NodeServerElasticOtel(HttpUser):
    host = "http://node-server-elastic-otel:3002"
    wait_time = between(1, 3)

    @task
    def favorites_and_login(self):
        self.client.get("/api/favorites")

        if random.random() < 0.5:
            self.client.post("/api/favorites", json={"id": random.randint(1, 100)})
        
        # in 50% of the cases, call the login endpoint
        if random.random() < 0.5:
            self.client.get("/api/login")

