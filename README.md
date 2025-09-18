# urban-octo-engine
projeto ultimo modulo devops

## Testes Unitários

Este projeto possui uma suite completa de testes unitários para garantir a qualidade do código.

### Executando os testes

```bash
# Instalar dependências
pip install -r requirements.txt

# Definir PYTHONPATH
export PYTHONPATH=$PWD

# Executar todos os testes
pytest

# Executar com verbosidade
pytest -v

# Executar com cobertura de código
pytest --cov=app --cov-report=term-missing
```

### Estrutura dos testes

- `tests/test_routes.py` - Testes das rotas da API
- `tests/test_models.py` - Testes dos modelos de dados
- `tests/test_integration.py` - Testes de integração e cenários completos

### Cobertura atual

O projeto mantém **98% de cobertura de código** com 32 testes unitários cobrindo:

- ✅ Endpoints da API REST (health, CRUD de tarefas)
- ✅ Modelos de dados (Task)
- ✅ Validações e tratamento de erros
- ✅ Cenários de integração completos
- ✅ Casos extremos e edge cases

### CI/CD

Os testes são executados automaticamente via GitHub Actions em:
- Cada push para a branch main
- Cada Pull Request criado
