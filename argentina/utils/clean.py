import pandas as pd


def wrangling(dfs):

    results_dfs = []

    for i in range(len(dfs)):
        df = dfs[i]

        # print('hola')

        df.loc[:, ['NCM-SIM', 'Fecha', 'Tipo de Dato',  'Importador', 'Localidad', 'Destinación', 'Aduana', 'Via Transporte', 'País de Origen',
                   'País de Procedencia', 'U$S Unitario', 'U$S FOB', 'Flete U$S', 'Seguro U$S', 'U$S CIF', 'Cantidad', 'Unidad de Medida', 'Kgs. Netos',
                   'Marca - Sufijos', 'Cantidad.1']] = df.loc[:, ['NCM-SIM', 'Fecha', 'Tipo de Dato',  'Importador', 'Localidad', 'Destinación', 'Aduana', 'Via Transporte', 'País de Origen',
                                                                  'País de Procedencia', 'U$S Unitario', 'U$S FOB', 'Flete U$S', 'Seguro U$S', 'U$S CIF', 'Cantidad', 'Unidad de Medida', 'Kgs. Netos',
                                                                  'Marca - Sufijos', 'Cantidad.1']]

        # Se eliminan registros que vengan por aire
        subset = df['Via Transporte']
        df = df[subset != 'AVION']

        # Se limpia la palabra MARCA: por redundante
        df['Marca - Sufijos'] = df['Marca - Sufijos'].str.replace(
            'MARCA: ', '')

        # Se eliminna registros que no tengan las marcas registradas
        df.loc[df['Marca - Sufijos'] ==
               "SIN MARCA", 'Marca - Sufijos'] = "S/M"

        print("~ Limpiando marcas...")

        # Estandarizo los valores del NCM
        df['NCM-SIM'] = df['NCM-SIM'].str.replace('.', '')
        df['NCM-SIM'] = df['NCM-SIM'].str.replace('[a-zA-Z]', '')
        df['NCM-SIM'] = df['NCM-SIM'].str[:6]

        print("~ Limpiando NCMs...")

        df["U$S Unitario"] = (
            df['U$S CIF'] / df['Kgs. Netos']).round(2)

        print("~ Creando columna de precio...")

        df = df.dropna()

        print("~ Dropping nulls...")

        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')

        results_dfs.append(df)

        dfs[i] = df

        print(f'> Done with: {df["Fecha"][5].year}\n~~~~~~~~~~~~~~~~~~~')

    return results_dfs
