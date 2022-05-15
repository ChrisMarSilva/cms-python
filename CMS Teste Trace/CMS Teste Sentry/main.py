import sentry_sdk
from sentry_sdk import capture_message, capture_exception
from sentry_sdk.integrations.logging import LoggingIntegration
import logging
from dotenv import load_dotenv


def main():
    try:

        # All of this is already happening by default!
        # level = Capture info and above as breadcrumbs # event_level = Send errors as events
        sentry_logging = LoggingIntegration(level=logging.DEBUG, event_level=logging.DEBUG)

        dsn = "https://934ce83d5abf443a9154b7b91fa9cfe4@o1205050.ingest.sentry.io/6334793"
        sentry_sdk.init(dsn=dsn, traces_sample_rate=1.0, integrations=[sentry_logging])

        logging.debug("02 - I am debug")
        logging.info("03 - I am a info")
        logging.error("04 - I am an error")
        logging.critical("05 - I am an critical")
        logging.fatal("06 - I am an fatal")
        logging.warning("07 - I am an warning")
        logging.exception("08 - I am an exception")
        
        capture_message("01 - hi")

        division_by_zero = 1 / 0

    except Exception as e:
        capture_exception(e)


if __name__ == '__main__':
    main()


# py -3 -m venv .venv

# python -m pip install psutil
# python -m pip install --upgrade sentry-sdk

# cd c:/Users/chris/Desktop/CMS Python/CMS Teste Email
# .venv\scripts\activate
# python main.py
