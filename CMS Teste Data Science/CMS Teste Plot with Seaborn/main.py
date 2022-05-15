from loguru import logger
import datetime as dt
import time
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from dotenv import load_dotenv


def teste_01_seaborn():
    try:

        # logger.info(f'{sns.get_dataset_names()}') 
        #  ['anagrams', 'anscombe', 'attention', 'brain_networks', 'car_crashes', 'diamonds', 'dots', 
        #   'exercise', 'flights', 'fmri', 'gammas', 'geyser', 'iris', 'mpg', 'penguins', 'planets', 
        #  'taxis', 'tips', 'titanic']

        tips = sns.load_dataset("tips")
        # logger.info(f'{tips.head(2)}')
        # logger.info(f'{tips.corr()}')
        # logger.info(f'{tips.columns}')
        # Index(['total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size'], dtype='object') 

        iris = sns.load_dataset("iris")
        # logger.info(f'{iris.head(2)}') 
        # logger.info(f'{iris.corr()}')
        # logger.info(f'{iris.columns}') 
        # Index(['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'], dtype='object')

        titanic = sns.load_dataset("titanic")
        # logger.info(f'{titanic.head(2)}') 
        # logger.info(f'{titanic.corr()}')
        # logger.info(f'{titanic.columns}') 
        # Index(['survived', 'pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked', 'class', 'who', 'adult_male', 'deck', 'embark_town', 'alive', 'alone'], dtype='object')

        planets = sns.load_dataset("planets")
        # logger.info(f'{planets.head(2)}') 
        # logger.info(f'{planets.corr()}')
        # logger.info(f'{planets.columns}') 
        # Index(['method', 'number', 'orbital_period', 'mass', 'distance', 'year'], dtype='object')

        diamonds = sns.load_dataset("diamonds")
        # logger.info(f'{diamonds.head(2)}') 
        # logger.info(f'{diamonds.corr()}')
        # logger.info(f'{diamonds.columns}') 
        # Index(['carat', 'cut', 'color', 'clarity', 'depth', 'table', 'price', 'x', 'y', 'z'], dtype='object')

        # sns.set_theme(style="darkgrid")
        # sns.set_theme(style="white", context="talk")
        # sns.set_theme(style="ticks", palette="pastel")
        # sns.set_theme(style="whitegrid")
        # sns.set_theme(style="white")
        # sns.set_theme(style="ticks")
        sns.set_theme()

        sns.scatterplot(x="tip", y="total_bill", data=tips, hue="day", size="size", sizes=(30, 60), palette="ch:r=-.2,d=.3_r") # palette="YlGnBu" 
        # sns.histplot(tips, x="tip", kde=True, bins=15, multiple="stack", palette="light:m_r", edgecolor=".3", linewidth=.5, log_scale=True)
        # sns.displot(tips, x='tip', kde=True, bins=15, facet_kws=dict(margin_titles=True))
        # sns.barplot(x="sex", y="tip", data=tips, palette="deep")
        # sns.boxplot(x="day", y="tip", data=tips, hue="sex", palette="YlGnBu") # palette=["m", "g"]
        # sns.boxplot(x="day", y="total_bill", data=tips, hue="sex", palette="YlGnBu")
        # sns.stripplot(x="day", y="tip", data=tips, hue="sex", palette="YlGnBu", dodge=True)
        # sns.jointplot(x="tip", y="total_bill", data=tips, kind="kde", shade=True, cmap="YlGnBu", color="#4CB391") #kind="reg"/"hex"/"kde"
        # sns.pairplot(tips, hue="tip")
        # sns.pairplot(titanic.select_dtypes(['number']), hue='pclass')
        # sns.heatmap(titanic.corr(), annot=True, cmap="coolwarm") # cmap=YlGnBu/coolwarm/icefire
        # sns.clustermap(iris.drop("species", axis=1))
        plt.show()

        return "Ok"

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        teste_01_seaborn()
        
        # python main.py

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade seaborn 
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
