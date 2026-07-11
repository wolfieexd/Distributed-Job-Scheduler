import pytest

@pytest.mark.asyncio
async def test_create_organization(client):
    response = await client.post("/api/v1/organizations/", json={"name": "Acme Corp"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Acme Corp"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_organizations(client):
    await client.post("/api/v1/organizations/", json={"name": "Org 1"})
    response = await client.get("/api/v1/organizations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Org 1"
