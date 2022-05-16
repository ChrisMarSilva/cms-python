# Projetos para teste em Pyhon

## Dependências

Para instalar as dependências, utilize o pip com o arquivo requirements.txt

```
pip install -r requirements.txt
```

ou instale as dependencias com o comando abaixo:

```
fastapi uvicorn python-multipart requests fonttools pymupdf pytest pytest-cov
```

## Testes

Para rodar os teste, utilize o comando:

```
pytest --cov=api tests/
```