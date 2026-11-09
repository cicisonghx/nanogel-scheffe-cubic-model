"""
plot_contour.py

Ternary contour map of raw log10(dH) across the AETC/AM/BAC
compositional simplex. This is pure data interpolation (Delaunay
triangulation + linear/gourad shading)

Usage:
    from plot_contour import Plot_contour
    Plot_contour(df)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import mpltern
import config

def Plot_contour(df, file_name = 'contour_raw_data.png'):
    response = np.log10(df['dH'])

    fig = plt.figure(figsize = (8,6), dpi = 300)
    ax = fig.add_subplot(1, 1, 1, projection="ternary")

    cs = ax.tripcolor(df["AETC"], df["AM"], df["BAC"], response,
                      cmap="PuBu", shading="gouraud")
    contour = ax.tricontour(df["AETC"], df["AM"], df["BAC"], response,
                            colors="k", linewidths=0.8)
    ax.clabel(contour, inline=True, fontsize=8, fmt="%.2f")

    ax.set_tlabel("AETC", fontweight="bold", fontsize=12)
    ax.set_llabel("AM", fontweight="bold", fontsize=12)
    ax.set_rlabel("BAC", fontweight="bold", fontsize=12)
    ax.grid(True, alpha=0.5)

    cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
    cbar = fig.colorbar(cs, cax=cax)
    cbar.set_label(r"$log_{10}d_H$ (nm)", rotation=270, va="baseline")

    plt.tight_layout()

    os.makedirs(config.figure_dir, exist_ok=True)
    save_path = os.path.join(config.figure_dir, file_name)
    plt.savefig(save_path, dpi=600, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved contour map -> {save_path}")
    
    return save_path

