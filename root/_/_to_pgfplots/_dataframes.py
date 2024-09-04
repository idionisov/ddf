import numpy as np
import pandas as pd
from ROOT import TH1, TH2, TGraph, TGraphErrors, TGraphAsymmErrors
from root.to_pandas import get_as_pandas


def get_df_xy_as_pfgplot(df: pd.DataFrame):
    tikz_code = r"""
        \addplot
            coordinates {
    """
    for index, row in df.iterrows():
        if index==0:
            tikz_code += f"        ({row['x']},{row['y']})\n"
        else:
            tikz_code += f"            ({row['x']},{row['y']})\n"
    
    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)

    return tikz_code




def get_df_xy_errors_as_pfgplot(df: pd.DataFrame):
    tikz_code = r"""
        \addplot [
            error bars/.cd,
                y dir=both, y explicit,
                x dir=both, x explicit,
        ] coordinates {
    """
    for index, row in df.iterrows():
        if index==0:
            tikz_code += f"        ({row['x']},{row['y']}) +- ({row['ex']},{row['ey']})\n"
        else:
            tikz_code += f"            ({row['x']},{row['y']}) +- ({row['ex']},{row['ey']})\n"
    
    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)

    return tikz_code


def get_df_xy_asymm_errors_as_pfgplot(df: pd.DataFrame):
    tikz_code = r"""
        \addplot [
            error bars/.cd,
                y dir=both, y explicit,
                x dir=both, x explicit,
        ] coordinates {
    """
    for index, row in df.iterrows():
        if index==0:
            tikz_code += f"        ({row['x']},{row['y']}) += ({row['exh']},{row['eyh']}) -= ({row['exl']},{row['eyl']})\n"
        else:
            tikz_code += f"            ({row['x']},{row['y']}) += ({row['exh']},{row['eyh']}) -= ({row['exl']},{row['eyl']})\n"
    
    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)

    return tikz_code