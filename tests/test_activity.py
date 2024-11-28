"Testes para activity"

from http import HTTPStatus
from fastapi.testclient import TestClient
from src.schemas.activity_schema import ActivityDB
from src.schemas.client_schema import ClientDB
from src.schemas.project_schema import ProjectDB

class TestActivity:
    "Objeto de testes para activity"
    def test_create_activity(self, client: TestClient, client_instance: ClientDB):
        "Testa a criação de um activity"
        test_activity = {
            "name": "testClient",
            "client_id": client_instance.id,
            "status": "testStatus"
        }
        response = client.post("/activity", json=test_activity)
        assert response.status_code == HTTPStatus.CREATED
        assert response.json().get("name") == test_activity.get("name")
        assert response.json().get("client_id") == client_instance.id

    def test_get_all_activity(self, client: TestClient):
        "Testa o retorno das activity"
        response = client.get("/activity").json()
        assert isinstance(response, list)

    def test_get_specific_activity(self, client: TestClient, activity: ActivityDB):
        "Testa o retorno de uma activity"
        response = client.get("/activity/", params={"activity_id": activity.id}).json()
        assert response.get("name") == activity.name

    def test_get_specific_activity_not_found(self, client: TestClient):
        "Testa o retorno de uma activity que não existe"
        response = client.get("/activity/", params={"activity_id": -1})
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_get_activity_from_client(self, client: TestClient, activity: ActivityDB):
        "Testa o retorno das activity de um client"
        response = client.get("/activity/", params={"client_id": activity.client_id})
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(), list)
        assert ActivityDB(**response.json()[0]) == activity

    def test_get_activity_from_client_not_found(self, client: TestClient):
        "Testa o retorno das activity de um client que não existe"
        response = client.get("/activity/", params={"client_id": -1})
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_get_activity_from_project(self, client: TestClient, activity: ActivityDB,
                                        project: ProjectDB):
        "Testa o retorno das activity de um project"
        response = client.get("/activity/", params={"project_id": project.id})
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(), list)
        assert ActivityDB(**response.json()[0]) == activity

    def test_get_activity_from_project_not_found(self, client: TestClient):
        "Testa o retorno das activity de um client que não existe"
        response = client.get("/activity/", params={"project_id": -1})
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_put_activity(self, client: TestClient, activity: ActivityDB):
        "Testa a atualização de uma activity"
        new_data = {
            "name": "NEW",
            "client_id": activity.client_id,
            "status": "NEW"
        }
        response = client.put(f"/activity/{activity.id}", json=new_data).json()
        assert response.get("name") == new_data['name']
        assert response.get("client_id") == activity.client_id

    def test_put_activity_not_found(self, client: TestClient):
        "Testa a atualização de uma activity que não existe"
        new_data = {
            "name": "NEW",
            "client_id": 1,
            "status": "NEW"
        }
        response = client.put(f"/activity/{-1}", json=new_data)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_activity(self, client: TestClient, activity: ActivityDB):
        "Testa a exclusão de um activity"
        response = client.delete(f"/activity/{activity.id}")
        assert response.status_code == HTTPStatus.OK

    def test_delete_activity_not_found(self, client: TestClient):
        "Testa a exclusão de um activity que não existe"
        response = client.delete(f"/activity/{-1}")
        assert response.status_code == HTTPStatus.NOT_FOUND
