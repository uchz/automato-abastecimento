#%%
import pandas as pd


#Procura o arquivo no Desktop
df = pd.read_excel('abastecimento-por-oc.xls', header=2)

#Removendo colunas
df.drop(columns=['TIPOTAREFA', 'DESCDESTINO','DESCORIGEM','CODENDORIGEM','CODENDDESTINO','NUTAREFA', 'DTTAREFA','TIPOTAREFA' ], inplace=True)

df = df[df['PRIORIDADE'] != -999999999]

# Criar uma nova coluna para armazenar os valores atribuídos
df['novo_valor'] = 0

# Inicializar a variável de controle para atribuir valores diferentes
novo_valor = -89

# Criar um dicionário para rastrear o último valor atribuído para cada ordem de carga
ultimo_valor_por_ordem = {}
df.set_index('ORDEMCARGA')

# Iterar sobre as linhas do DataFrame
for index, row in df.iterrows():
    ordem_de_carga = row['ORDEMCARGA']

    # Verificar se a ordem de carga já foi encontrada anteriormente
    if ordem_de_carga not in ultimo_valor_por_ordem:
        # Se não foi encontrada, atribuir um novo valor
        ultimo_valor_por_ordem[ordem_de_carga] = novo_valor
        novo_valor += 1

    # Atribuir o valor à nova coluna
    df.at[index, 'novo_valor'] = ultimo_valor_por_ordem[ordem_de_carga]


# Tirando valores duplicados
df.drop_duplicates(subset=['CODPROD'], inplace=True)
#%%

df.head()
#%%
### import pyautogui as py
import pyautogui as py

py.sleep(10)
for i,n in zip(df['CODPROD'], df['novo_valor']):

    py.sleep(1.5)
    #Seleciona o Cód de Prod
    py.click(30,326)
    py.sleep(1)
    #Escreve o código
    py.write(str(i))
    py.sleep(1.5)
    #Clicar em aplicar
    py.click(269,149)
    py.sleep(1.5)
    #Seleciona area de prioridade
    py.click(440,206)
    py.sleep(1.5)
    py.click(440,206)
    py.sleep(1.5)
    # Escreve a prioridade
    py.write(str(n))
    py.sleep(1.5)
    py.press('enter')
    py.sleep(1.5)
    #Retira os abastecimentos sem dependentes
    try:
        while True:
            if py.locateCenterOnScreen('nao.png', confidence=0.7):
                nao = py.locateCenterOnScreen('nao.png', confidence=0.7)
                py.click(nao.x, nao.y)
                py.sleep(1)
                py.click(1778,603)
                py.sleep(1)
                py.click(1047,646)
            else:
                pass
    except py.ImageNotFoundException:
         pass
    #Seleciona empilhador por área
    py.sleep(1.5)
    py.click(1788,151)
    for area in df['AREA DE SEPA ENDEREçO DESTINO']:
        if area == 'SEP VAREJO 01 - (PICKING)':
            for nome in empilhadores:
                py.sleep(1.5)
                py.doubleClick(616,351)
                py.click(616,351)
                py.sleep(1.5)
                py.write(nome)
                py.sleep(1)
                py.doubleClick(599,411)
        else:
            pass
    py.click(1384,849)
    py.sleep(1)
    

