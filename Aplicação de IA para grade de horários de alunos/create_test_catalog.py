import pandas as pd

# Dados de exemplo para o catálogo de teste
data = {
    'Cod. Disciplina': ['CAD8020', 'CAD8020', 'CIN7504', 'CAD8016', 'MAT1101', 'ECO1000', 'ADM1234', 'DIR5000', 'CAD8010', 'CAD8019'],
    'Nome': ['Finanças Corporativas I', 'Finanças Corporativas I', 'Gerenciamento de Projetos', 'Lab. Desenv. Carreira', 'Cálculo A', 'Introdução à Economia', 'Marketing Básico', 'Direito Empresarial', 'Gestão de Pessoas', 'Logística'],
    'Turma': ['01A', '01B', '01N', '01', 'N01', 'N02', 'N01', 'N03', 'M01', 'M02'],
    'Horário': ['2.1830-2 4.1830-2', '3.2020-2 5.2020-2', '3.2020-2 5.2020-2', '6.1830-2', '2.2020-2 4.2020-2', '3.1830-2 5.1830-2', '2.2020-2 4.2020-2', '6.2020-2', '2.0800-4', '3.1000-4'], # Formato D.HHMM-C
    'Créditos': [4, 4, 4, 2, 4, 4, 4, 2, 4, 4],
    'Vagas Ofertadas': [50, 50, 40, 60, 50, 50, 45, 40, 30, 30],
    'Vagas Disponíveis': [10, 5, 8, 15, 12, 3, 0, 9, 0, 2] # Algumas com vagas, outras não
}

df = pd.DataFrame(data)

# Salvar como arquivo Excel
output_path = '/home/ubuntu/catalogo_teste.xlsx'
df.to_excel(output_path, index=False)

print(f"Arquivo de teste criado em: {output_path}")

