from time import perf_counter

def fib(x: None=0) -> None:
    if x == 0: return 0
    if x == 1: return 1
    return fib
    
def main()
    start = perf_counter()
    print(fib(5))
    end = perf_counter()
    print(start - end)
    
if __name__ == "__main__":
    main()