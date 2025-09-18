FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "fastapi[all]" uvicorn

# Copiar código da aplicação
COPY . .

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expor porta
EXPOSE 80

# Comando de inicialização (corrigido)
CMD [ "uvicorn", "run:app", "--host", "0.0.0.0", "--port", "80" ]
