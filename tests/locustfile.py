from locust import HttpUser, task


class MazanunciosLocustTasks(HttpUser):
    @task
    def test_get_user(self):
        auth_header = {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiamJzZzk3Iiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNjA5MDk3NjE2fQ.pIe1K-p0P4y5ZsirY6YCYjbm-w1T3wchaG0Ud2E7SFk"
        }
        self.client.get("/v1/user/jbsg", headers=auth_header)