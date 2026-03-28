#!/usr/bin/env python3
"""Arbitrary precision integer calculator with common functions."""
import sys

def factorial(n):
    r = 1
    for i in range(2, n+1): r *= i
    return r

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a

def gcd(a, b):
    while b: a, b = b, a % b
    return a

def lcm(a, b): return abs(a * b) // gcd(a, b)

def is_perfect(n):
    return sum(i for i in range(1, n) if n % i == 0) == n

def collatz_len(n):
    steps = 0
    while n != 1: n = n // 2 if n % 2 == 0 else 3 * n + 1; steps += 1
    return steps

OPS = {
    'fact': lambda args: str(factorial(int(args[0]))),
    'fib': lambda args: str(fibonacci(int(args[0]))),
    'gcd': lambda args: str(gcd(int(args[0]), int(args[1]))),
    'lcm': lambda args: str(lcm(int(args[0]), int(args[1]))),
    'pow': lambda args: str(int(args[0]) ** int(args[1])),
    'sqrt': lambda args: str(int(int(args[0]) ** 0.5)),
    'perfect': lambda args: str(is_perfect(int(args[0]))),
    'digits': lambda args: str(len(str(abs(int(args[0]))))),
    'sum_digits': lambda args: str(sum(int(d) for d in str(abs(int(args[0]))))),
    'collatz': lambda args: str(collatz_len(int(args[0]))),
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: bignum.py <{'|'.join(OPS.keys())}> <args...>"); sys.exit(1)
    op = sys.argv[1]
    if op in OPS:
        result = OPS[op](sys.argv[2:])
        print(result[:1000] + ('...' if len(result) > 1000 else ''))
        if len(result) > 20: print(f"({len(result)} digits)")
    elif op == 'eval':
        print(eval(' '.join(sys.argv[2:])))
    else:
        print(f"Unknown: {op}")
