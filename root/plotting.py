import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ROOT
import seaborn as sns

from . import converters


def errplot(
    input_object,
    cols: dict = {
        "x": "x", "y": "y", "z": "z", "ex": "ex", "ey": "ey",
        "exl": "exl", "exh": "exh", "eyl": "eyl", "eyh": "eyh",
    },
    density: bool = False,
    ax=None,
    **kwargs
):
    """
    Plot a ROOT/uproot object or string path ("file.root:hist") as error bars.
    """
    label = kwargs.pop("label", None)
    if label is None:
        if isinstance(input_object, str):
            label = input_object.split(":")[-1] if ":" in input_object else input_object
        elif hasattr(input_object, "GetName"):
            label = input_object.GetName()
        elif hasattr(input_object, "name"):
            label = input_object.name

    data_frame = converters.to_pandas(input_object, cols=cols)
    y_values = data_frame[cols["y"]].copy()

    if density:
        if cols["ex"] in data_frame:
            bin_widths = 2.0 * data_frame[cols["ex"]]
        elif cols["exl"] in data_frame and cols["exh"] in data_frame:
            bin_widths = data_frame[cols["exl"]] + data_frame[cols["exh"]]
        else:
            bin_widths = 1.0

        total_integral = (y_values * bin_widths).sum()
        if total_integral > 0:
            scale_factor = total_integral * bin_widths
            y_values = y_values / scale_factor
            if cols["ey"] in data_frame:
                data_frame[cols["ey"]] = data_frame[cols["ey"]] / scale_factor
            if cols["eyl"] in data_frame:
                data_frame[cols["eyl"]] = data_frame[cols["eyl"]] / scale_factor
            if cols["eyh"] in data_frame:
                data_frame[cols["eyh"]] = data_frame[cols["eyh"]] / scale_factor

    x_errors = None
    if cols["ex"] in data_frame:
        x_errors = data_frame[cols["ex"]]
    elif cols["exl"] in data_frame and cols["exh"] in data_frame:
        x_errors = [data_frame[cols["exl"]], data_frame[cols["exh"]]]

    y_errors = None
    if cols["ey"] in data_frame:
        y_errors = data_frame[cols["ey"]]
    elif cols["eyl"] in data_frame and cols["eyh"] in data_frame:
        y_errors = [data_frame[cols["eyl"]], data_frame[cols["eyh"]]]

    target_axes = ax if ax is not None else plt.gca()

    return target_axes.errorbar(
        data_frame[cols["x"]], y_values, xerr=x_errors, yerr=y_errors, label=label, **kwargs
    )


def histplot(
    input_object,
    ax=None,
    density: bool = False,
    filled: bool = False,
    alpha: float = 0.4,
    **kwargs
):
    """
    Plot a 1D histogram (ROOT, uproot, or string path) as a step distribution.
    """
    label = kwargs.pop("label", None)
    if label is None:
        if isinstance(input_object, str):
            label = input_object.split(":")[-1] if ":" in input_object else input_object
        elif hasattr(input_object, "GetName"):
            label = input_object.GetName()
        elif hasattr(input_object, "name"):
            label = input_object.name

    x_centers, y_values, x_edges, x_errors, y_errors = converters.to_numpy(input_object)

    if density:
        bin_widths = x_edges[1:] - x_edges[:-1]
        total_integral = (y_values * bin_widths).sum()
        if total_integral > 0:
            scale_factor = total_integral * bin_widths
            y_values = y_values / scale_factor

    target_axes = ax if ax is not None else plt.gca()

    if filled:
        return target_axes.fill_between(x_edges[:-1], y_values, step="post", alpha=alpha, label=label, **kwargs)
    else:
        return target_axes.step(x_edges[:-1], y_values, where="post", label=label, **kwargs)


def hist2d_plot(
    input_object,
    ax=None,
    cbar: bool = True,
    cbar_label: str = "",
    logz: bool = False,
    cmap: str = "rocket",
    labels: bool = False,
    **kwargs
):
    """
    Plot a 2D histogram (TH2, TProfile2D, uproot 2D model, or string path) using Seaborn colormaps and pcolormesh.
    """
    if ax is None:
        fig, ax = plt.subplots()

    x_centers, y_centers, bin_values, x_edges, y_edges, x_errs, y_errs, z_errs = converters.to_numpy(input_object)

    color_norm = None
    if logz:
        from matplotlib.colors import LogNorm
        positive_values = bin_values[bin_values > 0]
        vmin = kwargs.pop("vmin", positive_values.min() if len(positive_values) > 0 else 1e-3)
        vmax = kwargs.pop("vmax", bin_values.max() if len(bin_values) > 0 else 1.0)
        color_norm = LogNorm(vmin=vmin, vmax=vmax)

    if isinstance(cmap, str):
        try:
            cmap = sns.color_palette(cmap, as_cmap=True)
        except ValueError:
            pass

    mesh = ax.pcolormesh(x_edges, y_edges, bin_values, cmap=cmap, norm=color_norm, **kwargs)

    if labels:
        for i in range(len(y_centers)):
            for j in range(len(x_centers)):
                val = bin_values[i, j]
                if val != 0:
                    ax.text(x_centers[j], y_centers[i], f"{val:.4g}", ha="center", va="center", fontsize=8)

    if cbar:
        colorbar_obj = plt.colorbar(mesh, ax=ax, label=cbar_label)
        return ax, mesh, colorbar_obj

    return ax, mesh


def ratio_plot(
    numerator_object,
    denominator_object,
    ax=None,
    ratio_ax=None,
    rlabel: str = "Ratio",
    rlim: tuple = None,
    density: bool = False,
    num_kwargs: dict = None,
    den_kwargs: dict = None,
    ratio_kwargs: dict = None,
    cols: dict = {
        "x": "x", "y": "y", "z": "z",
        "ex": "ex", "ey": "ey", "exl": "exl",
        "exh": "exh", "eyl": "eyl", "eyh": "eyh",
    },
    **kwargs
):
    """
    Create a dual-panel plot showing top distributions (numerator_object & denominator_object) and their ratio on the bottom panel.
    """
    numerator_kwargs = num_kwargs or {}
    denominator_kwargs = den_kwargs or {}
    ratio_kwargs = ratio_kwargs or {}

    if "fmt" not in numerator_kwargs:
        numerator_kwargs.setdefault("fmt", "o")
    if "fmt" not in denominator_kwargs:
        denominator_kwargs.setdefault("fmt", "s")

    for key, value in kwargs.items():
        numerator_kwargs.setdefault(key, value)
        denominator_kwargs.setdefault(key, value)
        ratio_kwargs.setdefault(key, value)

    if ax is None or ratio_ax is None:
        fig, (ax, ratio_ax) = plt.subplots(
            2, 1, figsize=(7, 6), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
        )
        fig.subplots_adjust(hspace=0.05)
    else:
        fig = ax.get_figure()

    errplot(numerator_object, cols=cols, density=density, ax=ax, **numerator_kwargs)
    errplot(denominator_object, cols=cols, density=density, ax=ax, **denominator_kwargs)

    ax.legend()

    df_num = converters.to_pandas(numerator_object, cols=cols)
    df_den = converters.to_pandas(denominator_object, cols=cols)

    x_num = df_num[cols["x"]].values.astype(float)
    y_num = df_num[cols["y"]].values.astype(float)

    x_den = df_den[cols["x"]].values.astype(float)
    y_den = df_den[cols["y"]].values.astype(float)

    yerr_num = df_num[cols["ey"]].values.astype(float) if cols["ey"] in df_num else np.zeros_like(y_num)
    yerr_den = df_den[cols["ey"]].values.astype(float) if cols["ey"] in df_den else np.zeros_like(y_den)

    widths_num = 2.0 * df_num[cols["ex"]].values.astype(float) if cols["ex"] in df_num else np.ones_like(y_num)
    widths_den = 2.0 * df_den[cols["ex"]].values.astype(float) if cols["ex"] in df_den else np.ones_like(y_den)

    if density:
        area_num = (y_num * widths_num).sum()
        area_den = (y_den * widths_den).sum()
        if area_num > 0:
            scale_num = area_num * widths_num
            y_num = y_num / scale_num
            yerr_num = yerr_num / scale_num
        if area_den > 0:
            scale_den = area_den * widths_den
            y_den = y_den / scale_den
            yerr_den = yerr_den / scale_den

    if len(x_num) == len(x_den) and np.allclose(x_num, x_den):
        y_num_comp, yerr_num_comp = y_num, yerr_num
        y_den_comp, yerr_den_comp = y_den, yerr_den
    else:
        if not density:
            y_num_dens = y_num / widths_num
            yerr_num_dens = yerr_num / widths_num
            y_den_dens = y_den / widths_den
            yerr_den_dens = yerr_den / widths_den
        else:
            y_num_dens, yerr_num_dens = y_num, yerr_num
            y_den_dens, yerr_den_dens = y_den, yerr_den

        y_num_comp, yerr_num_comp = y_num_dens, yerr_num_dens
        y_den_comp = np.interp(x_num, x_den, y_den_dens)
        yerr_den_comp = np.interp(x_num, x_den, yerr_den_dens)

    with np.errstate(divide="ignore", invalid="ignore"):
        ratio_values = np.where(y_den_comp != 0, y_num_comp / y_den_comp, np.nan)
        ratio_errors = np.where(
            y_den_comp != 0,
            np.sqrt((yerr_num_comp / y_den_comp)**2 + (ratio_values * yerr_den_comp / y_den_comp)**2),
            np.nan
        )

    x_points = x_num
    x_errors = df_num[cols["ex"]].values if cols["ex"] in df_num else None

    ratio_ax.axhline(1.0, color="gray", linestyle="--", linewidth=1.0)

    ratio_color = ratio_kwargs.pop("color", numerator_kwargs.get("color", "black"))
    ratio_format = ratio_kwargs.pop("fmt", numerator_kwargs.get("fmt", "o"))

    ratio_ax.errorbar(x_points, ratio_values, xerr=x_errors, yerr=ratio_errors, fmt=ratio_format, color=ratio_color, **ratio_kwargs)
    ratio_ax.set_ylabel(rlabel)

    if rlim is not None:
        ratio_ax.set_ylim(rlim)
    else:
        valid_mask = np.isfinite(ratio_values) & np.isfinite(ratio_errors)
        if np.any(valid_mask):
            y_reach_upper = ratio_values[valid_mask] + ratio_errors[valid_mask]
            y_reach_lower = ratio_values[valid_mask] - ratio_errors[valid_mask]
            ratio_min = min(1.0, y_reach_lower.min())
            ratio_max = max(1.0, y_reach_upper.max())
            span = ratio_max - ratio_min
            y_padding = 0.10 * span if span > 0 else 0.1
            ratio_ax.set_ylim(ratio_min - y_padding, ratio_max + y_padding)

    return fig, ax, ratio_ax


def stack_plot(
    input_objects: list,
    ax=None,
    labels: list = None,
    colors: list = None,
    palette: str = "deep",
    density: bool = False,
    alpha: float = 0.7,
    draw_outline: bool = True,
    cols: dict = {
        "x": "x", "y": "y", "z": "z",
        "ex": "ex", "ey": "ey", "exl": "exl",
        "exh": "exh", "eyl": "eyl", "eyh": "eyh",
    },
    **kwargs
):
    """
    Plot a stack of 1D histograms (ROOT, uproot, or string paths) as cumulative filled step areas.
    """
    if not input_objects:
        raise ValueError("input_objects list cannot be empty!")

    if labels is None:
        labels = []
        for obj in input_objects:
            if isinstance(obj, str):
                lbl = obj.split(":")[-1] if ":" in obj else obj
            elif hasattr(obj, "GetName"):
                lbl = obj.GetName()
            elif hasattr(obj, "name"):
                lbl = obj.name
            else:
                lbl = "Histogram"
            labels.append(lbl)

    if colors is None:
        colors = sns.color_palette(palette, n_colors=len(input_objects))

    y_list = []
    x_edges_base = None
    x_centers_base = None

    for obj in input_objects:
        x_centers, y_values, x_edges, x_errors, y_errors = converters.to_numpy(obj)
        if x_edges_base is None:
            x_edges_base = x_edges
            x_centers_base = x_centers
        elif len(x_edges) != len(x_edges_base) or not np.allclose(x_edges, x_edges_base):
            bin_widths = x_edges[1:] - x_edges[:-1]
            base_widths = x_edges_base[1:] - x_edges_base[:-1]
            y_dens = y_values / bin_widths
            y_values = np.interp(x_centers_base, x_centers, y_dens) * base_widths

        y_list.append(y_values)

    y_matrix = np.vstack(y_list)
    y_cumulative = np.cumsum(y_matrix, axis=0)

    if density:
        bin_widths = x_edges_base[1:] - x_edges_base[:-1]
        total_integral = (y_cumulative[-1] * bin_widths).sum()
        if total_integral > 0:
            y_cumulative = y_cumulative / total_integral

    target_axes = ax if ax is not None else plt.gca()

    for i in range(len(input_objects)):
        bottom_layer = y_cumulative[i - 1] if i > 0 else 0
        target_axes.fill_between(
            x_edges_base[:-1],
            bottom_layer,
            y_cumulative[i],
            step="post",
            color=colors[i],
            alpha=alpha,
            label=labels[i],
            **kwargs
        )
        if draw_outline:
            target_axes.step(x_edges_base[:-1], y_cumulative[i], where="post", color="black", linewidth=0.7)

    return target_axes, y_cumulative
