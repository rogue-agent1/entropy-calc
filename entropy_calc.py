#!/usr/bin/env python3
"""entropy_calc - Information entropy analysis."""
import sys, argparse, json, math
from collections import Counter

def shannon_entropy(data):
    freq = Counter(data)
    total = len(data)
    return -sum((c/total) * math.log2(c/total) for c in freq.values() if c > 0)

def main():
    p = argparse.ArgumentParser(description="Entropy calculator")
    p.add_argument("input", help="Text, file (@path), or hex data")
    p.add_argument("--mode", choices=["text","bytes","words"], default="text")
    args = p.parse_args()
    data = args.input
    if data.startswith("@"):
        with open(data[1:], "rb" if args.mode == "bytes" else "r") as f: data = f.read()
    if args.mode == "words": tokens = data.split()
    elif args.mode == "bytes": tokens = list(data if isinstance(data, bytes) else data.encode())
    else: tokens = list(data)
    ent = shannon_entropy(tokens)
    unique = len(set(tokens))
    max_ent = math.log2(unique) if unique > 1 else 0
    print(json.dumps({"entropy": round(ent, 4), "max_entropy": round(max_ent, 4), "efficiency": round(ent/max_ent, 4) if max_ent else 0, "unique_symbols": unique, "total_symbols": len(tokens), "bits_per_symbol": round(ent, 4), "total_bits": round(ent * len(tokens), 1)}, indent=2))

if __name__ == "__main__": main()
