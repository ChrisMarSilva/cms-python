# cython : language_level=3



def show(str s):
    print(s)

def show_all(list ls):
    cdef str s
    for s in ls:
        print(s)
