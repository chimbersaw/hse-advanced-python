def fib_list(n):
    # Computing fib this way(not linearly) makes AST look prettier
    def fib(i):
        if i <= 1:
            return i
        return fib(i - 1) + fib(i - 2)

    return [fib(i) for i in range(n)]
