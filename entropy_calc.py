#!/usr/bin/env python3
"""entropy_calc - Shannon entropy and information theory tools."""
import argparse, math, sys, json
from collections import Counter

def shannon_entropy(data):
    counts = Counter(data)
    n = len(data)
    return -sum((c/n) * math.log2(c/n) for c in counts.values() if c > 0)

def joint_entropy(x, y):
    pairs = list(zip(x, y))
    return shannon_entropy(pairs)

def mutual_information(x, y):
    return shannon_entropy(x) + shannon_entropy(y) - joint_entropy(x, y)

def conditional_entropy(x, y):
    return joint_entropy(x, y) - shannon_entropy(y)

def cross_entropy(p_dist, q_dist):
    return -sum(p * math.log2(q) for p, q in zip(p_dist, q_dist) if p > 0 and q > 0)

def kl_divergence(p_dist, q_dist):
    return sum(p * math.log2(p/q) for p, q in zip(p_dist, q_dist) if p > 0 and q > 0)

def main():
    p = argparse.ArgumentParser(description="Entropy calculator")
    p.add_argument("cmd", choices=["entropy", "file", "compare"])
    p.add_argument("input", nargs="?")
    p.add_argument("-s", "--string")
    args = p.parse_args()
    if args.cmd == "entropy":
        if args.string: data = args.string
        elif args.input: data = open(args.input, 'rb').read()
        else: data = sys.stdin.buffer.read()
        H = shannon_entropy(data)
        n_symbols = len(set(data))
        max_entropy = math.log2(n_symbols) if n_symbols > 1 else 0
        compression = (1 - H / 8) * 100  # vs 8 bits per byte
        print(f"Shannon entropy:   {H:.4f} bits/symbol")
        print(f"Max entropy:       {max_entropy:.4f} bits/symbol")
        print(f"Unique symbols:    {n_symbols}")
        print(f"Data length:       {len(data)}")
        print(f"Ideal compressed:  {H * len(data) / 8:.0f} bytes")
        print(f"Compression ratio: {compression:.1f}%")
    elif args.cmd == "file":
        data = open(args.input, 'rb').read()
        H = shannon_entropy(data)
        counts = Counter(data).most_common(20)
        print(f"Entropy: {H:.4f} bits/symbol")
        print(f"\nTop symbols:")
        for sym, count in counts:
            pct = count / len(data) * 100
            try: ch = chr(sym) if 32 <= sym < 127 else f"0x{sym:02x}"
            except: ch = f"0x{sym:02x}"
            print(f"  {ch:>6s}: {count:6d} ({pct:5.1f}%)")

if __name__ == "__main__":
    main()
