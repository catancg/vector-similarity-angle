# Vector similarity by angle

This small project generates random vectors, computes pairwise angle differences (in degrees), and saves a set of diagnostic plots.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

2. Run the analysis (example):

```bash
python analyze_vectors.py --n 500 --dim 128 --seed 42 --outdir results
```

3. Outputs are saved in the `results` folder: heatmap, histogram, PCA scatter, sampled angles, and `summary.json`.

To upload this repo to GitHub: provide a Personal Access Token with `repo` (or `public_repo`) scope and the target repository name. I can then create the remote repo and push the files if you want.
