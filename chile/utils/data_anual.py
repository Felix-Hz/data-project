def annual_data(dfs):
    global company_dic

    transition_dic = {
        "NCM": [],
        "Año": [],
        "Volumen Total": []
    }

    for df in dfs:
        transition_dic['NCM'].append(''.join(df['Código SACH'].unique()))

        transition_dic['Año'].append(df["Fecha"][0].year)

        volumenTotalImportacionTn = (
            df['Cantidad Comercial'].sum()/1000).round(2)

        transition_dic['Volumen Total'].append(volumenTotalImportacionTn)

        print(f"- {df['Fecha'][0].year} appended.")

    print("~~~~~~~~~~~~~~~~~~~\n> Transition dictionary:")

    for key, values in transition_dic.items():
        print(f"- {key}: {values}")

