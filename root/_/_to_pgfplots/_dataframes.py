import numpy as np
import pandas as pd
from ROOT import TH1, TH2, TGraph, TGraphErrors, TGraphAsymmErrors
from root.to_pandas import get_as_pandas


def _get_df_xy_as_pfgplot(df: pd.DataFrame, only_data: bool = False):
    if not only_data:
        tikz_code = r"""
            \begin{tikzpicture}
                \begin{axis}[]
                \addplot[]
                table [x=x, y=y] {
                    x y
        """
    else: 
        tikz_code =  "                    x y\n"
        tikz_code += "        "
    
    for index, row in df.iterrows():
        if index == 0:
            tikz_code += f"            {row['x']} {row['y']}\n"
        else:
            tikz_code += f"                    {row['x']} {row['y']}\n"
    

    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)

    return tikz_code


def _get_df_xy_errors_as_pfgplot(df: pd.DataFrame, only_data: bool = False):
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

    for index, row in df.iterrows():
        if index == 0:
            tikz_code += f"            {row['x']} {row['y']} {row['ex']} {row['ey']}\n"
        else:
            tikz_code += f"                    {row['x']} {row['y']} {row['ex']} {row['ey']}\n"
    
    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)

    return tikz_code


def _get_df_xy_asymm_errors_as_pfgplot(df: pd.DataFrame, only_data: bool = False):
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

    for index, row in df.iterrows():
        if index == 0:
            tikz_code += f"            {row['x']} {row['y']} {row['exl']} {row['exh']} {row['eyl']} {row['eyh']}\n"
        else:
            tikz_code += f"                    {row['x']} {row['y']} {row['exl']} {row['exh']} {row['eyl']} {row['eyh']}\n"
    
    if not only_data:
        tikz_code += "                };\n"
        tikz_code += "                \end{axis}\n"
        tikz_code += "            \end{tikzpicture}"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)

    return tikz_code