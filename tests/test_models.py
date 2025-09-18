import pytest
from datetime import datetime
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

class TestTaskModel:
    def test_task_creation_with_defaults(self, app):
        """Test task creation with default values"""
        with app.app_context():
            task = Task(title='Test Task')
            db.session.add(task)
            db.session.commit()
            
            assert task.id is not None
            assert task.title == 'Test Task'
            assert task.description is None  # Default is None, not empty string
            assert task.completed is False
            assert task.priority == 'medium'
            assert task.created_at is not None
            assert task.updated_at is not None

    def test_task_creation_with_all_fields(self, app):
        """Test task creation with all fields specified"""
        with app.app_context():
            task = Task(
                title='Complete Task',
                description='This is a complete task description',
                priority='high',
                completed=True
            )
            db.session.add(task)
            db.session.commit()
            
            assert task.title == 'Complete Task'
            assert task.description == 'This is a complete task description'
            assert task.priority == 'high'
            assert task.completed is True

    def test_task_to_dict_method(self, app):
        """Test the to_dict method returns correct format"""
        with app.app_context():
            task = Task(
                title='Dict Test Task',
                description='Testing to_dict method',
                priority='low',
                completed=True
            )
            db.session.add(task)
            db.session.commit()
            
            task_dict = task.to_dict()
            
            assert isinstance(task_dict, dict)
            assert task_dict['title'] == 'Dict Test Task'
            assert task_dict['description'] == 'Testing to_dict method'
            assert task_dict['priority'] == 'low'
            assert task_dict['completed'] is True
            assert 'id' in task_dict
            assert 'created_at' in task_dict
            assert 'updated_at' in task_dict
            assert isinstance(task_dict['created_at'], str)  # Should be ISO format string

    def test_task_repr_method(self, app):
        """Test the __repr__ method returns correct string representation"""
        with app.app_context():
            task = Task(title='Repr Test Task')
            db.session.add(task)
            db.session.commit()
            
            repr_str = repr(task)
            assert f'<Task {task.id}: Repr Test Task>' == repr_str

    def test_task_update_timestamps(self, app):
        """Test that updated_at timestamp changes when task is modified"""
        with app.app_context():
            task = Task(title='Timestamp Test')
            db.session.add(task)
            db.session.commit()
            
            original_updated_at = task.updated_at
            
            # Small delay to ensure timestamp difference
            import time
            time.sleep(0.1)
            
            # Update the task
            task.title = 'Updated Timestamp Test'
            db.session.commit()
            
            assert task.updated_at > original_updated_at

    def test_task_priority_values(self, app):
        """Test different priority values are accepted"""
        with app.app_context():
            priorities = ['low', 'medium', 'high']
            
            for priority in priorities:
                task = Task(title=f'Task with {priority} priority', priority=priority)
                db.session.add(task)
                db.session.commit()
                
                assert task.priority == priority
                
                # Clean up for next iteration
                db.session.delete(task)
                db.session.commit()

    def test_task_with_none_description(self, app):
        """Test task creation with None description"""
        with app.app_context():
            task = Task(title='No Description Task', description=None)
            db.session.add(task)
            db.session.commit()
            
            assert task.description is None
            task_dict = task.to_dict()
            assert task_dict['description'] is None