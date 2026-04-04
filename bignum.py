#!/usr/bin/env python3
"""bignum - Arbitrary precision arithmetic, number theory, and cryptographic primes."""

import sys, random, math

def cmd_calc(args):
    """Evaluate arbitrary precision expression."""
    expr = ' '.join(args)
    # safe eval with only math operations
    allowed = {'__builtins__': {}, 'abs': abs, 'pow': pow, 'min': min, 'max': max,
               'gcd': math.gcd, 'factorial': math.factorial, 'isqrt': math.isqrt}
    try:
        result = eval(expr, allowed)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); sys.exit(1)

def cmd_factor(args):
    """Prime factorization."""
    n = int(args[0])
    if n < 2: print(f"{n} (not factorable)"); return
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 1
    if temp > 1: factors.append(temp)
    from collections import Counter
    c = Counter(factors)
    parts = []
    for p, e in sorted(c.items()):
        parts.append(f"{p}^{e}" if e > 1 else str(p))
    print(f"{n} = {' × '.join(parts)}")
    print(f"  {len(factors)} prime factors, {len(c)} distinct")

def is_prime_miller(n, k=20):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    d, r = n - 1, 0
    while d % 2 == 0: d //= 2; r += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def cmd_prime(args):
    """Check if number is prime (Miller-Rabin)."""
    n = int(args[0])
    result = is_prime_miller(n)
    print(f"{n} is {'PRIME' if result else 'COMPOSITE'}")
    if not result and n > 1:
        # find smallest factor
        for d in range(2, min(n, 1000000)):
            if n % d == 0:
                print(f"  smallest factor: {d}")
                break

def cmd_genprime(args):
    """Generate random prime of given bit length."""
    bits = int(args[0]) if args else 256
    while True:
        n = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime_miller(n):
            print(f"Prime ({bits} bits, {len(str(n))} digits):")
            print(n)
            return

def cmd_gcd(args):
    nums = [int(a) for a in args]
    result = nums[0]
    for n in nums[1:]:
        result = math.gcd(result, n)
    print(f"GCD: {result}")
    # also LCM
    lcm = nums[0]
    for n in nums[1:]:
        lcm = lcm * n // math.gcd(lcm, n)
    print(f"LCM: {lcm}")

def cmd_modpow(args):
    """Modular exponentiation: base^exp mod m."""
    base, exp, mod = int(args[0]), int(args[1]), int(args[2])
    result = pow(base, exp, mod)
    print(f"{base}^{exp} mod {mod} = {result}")

def cmd_fibonacci(args):
    """Compute nth Fibonacci number (fast doubling)."""
    n = int(args[0])
    def fib(n):
        if n <= 0: return 0
        if n == 1: return 1
        if n % 2 == 0:
            k = n // 2
            fk = fib(k)
            fk1 = fib(k - 1)
            return fk * (2 * fk1 + fk)
        else:
            k = (n + 1) // 2
            fk = fib(k)
            fk1 = fib(k - 1)
            return fk * fk + fk1 * fk1
    result = fib(n)
    s = str(result)
    if len(s) > 100:
        print(f"F({n}) = {s[:50]}...{s[-50:]} ({len(s)} digits)")
    else:
        print(f"F({n}) = {result}")

def cmd_digits(args):
    """Analyze digit count and properties of a number."""
    n = int(args[0])
    s = str(abs(n))
    print(f"Digits: {len(s)}")
    print(f"Digit sum: {sum(int(d) for d in s)}")
    print(f"Digital root: {(n - 1) % 9 + 1 if n else 0}")
    print(f"Bits: {n.bit_length()}")
    print(f"Hex digits: {len(hex(abs(n))) - 2}")

CMDS = {
    'calc': (cmd_calc, 'EXPR — arbitrary precision arithmetic'),
    'factor': (cmd_factor, 'N — prime factorization'),
    'prime': (cmd_prime, 'N — primality test (Miller-Rabin)'),
    'genprime': (cmd_genprime, '[BITS] — generate random prime (default 256)'),
    'gcd': (cmd_gcd, 'N M [...] — GCD and LCM'),
    'modpow': (cmd_modpow, 'BASE EXP MOD — modular exponentiation'),
    'fibonacci': (cmd_fibonacci, 'N — nth Fibonacci (fast doubling)'),
    'digits': (cmd_digits, 'N — digit analysis'),
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("Usage: bignum <command> [args...]")
        for n, (_, d) in sorted(CMDS.items()):
            print(f"  {n:10s} {d}")
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd not in CMDS: print(f"Unknown: {cmd}", file=sys.stderr); sys.exit(1)
    CMDS[cmd][0](sys.argv[2:])

if __name__ == '__main__':
    main()
