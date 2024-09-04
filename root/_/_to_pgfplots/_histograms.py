from ROOT import TH1, TH2


def get_TH1_as_pgfplot(h: TH1):
    n_bins = h.GetXaxis().GetNbins()

    tikz_code = r"""
        \addplot[
            const plot,
            no markers
        ]
        coordinates{
    """
    tikz_code += f"         ({h.GetXaxis().GetBinLowEdge(1)}, {0})\n"
    
    for i in range(1, n_bins+1):
        tikz_code += f"             ({h.GetXaxis().GetBinLowEdge(i)}, {h.GetBinContent(i)})\n"
        tikz_code += f"             ({h.GetXaxis().GetBinUpEdge(i)}, {h.GetBinContent(i)})\n"

    tikz_code += f"             ({h.GetXaxis().GetBinUpEdge(n_bins)}, {0})\n"
    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code


def get_TH2_as_pgfplot(h: TH2):
    
    n_bins_x = h.GetXaxis().GetNbins()
    n_bins_y = h.GetYaxis().GetNbins()

    tikz_code = r"""
        \begin{axis}[
            view={0}{90},           % This creates a 2D view (top-down)
            colorbar,               % Adds a colorbar to the side
            xlabel={X-axis},        % Label for X-axis
            ylabel={Y-axis},        % Label for Y-axis
        ] \addplot[
            matrix plot*,           % For a 2D histogram (heatmap)
            point meta=explicit,    % Allows using the z-values explicitly
    """
    tikz_code += f"        mesh/cols={n_bins_x},            % Number of columns in the matrix\n"
    tikz_code += f"        mesh/rows={n_bins_y},            % Number of rows in the matrix\n"
    
    tikz_code += "        ] table [meta=z, col sep=space, row sep=crcr] {\n"
    tikz_code += "            x y z \\\\\n"

    for xbin in range(1, n_bins_x + 1):
        x = h.GetXaxis().GetBinCenter(xbin)

        for ybin in range(1, n_bins_y + 1):
            y = h.GetYaxis().GetBinCenter(ybin)
            z = h.GetBinContent(xbin, ybin)

            tikz_code += f"             {x} {y} {z}" + ' \\\\' + "\n"

    tikz_code += "        };\n"
    tikz_code += "        \end{axis}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code



def get_uproot_TH1_as_pgfplot(h):
    edges    = (h.edges).to_numpy()
    contents = (h.values).to_numpy()
    
    tikz_code = r"""
        \addplot[
            const plot,
            no markers
        ]
        coordinates{
    """

    tikz_code += f"         ({edges[0]}, {0})\n"
    for i in range(len(contents)):
        tikz_code += f"             ({edges[i]},   {contents[i]})\n"
        tikz_code += f"             ({edges[i+1]}, {contents[i]})\n"
    tikz_code += f"             ({edges[-1]}, {0})\n"
    
    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code


def get_uproot_TH2_as_pgfplot(h):
    x_edges = h.edges[0].to_numpy()
    y_edges = h.edges[1].to_numpy()
    contents = h.values.to_numpy()

    n_bins_x = len(x_edges) - 1
    n_bins_y = len(y_edges) - 1

    tikz_code = r"""
        \begin{axis}[
            view={0}{90},           % This creates a 2D view (top-down)
            colorbar,               % Adds a colorbar to the side
            xlabel={X-axis},        % Label for X-axis
            ylabel={Y-axis},        % Label for Y-axis
        ] \addplot[
            matrix plot*,           % For a 2D histogram (heatmap)
            point meta=explicit,    % Allows using the z-values explicitly
    """
    tikz_code += f"        mesh/cols={n_bins_x},            % Number of columns in the matrix\n"
    tikz_code += f"        mesh/rows={n_bins_y},            % Number of rows in the matrix\n"
    
    tikz_code += "        ] table [meta=z, col sep=space, row sep=crcr] {\n"
    tikz_code += "            x y z \\\\\n"

    for i in range(n_bins_x):
        x = (x_edges[i] + x_edges[i + 1]) / 2
        for j in range(n_bins_y):
            y = (y_edges[j] + y_edges[j + 1]) / 2
            z = contents[i, j]
            
            tikz_code += f"             {x} {y} {z}" + ' \\\\' + "\n"

    tikz_code += "        };\n"
    tikz_code += "        \end{axis}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code


def get_TH1_errors_as_pgfplot(h: TH1):

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

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code