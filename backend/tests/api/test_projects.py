import pytest

@pytest.mark.asyncio
async def test_create_project(client):
    # 1. Create Org
    org_resp = await client.post("/api/v1/organizations/", json={"name": "Proj Org"})
    org_id = org_resp.json()["id"]
    
    # 2. Create Project
    response = await client.post("/api/v1/projects/", json={"name": "Alpha Project", "organization_id": org_id})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alpha Project"
    assert data["organization_id"] == org_id
    assert "id" in data

@pytest.mark.asyncio
async def test_create_project_invalid_org(client):
    response = await client.post("/api/v1/projects/", json={"name": "Invalid", "organization_id": "00000000-0000-0000-0000-000000000000"})
    assert response.status_code == 404
