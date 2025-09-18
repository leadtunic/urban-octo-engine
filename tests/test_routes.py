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

    def test_create_task_with_minimal_data(self, client):
        """Test creating task with only required title field"""
        task_data = {'title': 'Minimal Task'}
        response = client.post('/api/v1/tasks',
                             data=json.dumps(task_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['task']['title'] == 'Minimal Task'
        assert data['task']['description'] == ''  # API defaults to empty string
        assert data['task']['priority'] == 'medium'  # Should default to medium
        assert data['task']['completed'] is False  # Should default to False

    def test_update_nonexistent_task(self, client):
        """Test updating a task that doesn't exist"""
        update_data = {'title': 'Updated Title'}
        response = client.put('/api/v1/tasks/99999',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['success'] is False

    def test_get_nonexistent_task(self, client):
        """Test getting a task that doesn't exist"""
        response = client.get('/api/v1/tasks/99999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False

    def test_delete_nonexistent_task(self, client):
        """Test deleting a task that doesn't exist"""
        response = client.delete('/api/v1/tasks/99999')
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['success'] is False

    def test_health_endpoint_details(self, client):
        """Test health endpoint returns all expected fields"""
        response = client.get('/api/v1/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check all expected fields are present
        expected_fields = ['status', 'message', 'version']
        for field in expected_fields:
            assert field in data
        
        # Check specific values
        assert data['status'] == 'healthy'
        assert 'DevOps' in data['message']
        assert data['version'] == '1.0.0'

    def test_tasks_with_different_priorities(self, client):
        """Test creating tasks with different priority levels"""
        priorities = ['low', 'medium', 'high']
        created_tasks = []
        
        for priority in priorities:
            task_data = {
                'title': f'Task with {priority} priority',
                'priority': priority
            }
            response = client.post('/api/v1/tasks',
                                 data=json.dumps(task_data),
                                 content_type='application/json')
            assert response.status_code == 201
            created_tasks.append(json.loads(response.data)['task'])
        
        # Verify all tasks were created with correct priorities
        for i, priority in enumerate(priorities):
            assert created_tasks[i]['priority'] == priority

    def test_task_completion_toggle(self, client, sample_task):
        """Test toggling task completion status"""
        # Initially should be False
        response = client.get(f'/api/v1/tasks/{sample_task}')
        task = json.loads(response.data)['task']
        assert task['completed'] is False
        
        # Mark as completed
        response = client.put(f'/api/v1/tasks/{sample_task}',
                            data=json.dumps({'completed': True}),
                            content_type='application/json')
        assert response.status_code == 200
        task = json.loads(response.data)['task']
        assert task['completed'] is True
        
        # Mark as incomplete again
        response = client.put(f'/api/v1/tasks/{sample_task}',
                            data=json.dumps({'completed': False}),
                            content_type='application/json')
        assert response.status_code == 200
        task = json.loads(response.data)['task']
        assert task['completed'] is False
