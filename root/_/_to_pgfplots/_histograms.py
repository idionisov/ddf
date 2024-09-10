from ROOT import TH1, TH2
import numpy as np


def _get_TH1_as_pgfplot(h: TH1, only_data: bool = False):
    n_bins = h.GetXaxis().GetNbins()

    if not only_data:
        tikz_code = r"""
            \begin{tikzpicture}
                \begin{axis}[
                    ymin=0
                ]
                \addplot[
                    const plot,
                    no markers
                ] table [x=x, y=y] {
        """
        tikz_code += "            x y \n"
    else: 
        tikz_code = ""
        tikz_code += "                    x y \n"
    
    
    tikz_code += f"                    {h.GetXaxis().GetBinLowEdge(1)} {0}\n"
    for i in range(1, n_bins + 1):
        x_low = h.GetXaxis().GetBinLowEdge(i)
        y = h.GetBinContent(i)
        tikz_code += f"                    {x_low} {y}\n"
        x_up = h.GetXaxis().GetBinUpEdge(i)
        tikz_code += f"                    {x_up} {y}\n"
    tikz_code += f"                    {x_up} {0}\n"

    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    # Strip unnecessary indentations
    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)

        
    return tikz_code


def _get_TH2_as_pgfplot(h: TH2, only_data: bool = False):
    
    n_bins_x = h.GetXaxis().GetNbins()
    n_bins_y = h.GetYaxis().GetNbins()

    if not only_data:
        tikz_code = r"""
            \begin{tikzpicture}
                \begin{axis} [
                    view={0}{90},           % This creates a 2D view (top-down)
                    colorbar,               % Adds a colorbar to the side
                    xlabel={X-axis},        % Label for X-axis
                    ylabel={Y-axis},        % Label for Y-axis
                ] \addplot [
                    matrix plot*,           % For a 2D histogram (heatmap)
                    point meta=explicit,    % Allows using the z-values explicitly
        """
        tikz_code += f"                mesh/cols={n_bins_x},            % Number of columns in the matrix\n"
        tikz_code += f"                mesh/rows={n_bins_y},            % Number of rows in the matrix\n"
        
        tikz_code += "                ] table [meta=z] {\n"
        tikz_code += "                    x y z\n"
    else:
        tikz_code =  "                x y z\n"
        tikz_code += "        "

    for xbin in range(1, n_bins_x + 1):
        x = h.GetXaxis().GetBinCenter(xbin)

        for ybin in range(1, n_bins_y + 1):
            y = h.GetYaxis().GetBinCenter(ybin)
            z = h.GetBinContent(xbin, ybin)

            tikz_code += f"                    {x} {y} {z}\n"

    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code



def _get_uproot_TH1_as_pgfplot(h, only_data: bool = False):
    edges    = np.array(h.axes[0].edges(), dtype=np.float64)
    contents = np.array(h.values(), dtype=np.float64)
    
    if not only_data:
        tikz_code = r"""
            \begin{tikzpicture}
                \begin{axis}[
                    ymin=0
                ]
                \addplot[
                    const plot,
                    no markers
                ] table [x=x, y=y] {
        """
        tikz_code += "            x y \n"
    else: 
        tikz_code = ""
        tikz_code += "                    x y \n"

    tikz_code += f"                    {edges[0]} {0}\n"
    for i in range(len(contents)):
        tikz_code += f"                    {edges[i]} {contents[i]}\n"
        tikz_code += f"                    {edges[i+1]} {contents[i]}\n"
    tikz_code += f"                    {edges[-1]} {0}\n"
    
    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code


def _get_uproot_TH2_as_pgfplot(h, only_data: bool = False):
    edges    = np.array(h.axes[0].edges(), dtype=np.float64)
    contents = np.array(h.values(), dtype=np.float64)

    x_edges  = np.array(h.axes[0].edges(), dtype=np.float64)
    y_edges  = np.array(h.axes[1].edges(), dtype=np.float64)
    contents = np.array(h.values(), dtype=np.float64)

    n_bins_x = len(x_edges) - 1
    n_bins_y = len(y_edges) - 1

    if not only_data:
        tikz_code = r"""
            \begin{tikzpicture}
                \begin{axis} [
                    view={0}{90},           % This creates a 2D view (top-down)
                    colorbar,               % Adds a colorbar to the side
                    xlabel={X-axis},        % Label for X-axis
                    ylabel={Y-axis},        % Label for Y-axis
                ] \addplot [
                    matrix plot*,           % For a 2D histogram (heatmap)
                    point meta=explicit,    % Allows using the z-values explicitly
        """
        tikz_code += f"                mesh/cols={n_bins_x},            % Number of columns in the matrix\n"
        tikz_code += f"                mesh/rows={n_bins_y},            % Number of rows in the matrix\n"
        
        tikz_code += "                ] table [meta=z] {\n"
        tikz_code += "                    x y z\n"
    else:
        tikz_code =  "                    x y z\n"

    for i in range(n_bins_x):
        x = (x_edges[i] + x_edges[i + 1]) / 2
        for j in range(n_bins_y):
            y = (y_edges[j] + y_edges[j + 1]) / 2
            z = contents[i, j]
            
            tikz_code += f"                    {x} {y} {z}\n"

    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code


def _get_TH1_errors_as_pgfplot(h: TH1):

    n_bins = h.GetXaxis().GetNbins()

    tikz_code = r"""
        \addplot [
            error bars/.cd,
                x dir=both, x explicit,
                y dir=both, y explicit,
        ] table [
            x error plus=ex,
            x error minus=ex,
            y error plus=ey,
            y error minus=ey,
        ] {
            x y ex ey
    """

    for i in range(1, n_bins + 1):
        x = h.GetXaxis().GetBinCenter(i)
        y = h.GetBinContent(i)
        bin_width = h.GetXaxis().GetBinWidth(i)
        ex = bin_width / 2
        ey = h.GetBinError(i)

        if i == 1:
            tikz_code += f"        {x} {y} {ex} {ey}\n"
        else:
            tikz_code += f"            {x} {y} {ex} {ey}\n"

    tikz_code += "        };"
    tikz_code += "    \end{axis};"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code