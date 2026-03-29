#!/usr/bin/env python3
"""bignum - Arbitrary precision arithmetic without Python's built-in bigint."""
import sys, json

class BigNum:
    BASE = 10000
    def __init__(self, digits=None, negative=False):
        self.digits = digits or [0]
        self.negative = negative
        self._strip()
    
    def _strip(self):
        while len(self.digits) > 1 and self.digits[-1] == 0: self.digits.pop()
        if self.digits == [0]: self.negative = False
    
    @staticmethod
    def from_int(n):
        if n < 0: return BigNum.from_int(-n)._neg()
        if n == 0: return BigNum([0])
        digits = []
        while n > 0: digits.append(n % BigNum.BASE); n //= BigNum.BASE
        return BigNum(digits)
    
    @staticmethod
    def from_str(s):
        neg = s.startswith("-")
        if neg: s = s[1:]
        s = s.lstrip("0") or "0"
        digits = []
        for i in range(len(s), 0, -4):
            start = max(0, i-4)
            digits.append(int(s[start:i]))
        return BigNum(digits, neg)
    
    def _neg(self):
        return BigNum(list(self.digits), not self.negative)
    
    def __repr__(self):
        if not self.digits: return "0"
        s = str(self.digits[-1])
        for d in reversed(self.digits[:-1]): s += str(d).zfill(4)
        return ("-" + s) if self.negative else s
    
    def _cmp_abs(self, other):
        if len(self.digits) != len(other.digits):
            return 1 if len(self.digits) > len(other.digits) else -1
        for i in range(len(self.digits)-1, -1, -1):
            if self.digits[i] != other.digits[i]:
                return 1 if self.digits[i] > other.digits[i] else -1
        return 0
    
    def _add_abs(self, other):
        n = max(len(self.digits), len(other.digits))
        result = []; carry = 0
        for i in range(n):
            s = carry
            if i < len(self.digits): s += self.digits[i]
            if i < len(other.digits): s += other.digits[i]
            result.append(s % self.BASE); carry = s // self.BASE
        if carry: result.append(carry)
        return BigNum(result)
    
    def _sub_abs(self, other):
        if self._cmp_abs(other) < 0:
            return other._sub_abs(self)._neg()
        result = []; borrow = 0
        for i in range(len(self.digits)):
            s = self.digits[i] - borrow
            if i < len(other.digits): s -= other.digits[i]
            if s < 0: s += self.BASE; borrow = 1
            else: borrow = 0
            result.append(s)
        return BigNum(result)
    
    def __add__(self, other):
        if self.negative == other.negative:
            r = self._add_abs(other); r.negative = self.negative; return r
        if self._cmp_abs(other) >= 0:
            r = self._sub_abs(other); r.negative = self.negative; r._strip(); return r
        r = other._sub_abs(self); r.negative = other.negative; r._strip(); return r
    
    def __mul__(self, other):
        n, m = len(self.digits), len(other.digits)
        result = [0]*(n+m)
        for i in range(n):
            carry = 0
            for j in range(m):
                prod = self.digits[i]*other.digits[j]+result[i+j]+carry
                result[i+j] = prod % self.BASE; carry = prod // self.BASE
            result[i+m] += carry
        r = BigNum(result, self.negative != other.negative); r._strip(); return r

def factorial(n):
    result = BigNum.from_int(1)
    for i in range(2, n+1):
        result = result * BigNum.from_int(i)
    return result

def main():
    print("BigNum arithmetic demo\n")
    a = BigNum.from_str("999999999999999999")
    b = BigNum.from_str("1")
    print(f"  {a} + {b} = {a + b}")
    c = BigNum.from_str("123456789")
    d = BigNum.from_str("987654321")
    print(f"  {c} * {d} = {c * d}")
    f50 = factorial(50)
    print(f"  50! = {f50}")
    f100 = factorial(100)
    s = repr(f100)
    print(f"  100! = {s[:30]}...({len(s)} digits)")

if __name__ == "__main__":
    main()
