from loguru import logger
import time
import datetime as dt


def teste_01_win10toast():
    try:

        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast("Sample Notification", "Python is awesome!!!", duration=10)

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


def teste_02_win10toast():
    try:

        from win10toast import ToastNotifier

        toaster = ToastNotifier()
        toaster.show_toast("Hello World!!!", "Python is 10 seconds awsm!", icon_path="custom.ico", duration=10)

        toaster.show_toast("Example two", "This notification is in it's own thread!", icon_path=None, duration=5, threaded=True)
        
        # Wait for threaded notification to finish
        while toaster.notification_active(): 
            time.sleep(0.1)

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


def teste_03_winotify():
    try:

        from winotify import Notification, audio
        toast = Notification(app_id="windows app", title="Winotify Test Toast", msg="New Notification!", icon=r"C:\Users\chris\Desktop\CMS Python\CMS Teste Outros\CMS Teste Toast Notifications\icon.png", duration='long')
        toast.set_audio(audio.Mail, loop=False)
        toast.show()

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


def main():
    logger.info(f'Inicio') 
    try:

        
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        # teste_01_win10toast()
        # teste_02_win10toast()

        teste_03_winotify()
        
        result = 'ok'
        logger.info(f'{result=}') 

        # python main.py

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == '__main__':
    # logger.add("file_{time}.log", level='DEBUG', rotation="500 MB", compression="zip", enqueue=True, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
    main()

# python -m pip install --upgrade win10toast
# python -m pip install --upgrade pypiwin32
# python -m pip install --upgrade setuptools
# python -m pip install --upgrade winotify


# python main.py
