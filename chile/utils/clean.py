import pandas as pd


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

    for i in range(len(dfs)):

        df = dfs[i]
        year_error_memory = df["Fecha"][0].year

        df = df.loc[:, ['Código SACH', 'Fecha',  'Importador', 'Aduana', 'Vía Transporte', 'País de Origen', 'País de Adquisición', 'FOB Unitario U$S', 'FOB U$S', 'Flete U$S', 'Seguro U$S', 'U$S CIF', 'U$S Unitario', 'Cantidad Comercial', 'Unidad de Medida', 'Kgs. Brutos',
                        'Mercadería', 'Variedad', 'Marca', 'Manifiesto', 'Fecha Manifiesto']]

        print("~ Limpiando vías de transporte...")

        # Se eliminan registros que vengan por aire
        subset = df['Vía Transporte']
        df = df[subset != 'AEREA']

        print("~ Limpiando NCMs...")

        # Estandarizo los valores del NCM
        df['Código SACH'] = df['Código SACH'].astype(str).str.replace('.', '')
        df['Código SACH'] = df['Código SACH'].astype(
            str).str.replace('[a-zA-Z]', '')
        df['Código SACH'] = df['Código SACH'].astype(str).str[:6]

        print("~ Creando columna de precio...")
        df["U$S Unitario"] = (
            df['U$S CIF'] / df['Cantidad Comercial']).round(2)

        df = df.loc[df['U$S Unitario'] <= 1.2]

        print("~ Limpiando outliers...")
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

        if not pd.isnull(df["Fecha"].iloc[0].year):
            print(
                f'> Done with: {df["Fecha"].iloc[0].year}\n~~~~~~~~~~~~~~~~~~~')
        else:
            print(f'> No data for: {year_error_memory}\n~~~~~~~~~~~~~~~~~~~')

    return results_dfs
