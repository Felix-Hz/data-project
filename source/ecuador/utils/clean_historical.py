import pandas as pd


def wrangling_historical_data(dfs):
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
        year_error_memory = df["Fecha"].iloc[0].year

        df = df.loc[:, ['NANDINA', 'Fecha', 'Importador', 'Proveedor', 'País de Origen', 'Aduana', 'Via Transporte',
                        'U$S CIF', 'CIF Unitario', 'Kgs. Netos', 'Cantidad',  'Marca',  "Descripción Comercial"]]

        # Se eliminan registros que vengan por aire
        subset = df['Via Transporte']
        df = df[subset != 'AEREA']

        df.loc[df['Marca'] ==
               "SIN MARCA", 'Marca'] = "S/M"

        df.loc[df['Marca'] ==
               "SIN  MARCA", 'Marca'] = "S/M"
        df.loc[df['Marca'] ==
               "SM", 'Marca'] = "S/M"
        df.loc[df['Marca'] ==
               "N/M", 'Marca'] = "S/M"
        df.loc[df['Marca'] ==
               "SMARCA", 'Marca'] = "S/M"
        df.loc[df['Marca'] ==
               "S/N", 'Marca'] = "S/M"
        df.loc[df['Marca'] ==
               "SN", 'Marca'] = "S/M"
        df.loc[df['Marca'] ==
               "No disponible", 'Marca'] = "S/M"

        print("~ Limpiando NCMs...")

        # Estandarizo los valores del NCM

        df['NANDINA'] = df['NANDINA'].astype(str).str.replace('.', '')
        df['NANDINA'] = df['NANDINA'].astype(
            str).str.replace('[a-zA-Z]', '')
        df['NANDINA'] = df['NANDINA'].astype(str).str[:6]

        df["U$S Unitario"] = (
            df['U$S CIF'] / df['Kgs. Netos']).round(2)

        print("~ Creando columna de precio...")

        df = df.loc[df['U$S Unitario'] <= 1.2]

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

        df = df.dropna()

        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')

        results_dfs.append(df)

        dfs[i] = df

        if df is not None and not df.empty and not pd.isnull(df["Fecha"].iloc[0].year):
            print(
                f'> Done with: {df["Fecha"].iloc[0].year}\n~~~~~~~~~~~~~~~~~~~')
        else:
            print(f'> No data for: {year_error_memory}\n~~~~~~~~~~~~~~~~~~~')

    return results_dfs
