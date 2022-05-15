from loguru import logger
import datetime as dt
import time
import re
import pandas as pd
from dotenv import load_dotenv


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        # https://www.w3schools.com/python/python_regex.asp

        # Metacharacters

        # Character	Description	Example	Try it
        # []	A set of characters	"[a-m]"	
        # \	Signals a special sequence (can also be used to escape special characters)	"\d"	
        # .	Any character (except newline character)	"he..o"	
        # ^	Starts with	"^hello"	
        # $	Ends with	"planet$"	
        # *	Zero or more occurrences	"he.*o"	
        # +	One or more occurrences	"he.+o"	
        # ?	Zero or one occurrences	"he.?o"	
        # {}	Exactly the specified number of occurrences	"he.{2}o"	
        # |	Either or	"falls|stays"	
        # ()	Capture and group

        # Special Sequences

        # Character	Description	Example	Try it
        # \A	Returns a match if the specified characters are at the beginning of the string	"\AThe"	
        # \b	Returns a match where the specified characters are at the beginning or at the end of a word
        # (the "r" in the beginning is making sure that the string is being treated as a "raw string")	r"\bain"
        # r"ain\b"	
        # \B	Returns a match where the specified characters are present, but NOT at the beginning (or at the end) of a word
        # (the "r" in the beginning is making sure that the string is being treated as a "raw string")	r"\Bain"
        # r"ain\B"	
        # \d	Returns a match where the string contains digits (numbers from 0-9)	"\d"	
        # \D	Returns a match where the string DOES NOT contain digits	"\D"	
        # \s	Returns a match where the string contains a white space character	"\s"	
        # \S	Returns a match where the string DOES NOT contain a white space character	"\S"	
        # \w	Returns a match where the string contains any word characters (characters from a to Z, digits from 0-9, and the underscore _ character)	"\w"	
        # \W	Returns a match where the string DOES NOT contain any word characters	"\W"	
        # \Z	Returns a match if the specified characters are at the end of the string

        # Sets

        # Set	Description	Try it
        # [arn]	Returns a match where one of the specified characters (a, r, or n) are present	
        # [a-n]	Returns a match for any lower case character, alphabetically between a and n	
        # [^arn]	Returns a match for any character EXCEPT a, r, and n	
        # [0123]	Returns a match where any of the specified digits (0, 1, 2, or 3) are present	
        # [0-9]	Returns a match for any digit between 0 and 9	
        # [0-5][0-9]	Returns a match for any two-digit numbers from 00 and 59	
        # [a-zA-Z]	Returns a match for any character alphabetically between a and z, lower case OR upper case	
        # [+]	In sets, +, *, ., |, (), $,{} has no special meaning, so [+] means: return a match for any + character in the string


        txt = "The rain in Spain"

        x = re.search("^The.*Spain$", txt)
        logger.info(f'#01 - {x=}') 

        x = re.findall("ai", txt)
        logger.info(f'#02 - {x=}') 
        x = re.findall("Portugal", txt)
        logger.info(f'#03 - {x=}') 
        
        x = re.search("\s", txt)
        logger.info(f'#04 - {x.start()=}') 
        x = re.search("Portugal", txt)
        logger.info(f'#05 - {x=}') 

        x = re.split("\s", txt)
        logger.info(f'#06 - {x=}') 
        x = re.split("\s", txt, 1)
        logger.info(f'#07 - {x=}') 

        x = re.sub("\s", "9", txt)
        logger.info(f'#08 - {x=}') 
        x = re.sub("\s", "9", txt, 2)
        logger.info(f'#09 - {x=}') 

        x = re.search("ai", txt)
        logger.info(f'#10 - {x=}') 
        logger.info(f'#11 - {x.string=}') 

        x = re.search(r"\bS\w+", txt)  # A expressão regular procura qualquer palavra que comece com "S" maiúsculo
        logger.info(f'#12 - {x.span()=}') 
        logger.info(f'#13 - {x.string=}') 
        logger.info(f'#14 - {x.group()=}') 

        # --------------

        x = re.search(pattern="Spain$", string=txt) # termina com 
        logger.info(f'#15 - {x=}') 
        
        x = re.search(pattern="^The", string=txt) # inicia com 
        logger.info(f'#16 - {x=}') 
        
        x = re.search(pattern="rain", string=txt) # contem 
        logger.info(f'#17 - {x=}') 
        
        # --------------

        train = pd.read_csv(filepath_or_buffer=r'C:\Users\chris\Desktop\CMS Python\CMS Teste Outros\CMS Teste Regex\train_titanic.csv')
        test = pd.read_csv(filepath_or_buffer=r'C:\Users\chris\Desktop\CMS Python\CMS Teste Outros\CMS Teste Regex\test_titanic.csv')
        df = pd.concat(objs=(train, test))
        df.reset_index(drop=True, inplace=True)

        # logger.info(f"{df.info()}") 
        # logger.info(f"{df}") 
        # logger.info(f"{df[df['Name'].str.contains('Mr.')]}") 
        # logger.info(f"{df[df['Name'].str.contains('Mr.|Miss')]}") 
        # logger.info(f"{df[df['Name'].str.contains('Allen')]}") 
        # logger.info(f"{df[df['Name'].str.contains('^Allen')]}") 
        # logger.info(f"{df[df['Name'].str.contains('Henry$')]}") 
        # logger.info(f"{df[df['Name'].str.contains('^Allen.*Henry$')]}") 
        # logger.info(f"{df[df['Name'].str.contains('^A|y$')]}") 
        # logger.info(f"{df[df['Ticket'].str.contains('^[0-9]')]}") 
        # logger.info(f"{df[df['Ticket'].str.contains('^[a-zA-Z]')]}") 
        # logger.info(f"{df[df['Ticket'].str.contains('[0-9]')==False]}") 

        # trocar dados
        idx = df[df['Name'].str.contains('Henry$')].index
        df.loc[idx, 'Name'] = df.loc[idx, 'Name'].str.replace('Henry', 'Freitas')
        logger.info(f"{df[df['Name'].str.contains('Freitas$')]}") 

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
