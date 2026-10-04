import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('dados/relatorio_extrato.xlsx', skiprows=1, skipfooter=8)
df = df.drop(columns=['Situação'])

#Corrigindo os valores da coluna valor
df['Valor'] = df['Valor'].str.replace('.', '', regex=False)
df['Valor'] = df['Valor'].str.replace(',', '.', regex=False)
df['Valor'] = df['Valor'].str.replace('+ ', '', regex=False)
df['Valor'] = df['Valor'].str.replace('- ', '-', regex=False)
df['Valor'] = pd.to_numeric(df['Valor'])


#convertendo a coluna data
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)

'''
Verificacao do erro ao transformar a coluna valor em int
print(df['Valor'].map(type).value_counts())
print(pd.to_numeric(df['Valor'], errors='coerce').isna().sum())
'''

''' 
#Verificando algumas informacoes basicas
print(df.describe())
print(df.size())
print(df.info())
print(df.isnull().sum())

print(df['Plano de contas'].unique())
print(df['Conta bancária'].unique())

'''

#Iniciando analise dos gastos

#analise por plano de contas e valores
gastos = df[df['Valor']<0]
despesas = gastos.groupby('Plano de contas')['Valor'].sum()

print(despesas)
print(gastos['Valor'].sum())

#analise por fornecedor e valores
despesas_fornecedor = gastos.groupby('Fornecedor')['Valor'].sum()
print(despesas_fornecedor)

#grafico de gastos
#despesas.abs().plot(kind='bar')
plt.title('Despesas de Agosto')
plt.xlabel('Plano de contas')
plt.ylabel('Valor')
plt.xticks(rotation=45, ha='right', fontsize=6)
#plt.show()

#grafico de gastos em torta
valores = despesas.abs()
nomes = despesas.index
porcentagens = valores / valores.sum() * 100

cores=['black', 'gray', 'yellow', 'red', 'blue', 'pink', 'darkblue', 'green','magenta', 'white', 'orange', 'lightgray', 'darkgreen','brown', 'purple', 'darkorange', 'lightblue', 'lightgreen', 'cyan', 'gold']


legenda = [f'{nome} - {porcentagem:.1f}%'
           for nome, porcentagem in zip(nomes, porcentagens)]

plt.pie(valores, colors=cores)
#plt.legend(legenda, loc='upper right', bbox_to_anchor=(1.6, 1))
plt.xlabel(None)
plt.ylabel(None)

#plt.show()


#grafico de gastos por data
gastos_diario = gastos.groupby('Data')['Valor'].sum().abs()
#gastos_diario.plot(kind='line')
plt.title('Gastos Diarios de Agosto')
plt.xlabel('Data') 
plt.ylabel('Valor')
#plt.xticks(rotation=45, ha='right', fontsize =6)
#plt.show()

#iniciando analise de recebimentos

#analise por plano de contas e valores
recebimentos = df[df['Valor']>0]
receitas = recebimentos.groupby('Plano de contas')['Valor'].sum()
print(receitas)

#analise por fornecedor e valores de recebimento
receitas_clientes = recebimentos.groupby('Fornecedor')['Valor'].sum()
print(receitas_clientes)

#grafico recebimentos
#receitas.abs().plot(kind='bar')
plt.title('Receitas de Agosto')
plt.xlabel('Plano de contas')
plt.ylabel('Valor')

#plt.show()

#grafico de recebimentos por data

recebimmentos_diario = recebimentos.groupby('Data')['Valor'].sum().abs()
recebimmentos_diario.plot(kind='line')
plt.title('Recebimentos Diarios de Agosto')
plt.xlabel('Data')
plt.ylabel('Valor')
plt.xticks(rotation=45, ha='right', fontsize=6)
plt.show()


#analisando receita liquida

taxas = df[df['Plano de contas'] == 'Taxas/Tarifas']
print(taxas['Valor'].sum())

receita_liquida = recebimentos['Valor'].sum() + taxas['Valor'].sum()
print(receita_liquida)


#resultado

resultado = recebimentos['Valor'].sum() + gastos['Valor'].sum()
print(resultado)
