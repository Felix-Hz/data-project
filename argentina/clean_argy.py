def argy_wrangling(dfs):

    for df in dfs:
        # print('hola')

        df = df.loc[:, ['NCM-SIM', 'Fecha', 'Tipo de Dato',  'Importador', 'Localidad', 'Destinación', 'Aduana', 'Via Transporte', 'País de Origen',
                        'País de Procedencia', 'U$S Unitario', 'U$S FOB', 'Flete U$S', 'Seguro U$S', 'U$S CIF', 'Cantidad', 'Unidad de Medida', 'Kgs. Netos',
                        'Marca - Sufijos', 'Cantidad.1']]

        # Se eliminan registros que vengan por aire
        subset = df['Via Transporte']
        df_new_36 = df[subset != 'AVION']

        # Se limpia la palabra MARCA: por redundante
        df['Marca - Sufijos'] = df['Marca - Sufijos'].str.replace(
            'MARCA: ', '')

        # Se eliminna registros que no tengan las marcas registradas
        df.loc[df['Marca - Sufijos'] ==
               "SIN MARCA", 'Marca - Sufijos'] = "S/M"

        df["U$S Unitario"] = (
            df['U$S CIF'] / df['Kgs. Netos']).round(2)

        # Estandarizo los valores del NCM
        df['NCM-SIM'] = df['NCM-SIM'].str.replace('.', '')
        df['NCM-SIM'] = df['NCM-SIM'].str.replace('[a-zA-Z]', '')
        df['NCM-SIM'] = df['NCM-SIM'].str[:6]

        df = df.dropna()

        print(f'> Done with: {df["Fecha"][0].year}\n~~~~~~~~~~~~~~~~~~~')

