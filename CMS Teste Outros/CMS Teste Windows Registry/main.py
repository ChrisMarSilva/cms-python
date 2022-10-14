import datetime as dt
import time
import winreg

from loguru import logger


def teste_01():
    try:

        logger.info(f"xxxx   01   xxxxxx")

        # connecting to key in registry
        access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)

        # accessing the key to open the registry directories under
        access_key = winreg.OpenKey(
            access_registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion"
        )

        for n in range(20):
            try:
                x = winreg.EnumKey(access_key, n)
                logger.info(f"{x=}")
            except:
                break

        # logger.info(f"xxxx   02   xxxxxx")
        # key = winreg.OpenKey(
        #     winreg.HKEY_LOCAL_MACHINE,
        #     r"Software\Microsoft\Outlook Express",
        #     0,
        #     winreg.KEY_ALL_ACCESS,
        # )
        # winreg.QueryValueEx(key, "InstallRoot")
        # Falha Geral: "[WinError 5] Acesso negado"

        logger.info(f"xxxx   03   xxxxxx")

        keyVal = r"SOFTWARE\Microsoft\Internet Explorer\Main"
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, keyVal, 0, winreg.KEY_ALL_ACCESS
            )
        except:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, keyVal)
        winreg.SetValueEx(
            key, "Start Page", 0, winreg.REG_SZ, "https://www.blog.pythonlibrary.org/"
        )
        winreg.CloseKey(key)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_02():
    try:

        path = winreg.HKEY_CURRENT_USER

        software = winreg.OpenKey(path, r"SOFTWARE\\")
        new_key = winreg.CreateKey(software, "NeuralNine")

        winreg.SetValueEx(new_key, "myvalue1", 0, winreg.REG_SZ, "Hello World")
        winreg.SetValueEx(new_key, "myvalue2", 0, winreg.REG_SZ, "123465")

        if new_key:
            winreg.CloseKey(new_key)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_03():
    try:

        path = winreg.HKEY_CURRENT_USER

        neuralnine = winreg.OpenKey(path, r"SOFTWARE\\NeuralNine\\")

        myvalue1 = winreg.QueryValueEx(neuralnine, "myvalue1")
        myvalue2 = winreg.QueryValueEx(neuralnine, "myvalue2")

        if neuralnine:
            winreg.CloseKey(neuralnine)

        logger.info(f"{myvalue1[0]=}")
        logger.info(f"{myvalue2[0]=}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    start_time = time.perf_counter()
    logger.info(f"Inicio")
    try:

        # teste_01()
        # teste_02()
        teste_03()

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == "__main__":
    main()

# python -m pip install --upgrade pip
# python -m pip install --upgrade xxxx

# C:/Python310/python.exe "C:\Users\chris\Desktop\CMS Python\CMS Teste Outros\CMS Teste Windows Registry/main.py"

# cd "C:\Users\chris\Desktop\CMS Python\CMS Teste Outros\CMS Teste Windows Registry"
# python main.py
