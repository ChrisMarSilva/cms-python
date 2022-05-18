#!/usr/bin/env python3
import time
import pyperf


def main_old_1():
    for i in range (1_000_000):
        num = i + i
        # print(i)

def main_old_2():
    runner = pyperf.Runner()
    runner.timeit(
        name="sort a sorted list",
        stmt="sorted(s, key=f)",
        setup="f = lambda x: x; s = list(range(10))"  # 1_000
    )

def my_slow_function():
    time.slee(0.01)


def main():
    runner = pyperf.Runner()
    runner.bench_func("my_slow_function", my_slow_function)


if __name__ == '__main__':
    main()

# python -m pip install --upgrade pyperf
# python -m pip install --upgrade pip
# python3 -m pip install pyperf
# pip install pyperf

# python main.py
# python3 main.py

# python3 -m main.py -o bench2.json

# python3 -m pyperf timeit '1_000*[2]' -o bench.json
# python3 -m pyperf timeit '[1,2]*1000' -o bench.json
# the standard deviation (1.83 us) is 27% of the mean (6.83 us)
# the maximum (12.0 us) is 75% greater than the mean (6.83 us)
# Mean +- std dev: 6.83 us +- 1.83 us

# python3 -m pyperf system tune

# python3 -m pyperf stats bench.json
# python3 -m pyperf stats bench.json -q
# python3 -m pyperf hist bench.json -q
# python3 -m pyperf show bench.json
# python3 -m pyperf show bench.json --metadata
# python3 -m pyperf check bench.json
# python3 -m pyperf metadata bench.json

# python3.6 -m pyperf timeit '[1,2]*1000' -o py36.json
# python3.8 -m pyperf timeit '[1,2]*1000' -o py38.json
# python3 -m pyperf compare_to py36.json py38.json
# python3 -m pyperf compare_to py36.json py38.json --table
