# CSE440 Lab Project — Group 3

**Multi-Class News Topic Classification: A Comparative Analysis**
Imtiaz Hossain (23101137), Md Saidul Islam Apu (21301668)

## Project layout

| Path | Purpose |
|---|---|
| `3_23101137_21301668.ipynb` | Main deliverable notebook — 74 cells, 27 experiments (all outputs visible) |
| `Training_data_3.csv` | Training corpus (102,002 rows) |
| `Test_data.csv` | Held-out test corpus (12,000 rows) |
| `Spring 2026 - CSE440 Lab Project.pdf` | Original project specification |
| `artifacts/results_summary.csv` | Final results table (27 rows) |
| `artifacts/plots/` | All 33 figures (5 EDA + 1 grid + 27 confusion matrices) |
| `report/3_23101137_21301668.tex` | IEEE-format LaTeX report |
| `report/plots/` | Subset of figures referenced by the .tex |

## Hardware

- GPU: NVIDIA RTX 3070 (8 GB VRAM, CUDA 11.8)
- All neural networks run on **PyTorch 2.7.1+cu118** — TensorFlow ≥ 2.11 dropped native-Windows GPU support.

## How to reproduce

Open the notebook in Jupyter and `Cell → Run All`:
```bash
jupyter notebook 3_23101137_21301668.ipynb
```
Full run from scratch on the RTX 3070: roughly 1.5 h for the RNN family, ~12 min per BERT variant. The notebook is already populated with outputs for all 27 runs plus the 27 confusion-matrix re-evaluations.

## Final results — 27 runs

Test-set macro-F1 (saved to `artifacts/results_summary.csv`):

| Model | none | extreme | optimum |
|---|---|---|---|
| Logistic Regression | 0.9098 | **0.9209** | 0.9192 |
| Deep NN             | 0.8804 | 0.9139 | **0.9144** |
| SimpleRNN           | 0.8883 | 0.9009 | **0.9021** |
| GRU                 | 0.9151 | 0.9163 | **0.9168** |
| LSTM                | 0.9168 | **0.9183** | 0.9159 |
| Bi-SimpleRNN        | 0.8990 | 0.9009 | **0.9031** |
| Bi-GRU              | 0.9148 | 0.9155 | **0.9214** |
| Bi-LSTM             | 0.9108 | **0.9186** | 0.9164 |
| **BERT-Base**       | **0.9376** | 0.9288 | 0.9313 |

All neural models trained up to 15 epochs with EarlyStopping (patience=2 on validation macro-F1). BERT EarlyStopping fired at epoch 5–6 across the three variants.

- **Best**: BERT-Base on *none* — macro-F1 0.9376 (~35 min train, EarlyStop at ep 6)
- **Best non-Transformer**: Bi-GRU on *optimum* — macro-F1 0.9214 (~19 s train, ~110× faster)
- **Worst**: Deep NN on *none* — macro-F1 0.8804

Hyperparameter probes:
- LogReg on *optimum*: C ∈ {0.5, 1.0, 2.0} → val macro-F1 0.9174 / **0.9225** / 0.9273. Chose C=1.0.
- LSTM on *optimum*: hidden ∈ {64, 128} → both ~0.91 at 4-epoch budget. Chose hidden=64 for the full 8-epoch sweep.

