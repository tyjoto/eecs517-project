from eecs517project.plotting.base import base_plot

def beam_dump_striking_ion_energies_hist(ergs,*args,saveas: str | None = None,**kwargs):

    plot_kw = kwargs.pop("plot_kw", {})
    subplot_kw = kwargs.pop("subplot_kw", {})

    plot_kw.setdefault("bins", 50)
    plot_kw.setdefault("density", False)
    plot_kw.setdefault("label", r"$\epsilon_Z$")

    subplot_kw.setdefault("xlabel", r"$\epsilon$"+" [eV]")
    subplot_kw.setdefault("ylabel", "Counts"+" [-]")
    
    fig, ax = base_plot("hist", ergs, *args,saveas=saveas,plot_kw=plot_kw,subplot_kw=subplot_kw,**kwargs)

    return fig, ax