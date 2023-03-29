import pandas as pd


def wrangling_2309_historical(dfs):
    '''

        Data wrangling for the ncm 2309 to grab the dicalcium phosphates that have been registered here, when they should be
        in the ncm 283525.

            Args:
                - dfs (list): A list of dataframes to be cleaned and processed.

            Returns:
                - list: A list of clean dataframes.

    '''

    results_dfs = []

    print(f"\n> GRABBING THE PHOSPHATES FROM THE 2309:\n")

    for i in range(len(dfs)):
        df = dfs[i]

        year_error_memory = df["Fecha"].iloc[0].year
        year = df["Fecha"].iloc[0].year
        ncm = df["NANDINA"].iloc[0]

        year_error_memory = df["Fecha"].iloc[0].year

        mask = df['Descripción de Mercadería'].str.contains(
            'fosf|phosp|dicalcium|dcp|monodicalcium|mdcp|monocalcium|mcp', case=False)
        df = df[mask]

        results_dfs.append(df)

    if df is not None and not df.empty and not pd.isnull(df["Fecha"].iloc[0].year):
        print(
            f'> Done with: {ncm} ({year})\n~~~~~~~~~~~~~~~~~~~')
    else:
        print(
            f'> No data for: {ncm} ({year_error_memory})\n~~~~~~~~~~~~~~~~~~~')

    return results_dfs
