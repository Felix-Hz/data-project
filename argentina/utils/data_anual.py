def annual_data(dfs):
    global company_dic

    transition_dic = {
        "NCM": [],
        "Año": [],
        "Volumen Total": []
    }

    for df in dfs:
        transition_dic['NCM'].append(''.join(df['NCM-SIM'].unique()))

        transition_dic['Año'].append(df["Fecha"][4].year)

        volumenTotalImportacionTn = (df['Kgs. Netos'].sum()/1000).round(2)

        transition_dic['Volumen Total'].append(volumenTotalImportacionTn)

        print(f"- {df['Fecha'][4].year} appended.")

    print("~~~~~~~~~~~~~~~~~~~\n> Transition dictionary:")

    for key, values in transition_dic.items():
        print(f"- {key}: {values}")
