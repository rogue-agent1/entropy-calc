#!/usr/bin/env python3
"""Shannon entropy calculator for strings and files."""
import sys, math, collections

def entropy(data):
    if not data: return 0.0
    freq = collections.Counter(data)
    n = len(data)
    return -sum((c/n) * math.log2(c/n) for c in freq.values())

def byte_entropy(data):
    if not data: return 0.0
    freq = [0]*256
    for b in data: freq[b] += 1
    n = len(data)
    return -sum((f/n)*math.log2(f/n) for f in freq if f > 0)

def analyze(data):
    e = entropy(data)
    max_e = math.log2(len(set(data))) if len(set(data)) > 1 else 0
    return {"entropy": e, "max_entropy": max_e, "efficiency": e/max_e if max_e else 0,
            "length": len(data), "unique_chars": len(set(data))}

def cli():
    if len(sys.argv) < 2:
        print("Usage: entropy_calc <string|--file path>"); sys.exit(1)
    if sys.argv[1] == "--file":
        with open(sys.argv[2], "rb") as f: data = f.read()
        e = byte_entropy(data)
        print(f"File: {sys.argv[2]}"); print(f"Size: {len(data)} bytes")
        print(f"Byte entropy: {e:.4f} bits/byte (max 8.0)")
        print(f"Randomness: {e/8*100:.1f}%")
    else:
        text = " ".join(sys.argv[1:])
        info = analyze(text)
        print(f"Text: {text[:60]}{'...' if len(text)>60 else ''}")
        print(f"Entropy: {info['entropy']:.4f} bits/char")
        print(f"Max possible: {info['max_entropy']:.4f} bits/char")
        print(f"Efficiency: {info['efficiency']*100:.1f}%")
        print(f"Length: {info['length']}, Unique chars: {info['unique_chars']}")

if __name__ == "__main__": cli()
