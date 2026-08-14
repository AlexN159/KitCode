from fastapi.testclient import TestClient

from backend import exercise_bank, main


def test_complete_local_practice_workflow(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DATA_FILE", tmp_path / "progress.json")
    api = TestClient(main.app)

    health = api.get("/api/health")
    assert health.status_code == 200
    assert health.json()["exercise_count"] >= 140

    catalog = api.get("/api/exercises?difficulty=Easy&q=parity").json()
    assert catalog["total"] >= 1
    assert all("solution" not in item and "hidden_tests" not in item for item in catalog["exercises"])

    exercise_id = "number-001"
    detail = api.get(f"/api/exercises/{exercise_id}").json()
    assert detail["starter_code"]
    assert detail["examples"]
    assert "solution" not in detail and "hidden_tests" not in detail

    run = api.post("/api/run", json={"code": "n = int(input())\nprint('even' if n % 2 == 0 else 'odd')", "input": "8\n"}).json()
    assert run["ok"] is True and run["stdout"].strip() == "even"

    trace = api.post("/api/trace", json={"code": "value = 2\nanswer = value * 3\nprint(answer)"}).json()
    assert trace["ok"] is True
    assert any(step["source"] == "answer = value * 3" for step in trace["steps"])

    solution = exercise_bank.EXERCISES[exercise_id]["solution"]
    submission = api.post("/api/submit", json={"exercise_id": exercise_id, "code": solution}).json()
    assert submission["accepted"] is True
    assert submission["passed"] == submission["total"]
    hidden = [result for result in submission["results"] if result["visibility"] == "hidden"]
    assert hidden and all(result["input"] is None and "expected_output" not in result for result in hidden)
    assert api.get(f"/api/progress/{exercise_id}").json()["status"] == "completed"


def test_static_app_and_request_limits_are_packaged():
    api = TestClient(main.app)
    page = api.get("/")
    assert page.status_code == 200
    assert "KitCode" in page.text

    too_slow = api.post("/api/run", json={"code": "print('x')", "timeout_seconds": 11})
    too_many_steps = api.post("/api/trace", json={"code": "print('x')", "max_steps": 501})
    assert too_slow.status_code == 422
    assert too_many_steps.status_code == 422


def test_ai_show_mode_is_a_supported_optional_capability(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("KITCODE_COACH_PROVIDER", raising=False)
    monkeypatch.setattr(main, "_codex_status", lambda: (None, False, "unavailable for test"))
    api = TestClient(main.app)
    response = api.post(
        "/api/ai/coach",
        json={"exercise_id": "number-001", "code": "print('todo')", "question": "What should I type next?", "mode": "show"},
    )
    assert response.status_code == 503
    assert "AI Coach settings" in response.json()["detail"]
