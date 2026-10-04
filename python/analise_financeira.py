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
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date

#Iniciando analise dos gastos

#analise por plano de contas e valores
gastos = df[df['Valor']<0]
despesas = gastos.groupby('Plano de contas')['Valor'].sum()
gastos_totais = gastos['Valor'].sum()

print(despesas)
print(gastos_totais)

#grafico de gastos
sns.barplot(x=despesas.index,y=despesas.abs().values)
plt.title('Despesas de Agosto')
plt.xlabel('Plano de contas')
plt.ylabel('Valor')
plt.xticks(rotation=45, ha='right', fontsize=6)

plt.savefig('graficos/despesas_por_plano.png', bbox_inches='tight')
plt.close()

#grafico de gastos em torta
valores_gastos = despesas.abs()
nomes_gastos = despesas.index
porcentagens = valores_gastos / valores_gastos.sum() * 100

cores=['black', 'gray', 'yellow', 'red', 'blue', 'pink', 'darkblue', 'green','magenta', 'white', 'orange', 'lightgray', 'darkgreen','brown', 'purple', 'darkorange', 'lightblue', 'lightgreen', 'cyan', 'gold']


legenda = [f'{nome} - {porcentagem:.1f}%'
           for nome, porcentagem in zip(nomes_gastos, porcentagens)]

plt.pie(valores_gastos, colors=cores)
plt.title('Despesas por Plano de Contas')
plt.legend(legenda, loc='center right', bbox_to_anchor=(2, 0.5))
plt.xlabel(None)
plt.ylabel(None)

plt.savefig('graficos/despesas_por_plano_pie.png', bbox_inches='tight')
plt.close()

#analise por fornecedor e valores
despesas_fornecedor = gastos.groupby('Fornecedor')['Valor'].sum()
print(despesas_fornecedor)

#grafico de gastos por fornecedor

sns.barplot(x=despesas_fornecedor.abs().values, y=despesas_fornecedor.index)
plt.title('Despesas por Fornecedor')
plt.xlabel('Valor')
plt.ylabel('Fornecedor')
plt.yticks(fontsize=5)

plt.savefig('graficos/despesas_por_fornecedor.png', bbox_inches='tight')
plt.close()


#grafico de gastos por data
gastos_diario = gastos.groupby('Data')['Valor'].sum().abs()
gastos_diario.plot(kind='line')
plt.title('Gastos Diarios de Agosto')
plt.xlabel('Data') 
plt.ylabel('Valor')
plt.xticks(rotation=45, ha='right', fontsize =6)

plt.savefig('graficos/gastos_diarios.png', bbox_inches='tight')
plt.close()

#iniciando analise de recebimentos

#analise por plano de contas e valores
recebimentos = df[df['Valor']>0]
receitas = recebimentos.groupby('Plano de contas')['Valor'].sum()
print(receitas)

#analise por fornecedor e valores de recebimento
receitas_clientes = recebimentos.groupby('Fornecedor')['Valor'].sum()
print(receitas_clientes)

#grafico recebimentos
sns.barplot( x=receitas.index, y=receitas.values)
plt.title('Receitas de Agosto')
plt.xlabel('Plano de contas')
plt.ylabel('Valor')

plt.savefig('graficos/receitas_por_plano.png', bbox_inches='tight')
plt.close()


#grafico de recebimentos em pie
valores_recebidos= receitas_clientes
nomes_recebidos = receitas_clientes.index

porcentagens_recebidos = valores_recebidos/ valores_recebidos.sum() * 100

legenda_recebidos= [f'{nome_recebido} - {porcentagem_recebido:.1f}%'
                    for nome_recebido, porcentagem_recebido in zip(nomes_recebidos, porcentagens_recebidos)]

plt.pie(valores_recebidos, colors='blue')
plt.title('Receitas por Fornecedor')
plt.legend(legenda_recebidos, loc='upper right', bbox_to_anchor=(1.6, 1))
plt.xlabel('')
plt.ylabel('')

plt.savefig('graficos/receitas_por_fornecedor.png', bbox_inches='tight')
plt.close()

#grafico de recebimentos por data

recebimentos_diario = recebimentos.groupby('Data')['Valor'].sum()
recebimentos_diario.plot(kind='line')
plt.title('Recebimentos Diarios de Agosto')
plt.xlabel('Data')
plt.ylabel('Valor')
plt.xticks(rotation=45, ha='right', fontsize=6)

plt.savefig('graficos/recebimentos_diarios.png', bbox_inches='tight')
plt.close()

#analisando receita liquida
taxas = df[df['Plano de contas'] == 'Taxas/Tarifas']

receita_bruta = recebimentos['Valor'].sum()
taxas_total = taxas['Valor'].sum()
receita_liquida = receita_bruta + taxas_total

print(receita_bruta)
print(taxas_total)
print(receita_liquida)

#grafico pie da receita liquida

dados_pie = [receita_liquida, abs(taxas_total)]
nomes=['Receita Líquida', 'Taxas/Tarifas']

plt.pie(dados_pie, autopct='%1.1f%%')
plt.title('Composição da Receita Bruta')
plt.legend(nomes, loc='upper right', bbox_to_anchor=(1.6, 1))
plt.xlabel('')
plt.ylabel('')

plt.savefig('graficos/receita_liquida.png', bbox_inches='tight')
plt.close()


#resultado

resultado = receita_bruta + gastos_totais
print(resultado)

#grafico resultado

dados_resultados = pd.DataFrame({
    'Tipo': ['Recebimentos', 'Gastos', 'Resultado'],
    'Valor': [receita_bruta, abs(gastos_totais), resultado]
})

sns.barplot(data=dados_resultados, x='Valor', y='Tipo')
plt.title('Resultado Mês de Agosto')
plt.xlabel('')
plt.ylabel('')

plt.savefig('graficos/resultado_financeiro.png', bbox_inches='tight')
plt.close()
