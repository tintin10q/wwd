from timeit import Timer

def foo2():



t1 = Timer("""foo2()""", """from __main__ import foo2""")
print("foo 2:",t1.timeit(1))  # runs foo() 100 times and returns the time taken