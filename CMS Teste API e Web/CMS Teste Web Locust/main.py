from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        # self.client.post("/login", {"username": "test_user", "password": ""})
        pass

    # @task
    # def index(self):
    #     self.client.get("/")
    #     self.client.get("/static/assets.js")

    # @task
    # def about(self):
    #     self.client.get("/about/")

    @task
    def ping(self):
        self.client.get("/ping/")

    @task
    def health(self):
        self.client.get("/health/")

    @task
    def data(self):
        self.client.get("/data/")

    @task
    def getall(self):
        self.client.get("/getall/")

    # @task
    # def ping(self):
    #     self.client.get("/​WeatherForecast​/ping/")


# python -m pip install --upgrade pip
# python -m pip install --upgrade locust

# python -m locust -f main.py
