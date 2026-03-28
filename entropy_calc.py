#!/usr/bin/env python3
"""entropy_calc - Calculate Shannon entropy and randomness metrics."""
import argparse, math, sys, collections

def shannon_entropy(data):
    if not data: return 0
    freq = collections.Counter(data)
    n = len(data)
    return -sum((c/n) * math.log2(c/n) for c in freq.values())

def byte_entropy(data):
    if not data: return 0
    freq = collections.Counter(data)
    n = len(data)
    return -sum((c/n) * math.log2(c/n) for c in freq.values())

def chi_squared(data):
    expected = len(data) / 256
    freq = [0] * 256
    for b in data: freq[b] += 1
    return sum((f - expected)**2 / expected for f in freq)

def serial_correlation(data):
    n = len(data)
    if n < 2: return 0
    mean = sum(data) / n
    num = sum((data[i]-mean)*(data[(i+1)%n]-mean) for i in range(n))
    den = sum((data[i]-mean)**2 for i in range(n))
    return num / den if den else 0

def monte_carlo_pi(data):
    if len(data) < 8: return 0
    pairs = len(data) // 8
    inside = 0
    for i in range(pairs):
        x = int.from_bytes(data[i*8:i*8+4], "big") / 2**32
        y = int.from_bytes(data[i*8+4:i*8+8], "big") / 2**32
        if x*x + y*y <= 1: inside += 1
    return 4 * inside / pairs if pairs else 0

def main():
    p = argparse.ArgumentParser(description="Entropy calculator")
    p.add_argument("input", help="File or '-' for stdin")
    p.add_argument("-t","--text", action="store_true", help="Treat as text")
    a = p.parse_args()
    if a.input == "-": data = sys.stdin.buffer.read()
    else:
        with open(a.input, "rb") as f: data = f.read()
    if a.text:
        text = data.decode("utf-8", errors="replace")
        ent = shannon_entropy(text)
        max_ent = math.log2(len(set(text))) if set(text) else 0
        print(f"Text length: {len(text)} chars")
        print(f"Unique chars: {len(set(text))}")
        print(f"Shannon entropy: {ent:.4f} bits/char")
        print(f"Max possible: {max_ent:.4f} bits/char")
        print(f"Efficiency: {100*ent/max_ent:.1f}%" if max_ent else "N/A")
    else:
        ent = byte_entropy(data)
        chi = chi_squared(data)
        sc = serial_correlation(list(data))
        pi_est = monte_carlo_pi(data)
        print(f"File size: {len(data):,} bytes")
        print(f"Byte entropy: {ent:.4f} bits/byte (max 8.0)")
        print(f"Randomness: {100*ent/8:.1f}%")
        print(f"Chi-squared: {chi:.2f} (ideal ~256)")
        print(f"Serial correlation: {sc:.6f} (ideal ~0)")
        if len(data) >= 8:
            print(f"Monte Carlo Pi: {pi_est:.6f} (ideal 3.14159)")
        quality = "Random" if ent > 7.5 else "Moderate" if ent > 6 else "Low" if ent > 4 else "Not random"
        print(f"\nQuality: {quality}")

if __name__ == "__main__": main()
