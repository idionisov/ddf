from typing import Union
import mplhep

def addMplLabel(
    loc: int = 0,
    mainText: str = "SND@LHC",
    extraText: str = "",
    suppText: str = "",
    mainTextWeight: str = "bold",
    mainTextItalic: bool = False,
    extraTextItalic: bool = True,
    suppTextItalic: bool = False,
    font: Union[str, None] = None,
    fontsize: Union[str, None] = None,
    pad = 0,
    ax = None
):
    """Add typical LHC experiment primary label to the axes.

        Parameters
        ----------
            loc: int, Optional
                Label position:
                    - 0 : Above axes, left aligned
                    - 1 : Top left corner
                    - 2 : Top left corner, multiline
                    - 3 : Split EXP above axes, rest of label in top left corner"
            mainText: string, Optional
                Main experiment label, typically bold and larger
                font-size. For example "SND@LHC"

            extraText: string, Optional
                Secondary experiment label, typically not-bold and smaller
                font-size. For example "Simulation" or "Preliminary"

            suppText: string, Optional
                Supplementary text on the top-right

            mainTextWeight: string, Optional
                Set fontweight of the main text label. Default "bold".

            mainTextItalic: bool, Optional
                Whether to make the main text Italic. Default "False".

            extraTextItalic: bool, optional
                Whether to make the secondary text Italic. Default "True".

            suppTextItalic: bool, Optional
                Whether to make the supplementary text Italic. Default "False".

            font: string, Optional
                Name of font to be used.

            fontsize: string, Optional
                Defines size of "secondary label". Experiment label is 1.3x larger.

            ax: matplotlib.axes.Axes, Optional
                Axes object (if None, last one is fetched)

            pad: float, Optional
                Additional padding from axes border in units of axes fraction size.
        Returns
        -------
            ax : matplotlib.axes.Axes
                A matplotlib `Axes <https://matplotlib.org/3.1.1/api/axes_api.html>`
                object
    """

    return mplhep.label.exp_text(
        text=extraText,
        exp=mainText,
        supp=suppText,
        italic=(mainTextItalic, extraTextItalic, suppTextItalic),
        loc=loc,
        ax=ax,
        fontname=font,
        fontsize=fontsize,
        exp_weight=mainTextWeight,
        pad=pad
    )
