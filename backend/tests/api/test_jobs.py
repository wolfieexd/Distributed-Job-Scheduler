import pytest

@pytest.mark.asyncio
async def test_submit_job_api(client, test_queue):
    payload = {"task": "send_email", "to": "user@example.com"}
    response = await client.post(
        f"/api/v1/queues/{str(test_queue.id)}/jobs", 
        json={"payload": payload, "max_retries": 3}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "queued"
    assert data["payload"]["task"] == "send_email"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_job_api(client, test_queue):
    post_resp = await client.post(
        f"/api/v1/queues/{str(test_queue.id)}/jobs", 
        json={"payload": {"a": 1}, "max_retries": 1}
    )
    job_id = post_resp.json()["id"]
    
    get_resp = await client.get(f"/api/v1/jobs/{job_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == job_id
    assert data["status"] == "queued"
