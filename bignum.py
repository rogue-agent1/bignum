#!/usr/bin/env python3
"""Big number arithmetic — factorial, fibonacci, catalan, combinations."""
import sys

def factorial(n):
    r = 1
    for i in range(2, n+1): r *= i
    return r

def fib(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n+1): a, b = b, a+b
    return b

def fib_matrix(n):
    def mat_mul(A, B):
        return [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
                [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]
    if n <= 1: return max(0, n)
    result, base = [[1,0],[0,1]], [[1,1],[1,0]]
    n -= 1
    while n:
        if n & 1: result = mat_mul(result, base)
        base = mat_mul(base, base); n >>= 1
    return result[0][0]

def comb(n, r):
    if r > n: return 0
    if r > n-r: r = n-r
    result = 1
    for i in range(r): result = result * (n-i) // (i+1)
    return result

def catalan(n): return comb(2*n, n) // (n+1)
def stirling2(n, k):
    if n == 0 and k == 0: return 1
    if n == 0 or k == 0: return 0
    return k * stirling2(n-1, k) + stirling2(n-1, k-1)

def cli():
    if len(sys.argv) < 3:
        print("Usage: bignum <cmd> <n> [k]"); print("  fact|fib|fibmat|comb|catalan|stirling"); sys.exit(1)
    cmd, n = sys.argv[1], int(sys.argv[2])
    if cmd == "fact": r = factorial(n); s = str(r); print(f"{n}! = {s[:80]}{'...' if len(s)>80 else ''} ({len(s)} digits)")
    elif cmd == "fib": r = fib(n); s = str(r); print(f"F({n}) = {s[:80]}{'...' if len(s)>80 else ''} ({len(s)} digits)")
    elif cmd == "fibmat": r = fib_matrix(n); s = str(r); print(f"F({n}) = {s[:80]}{'...' if len(s)>80 else ''} ({len(s)} digits)")
    elif cmd == "comb": k = int(sys.argv[3]); print(f"C({n},{k}) = {comb(n,k)}")
    elif cmd == "catalan": print(f"Catalan({n}) = {catalan(n)}")
    elif cmd == "stirling": k = int(sys.argv[3]); print(f"S({n},{k}) = {stirling2(n,k)}")

if __name__ == "__main__": cli()
