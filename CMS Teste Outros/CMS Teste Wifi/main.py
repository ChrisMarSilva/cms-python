from loguru import logger
import datetime as dt
import time
import os


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        # Command # use c to run process one by one # use k to run one command only      

        # Show all wifi connected before
        # os.system('cmd /c "netsh wlan show profile"')  
        # Todos os Perfis de Usuários: ROS_5G
        # Todos os Perfis de Usuários: PONGA_5G
        # Todos os Perfis de Usuários: PONGA 5G
        # Todos os Perfis de Usuários: Martins Oficial_5G
        # Todos os Perfis de Usuários: Martins Oficial
        # Todos os Perfis de Usuários: POCO X3 Pro
        # Todos os Perfis de Usuários: Martins_5G
        # Todos os Perfis de Usuários: Martins
        # Todos os Perfis de Usuários: Heloisa
        # Todos os Perfis de Usuários: CMS Mi Phone

        # Select any one of profile
        # os.system('cmd /c "netsh wlan show profile "Martins_5G" key=clear"') 

        # Perfil Martins_5G na interface Wi-Fi 2:
        # =======================================================================

        # Aplicado: Todos os Perfis de Usuários

        # Informações do perfil
        # -------------------
        #     Versão                : 1
        #     Tipo                   : LAN sem Fio
        #     Nome                   : Martins_5G
        #     Opções de controle        :
        #         Modo de conexão    : Conectar automaticamente
        #         Transmissão da rede  : conectar somente se esta rede estiver transmitindo
        #         Alternância automática : Não alternar para outra rede
        #         Uso de MAC Aleatório: Desabilitado

        # Configurações de conectividade
        # ---------------------
        #     Número de SSIDs        : 1
        #     Nome SSID              : "Martins_5G"
        #     Tipo de rede           : Infraestrutura
        #     Tipo de Rádio               : [ Qualquer Tipo de Rádio ]
        #     Extensão do fornecedor       : Não presente

        # Configurações de segurança
        # -----------------
        #     Autenticação         : WPA2-Personal
        #     Codificação         : CCMP
        #     Autenticação         : WPA2-Personal
        #     Codificação         : GCMP
        #     Chave de segurança           : Presente
        #     Conteúdo da Chave            : maite@15

        # Configurações de custo
        # -------------
        #     Custo                   : Irrestrito
        #     Congestionado              : Não
        #     Limite de Dados Aproximado: Não
        #     Limite de Dados Excedido        : Não
        #     Roaming                : Não
        #     Origem de Custo            : Padrão

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# python -m pip install --upgrade xxxxxxx

# python main.py
