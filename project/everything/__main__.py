import os
import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable

import eecs517project.utls.constants as c
from eecs517project.solver import solver

path = os.path.dirname(__file__)

filename = "export.csv"
abs_file = os.path.join(path, filename)
D = 30    # cm 
Pgs = np.geomspace(1e-9,1e-3,7)
#print(Pgs)
Vbs = np.linspace(600,2100,6)
#print(Vbs)
Ls = np.geomspace(D/2,64*D,8,dtype=np.int64)/100 #m
#print(Ls)
lenPgs = len(Pgs)
lenVbs = len(Vbs)
lenLs = len(Ls)
lenT = lenLs*lenPgs*lenVbs
labels = [
    r"$P_{gas}$ [Torr]",
    r"$V_{b}$ [V]",
    r"$L$ [m]"
]
clabels = [
    "Misses Target [%]",
    "Beam Sputter [%]",
    "Sputter Yield [-]"
]
titles = [
    "Pressure = {0:.0e} Torr",
    "Beam Energies = {0} V",
    "Distance = {0:.2f} m"
]
saves_Z = [
    "miss_{0}.png",
    "sput_{0}.png",
    "yield_{0}.png"
]
save_T = [
    "Pgas{0:.0e}",
    "Vb{0}",
    "L{0:.2f}"
]

def get_settings(D,Pg,Vb,L):
    # controlling parameters
    #Vb = 600    # V
    #Pg = 3.2e-7  # Torr
    #L = 0.6    # m


    # particles
    Nparticles = 1e6
    # beam ions parameters
    m_i = 131.30# amu
    amu = True  # not needed to be defined
    Vg = 0      # V

    # Length to beam dump parameter

    # beam parameteres
    I = 0.53   # A = c/s
    Z = 1       # [-]
    # beam calculations for next two parameters
    A = np.pi*D*D/4 # m^2
    J = I/A     # A/m^2
    ez = Vb + Vg# eV
    vz0_calculated = np.sqrt(ez*c.e*2/m_i/c.m_p)
    #print(f"v_i0 = {vz0_calculated} m/s")
    n_ib = J/c.e/vz0_calculated # m^-3
    # Parameters that are predefined for this special case
    T = L/vz0_calculated
    Wparticles = I*T/Nparticles

    # background neutral parameters
    #Pg = 3.2e-5  # Torr
    Tg = 300  # K

    # cross section bool paremetrs 
    Xe_CEX = True
    Xe_MEX = True
    C_CEX = False
    C_MEX = False

    # output bool paremeters
    hist_striking_ion_energies = True

    beam = {
        "Xe+": {
            "I": I,
            "D": D,
            "Vb": Vb,
            "Vg": Vg,
            "T": T,
            "Z": Z,
            "W": Wparticles,
            "m_i": m_i,
            "src": "beam"
        }
    }
    background = {
        "Xe": {
            "Pg": Pg,
            "Tg": Tg,
        }
    }
    cross_sections = {
        "Xe+": {
            "CEX": Xe_CEX,
            "MEX": Xe_MEX,
        },
        "C+": {
            "CEX": C_CEX,
            "MEX": C_MEX,
        }
    }
    outputs = {
        "hist_striking_ion_energies": hist_striking_ion_energies,
    }
    domain = {
        "Z": L,
        "T": T,
    }


    settings = {
        "particles": beam,
        "background": background,
        "cross_sections": cross_sections,
        "outputs": outputs,
        "domain": domain,
        "saveto": path,
    }

    return settings

def solve_loop():
    print(">>Starting Unattenuated propagating xenon ion particle")
    start_time = time.time()

    Results = np.zeros((lenT,6))

    c = 0
    for Pg in Pgs:
        for Vb in Vbs:
            for L in Ls:
                settings = get_settings(D,Pg,Vb,L)

                x,y = solver(settings, returns=True)
                z = np.array([x,y]).reshape((6,))
                Results[c] = z
                c +=1

    header="Pg [torr], Vb [V], L [m], Miss% [%], Sput% [%], SputY [-]"
    np.savetxt(abs_file,Results, delimiter=",", header=header)

    # x: Pg, Vb, L
    # y: miss%, sput%,sputY
    time_total = time.time()-start_time
    print(f"Total Elaspsed time: {time_total}s\n\ndone.")

    print("done.")

def make_plots():
    D = 30    # cm 


    data = np.loadtxt(abs_file, delimiter=",",skiprows=1)

    # unwrap data
    # x 
    dPgs = data[:,0]
    dVbs = data[:,1]
    dLs = data[:,2]
    # y
    Miss = data[:,3]
    Sput = data[:,4]
    Yield = data[:,5]
    # key
    # 0: Pressure
    # 1: Vb
    # 2: L
    # 3: miss%
    # 4: Sput%
    # 5: Yield
    strings = ["pressure", "energy", "distance"]

    def plot_round():
        fig_miss, ax_miss = plt.subplots()
        fig_sput, ax_sput = plt.subplots()
        fig_yield, ax_yield = plt.subplots()
        cax_miss = None
        cax_sput = None
        cax_yield = None
        vmin_miss = 0
        vmax_miss = np.round(max(Miss))
        vmin_sput = 0
        vmax_sput = np.round(max(Sput))
        vmin_yield = 0
        vmax_yield = max(Yield)
        vmax_yield = np.round(vmax_yield)


        def plotit(A,Z,X,Y,T,x,y,z, fig,ax, cax=None, vmin=None, vmax=None, yscale="linear"):
            ax.cla()
            ax.set(yscale=yscale)
            cplot = ax.tricontourf(x,y,z, vmin = vmin, vmax=vmax)
            ax.scatter(x,y)
            ax.scatter(x[-13],y[-13],color="r")
            #ticks = np.linspace(vmin,vmax,11) if vmin is not None and vmax is not None else None
            ticks = None
            if cax is not None:
                cax = fig.colorbar(ScalarMappable(norm=cplot.norm, cmap=cplot.cmap), cax=cax.ax, ticks=ticks) 
            else:
                cax = fig.colorbar(cplot, ticks=ticks)
                cax = fig.colorbar(ScalarMappable(norm=cplot.norm, cmap=cplot.cmap), cax=cax.ax, ticks=ticks)

            title = titles[T].format(A)
            saveas = save_T[T].format(A)
            saveas.replace(".","_")
            saveas = os.path.join(path,saves_Z[Z].format(saveas))
            ax.set(xlabel=labels[X], ylabel=labels[Y], title=title)#clabel=r"Miss Target [%]")
            cax.set_label(clabels[Z])
            fig.savefig(saveas)
            if Z==0 and X==1 and Y==0 and T==2:
                print(f"{A}")
                print(x,y,z)
                print(saveas)
                print(x[-13],y[-13],z[-13])
            return fig, ax, cax

        # pressure loop
        for p in Pgs:
            indices = np.where(dPgs==p)
            x = dLs[indices]
            y = dVbs[indices]
            z_miss = Miss[indices]
            z_sput = Sput[indices]
            z_yield = Yield[indices]
            z_yield = np.nan_to_num(z_yield)

            # miss target plot
            fig_miss, ax_miss, cax_miss = plotit(A=p,Z=0,X=2,Y=1,T=0,x=x,y=y,z=z_miss,fig=fig_miss,ax=ax_miss, cax=cax_miss, vmin=vmin_miss, vmax=vmax_miss)
            # sput target plot
            fig_sput, ax_sput, cax_sput = plotit(A=p,Z=1,X=2,Y=1,T=0,x=x,y=y,z=z_sput,fig=fig_sput,ax=ax_sput, cax=cax_sput, vmin=vmin_sput, vmax=vmax_sput)
            # yield target plot
            fig_yield, ax_yield, cax_yield = plotit(A=p,Z=2,X=2,Y=1,T=0,x=x,y=y,z=z_yield,fig=fig_yield,ax=ax_yield, cax=cax_yield, vmin=vmin_yield, vmax=vmax_yield)


            #plt.show()
            #plt.close()
        
        # Vb loop
        for V in Vbs:
            indices = np.where(dVbs==V)
            x = dLs[indices]
            y = dPgs[indices]
            z_miss = Miss[indices]
            z_sput = Sput[indices]
            z_yield = Yield[indices]
            z_yield = np.nan_to_num(z_yield)
            

            # miss target plot
            fig_miss, ax_miss, cax_miss = plotit(A=V,Z=0,X=2,Y=0,T=1,x=x,y=y,z=z_miss,fig=fig_miss,ax=ax_miss, cax=cax_miss, vmin=vmin_miss, vmax=vmax_miss, yscale="log")
            # sput target plot
            fig_sput, ax_sput, cax_sput = plotit(A=V,Z=1,X=2,Y=0,T=1,x=x,y=y,z=z_sput,fig=fig_sput,ax=ax_sput, cax=cax_sput, vmin=vmin_sput, vmax=vmax_sput, yscale="log")
            # yield target plot
            fig_yield, ax_yield, cax_yield = plotit(A=V,Z=2,X=2,Y=0,T=1,x=x,y=y,z=z_yield,fig=fig_yield,ax=ax_yield, cax=cax_yield, vmin=vmin_yield, vmax=vmax_yield, yscale="log")


            #plt.show()
            #plt.close()
        
        # L loop
        for L in Ls:
            indices = np.where(dLs==L)
            x = dVbs[indices]
            y = dPgs[indices]
            z_miss = Miss[indices]
            z_sput = Sput[indices]
            z_yield = Yield[indices]
            z_yield = np.nan_to_num(z_yield)
            

            # miss target plot
            fig_miss, ax_miss, cax_miss = plotit(A=L,Z=0,X=1,Y=0,T=2,x=x,y=y,z=z_miss,fig=fig_miss,ax=ax_miss, cax=cax_miss, vmin=vmin_miss, vmax=vmax_miss, yscale="log")
            # sput target plot
            fig_sput, ax_sput, cax_sput = plotit(A=L,Z=1,X=1,Y=0,T=2,x=x,y=y,z=z_sput,fig=fig_sput,ax=ax_sput, cax=cax_sput, vmin=vmin_sput, vmax=vmax_sput, yscale="log")
            # yield target plot
            fig_yield, ax_yield, cax_yield = plotit(A=L,Z=2,X=1,Y=0,T=2,x=x,y=y,z=z_yield,fig=fig_yield,ax=ax_yield, cax=cax_yield, vmin=vmin_yield, vmax=vmax_yield, yscale="log")


            #plt.show()
            #plt.close()
        
        
    plot_round()

    

def main():
    # solve_loop()
    make_plots()

if __name__ == "__main__":
    main()
    #make_plots()