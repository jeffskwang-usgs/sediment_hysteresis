from shiny import ui, render, App
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skewnorm

import matplotlib as mpl
mpl.rcParams["font.family"] = "monospace"
mpl.rcParams.update({'font.size': 12})

fontsize = 24
cells = 250
max_x = 6
prop = dict(arrowstyle="-|>,head_width=0.4,head_length=0.8",shrinkA=0,shrinkB=0,color='k')

q_color = (31./255., 119./255., 180./255., 50./255.)
qs_color =(255./255., 127./255., 14./255., 50./255.)

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.h2("Stream Flow Parameters", style="color:#1f77b4"),
            ui.input_slider(id="q_loc", label=r"ξ, Location:", min=-2., max=2., value=0.,ticks=True),
            ui.input_slider(id="q_scale", label=r"ω, Scale:", min=0.25, max=4., value=1.,ticks=True),
            ui.input_slider(id="q_shape", label=r"α, Shape:", min=-8., max=8., value=0.8,ticks=True),
            ui.hr(),
            ui.h2("Turbidity Parameters", style="color:#ff7f0e"),
            ui.input_slider(id="qs_loc", label=r"ξ, Location:", min=-2., max=2., value=-1.,ticks=True),
            ui.input_slider(id="qs_scale", label=r"ω, Scale:", min=0.25, max=4., value=0.85,ticks=True),
            ui.input_slider(id="qs_shape", label=r"α, Shape:", min=-8., max=8., value=3.5,ticks=True)
        ),
        ui.panel_main(
            ui.output_plot(id="histogram")
        )
    )
)

def server(input, output, session):
    @output
    @render.plot
    def histogram():
        fig, axs = plt.subplots(nrows=1,ncols=2)
        x = np.linspace(-max_x,max_x,cells)
        q = skewnorm.pdf(x,loc=input.q_loc(),scale=input.q_scale(),a=input.q_shape())
        qs = skewnorm.pdf(x,loc=input.qs_loc(),scale=input.qs_scale(),a=input.qs_shape())
        axs[0].fill_between(x, q, facecolor=q_color,edgecolor='tab:blue')
        axs[0].fill_between(x, qs, facecolor=qs_color,edgecolor='tab:orange')
        axs[0].set_xlim(-4,4)
        axs[0].set_ylim(0,1.4)
        axs[0].set_xlabel("Time")
        axs[0].set_xticks([])
        axs[0].set_yticks([])

        axs[0].text(-.001,0.5,"Stream Flow     ", color = "tab:blue", rotation = "vertical",ha='right',va='top', transform=axs[0].transAxes)
        axs[0].text(-.001,0.5,"     Turbidity", color = "tab:orange", rotation = "vertical",ha='right',va='bottom', transform=axs[0].transAxes)

        axs[0].tick_params(direction="out")
        axs[0].spines["top"].set_visible(False)
        axs[0].spines["right"].set_visible(False)

        max_q = np.max(q)
        max_qs = np.max(qs)
        axs[1].plot(q/max_q,qs/max_qs,color='k', clip_on=False)
        for i in range(0,cells-1,10):
            if q[i+1]/max_q > 0.001 and qs[i+1]/max_qs > 0.001:
                axs[1].annotate("", xy=(q[i+1]/max_q,qs[i+1]/max_qs), xytext=(q[i]/max_q,qs[i]/max_qs), arrowprops=prop, clip_on=False)
        axs[1].set_xlim(0,1.)
        axs[1].set_ylim(0,1.)
        axs[1].set_xlabel("Normalized Stream Flow [-]",color="tab:blue")
        axs[1].set_ylabel("Normalized Turbidity [-]",color="tab:orange")

        axs[1].tick_params(direction="out")
        axs[1].spines["top"].set_visible(False)
        axs[1].spines["right"].set_visible(False)
app = App(ui=app_ui, server=server) 