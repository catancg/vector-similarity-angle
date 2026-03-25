#!/usr/bin/env python3
"""Generate vectors, compute pairwise angle differences, and plot results.

Usage: python analyze_vectors.py --n 200 --dim 64
"""
import argparse
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA


def generate_vectors(n=200, dim=64, seed=None, distribution='normal'):
    rng = np.random.default_rng(seed)
    if distribution == 'normal':
        V = rng.normal(size=(n, dim))
    elif distribution == 'uniform':
        V = rng.uniform(-1, 1, size=(n, dim))
    else:
        raise ValueError('unknown distribution')
    return V


def angle_matrix_from_vectors(V):
    # V shape: (n, dim)
    norms = np.linalg.norm(V, axis=1)
    dots = V @ V.T
    denom = np.outer(norms, norms)
    eps = 1e-12
    cos_sim = dots / (denom + eps)
    cos_sim = np.clip(cos_sim, -1.0, 1.0)
    angles = np.degrees(np.arccos(cos_sim))
    return angles, cos_sim


def plot_heatmap(angle_mat, outpath, vmax=None):
    plt.figure(figsize=(8, 6))
    sns.heatmap(angle_mat, cmap='viridis', vmin=0, vmax=vmax)
    plt.title('Pairwise angles (degrees)')
    plt.xlabel('Vector index')
    plt.ylabel('Vector index')
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_histogram(angle_mat, outpath):
    # take upper triangle angles (excluding diagonal)
    n = angle_mat.shape[0]
    i, j = np.triu_indices(n, k=1)
    vals = angle_mat[i, j]
    plt.figure(figsize=(6, 4))
    sns.histplot(vals, bins=60, kde=True)
    plt.xlabel('Angle (degrees)')
    plt.title('Distribution of pairwise angles')
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_pca_scatter(V, angle_mat, outpath, annotate_count=0):
    pca = PCA(n_components=2)
    proj = pca.fit_transform(V)
    # color by mean angle to others
    mean_angle = np.mean(angle_mat, axis=1)
    plt.figure(figsize=(7, 6))
    sc = plt.scatter(proj[:, 0], proj[:, 1], c=mean_angle, cmap='plasma', s=40, alpha=0.9)
    plt.colorbar(sc, label='Mean pairwise angle (deg)')
    plt.title('PCA projection colored by mean angle')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    if annotate_count > 0:
        for idx in range(min(annotate_count, proj.shape[0])):
            plt.text(proj[idx, 0], proj[idx, 1], str(idx), fontsize=8)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_similarity_scatter(angle_mat, outpath, sample_pairs=1000, seed=None):
    rng = np.random.default_rng(seed)
    n = angle_mat.shape[0]
    i = rng.integers(0, n, size=sample_pairs)
    j = rng.integers(0, n, size=sample_pairs)
    vals = angle_mat[i, j]
    plt.figure(figsize=(6, 4))
    plt.scatter(np.zeros_like(vals), vals, alpha=0.3)
    plt.ylabel('Angle (deg)')
    plt.title('Sampled pairwise angles')
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def run(n=200, dim=64, seed=0, outdir='out', distribution='normal', show=False):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    V = generate_vectors(n, dim, seed=seed, distribution=distribution)
    angles, cos_sim = angle_matrix_from_vectors(V)

    # Heatmap capped at 180 degrees; most angles concentrate around 90 for random vectors
    plot_heatmap(angles, outdir / 'angles_heatmap.png', vmax=180)
    plot_histogram(angles, outdir / 'angles_histogram.png')
    plot_pca_scatter(V, angles, outdir / 'pca_mean_angle.png', annotate_count=0)
    plot_similarity_scatter(angles, outdir / 'sampled_angles.png', seed=seed)

    # Save a small summary text
    n_pairs = n * (n - 1) // 2
    upper = angles[np.triu_indices(n, k=1)]
    summary = {
        'n_vectors': n,
        'dim': dim,
        'mean_angle_deg': float(np.mean(upper)),
        'median_angle_deg': float(np.median(upper)),
        'std_angle_deg': float(np.std(upper)),
        'n_pairs': int(n_pairs),
    }
    import json

    with open(outdir / 'summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    if show:
        import webbrowser
        print('Plots saved to', outdir)
        # Attempt to open the heatmap
        try:
            webbrowser.open((outdir / 'angles_heatmap.png').absolute().as_uri())
        except Exception:
            pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--n', type=int, default=200, help='number of vectors')
    p.add_argument('--dim', type=int, default=64, help='dimension of vectors')
    p.add_argument('--seed', type=int, default=0, help='random seed')
    p.add_argument('--outdir', type=str, default='out', help='output directory for plots')
    p.add_argument('--distribution', type=str, default='normal', choices=['normal', 'uniform'])
    p.add_argument('--show', action='store_true', help='open the main heatmap after running')
    args = p.parse_args()
    run(n=args.n, dim=args.dim, seed=args.seed, outdir=args.outdir, distribution=args.distribution, show=args.show)


if __name__ == '__main__':
    main()
