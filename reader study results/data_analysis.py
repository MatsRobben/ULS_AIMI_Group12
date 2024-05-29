import pandas as pd
import numpy as np

df = pd.read_excel("group2_iou_scores.xlsx")
df = df.to_dict()
results = df["Case Number,FennaR_GT_IoU,Lucia_GT_IoU,MatsWillem_GT_IoU,mdeboerblazdell_GT_IoU,combined_GT_IoU"]

fenna_iou = []
lucia_iou = []
mats_iou = []
max_iou = []
combined_iou = []


for value in results.values():
    results = value.split(",")
    results = [float(r) for r in results]
    fenna_iou.append(results[1])
    lucia_iou.append(results[2])
    mats_iou.append(results[3])
    max_iou.append(results[4])
    combined_iou.append(results[5])

print(f"Fenna: average: {np.average(fenna_iou):.3f}, std: {np.std(fenna_iou):.3f}, max: {np.max(fenna_iou):.3f}, min: {np.min(fenna_iou):.3f}")
print(f"Lucia: average: {np.average(lucia_iou):.3f}, std: {np.std(lucia_iou):.3f}, max: {np.max(lucia_iou):.3f}, min: {np.min(lucia_iou):.3f}")
print(f"Mats: average: {np.average(mats_iou):.3f}, std: {np.std(mats_iou):.3f}, max: {np.max(mats_iou):.3f}, min: {np.min(mats_iou):.3f}")
print(f"Max: average: {np.average(max_iou):.3f}, std: {np.std(max_iou):.3f}, max: {np.max(max_iou):.3f}, min: {np.min(max_iou):.3f}")
print(f"Combined: average: {np.average(combined_iou):.3f}, std: {np.std(combined_iou):.3f}, max: {np.max(combined_iou):.3f}, min: {np.min(combined_iou):.3f}")



