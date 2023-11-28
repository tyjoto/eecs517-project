from typing import Any

import matplotlib.pyplot as plt
from matplotlib import style

from eecs517project.plotting.options import (
    plot,
    semilogy,
    semilogx,
    loglog,
    hist,
)

style.use("bmh")

def choose_plot_type(plot_type,ax):
    if plot_type in plot:
        plotter = ax.plot
    elif plot_type in semilogy:
        plotter = ax.semilogy
    elif plot_type in semilogx:
        plotter = ax.semilogx
    elif plot_type in loglog:
        plotter = ax.loglog
    elif plot_type in hist:
        plotter = ax.hist
    else:
        raise NotImplementedError(f"'{plot_type}' is not yet implemented")
    #plotter(*args,**kwargs)
    return plotter


def base_plot(
        plot_type: int | str,
        *args, 
        saveas: str | None = None,
        fig_tightlayout: bool = True,
        legend: bool = True,
        nrows: int = 1, ncols: int = 1, 
        subplot_kw: dict[str, Any] | None = None,
        subplots_kw: dict[str, Any] | None = None,
        gridspec_kw: dict[str, Any] | None = None,
        fig_kw: dict[str, Any] |  None = None,
        plot_kw: dict[str, Any] | None = None,
        savefig_kw: dict[str, Any] | None = None,
        **kwargs
        ):
    """
    subplot_kw: dict of kws for all subplots created (u.e. xlabel, ylabel, title)
    subplots_kw: dict of kws for making the subplots (i.e. sharex, sharey)
    fig_kw: dict of kws for making the figure (i.e. )
    plot_kw: dict of kws for making the plot (i.e. label, markerfacecolor)
    savefig_kw: dict of kws for saving the figure
    """
    fig_kw = {} if fig_kw is None else fig_kw
    subplots_kw = {} if subplots_kw is None else subplots_kw
    plot_kw = {} if plot_kw is None else plot_kw
    savefig_kw = {} if savefig_kw is None else savefig_kw

    fig, ax = plt.subplots(
        nrows=nrows,ncols=ncols,
        subplot_kw=subplot_kw, 
        gridspec_kw=gridspec_kw, 
        **subplots_kw,
        **fig_kw)
    
    plotter = choose_plot_type(plot_type=plot_type, ax=ax)
    plotter(*args,**plot_kw)

    if legend is True:
        ax.legend()

    if fig_tightlayout is True:
        fig.tight_layout()

    if saveas is not None:
        fig.savefig(saveas, **savefig_kw)
    
    return fig, ax