# Dockerfile

# 1. Use a imagem base oficial do Python 3.12 (versão slim)
#    Isto é compatível com a sua versão local 3.12.3
FROM python:3.12-slim

# 2. Defina o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copie o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# 4. Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie o resto do código da sua aplicação para o diretório de trabalho
COPY . .

# 6. Exponha a porta que a aplicação vai rodar
EXPOSE 8000

# 7. Comando para iniciar a aplicação quando o container for executado
CMD ["uvicorn", "omnicopy.main:app", "--host", "0.0.0.0", "--port", "8000"]