from flask import Flask, jsonify
from flask_apscheduler import APScheduler
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import os


def show_users():
    # with db.app.app_context():
    #     print(User.query.all())
    pass


class Config:
    # JOBS = [{"id": "job1", "func": "main:job1", "args": (1, 2), "trigger": "interval", "seconds": 10}]
    # JOBS = [{"id": "job1", "func": show_users, "trigger": "interval", "seconds": 2}]
    # SCHEDULER_JOBSTORES = { "default": SQLAlchemyJobStore(url="sqlite:///flask_context.db")}
    # SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 20}}
    # SCHEDULER_JOB_DEFAULTS = {"coalesce": False, "max_instances": 3}
    SCHEDULER_API_ENABLED = True


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/
app.config.from_object(Config())


scheduler = APScheduler()


def scheduledTask():
    app.logger.info("This task is running every 5 seconds")

def job1(var_one, var_two):
    # app.logger.info(str(var_one) + " " + str(var_two))
    print(str(var_one) + " " + str(var_two))


@scheduler.task("interval", id="do_job_1", seconds=10, misfire_grace_time=900)
def job1():
    print("Job 1 executed")


@scheduler.task("cron", id="do_job_2", minute="*")
def job2():
    print("Job 2 executed")




# Sunday (Domingo): Monday (Segunda-feira): Tuesday (Terça-feira): Wednesday (Quarta-feira): Thursday (Quinta-feira): Friday (Sexta-feira): Saturday (Sábado):
@scheduler.task("cron", id="do_job_3", week="*", day_of_week="wed")
def job3():
    print("Job 3 executed")



@app.route('/')
def index():
    app.logger.info("index")
    return jsonify('ok')


@app.route('/agendar')
def agendar():
    app.logger.info("agendar")
    # scheduler.add_job(id='Scheduled task', func=scheduledTask, trigger='interval', seconds=5)
    # scheduler.start()
    return jsonify('agendado')




if __name__ == '__main__':
    # scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True  # noqa: E800
    scheduler.init_app(app=app)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000, debug=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade Flask-APScheduler
# python main.py
