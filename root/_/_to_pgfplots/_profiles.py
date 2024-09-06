from ROOT import TProfile
import numpy as np


def get_TProfile_as_pgfplot(profile: TProfile, only_data: bool = False):
    n_bins = profile.GetXaxis().GetNbins()

    if not only_data:
        tikz_code = r"""
            \begin{tikzpicture}
                \begin{axis}[]
                \addplot[
                    error bars/.cd,
                    x dir = both, x explicit,
                    y dir = both, y explicit,
                ] table [
                    x error plus  = ex,
                    x error minus = ex,
                    y error plus  = ey,
                    y error minus = ey,
                ] {
                    x y ex ey
        """
    else:
        tikz_code = "                    x y ex ey\n"
        tikz_code += "        "

    for i in range(1, n_bins + 1):
        x = profile.GetXaxis().GetBinCenter(i)
        y = profile.GetBinContent(i)
        bin_width = profile.GetXaxis().GetBinWidth(i)
        ex = bin_width / 2
        ey = profile.GetBinError(i)

        if i == 1:
            tikz_code += f"            {x} {y} {ex} {ey}\n"
        else:
            tikz_code += f"                    {x} {y} {ex} {ey}\n"

    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code


def get_uproot_TProfile_as_pgfplot(profile, only_data: bool = False):
    edges = np.array(profile.axes[0].edges(), dtype=np.float64)
    
    bin_centers  = (edges[:-1] + edges[1:])/2
    bin_widths   = edges[1:] - edges[:-1]
    bin_contents = np.array(profile.values(), dtype=np.float64)
    bin_errors   = np.array(profile.errors(), dtype=np.float64)
    n_bins       = len(bin_centers)

    if not only_data:
        tikz_code = r"""
            \begin{tikzpicture}
                \begin{axis}[]
                \addplot[
                    error bars/.cd,
                    x dir = both, x explicit,
                    y dir = both, y explicit,
                ] table [
                    x error plus  = ex,
                    x error minus = ex,
                    y error plus  = ey,
                    y error minus = ey,
                ] {
                    x y ex ey
        """
    else:
        tikz_code = "                    x y ex ey\n"
        tikz_code += "        "

    for i in range(n_bins):
        x  = bin_centers[i]
        y  = bin_contents[i]
        ex = bin_widths[i]/2
        ey = bin_errors[i]

        if i == 0:
            tikz_code += f"            {x} {y} {ex} {ey}\n"
        else:
            tikz_code += f"                    {x} {y} {ex} {ey}\n"

    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code