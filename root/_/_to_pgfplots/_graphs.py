from ROOT import TGraph, TGraphErrors, TGraphAsymmErrors


def get_TGraph_as_pgfplot(tgraph: TGraph):
    n_points = tgraph.GetN()

    tikz_code = r"""
        \addplot
        coordinates {
    """

    for i in range(n_points):
        if i==0:
            tikz_code += f"        ({tgraph.GetPointX(i)},{tgraph.GetPointY(i)})\n"
        else:
            tikz_code += f"            ({tgraph.GetPointX(i)},{tgraph.GetPointY(i)})\n"
    
    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)

    return tikz_code



def get_TGraphErrors_as_pgfplot(tgraph: TGraphErrors):
    n_points = tgraph.GetN()

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

    for i in range(n_points):
        x  = tgraph.GetPointX(i)
        y  = tgraph.GetPointY(i)
        ex = tgraph.GetErrorX(i)
        ey = tgraph.GetErrorY(i)

        if i==0:
            tikz_code += f"        {x} {y} {ex} {ey}\n"
        else:
            tikz_code += f"            {x} {y} {ex} {ey}\n"
    
    # End of the TikZ picture with proper indentation
    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code


def get_TGraphAsymmErrors_as_pgfplot(tgraph: TGraphAsymmErrors):
    n_points = tgraph.GetN()

    tikz_code = r"""
        \addplot [
            error bars/.cd,
                x dir=both, x explicit,
                y dir=both, y explicit,
        ] table [
            x error plus=ex+,
            x error minus=ex-,
            y error plus=ey+,
            y error minus=ey-,
        ] {
            x y ex+ ey+ ex- ey-
    """

    for i in range(n_points):    
        x   = tgraph.GetPointX(i)
        y   = tgraph.GetPointY(i)
        exl = tgraph.GetErrorXlow(i)
        exh = tgraph.GetErrorXhigh(i)
        eyl = tgraph.GetErrorYlow(i)
        eyh = tgraph.GetErrorYhigh(i)

        if i==0:
            tikz_code += f"        {x} {y} {exh} {eyh} {exl} {eyl}\n"
        else:
            tikz_code += f"            {x} {y} {exh} {eyh} {exl} {eyl}\n"
    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code


def get_uproot_TGraph_as_pgfplot(graph):
    x = graph['x'].to_numpy()
    y = graph['y'].to_numpy()

    tikz_code = r"""
        \addplot
            coordinates {
    """

    for xi, yi in zip(x, y):
        tikz_code += f"            ({xi},{yi})\n"

    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)

    return tikz_code


def get_uproot_TGraphErrors_as_pgfplot(graph):
    x  = graph.edges[0].to_numpy()
    y  = graph.values.to_numpy()
    ex = graph.errors[0].to_numpy()
    ey = graph.errors[1].to_numpy()

    n_points = len(x)

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

    for i in range(n_points):
        if i == 0:
            tikz_code += f"        {x[i]} {y[i]} {ex[i]} {ey[i]}\n"
        else:
            tikz_code += f"            {x[i]} {y[i]} {ex[i]} {ey[i]}\n"
    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code



def get_uproot_TGraphAsymmErrors_as_pgfplot(graph):
    x   = graph.edges[0].to_numpy()
    y   = graph.values.to_numpy()
    exl = graph.errors[0].low
    exh = graph.errors[0].high
    eyl = graph.errors[1].low
    eyh = graph.errors[1].high

    n_points = len(x)

    tikz_code = r"""
        \addplot [
            error bars/.cd,
                x dir=both, x explicit,
                y dir=both, y explicit,
        ] table [
            x error plus=ex+,
            x error minus=ex-,
            y error plus=ey+,
            y error minus=ey-,
        ] {
            x y ex+ ey+ ex- ey-
    """

    for i in range(n_points):
        if i == 0:
            tikz_code += f"        {x[i]} {y[i]} {exl[i]} {exh[i]} {eyl[i]} {eyh[i]}\n"
        else:
            tikz_code += f"            {x[i]} {y[i]} {exl[i]} {exh[i]} {eyl[i]} {eyh[i]}\n"
    tikz_code += "        };"


    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code