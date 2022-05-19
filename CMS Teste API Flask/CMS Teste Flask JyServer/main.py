from flask import Flask, render_template
import jyserver.Flask as js
import time


app = Flask(import_name=__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # https://randomkeygen.com/


@js.use(app)
class App:

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        self.js.document.getElementById('count').innerHTML = self.count

    def stop(self):
        self.running = False
        self.js.dom.b2.onclick = self.restart

    def restart(self):
        self.running = True
        self.js.dom.b2.onclick = self.stop

    def reset(self):
        self.start0 = time.time()
        self.js.dom.time.innerHTML = "{:.1f}".format(0)

    @js.task
    def main(self):
        self.start0 = time.time()
        while True:
            t = "{:.1f}".format(time.time() - self.start0)
            self.js.dom.time.innerHTML = t
            time.sleep(0.1)
            # break


@app.route('/')
def index():
    # return render_template('index.html')
    App.main()
    return App.render(render_template('index.html'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# python -m pip install --upgrade flask
# python -m pip install --upgrade jyserver
# python main.py
