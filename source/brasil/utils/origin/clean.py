import pandas as pd
import numpy as np


def wrangling(dfs):
    '''

        Data wrangling for initial dataframes. This function selects columns, deletes airway products, standardizes NCMs,
        creates a unitary U$S price, filters unitary price, removes outliers & drops nulls.

            Args:
                - dfs (list): A list of dataframes to be cleaned and processed.

            Returns:
                - list: A list of clean dataframes.

    '''

    results_dfs = []

    print(f"\n> MUNGING HISTORICAL DATA:\n")

    for i in range(len(dfs)):
        df = dfs[i]
        year_error_memory = str(df['Fecha'].iloc[0])[3:]
        ncm = (df['Código NCM'].iloc[0].replace('.', ''))[:6]

        df = df.loc[:, ['Operación', 'Fecha', 'Código NCM', 'País de Origen', 'Puerto', 'Estado', 'Unitario FOB',
                        'U$S FOB', 'Cantidad Comercial', 'Unidad de Medida', 'Kgs. Brutos', 'Descripción de Mercadería']]

        print("~ Limpiando NCMs...")

        # Estandarizo los valores del NCM
        df['Código NCM'] = df['Código NCM'].astype(str).str.replace('.', '')
        df['Código NCM'] = df['Código NCM'].astype(str).str[:6]

        print("~ Creando columna de precio...")

        # initialize the column with NaN values
        df['U$S FOB Unitario'] = np.nan
        df["U$S FOB Unitario"] = (df['U$S FOB'] /
                                  df['Kgs. Brutos']).round(2)

        if (df['Código NCM'].iloc[0] == "283525"):
            df.loc[df['U$S FOB Unitario'] >= 1.0, "U$S FOB Unitario"] = np.nan
        elif (df['Código NCM'].iloc[0] == "283526"):
            df.loc[df['U$S FOB Unitario'] >= 1.4, "U$S FOB Unitario"] = np.nan

        print("~ Dropping nulls...")

        df['País de Origen'].fillna('N/D', inplace=True)

        df.dropna(inplace=True)

        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%m/%Y')

        results_dfs.append(df)

        if df is not None and not df.empty and not pd.isnull(df["Fecha"].iloc[0].year):
            print(
                f'> Done with: {ncm} ({year_error_memory})\n~~~~~~~~~~~~~~~~~~~')
        else:
            print(
                f'> No data for: {ncm} ({year_error_memory})\n~~~~~~~~~~~~~~~~~~~')

    return results_dfs
