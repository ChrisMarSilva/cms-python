from loguru import logger
import newrelic.agent
import time



def main():
    try:

        newrelic.agent.initialize('./newrelic.ini')
        newrelic.agent.register_application(timeout= 10.0)

        for i in range(10_000):
            with newrelic.agent.BackgroundTask(newrelic.agent.application(), name='print_task'):
                pass  # time.sleep(1)
            
        for i in range(100_000):
            with newrelic.agent.BackgroundTask(newrelic.agent.application(), name='print_numbers'):
                pass  # time.sleep(2)

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()


# docker run -d --name newrelic-infra --network=host --cap-add=SYS_PTRACE --privileged --pid=host -v "/:/host:ro" -v "/var/run/docker.sock:/var/run/docker.sock" -e NRIA_LICENSE_KEY=b7b652fcd3864cdab6b777d0bd3c6998dd87NRAL newrelic/infrastructure:latest
# python -m pip install --upgrade newrelic
# python main.py
