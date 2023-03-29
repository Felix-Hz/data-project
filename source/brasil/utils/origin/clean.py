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
        year_error_memory = str(df['YEAR/MONTH'].iloc[0])[:4]

        df = df.loc[:, ['ORIGIN COUNTRY', 'YEAR/MONTH', 'Net weight', 'UNIT CIF VALUE', 'Acquisition country', 'Product description', 'POSSIBLE CONSIGNEE',
                        'POSSIBLE SHIPPER', 'NCM',  'MODAL', 'TOTAL FOB ESTIMATED VALUE', 'CNPJ > Brazilian Company ID', 'TOTAL CIF VALUE', 'Measure Unit']]

        # Se eliminan registros que vengan por aire
        subset = df['MODAL']
        df = df[subset != 'AEREA']

        print("~ Limpiando NCMs...")

        # Estandarizo los valores del NCM
        df['NCM'] = df['NCM'].astype(str).str.replace('.', '')
        df['NCM'] = df['NCM'].astype(str).str[:6]

        print("~ Creando columna de precio...")

        df['U$S Unitario'] = np.nan  # initialize the column with NaN values
        df.loc[df['UNIT CIF VALUE'] <= 1.4,
               'U$S Unitario'] = df.loc[df['UNIT CIF VALUE'] <= 1.4, 'UNIT CIF VALUE']

        print("~ Dropping outliers...")

        q1 = df['U$S Unitario'].quantile(0.25)
        q3 = df['U$S Unitario'].quantile(0.75)

        interquartileRange = q3 - q1
        # use outlier step (1.5) to determine the boundaries w/ iqr to filter the price with
        lower_bound = q1 - 1.5 * interquartileRange
        upper_bound = q3 + 1.5 * interquartileRange

        # drop outliers
        outlier_indices = df[(df['U$S Unitario'] < lower_bound) | (
            df['U$S Unitario'] > upper_bound)].index
        df = df.drop(outlier_indices)

        print("~ Dropping nulls...")

        df['Acquisition country'].fillna('N/D', inplace=True)
        df['U$S Unitario'].fillna(
            df['TOTAL CIF VALUE'] / df['Net weight'], inplace=True)
        df.dropna(subset=['POSSIBLE CONSIGNEE'], inplace=True)

        df['Fecha'] = pd.to_datetime(df['YEAR/MONTH'], format='%Y%m')

        results_dfs.append(df)

        dfs[i] = df

        if df is not None and not df.empty and not pd.isnull(df["Fecha"].iloc[0].year):
            print(
                f'> Done with: {df["Fecha"].iloc[0].year}\n~~~~~~~~~~~~~~~~~~~')
        else:
            print(f'> No data for: {year_error_memory}\n~~~~~~~~~~~~~~~~~~~')

    return results_dfs
