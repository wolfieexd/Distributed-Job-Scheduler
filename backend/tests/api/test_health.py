import pytest
from app.api.v1.endpoints.health import health_check

@pytest.mark.asyncio
async def test_health_check_endpoint(client):
    """
    Simple Test: Ensure the health endpoint returns 200 OK 
    and verifies that both the database and redis are healthy.
    """
    response = await client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["api"] == "ok"
    assert data["db"] == "ok"
    assert data["redis"] == "ok"
