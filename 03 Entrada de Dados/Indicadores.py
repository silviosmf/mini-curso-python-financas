import pandas as pd

def ebit(list_dre_empresas):
    caminho_arquivos = '../dados/cvm'
    # Carregar DRE
    dre = pd.read_csv(f'{caminho_arquivos}/DRE.csv', sep=';', encoding='ISO-8859-1', decimal=',')

    list_ = []
    for cnpj in list_dre_empresas['cnpj']:
        list_.append(dre[dre['CNPJ_CIA'] == cnpj])

    list_df_ebit = []
    for dre_empresa in list_:
        df_ebit = dre_empresa[(dre_empresa['CD_CONTA'] == '3.05')]

        df_ebit['TRIMESTRE'] = 0
        df_ebit.loc[(pd.to_datetime(df_ebit['DT_INI_EXERC']).dt.month == 1) & 
            (pd.to_datetime(df_ebit['DT_FIM_EXERC']).dt.month == 3), 'TRIMESTRE'] = 1
        df_ebit.loc[(pd.to_datetime(df_ebit['DT_INI_EXERC']).dt.month == 1) & 
            (pd.to_datetime(df_ebit['DT_FIM_EXERC']).dt.month == 6), 'TRIMESTRE'] = 2
        df_ebit.loc[(pd.to_datetime(df_ebit['DT_INI_EXERC']).dt.month == 1) & 
            (pd.to_datetime(df_ebit['DT_FIM_EXERC']).dt.month == 9), 'TRIMESTRE'] = 3
        df_ebit.loc[(pd.to_datetime(df_ebit['DT_INI_EXERC']).dt.month == 1) & 
            (pd.to_datetime(df_ebit['DT_FIM_EXERC']).dt.month == 12), 'TRIMESTRE'] = 4

        df_ebit = df_ebit[df_ebit['TRIMESTRE'] != 0]
        df_ebit['DT_FIM_EXERC'] = pd.to_datetime(df_ebit['DT_FIM_EXERC']) 

        df_ebit = df_ebit[['DT_FIM_EXERC','VL_CONTA']]
        df_ebit.columns = ['Date','Ebit']
        df_ebit.set_index('Date', inplace=True)

        list_df_ebit.append(df_ebit)

    return list_df_ebit


def df_fluxos_de_caixa(dt_inicial, dt_final, cnpj):
    caminho_arquivos = '../dados/cvm'
    # Carregar DFC
    dfc = pd.read_csv(f'{caminho_arquivos}/DFC_MI.csv', sep=';', encoding='ISO-8859-1', decimal=',')    

    list_fc = []

    for ano in range(dt_inicial,dt_final+1):
        for mes in range(3,15,3):
            dfc_resultado =  dfc[(dfc['CNPJ_CIA'] == cnpj) & 
                (pd.to_datetime(dfc['DT_REFER']).dt.month == mes) &
                (pd.to_datetime(dfc['DT_REFER']).dt.year == ano) &
                (dfc['CD_CONTA'].str.contains('6.05.0'))]
            list_fc.append({'data':dfc_resultado.iloc[0]['DT_REFER'],
                        'fluxo_caixa':dfc_resultado.iloc[1]['VL_CONTA'] - dfc_resultado.iloc[0]['VL_CONTA']})

    # Criar DataFrame com Saldo do Fluxo de Caixa por Semestre para a empresas selecionada
    df_fc = pd.DataFrame(list_fc)


    return df_fc