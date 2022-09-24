from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/", status_code=200)
async def get_index():
    return {"Hello": "World"}, 200

@app.get("/{asin}", status_code=200)
async def get_data(asin: str):
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'})
    asin = "B084KYMBFH"
    resp = session.get(f"https://amazon.co.uk/dp/{asin}")
    if resp.status_code != 200:
        return {"error": f"bad status code {resp.status_code}"}, 400
    soup = BeautifulSoup(resp.text, "html.parser")
    try:
        data = {"asin": asin, "name": soup.select_one("h1#title").text.strip(), "price": soup.select_one("span.a-offscreen").text,}
        return {"results": data}, 200
    except KeyError:
        return {"error": "Unable to parse page"}, 500

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="localhost", port=5001, log_level="error", reload=False, debug=False, workers=10)
    # uvicorn.run("src.app:app", host="127.0.0.1", port=5001, log_level="info", reload=True, debug=True)
    # import asyncio
    # from hypercorn.config import Config
    # from hypercorn.asyncio import serve
    # config = Config()
    # config.bind = ["127.0.0.1:5001"]
    # config.use_reloader = True
    # asyncio.run(serve(app, config))


# python -m pip install --upgrade pip
# python -m pip install --upgrade fastapi
# python -m pip install --upgrade uvicorn
# python -m pip install --upgrade requests
# python -m pip install --upgrade beautifulsoup4

# python main.py
# hypercorn main:app --worker-class trio
# uvicorn main:app --reload --port 5001
