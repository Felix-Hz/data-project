import pandas as pd


def wrangling(df):
    '''

        Data wrangling for initial dataframes. This function selects columns, deletes airway products, standardizes NCMs,
        creates a unitary U$S price, filters unitary price, removes outliers & drops nulls.

            Args:
                - dfs (list): A list of dataframes to be cleaned and processed.

            Returns:
                - list: A list of clean dataframes.

    '''

    print(f"\n> MUNGING CURRENT DATA:\n")

    year_error_memory = df["Fecha"].iloc[0].year

    df = df.loc[:, ['NANDINA', 'Fecha', 'País de Origen', 'País de Procedencia', 'Probable Importador', 'Probable Proveedor', 'Aduana', 'Transporte',
                    'País de Compra', 'U$S CIF', 'CIF Unitario', 'U$S FOB', 'FOB Unitario', 'Flete', 'Seguro', 'Kgs. Netos', 'Kgs. Brutos', 'Cantidad', 'Unidad']]

    # Se eliminan registros que vengan por aire
    subset = df['Transporte']
    df = df[subset != 'AEREA']

    print("~ Limpiando NCMs...")

    # Estandarizo los valores del NCM

    df['NANDINA'] = df.loc[:, 'NANDINA'] = 283525

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

    if df is not None and not df.empty and not pd.isnull(df["Fecha"].iloc[0].year):
        print(
            f'> Done with: {df["Fecha"].iloc[0].year}\n~~~~~~~~~~~~~~~~~~~')
    else:
        print(f'> No data for: {year_error_memory}\n~~~~~~~~~~~~~~~~~~~')

    return df
