from loguru import logger
import datetime as dt
import time
import os, sys
import subprocess, shlex


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()

        # os.system('date')
        # os.system('notepad')

        # path = "C:\\Program Files (x86)\\Notepad++\\notepad++.exe"
        # os.system(f'"{path}"')
        # subprocess.call([path])
        # subprocess.call(path, 'C:\\test.txt'])
        
        # os.chdir("C:\mysql\bin")
        # os.system("mysqldump -u root -p senha banco > c:\temp\dump.sql")

        # mycmd='"C:\\Program Files\\7-Zip\\7z" x "D:\\my archive.7z" -o"D:\\extract folder" -aou'
        # subprocess.run(shlex.split(mycmd))

        # result = subprocess.run([sys.executable, "-c", "print('ocean')"])
        result = subprocess.run([sys.executable, "-c", "print('ocean')"], capture_output=True, text=True)
        logger.info(f'{result=}') 
        logger.info(f'{result.stdout=}') 
        logger.info(f'{result.stderr=}') 
        logger.info('') 

        result = subprocess.run([sys.executable, "-c", "raise ValueError('oops')"], capture_output=True, text=True)
        logger.info(f'{result=}') 
        logger.info(f'{result.stdout=}') 
        logger.info(f'{result.stderr=}') 
        logger.info('') 

        result = subprocess.run('ls', shell=True, capture_output=True, text=True)
        logger.info(f'{result=}') 
        logger.info(f'{result.stdout=}') 
        logger.info(f'{result.stderr=}') 
        logger.info('') 


        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# python -m pip install --upgrade subprocess
# python -m pip install --upgrade pip

# python main.py
