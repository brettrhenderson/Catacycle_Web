"""pre plotting data manipulation"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_raw(filename):
    xl = pd.ExcelFile(filename)
    raw_data = []
    existing_reactants = None
    match = True
    # import excel sheets of reaction 1 and 2
    for i in range(len(xl.sheet_names)):
        raw_data.append(pd.read_excel(filename, i))
        if existing_reactants is None:
            existing_reactants = raw_data[-1].columns.tolist()
        else:
            cols = raw_data[-1].columns.tolist()
            if cols != existing_reactants:
                match = False
                if len(cols) != len(existing_reactants):
                    raise ValueError("Sheets contain different numbers of species monitored.")
        # print(f"\ncolumns read from experiment {i+1}: \n{len(raw_data[i].columns)}")
    if not match:
        existing_reactants = [str(i) for i in range(1, len(raw_data[1].columns) + 1)]
    return raw_data, xl.sheet_names, existing_reactants[1:]

#produce a column summing all counts at each
# timestep for total ion count normalization
def get_TC(data):
    totals = []
    for df in data:
        totals.append(df.iloc[:, 1:].sum(axis=1))
    return totals

def testtc(df):
    return df.values[:, 1:].sum(axis=1)

def get_sheet_totals(normalization_method, data):
    """returns chosen normalization value"""
    totals = []
    if normalization_method == "TC" or normalization_method == "Total Count":
        totals = get_TC(data)
    elif normalization_method == "MV" or normalization_method == "Max Value":
        for df in data:
            totals.append(df.iloc[:, 1:].max().max())
    # if neither TC nor MV is selected, the operations of Total1 and Total2
    # will not change any values
    else:
        totals = [1]*len(data)
    return totals

def normalize_columns(data, totals):
    """function that normalizes all columns by the sum on that time step (excludes the time column in a sheet)"""
    Rnorm = []
    for i, df in enumerate(data):
        Rnorm.append(pd.concat([df.iloc[:,0], df.iloc[:, 1:].div(totals[i], axis=0)], axis=1))
    return Rnorm

def shift_times(data, shifts):
    """function that normalizes all columns by the sum on that time step (excludes the time column in a sheet)"""
    if isinstance(shifts, float):
        shifts = [shifts for _ in data]
    for i, df in enumerate(data):
        df.iloc[:, 0] -= shifts[i]
    return data

def get_max_times(data):
    maxtime = []
    for df in data:
        maxtime.append(df.iloc[:, 0].max())
    return maxtime

def select_data(data, reactions=None, species=None):
    """selects data to plot"""
    if reactions is None:   #return all reactions
        if species is None:     #return all species
            return data
        return [data[rxn].iloc[:, [0]+[spec+1 for spec in species]] for rxn in range(len(data))]
    elif species is None:
        return [data[rxn] for rxn in reactions]
    return [data[rxn].iloc[:, [0]+[spec+1 for spec in species]] for rxn in reactions]

def plot_vtna(data,  concs, order=1, trans_zero=None,  windowsize=None, colors=None, marker_shape="o", markersize=15,
              linestyle=':', guide_lines=True, f_format='png', return_image=False, figsize=(8,6)):
    """Plot the Aligned Reaction Traces"""
    if trans_zero is None:
        trans_zero = [0]*len(data)
    if windowsize is None:
        windowsize = [1]*len(data)
    # set defaults and declare variables
    
    #put ipynb fn here to plot fitted graph once order etc. is known
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, autoscale_on=True) #, xlim=(0, 20), ylim=(-0.1, 1.1))
    maxtime = max(get_max_times(data))
    for i, rxn in enumerate(data):
        for j, col in enumerate(rxn.columns):
            if j > 0:
                t_vtna = (rxn.iloc[:, 0] + trans_zero[i]) * float(concs[i]) ** order
                smoothed = rxn.loc[:, col].rolling(windowsize[i], center=True).mean()
                ax.plot(t_vtna, smoothed, marker=marker_shape, linestyle=linestyle, markersize=markersize, label=f"{concs[i]}, rct {j}")

    if guide_lines:
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        ax.vlines(0, 0, 1, linestyle=':', linewidth=1, color='k')
        ax.hlines(0, xmin, xmax, linestyle=':', linewidth=1, color='k')
        ax.hlines(1, xmin, xmax, linestyle=':', linewidth=1, color='k')
    ax.set_xlabel('time', fontsize=16)
    ax.set_ylabel('Relative Abundance', fontsize=16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.legend()
    #plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    filename = "../../static/sampledata/VTNA329.XLSX"
    raw_data, sheet_names, reac_names = load_raw(filename)
    print(f'RXNS: {sheet_names}, REACTANTS: {reac_names}')
    # totals = get_sheet_totals('TC', raw_data)
    # norm_data = normalize_columns(raw_data, totals)
    # print(norm_data[0].head())
    # max_times = get_max_times(norm_data)
    # print(max_times)
    # print(sheet_names)
    # gimme = select_data(norm_data, [0,1], [0, 1])
    # print(gimme[1].head())
    # print(f'{len(gimme[0].columns)}')
