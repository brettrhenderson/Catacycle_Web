"""pre plotting data manipulation"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def load_raw(filename):
    xl = pd.ExcelFile(filename)
    raw_data = []
    # import excel sheets of reaction 1 and 2
    for i in range(len(xl.sheet_names)):
        raw_data.append(pd.read_excel(filename, i))
    return raw_data, xl.sheet_names

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
    if normalization_method == "TC":
        totals = get_TC(data)
    elif normalization_method == "MV":
        for df in data:
            totals.append(df.iloc[:, 1:].max().max())
    # if neither TC nor MV is selected, the operations of Total1 and Total2
    # will not change any values
    else:
        totals = [1]*len(data)
    return totals

def normalize_columns(data, totals):
    """function that normalizes all columns by the sum on that time step (excludes the time coumn in a sheet)"""
    Rnorm = []
    for i, df in enumerate(data):
        Rnorm.append(pd.concat([df.iloc[:,0], df.iloc[:, 1:].div(totals[i], axis=0)], axis=1))
    return Rnorm

def get_max_times(Rnorm):
    maxtime = []
    for df in Rnorm:
        maxtime.append(df.iloc[:, 0].max())
    return maxtime

def select_data(Rnorm, reactions=None, species=None):
    """selects data to plot"""
    if reactions is None:   #return all reactions
        if species is None:     #return all species
            return Rnorm
        return [Rnorm[rxn].iloc[:, [0]+[spec+1 for spec in species]] for rxn in range(len(Rnorm))]
    elif species is None:
        return [Rnorm[rxn] for rxn in reactions]
    return [Rnorm[rxn].iloc[:, [0]+[spec+1 for spec in species]] for rxn in reactions]


if __name__ == "__main__":
    filename = "sampledata/VTNA329.xlsx"
    raw_data, sheet_names = load_raw(filename)
    totals = get_TC(raw_data)
    for total in totals:
        print(total.head())
    # totals = get_sheet_totals('TC', raw_data)
    # norm_data = normalize_columns(raw_data, totals)
    # print(norm_data[0].head())
    # max_times = get_max_times(norm_data)
    # print(max_times)
    # print(sheet_names)
    # gimme = select_data(norm_data, [0,1], [0, 1])
    # print(gimme[1].head())
    # print(f'{len(gimme[0].columns)}')