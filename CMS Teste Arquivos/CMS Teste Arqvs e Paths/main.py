import asyncio
import datetime as dt
import time

from dotenv import load_dotenv
from loguru import logger


def teste_01_pathlib():
    try:

        import collections
        import pathlib
        from datetime import datetime

        # from pathlib import Path
        # Pathlib, os.path, glob, shutil e stat

        home = pathlib.Path.home()
        logger.info(f"{home=}")
        logger.info(f"")

        wave_absolute = pathlib.Path(home, "ocean", "wave.txt")
        logger.info(f"{wave_absolute=}")
        logger.info(f"{wave_absolute.name=}")
        logger.info(f"{wave_absolute.suffix=}")
        logger.info(f"{wave_absolute.parent=}")
        logger.info(f"")

        shark = pathlib.Path(
            pathlib.Path.home(), "ocean", "animals", pathlib.Path("fish", "shark.txt")
        )
        logger.info(f"{shark=}")
        logger.info(f"{shark.name=}")
        logger.info(f"{shark.suffix=}")
        logger.info(f"{shark.parent=}")
        logger.info(f"")

        wave = pathlib.Path("ocean", "wave.txt")
        tides = wave.with_name("tides.txt")
        logger.info(f"{wave=}")
        logger.info(f"{tides=}")
        logger.info(f"{tides.name=}")
        logger.info(f"{tides.suffix=}")
        logger.info(f"{tides.parent=}")
        logger.info(f"")

        shark = pathlib.Path("ocean", "animals", "fish", "shark.txt")
        logger.info(f"{shark=}")
        logger.info(f"{shark.name=}")
        logger.info(f"{shark.suffix=}")
        logger.info(f"{shark.parent=}")
        logger.info(f"{shark.parent.parent=}")
        logger.info(f"")

        logger.info(f"Lista #1 - Diretorio")
        pat = r"C:\Users\chris\Desktop\CMS Python\CMS Teste Data Science\CMS Teste Pandas em Paralelo"
        for txt_path in pathlib.Path(pat).glob("*.xlsx"):
            logger.info(f"{txt_path.name}")
        logger.info(f"")

        logger.info(f"Lista #2 - Sub-Diretorio")
        pat = r"C:\Users\chris\Desktop\CMS Python\CMS Teste Data Science"
        for txt_path in pathlib.Path(pat).glob("**/*.xlsx"):
            logger.info(f"{txt_path.name}")
        logger.info(f"")

        shark = pathlib.Path("ocean", "animals", "fish", "shark.txt")
        below_ocean = shark.relative_to(pathlib.Path("ocean"))
        below_animals = shark.relative_to(pathlib.Path("ocean", "animals"))
        logger.info(f"{shark=}")
        logger.info(f"{below_ocean=}")
        logger.info(f"{below_animals=}")

        p = pathlib.Path(".")
        logger.info(f"{p.parts=}")
        logger.info(f"{p.iterdir()=}")
        logger.info(f"{p.is_dir()=}")
        logger.info(f"{p.is_file()=}")
        logger.info(f"{p.absolute()=}")
        logger.info(f"{p.anchor=}")
        # logger.info(f'{p.as_uri()=}')
        logger.info(f"{p.parent=}")
        r = [x for x in p.iterdir() if x.is_dir()]
        logger.info(f"{r=}")

        r = list(p.glob("**/*.py"))
        logger.info(f"{r=}")

        r = pathlib.Path.cwd()
        logger.info(f"{r=}")

        r = pathlib.Path.cwd().joinpath("in").joinpath("input.xlsx")
        logger.info(f"{r=}")

        r = pathlib.Path.cwd().joinpath("python", "scripts", "test.py")
        logger.info(f"{r=}")

        # C:\Users\chris\Desktop\CMS Python\CMS Teste Arquivos\CMS Teste Arqvs e Paths\teste.txt
        path = pathlib.Path.cwd() / "teste.txt"
        logger.info(f"{path.read_text()=}")
        # path.write_text(path.read_text() + '\n4\n5')
        # logger.info(f'{path.read_text()=}')

        path = pathlib.Path.cwd() / "teste.txt"
        logger.info(f"{path.resolve()=}")
        logger.info(f"{pathlib.Path.cwd()=}")
        logger.info(f"{path.resolve().parent == pathlib.Path.cwd()=}")
        logger.info(f"{path.parent == pathlib.Path.cwd()=}")
        logger.info(f"{path.name=}")
        logger.info(f"{path.stem=}")  #
        logger.info(f"{path.suffix=}")
        logger.info(f"{path.suffixes=}")
        logger.info(f"{path.parent=}")
        logger.info(f"{path.parent.parent=}")
        logger.info(f"{path.anchor=}")
        # path.replace(path.with_suffix('.py')) # renomear extensão do arquivo
        logger.info(f"{path.suffix=}")

        r = collections.Counter(p.suffix for p in pathlib.Path.cwd().iterdir())
        logger.info(f"{r=}")

        def tree(directory):
            print(f"+ {directory}")
            for path in sorted(directory.rglob("*")):
                depth = len(path.relative_to(directory).parts)
                spacer = "    " * depth
                print(f"{spacer}+ {path.name}")

        tree(pathlib.Path.cwd())

        # time, file_path = max((f.stat().st_mtime, f) for f in directory.iterdir())
        # print(datetime.fromtimestamp(time), file_path)
        # max((f.stat().st_mtime, f) for f in directory.iterdir())[1].read_text()

        def unique_path(directory, name_pattern):
            counter = 0
            while True:
                counter += 1
                path = directory / name_pattern.format(counter)
                if not path.exists():
                    return path

        path = unique_path(pathlib.Path.cwd(), "test{:03d}.txt")
        logger.info(f"{path=}")

        r = pathlib.WindowsPath("test.md")
        logger.info(f"{r=}")

        p = pathlib.Path("123.txt")
        p.touch()  # criar arquivo
        # p.unlink() # remover arquivo
        # p.rename() # renomear arquivo
        # p.mkdir() # criar pasta
        # p.rmdir() # remover pasta, somente se a pasta estiver vazia
        # mas para remover diretorio e subdiretorios tem se ser o shutil.rmtree('./dir')
        # p.replace_parts('C:/downloads','D:/uploads')

        # pathlib.Path('some_file').unlink(missing_ok=True)
        # try:
        #     pathlib.Path('some_file').unlink()
        # except FileNotFoundError:
        #     pass

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


def teste_02_pathlib3x():
    try:

        import pathlib3x as pathlib

        my_file = pathlib.Path("./PastaOrigem")
        to_file = pathlib.Path("./PastaDestino")
        my_file.copy(to_file)  # copy # copytree

        output_path = pathlib.Path("C:/Downloads/Backups")
        output_path.rmtree(ignore_errors=True)
        output_path.mkdir()
        for file in pathlib.Path("C:/Downloads").glob("*.txt"):
            new_file = output_path + file.name
            file.copy(new_file)

        # source_dir = pathlib.Path('c:/source_dir')
        # target_dir = pathlib.Path('c:/target_dir')
        # for file in source_dir.glob('**/*.txt'):
        #     file.copy(file.replace_parts(source_dir, target_dir))

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


async def teste_03_aiopathlib():
    try:

        import aiopathlib

        # from aiopathlib import AsyncPath

        text = await aiopathlib.AsyncPath("filename").read_text()
        logger.info(text)

        content = await aiopathlib.AsyncPath(aiopathlib.Path("filename")).read_bytes()
        logger.info(content)

        apath = aiopathlib.AsyncPath("dirname/subpath")
        if not await apath.exists():
            await apath.mkdir(parents=True)

        # await ap.remove()  # == await ap.unlink() == p.unlink()
        # await ap.mkdir()  # == p.mkdir()

        ap = aiopathlib.AsyncPath("test.json")
        lst = [aiopathlib.Path(i) for i in ap.glob("*")]  # glob # rglob
        logger.info(lst)

        async def uma_funcao_qualquer():
            await time.sleep(1)

        async def lista_arquivos(path=aiopathlib.AsyncPath("."), pattern="*"):
            path = aiopathlib.AsyncPath(path)
            return [file async for file in path.glob(pattern)]

        async def async_map():
            return await asyncio.gather(lista_arquivos(), uma_funcao_qualquer())

        await async_map()

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


async def teste_04_aiofile():
    try:

        import io
        from argparse import ArgumentParser
        from csv import DictReader
        from pathlib import Path
        from tempfile import gettempdir
        from typing import IO, Any

        from aiofile import AIOFile, LineReader, Reader, Writer, async_open

        # Basic example:
        tmp_filename = Path(gettempdir()) / "hello.txt"
        async with async_open(tmp_filename, "w+") as afp:
            await afp.write("Hello ")
            await afp.write("world")
            afp.seek(0)
            print(await afp.read())
            await afp.write("Hello from\nasync world")
            print(await afp.readline())
            print(await afp.readline())

        # Copy file example program (cp):
        parser = ArgumentParser(description="Copying files using asynchronous io API")
        parser.add_argument("source", type=Path)
        parser.add_argument("dest", type=Path)
        parser.add_argument("--chunk-size", type=int, default=65535)
        arguments = parser.parse_args()
        async with async_open(arguments.source, "rb") as src, async_open(
            arguments.dest, "wb"
        ) as dest:
            async for chunk in src.iter_chunked(arguments.chunk_size):
                await dest.write(chunk)

        # Example with opening already opened file pointer:
        with open("test.txt", "w+") as fp:  # fp: IO[Any]
            async with async_open(fp) as afp:
                await afp.write("Hello from\nasync world")
                print(await afp.readline())

        # When you want to read or write file linearly following example might be helpful.
        async with AIOFile("/tmp/hello.txt", "w+") as afp:
            writer = Writer(afp)
            reader = Reader(afp, chunk_size=8)
            await writer("Hello")
            await writer(" ")
            await writer("World")
            await afp.fsync()
            async for chunk in reader:
                print(chunk)

        # LineReader - read file line by line
        async with AIOFile("/tmp/hello.txt", "w+") as afp:
            writer = Writer(afp)
            await writer("Hello")
            await writer(" ")
            await writer("World")
            await writer("\n")
            await writer("\n")
            await writer("From async world")
            await afp.fsync()
            async for line in LineReader(afp):
                print(line)

        #  Write and Read
        async with AIOFile("/tmp/hello.txt", "w+") as afp:
            await afp.write("Hello ")
            await afp.write("world", offset=7)
            await afp.fsync()
            print(await afp.read())

        # Read file line by line
        async with AIOFile("/tmp/hello.txt", "w") as afp:
            writer = Writer(afp)
            for i in range(10):
                await writer("%d Hello World\n" % i)
            await writer("Tail-less string")
        async with AIOFile("/tmp/hello.txt", "r") as afp:
            async for line in LineReader(afp):
                print(line[:-1])

        # Async CSV Dict Reader

        class AsyncDictReader:
            def __init__(self, afp, **kwargs):
                self.buffer = io.BytesIO()
                self.file_reader = LineReader(
                    afp,
                    line_sep=kwargs.pop("line_sep", "\n"),
                    chunk_size=kwargs.pop("chunk_size", 4096),
                    offset=kwargs.pop("offset", 0),
                )
                self.reader = DictReader(
                    io.TextIOWrapper(
                        self.buffer,
                        encoding=kwargs.pop("encoding", "utf-8"),
                        errors=kwargs.pop("errors", "replace"),
                    ),
                    **kwargs,
                )
                self.line_num = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.line_num == 0:
                    header: str = await self.file_reader.readline()
                    self.buffer.write(header)
                line: str = await self.file_reader.readline()
                if not line:
                    raise StopAsyncIteration
                self.buffer.write(line)
                self.buffer.seek(0)
                try:
                    result = next(self.reader)
                except StopIteration as e:
                    raise StopAsyncIteration from e
                self.buffer.seek(0)
                self.buffer.truncate(0)
                self.line_num = self.reader.line_num
                return result

        async with AIOFile("sample.csv", "rb") as afp:
            async for item in AsyncDictReader(afp):
                print(item)

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


async def teste_05_aiofiles():
    try:

        import aiofiles

        # https://github.com/Tinche/aiofiles
        # https://pypi.org/project/aiofiles/

        async with aiofiles.open("filename", mode="r") as f:
            contents = await f.read()
        logger.info(contents)

        async with aiofiles.open("filename") as f:
            async for line in f:
                logger.info(line)

        async with aiofiles.tempfile.TemporaryFile("wb") as f:
            await f.write(b"Hello, World!")

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


async def teste_06_aiopath():
    try:

        from aiohttp import ClientSession
        from aiopath import AsyncPath

        # async with ClientSession() as session:
        #     async with session.get('http://python.org') as response:
        #         print("Status:", response.status)
        #         print("Content-type:", response.headers['content-type'])
        #         html = await response.text()
        #         print("Body:", html[:15], "...")

        async def save_page(url: str, name: str):
            path = AsyncPath(name)
            if await path.exists():
                return
            async with ClientSession() as session:
                response = await session.get(url)
                content: bytes = await response.read()
            await path.write_bytes(content)

        urls = [
            "https://example.com",
            "https://github.com/alexdelorenzo/aiopath",
            "https://alexdelorenzo.dev",
            "https://dupebot.firstbyte.dev",
        ]
        scrapers = (save_page(url, f"{index}.html") for index, url in enumerate(urls))
        await asyncio.gather(*scrapers)

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


def main():
    try:

        logger.info(f"Inicio")
        start_time = (
            time.perf_counter()
        )  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        teste_01_pathlib()
        teste_02_pathlib3x()
        asyncio.run(teste_03_aiopathlib())
        asyncio.run(teste_04_aiofile())
        asyncio.run(teste_05_aiofiles())
        asyncio.run(teste_06_aiopath())

        # python main.py

        end_time = (
            time.perf_counter() - start_time
        )  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == "__main__":
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade pathlib3x
# python -m pip install --upgrade aiopathlib
# python -m pip install --upgrade aiofile
# python -m pip install --upgrade aiofiles
# python -m pip install --upgrade aiopath
# python -m pip install --upgrade aiohttp
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
