#!/usr/bin/env python3
"""Simple demo: 4 two-dimensional vectors, pairwise angle comparison.

Generates a plot of the vectors in 2D and prints/saves the pairwise angle matrix.
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def angle_deg(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    cos = np.dot(a, b) / (na * nb)
    cos = np.clip(cos, -1.0, 1.0)
    return float(np.degrees(np.arccos(cos)))


def main(outdir='out'):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Define 4 explicit 2D vectors
    vectors = np.array([
        [1.0, 0.0],   # along +x
        [0.0, 1.0],   # along +y
        [1.0, 1.0],   # 45 degrees
        [-1.0, 0.5],  # a vector pointing left-up
    ])

    n = vectors.shape[0]
    angles = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            angles[i, j] = angle_deg(vectors[i], vectors[j])

    # Print the angle matrix
    np.set_printoptions(precision=2, suppress=True)
    print('Pairwise angles (degrees):')
    print(angles)

    # Plot vectors in 2D with annotations
    plt.figure(figsize=(6, 6))
    ax = plt.gca()
    colors = ['C0', 'C1', 'C2', 'C3']
    for i, v in enumerate(vectors):
        ax.arrow(0, 0, v[0], v[1], head_width=0.08, head_length=0.12, fc=colors[i], ec=colors[i], length_includes_head=True)
        ax.text(v[0] * 1.05, v[1] * 1.05, f'{i}', color=colors[i], fontsize=12)

    # Annotate pairwise angles (i < j) near the midpoint between vector tips
    for i in range(n):
        for j in range(i + 1, n):
            vi = vectors[i]
            vj = vectors[j]
            mid = (vi + vj) / 2.0
            angle_val = angles[i, j]
            # small offset outward from origin for readability
            offset = 0.12
            pos = mid * 1.05
            ax.text(pos[0], pos[1], f'{angle_val:.1f}°', fontsize=9, color='k', ha='center', va='center', bbox=dict(facecolor='white', alpha=0.6, boxstyle='round'))

    maxc = np.max(np.abs(vectors)) * 1.4
    ax.set_xlim(-maxc, maxc)
    ax.set_ylim(-maxc, maxc)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title('4 Two-Dimensional Vectors (indices labeled)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.tight_layout()
    plt.savefig(outdir / 'vectors_2d.png')
    plt.close()

    # Save a small textual summary
    import json

    summary = {
        'vectors': vectors.tolist(),
        'angles_degrees': angles.tolist(),
    }
    with open(outdir / 'simple_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    print('Saved plots to', outdir)


if __name__ == '__main__':
    main()
