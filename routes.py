from flask import Blueprint, request, jsonify
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/v1')

@tasks_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'message': 'DevOps Python API está funcionando!',
        'version': '1.0.0'
    }), 200

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Listar todas as tarefas"""
    try:
        tasks = Task.query.all()
        return jsonify({
            'success': True,
            'tasks': [task.to_dict() for task in tasks],
            'count': len(tasks)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Criar nova tarefa"""
    try:
        data = request.get_json()
        
        # Validação
        if not data or not data.get('title'):
            return jsonify({
                'success': False, 
                'error': 'Título é obrigatório'
            }), 400
        
        # Criar tarefa
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium')
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarefa criada com sucesso',
            'task': task.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Obter tarefa específica"""
    try:
        task = Task.query.get_or_404(task_id)
        return jsonify({
            'success': True,
            'task': task.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Atualizar tarefa"""
    try:
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        
        # Atualizar campos
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            task.completed = data['completed']
        if 'priority' in data:
            task.priority = data['priority']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarefa atualizada com sucesso',
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Deletar tarefa"""
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarefa deletada com sucesso'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
