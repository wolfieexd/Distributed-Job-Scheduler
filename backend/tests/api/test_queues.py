import pytest

@pytest.mark.asyncio
async def test_create_queue(client):
    org_resp = await client.post("/api/v1/organizations/", json={"name": "Queue Org"})
    org_id = org_resp.json()["id"]
    proj_resp = await client.post("/api/v1/projects/", json={"name": "Queue Proj", "organization_id": org_id})
    proj_id = proj_resp.json()["id"]
    
    response = await client.post(
        "/api/v1/queues/", 
        json={"name": "high-priority", "priority": 1, "concurrency_limit": 50, "project_id": proj_id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "high-priority"
    assert data["concurrency_limit"] == 50

@pytest.mark.asyncio
async def test_get_queues_by_project(client):
    org_resp = await client.post("/api/v1/organizations/", json={"name": "Multi Queue Org"})
    org_id = org_resp.json()["id"]
    proj_resp = await client.post("/api/v1/projects/", json={"name": "Multi Queue Proj", "organization_id": org_id})
    proj_id = proj_resp.json()["id"]
    
    await client.post("/api/v1/queues/", json={"name": "q1", "priority": 1, "concurrency_limit": 10, "project_id": proj_id})
    await client.post("/api/v1/queues/", json={"name": "q2", "priority": 2, "concurrency_limit": 5, "project_id": proj_id})
    
    response = await client.get(f"/api/v1/queues/project/{proj_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
