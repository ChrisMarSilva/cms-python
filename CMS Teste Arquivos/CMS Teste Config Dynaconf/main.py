from loguru import logger
import datetime as dt
import time
from dynaconf import Dynaconf, Validator
from dotenv import load_dotenv


def main():
    try:

        # https://www.dynaconf.com/

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        settings = Dynaconf(
            settings_files=[                      # Paths or globs to any toml|yaml|ini|json|py
                "configs/default_settings.toml",  # a file for default settings
                "configs/settings.toml",          # a file for main settings
                "configs/.secrets.toml"           # a file for sensitive data (gitignored)
            ],
            environments=True,                    # Enable layered environments
                                                # (sections on config file for development, production, testing)

            load_dotenv=True,                     # Load envvars from a file named `.env`
                                                # TIP: probably you don't want to load dotenv on production environments
                                                #      pass `load_dotenv={"when": {"env": {"is_in": ["development"]}}}

            envvar_prefix="DYNACONF",             # variables exported as `DYNACONF_FOO=bar` becomes `settings.FOO == "bar"`
            env_switcher="ENV_FOR_DYNACONF",      # to switch environments `export ENV_FOR_DYNACONF=production`

            dotenv_path="configs/.env"            # custom path for .env file to be loaded
        )

        # -- Lets add some Validation and Defaults
        settings.validators.register(
            # Must there be a NAME defined
            # under [development] env (run mode) the name should be equal to "Bruno"
            Validator("NAME", must_exist=True, eq="Bruno", env="development"),
            # under [production] the name should be equal to "Root"
            Validator("NAME", must_exist=True, eq="Root", env="production"),
            # there must be a DB dictionary, having a PORT as integer
            Validator("DB.PORT", must_exist=True, is_type_of=int),
            # under the env [production] its value must be >=8000 and <=9000
            Validator("DB.PORT",gte=8000, lte=9000, env="production"),

            # Defaults can also be provided here (however in the [default] section of files is better)
            Validator("DB.USER", default="admin"),
            Validator("FACTOR", default=8),

            # Defaults can also be used to define computed values if default=a_callable
            Validator("DB.TIMEOUT", default=lambda _settings, _value: 24 * 60 * _settings.factor),

            # You can compound validators for better meaning
            Validator("DB.USER", ne="pgadmin") & Validator("DB.USER", ne="master"),

            # You can validate a key ONLY IF other exits
            # Password must be defined if user is defined
            Validator("DB.PASSWORD", must_exist=True, when=Validator("DB.USER", must_exist=True)),
        )

        settings.validators.validate()

                
        # -- Access the variables using dot notation
        print(settings.NAME)  # outputs: Bruno

        # -- You can also access using dict like notation
        print(settings["NAME"])  # outputs: Bruno

        # -- Access is case insensitive so you achieve the same with
        print(settings.name)  # outputs: Bruno
        print(settings["name"])  # outputs: Bruno

        # If you are not sure that a value exists, use dict like .get Lookup
        #                      KEY          DEFAULT Value if doesn't exist
        print(settings.get("DoesThisExist", "looks like doesn't exist"))  # outputs: looks like doesn't exist


        # You can use Dynaconf to populate an objet
        class Person:
            name: str
            db: dict


        p = Person()

        settings.populate_obj(p, keys=["NAME", "DB"])  # only first level keys, all upper case.

        print(p.NAME)        # outputs: Bruno
        print(p.DB["PORT"])  # outputs: 8181


        # You can use dot notation to get nested values
        print(settings.db.port)                         # outputs: 8181
        print(settings['db.server'])                    # outputs: Bruno.com
        print(settings.get("db.password", "changeme"))  # outputs: NewSecret789


        print(settings.db['timeout'])  # this was computed by the Validator, see `config.py`
                                    # outputs: 11520

        # Remember our lazy computed values? from `.env` file using `@jinja`.
        print(settings.doubles_list)  # this is going to be computed on access, see `.env`
                                    # outputs: [2 4 6 8 ]


        # Feature flags? you can programatically switch environments :)
        with settings.using_env('production'):
            # now values comes from [production] section of config files
            print(settings.NAME)  # outputs: Root

        # not production anymore
        print(settings.NAME)  # outputs: Bruno


        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade dynaconf
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
