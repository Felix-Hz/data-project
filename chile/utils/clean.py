import pandas as pd


def wrangling(dfs):

    results_dfs = []

    for i in range(len(dfs)):
        df = dfs[i]

        df = df.loc[:, ['Código SACH', 'Fecha',  'Importador', 'Aduana', 'Vía Transporte', 'País de Origen', 'País de Adquisición', 'FOB Unitario U$S', 'FOB U$S', 'Flete U$S', 'Seguro U$S', 'U$S CIF', 'U$S Unitario', 'Cantidad Comercial', 'Unidad de Medida', 'Kgs. Brutos',
                        'Mercadería', 'Variedad', 'Marca', 'Manifiesto', 'Fecha Manifiesto']]

        print("~ Limpiando vías de transporte...")

        # Se eliminan registros que vengan por aire
        subset = df['Vía Transporte']
        df = df[subset != 'AEREA']

        print("~ Limpiando NCMs...")

        # Estandarizo los valores del NCM
        df['Código SACH'] = df['Código SACH'].astype(str).str.replace('.', '')
        df['Código SACH'] = df['Código SACH'].astype(str).str.replace('[a-zA-Z]', '')
        df['Código SACH'] = df['Código SACH'].astype(str).str[:6]

        print("~ Creando columna de precio...")
        df["U$S Unitario"] = (df['U$S CIF'] / df['Cantidad Comercial']).round(2)

        # df_new_filtered = df_new.loc[(df_new['U$S Unitario'] <= 1.2)]

        print("~ Dropping nulls...")

        df = df.dropna()

        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')

        results_dfs.append(df)

        dfs[i] = df

        print(f'> Done with: {df["Fecha"][5].year}\n~~~~~~~~~~~~~~~~~~~')

    return results_dfs
