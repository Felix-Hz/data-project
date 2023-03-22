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

        df = df.loc[:, ['NCM-SIM', 'Fecha', 'Tipo de Dato',  'Importador', 'Localidad', 'Destinación', 'Aduana', 'Via Transporte', 'País de Origen',
                        'País de Procedencia', 'U$S Unitario', 'U$S FOB', 'Flete U$S', 'Seguro U$S', 'U$S CIF', 'Cantidad', 'Unidad de Medida', 'Kgs. Netos',
                        'Marca - Sufijos', 'Cantidad.1']]

        # Se eliminan registros que vengan por aire
        subset = df['Via Transporte']
        df = df[subset != 'AVION']

        print("~ Limpiando marcas...")

        # Se limpia la palabra MARCA: por redundante
        df['Marca - Sufijos'] = df['Marca - Sufijos'].str.replace(
            'MARCA: ', '')

        # Se eliminna registros que no tengan las marcas registradas
        df.loc[df['Marca - Sufijos'] ==
               "SIN MARCA", 'Marca - Sufijos'] = "S/M"

        print("~ Limpiando NCMs...")

        # Estandarizo los valores del NCM
        df['NCM-SIM'] = df['NCM-SIM'].str.replace('.', '')
        df['NCM-SIM'] = df['NCM-SIM'].str.replace('[a-zA-Z]', '')
        df['NCM-SIM'] = df['NCM-SIM'].str[:6]

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

        print(f'> Done with: {df["Fecha"].iloc[0].year}\n~~~~~~~~~~~~~~~~~~~')

    return results_dfs
