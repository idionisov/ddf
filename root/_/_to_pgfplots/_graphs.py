from ROOT import TGraph, TGraphErrors, TGraphAsymmErrors
import numpy as np

def get_TGraph_as_pgfplot(tgraph: TGraph, only_data: bool = False):
    n_points = tgraph.GetN()

    if not only_data:
        tikz_code = r"""
            \begin{tikzpicture}
                \begin{axis}[]
                \addplot[]
                table [x=x, y=y] {
                    x y
        """
    else:
        tikz_code = "                    x y\n"
        tikz_code += "        "

    for i in range(n_points):
        if i == 0:
            tikz_code += f"            {tgraph.GetPointX(i)} {tgraph.GetPointY(i)}\n"
        else:
            tikz_code += f"                    {tgraph.GetPointX(i)} {tgraph.GetPointY(i)}\n"
    
    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)

    return tikz_code



def get_TGraphErrors_as_pgfplot(tgraph: TGraphErrors, only_data: bool = False):
    n_points = tgraph.GetN()

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

    for i in range(n_points):
        x  = tgraph.GetPointX(i)
        y  = tgraph.GetPointY(i)
        ex = tgraph.GetErrorX(i)
        ey = tgraph.GetErrorY(i)

        if i==0:
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

def get_TGraphAsymmErrors_as_pgfplot(tgraph: TGraphAsymmErrors, only_data: bool = False):
    n_points = tgraph.GetN()

    if not only_data:
        tikz_code = r"""
            \begin{tikzpicture}
                \begin{axis}[]
                \addplot[
                    error bars/.cd,
                    x dir = both, x explicit,
                    y dir = both, y explicit,
                ] table [
                    x error plus  = ex+,
                    x error minus = ex-,
                    y error plus  = ey+,
                    y error minus = ey-,
                ] {
                    x y ex+ ex- ey+ ey-
        """
    else:
        tikz_code = "                    x y ex- ex+ ey- ey+\n"
        tikz_code += "        "

    for i in range(n_points):    
        x   = tgraph.GetPointX(i)
        y   = tgraph.GetPointY(i)
        exl = tgraph.GetErrorXlow(i)
        exh = tgraph.GetErrorXhigh(i)
        eyl = tgraph.GetErrorYlow(i)
        eyh = tgraph.GetErrorYhigh(i)

        if i==0:
            tikz_code += f"            {x} {y} {exh} {eyh} {exl} {eyl}\n"
        else:
            tikz_code += f"                    {x} {y} {exh} {eyh} {exl} {eyl}\n"
    
    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code


def get_uproot_TGraph_as_pgfplot(graph, only_data: bool = False):
    x  = graph.all_members["fX"].astype(np.float64)
    y  = graph.all_members["fY"].astype(np.float64)
    n_points = len(x)
    
    if not only_data:
        tikz_code = r"""
            \begin{tikzpicture}
                \begin{axis}[]
                \addplot[]
                table [x=x, y=y] {
                    x y
        """
    else:
        tikz_code = "                    x y\n"
        tikz_code += "        "

    for xi, yi in zip(x, y):
        if xi==x[0] and yi==y[0]:
            tikz_code += f"            {xi} {yi}\n"
        else:
            tikz_code += f"                    {xi} {yi}\n"

    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)

    return tikz_code


def get_uproot_TGraphErrors_as_pgfplot(graph, only_data: bool = False):
    x  = graph.all_members["fX"].astype(np.float64)
    y  = graph.all_members["fY"].astype(np.float64)
    ex = graph.all_members["fEX"].astype(np.float64)
    ey = graph.all_members["fEY"].astype(np.float64)
    n_points = len(x)

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

    for i in range(n_points):
        if i == 0:
            tikz_code += f"            {x[i]} {y[i]} {ex[i]} {ey[i]}\n"
        else:
            tikz_code += f"                    {x[i]} {y[i]} {ex[i]} {ey[i]}\n"
    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code



def get_uproot_TGraphAsymmErrors_as_pgfplot(graph, only_data: bool = False):
    x   = graph.all_members["fX"].astype(np.float64)
    y   = graph.all_members["fY"].astype(np.float64)
    exl = graph.all_members["fEXlow"].astype(np.float64)
    exh = graph.all_members["fEXhigh"].astype(np.float64)
    eyl = graph.all_members["fEYlow"].astype(np.float64)
    eyh = graph.all_members["fEYhigh"].astype(np.float64)
    n_points = len(x)

    if not only_data:
        tikz_code = r"""
            \begin{tikzpicture}
                \begin{axis}[]
                \addplot[
                    error bars/.cd,
                    x dir = both, x explicit,
                    y dir = both, y explicit,
                ] table [
                    x error plus  = ex+,
                    x error minus = ex-,
                    y error plus  = ey+,
                    y error minus = ey-,
                ] {
                    x y ex+ ex- ey+ ey-
        """
    else:
        tikz_code = "                    x y ex- ex+ ey- ey+\n"
        tikz_code += "        "

    for i in range(n_points):
        if i == 0:
            tikz_code += f"            {x[i]} {y[i]} {exl[i]} {exh[i]} {eyl[i]} {eyh[i]}\n"
        else:
            tikz_code += f"                    {x[i]} {y[i]} {exl[i]} {exh[i]} {eyl[i]} {eyh[i]}\n"
    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"


    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code