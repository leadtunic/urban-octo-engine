import pytest
import json
from app import create_app, db
from app.models import Task

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('app.config.TestingConfig')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_task(app):
    with app.app_context():
        task = Task(title='Teste DevOps', description='Tarefa de teste')
        db.session.add(task)
        db.session.commit()
        task_id = task.id  # Pegue o id antes de sair do contexto
        yield task_id
        # Limpeza: remove a task criada após o teste (opcional)
        Task.query.filter_by(id=task_id).delete()
        db.session.commit()

class TestHealthCheck:
    def test_health_endpoint(self, client):
        response = client.get('/api/v1/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'

class TestTaskAPI:
    def test_get_empty_tasks(self, client):
        response = client.get('/api/v1/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 0

    def test_create_task(self, client):
        task_data = {
            'title': 'Nova Tarefa DevOps',
            'description': 'Implementar CI/CD',
            'priority': 'high'
        }
        response = client.post('/api/v1/tasks', 
                             data=json.dumps(task_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['task']['title'] == task_data['title']

    def test_get_task_by_id(self, client, sample_task):
        response = client.get(f'/api/v1/tasks/{sample_task}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['task']['title'] == 'Teste DevOps'

    def test_update_task(self, client, sample_task):
        update_data = {'completed': True, 'priority': 'low'}
        response = client.put(f'/api/v1/tasks/{sample_task}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['task']['completed'] is True

    def test_delete_task(self, client, sample_task):
        response = client.delete(f'/api/v1/tasks/{sample_task}')
        assert response.status_code == 200
        
        # Verificar se foi deletado
        get_response = client.get(f'/api/v1/tasks/{sample_task}')
        assert get_response.status_code == 404

    def test_create_task_without_title(self, client):
        task_data = {'description': 'Sem título'}
        response = client.post('/api/v1/tasks',
                             data=json.dumps(task_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
