from flask import Flask, jsonify, render_template, request
from loguru import logger
import datetime as dt
import time
import lxml
from bs4 import BeautifulSoup
from random import randint
import redis
from redis import Redis
from rq import Queue, Retry
from dotenv import load_dotenv


app = Flask(import_name=__name__, template_folder='')
# r = redis.Redis()
# q = Queue(connection=r)
# q = Queue(connection=Redis())
q = Queue(connection=Redis(host='localhost', port=6379, db=0, password='123', charset='utf-8', decode_responses=True))


@app.route("/")
def home():
    return render_template("index.html")


def background_task(n):
    """ Function that returns len(n) and simulates a delay """
    delay = 2
    logger.info("Task running")
    logger.info(f"Simulating a {delay} second delay")
    time.sleep(delay)
    logger.info(f'{len(n)=}') 
    logger.info("Task complete")
    return len(n)


@app.route("/task")
def index():
    try:
        if request.args.get("n"):
            job = q.enqueue(background_task, request.args.get("n"))
            # queue.enqueue(say_hello, retry=Retry(max=3)) # Retry up to 3 times, failed job will be requeued immediately
            # queue.enqueue(say_hello, retry=Retry(max=3, interval=[10, 30, 60])) # Retry up to 3 times, failed job will be requeued immediately
            return f"Task ({job.id}) added to queue at {job.enqueued_at}"
        return "No value for count provided"
    except Exception as e:
        return str(e)



def count_words(url):
    logger.info(f"Counting words at {url}")
    start = time.time()
    from urllib import request
    resp = request.urlopen(url)
    soup = BeautifulSoup(resp.read().decode(), "lxml")
    paragraphs = " ".join([p.text for p in soup.find_all("p")])
    word_count = dict()
    for i in paragraphs.split():
        if not i in word_count:
            word_count[i] = 1
        else:
            word_count[i] += 1
    end = time.time()
    time_elapsed = end - start
    logger.info(word_count)
    logger.info(f"Total words: {len(word_count)}")
    logger.info(f"Time elapsed: {time_elapsed} ms")
    return len(word_count)


@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    jobs = q.jobs  # Get a list of jobs in the queue
    message = None
    if request.args:  # Only run if a query string is sent in the request
        url = request.args.get("url")  # Gets the URL coming in as a query string
        task = q.enqueue(count_words, url)  # Send a job to the task queue
        jobs = q.jobs  # Get a list of jobs in the queue
        q_len = len(q)  # Get the queue length
        message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {q_len} jobs queued"
    return render_template("add_task.html", message=message, jobs=jobs)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)


# py -3 -m venv .venv
# python -m pip install --upgrade redis
# python -m pip install --upgrade rq
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate

# python main.py
# uvicorn main:app --reload --port 5000
# rq worker flask-task

#localhost:5000/task?n=hello
