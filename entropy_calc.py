#!/usr/bin/env python3
"""entropy_calc - Shannon entropy, mutual information, and KL divergence."""
import sys, json, math
from collections import Counter

def entropy(data):
    n = len(data)
    if n == 0: return 0.0
    counts = Counter(data)
    return -sum((c/n) * math.log2(c/n) for c in counts.values())

def joint_entropy(x, y):
    pairs = list(zip(x, y))
    return entropy(pairs)

def mutual_info(x, y):
    return entropy(x) + entropy(y) - joint_entropy(x, y)

def kl_divergence(p, q):
    total = 0.0
    for pi, qi in zip(p, q):
        if pi > 0:
            if qi <= 0: return float('inf')
            total += pi * math.log2(pi / qi)
    return total

def conditional_entropy(x, y):
    return joint_entropy(x, y) - entropy(y)

def main():
    print("Information theory calculator\n")
    data = "aabbbccccdddddeeeee"
    print(f"H('{data}') = {entropy(data):.4f} bits")
    fair_coin = [0,1]*50
    print(f"H(fair coin) = {entropy(fair_coin):.4f} bits")
    biased = [0]*90 + [1]*10
    print(f"H(90/10 coin) = {entropy(biased):.4f} bits")
    x = [0,0,1,1,0,1,0,1,1,0]
    y = [0,0,1,1,0,1,1,0,1,0]
    print(f"\nI(X;Y) = {mutual_info(x,y):.4f} bits")
    print(f"H(X|Y) = {conditional_entropy(x,y):.4f} bits")
    p = [0.25, 0.25, 0.25, 0.25]
    q = [0.1, 0.2, 0.3, 0.4]
    print(f"\nKL(uniform||q) = {kl_divergence(p,q):.4f} bits")
    print(f"KL(q||uniform) = {kl_divergence(q,p):.4f} bits")

if __name__ == "__main__":
    main()
