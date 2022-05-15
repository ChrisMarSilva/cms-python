from loguru import logger
import datetime as dt
import time
import configparser
from ConfigParser import SafeConfigParser
import io
from dotenv import load_dotenv


def teste_01_criar_arqv():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'ServerAliveInterval': '45', 'Compression': 'yes', 'CompressionLevel': '9'}
    config['bitbucket.org'] = {}
    config['bitbucket.org']['User'] = 'hg'
    config['topsecret.server.com'] = {}
    topsecret  = config['topsecret.server.com']
    topsecret['Port'] = '50022'     # mutates the parser
    topsecret['ForwardX11'] = 'no'  # same here
    config['DEFAULT']['ForwardX11'] = 'yes'
    with open('example.ini', 'w') as configfile:
        config.write(configfile)

def teste_02_ler_arqv():

    #     # Load the configuration file
    # with open("config.ini") as f:
    #     sample_config = f.read()
    # config = ConfigParser.RawConfigParser(allow_no_value=True)
    # config.readfp(io.BytesIO(sample_config))

    # # List all contents
    # print("List all contents")
    # for section in config.sections():
    #     print("Section: %s" % section)
    #     for options in config.options(section):
    #         print(
    #             "x %s:::%s:::%s"
    #             % (options, config.get(section, options), str(type(options)))
    #         )
    

    parser = SafeConfigParser()
    parser.read('config.ini')
    print(parser.get('bug_tracker', 'url'))

    config = configparser.ConfigParser()
    logger.info(f'{config.sections()=}') 
    logger.info(f"{config.read('example.ini')=}") 
    logger.info(f'{config.sections()}')

    logger.info(f"{'bitbucket.org' in config=}") 
    logger.info(f"{'bytebong.com' in config=}") 
    logger.info(f"{config['bitbucket.org']['User']=}") 
    logger.info(f"{config['DEFAULT']['Compression']=}") 
    topsecret = config['topsecret.server.com']
    logger.info(f"{topsecret['ForwardX11']=}") 
    logger.info(f"{topsecret['Port']=}") 
    logger.info(f"{topsecret.getboolean('ForwardX11')=}") 
    logger.info(f"{config['bitbucket.org'].getboolean('ForwardX11')=}")
    logger.info(f"{config.getboolean('bitbucket.org', 'Compression')=}") 

    for key in config['bitbucket.org']:  
        logger.info(f'{key=}') 

def teste_03_ler_arqv():
    another_config = configparser.ConfigParser()
    another_config.read('example.ini')
    logger.info(f"{another_config['topsecret.server.com']['Port']}")
    another_config.read_string("[topsecret.server.com]\nPort=48484")
    logger.info(f"{another_config['topsecret.server.com']['Port']}")
    another_config.read_dict({"topsecret.server.com": {"Port": 21212}})
    logger.info(f"{another_config['topsecret.server.com']['Port']}")
    logger.info(f"{another_config['topsecret.server.com']['ForwardX11']}")

def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        teste_01_criar_arqv()
        teste_02_ler_arqv()
        teste_03_ler_arqv()

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade xxxxxxx
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
