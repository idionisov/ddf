from ROOT import TProfile


def get_TProfile_as_pgfplot(profile: TProfile):
    n_bins = profile.GetXaxis().GetNbins()

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
        x = profile.GetXaxis().GetBinCenter(i)
        y = profile.GetBinContent(i)
        bin_width = profile.GetXaxis().GetBinWidth(i)
        ex = bin_width / 2
        ey = profile.GetBinError(i)

        if i == 1:
            tikz_code += f"        {x} {y} {ex} {ey}\n"
        else:
            tikz_code += f"            {x} {y} {ex} {ey}\n"

    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code


def get_uproot_TProfile_as_pgfplot(profile):
    bin_centers  = profile.axis.edges[1:-1]
    bin_contents = profile.values
    bin_errors   = profile.errors

    n_bins = len(bin_centers)

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

    for i in range(n_bins):
        x = bin_centers[i]
        y = bin_contents[i]
        bin_width = profile.axis.edges[i + 1] - profile.axis.edges[i]
        ex = bin_width / 2
        ey = bin_errors[i]

        if i == 0:
            tikz_code += f"        {x} {y} {ex} {ey}\n"
        else:
            tikz_code += f"            {x} {y} {ex} {ey}\n"

    tikz_code += "        };"

    lines = tikz_code.splitlines()
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    tikz_code = '\n'.join(line[min_indent:] for line in lines)
    
    return tikz_code