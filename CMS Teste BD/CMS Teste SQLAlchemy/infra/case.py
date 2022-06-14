

class AlgumaCoisa:
    def __enter__(self):
        print('Estou Entrando')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Estou Saindo')


with AlgumaCoisa() as ola:
    try:
        raise
        print('Estou no Meio')
    except Exception as e:
        print(f'Estou no Erro: "{e}"')
