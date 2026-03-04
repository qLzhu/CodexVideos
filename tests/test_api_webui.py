from fastapi.testclient import TestClient

from app.api.main import app


def test_health_and_version() -> None:
    client = TestClient(app)
    assert client.get('/health').status_code == 200
    assert client.get('/version').status_code == 200


def test_webui_endpoints() -> None:
    client = TestClient(app)

    assert client.get('/api/projects').status_code == 200
    templates = client.get('/api/templates')
    assert templates.status_code == 200
    first_template = templates.json()['items'][0]['path']

    rendered = client.post('/api/templates/render', json={
        'template': first_template,
        'variables': {
            'project_name': '测试项目',
            'genre': '悬疑',
            'target_audience': '18+',
            'core_conflict': '冲突',
        },
    })
    assert rendered.status_code == 200
    assert '测试项目' in rendered.json()['rendered']

    configs = client.get('/api/jobs/configs').json()['items']
    run = client.post('/api/jobs/run', json={'job_config': configs[0], 'dry_run': True})
    assert run.status_code == 200

    assert client.get('/api/jobs').status_code == 200
    assert client.get('/api/reports/qc').status_code == 200
