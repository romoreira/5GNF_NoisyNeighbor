import pandas as pd
import glob
import os

# Diretório com os CSVs
csv_dir = 'resources_stats'

# Encontre todos os arquivos csv no diretório
csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))

# Comece lendo o primeiro arquivo para iniciar o merge
merged_df = None

for file in csv_files:
    df = pd.read_csv(file)
    # Nomeia as colunas diferentes, exceto 'time'
    cols = ['time'] + [f"{os.path.splitext(os.path.basename(file))[0]}_{col}" for col in df.columns if col != 'time']
    df.columns = cols
    if merged_df is None:
        merged_df = df
    else:
        merged_df = pd.merge(merged_df, df, on='time', how='outer')

# Salva resultado
merged_df.to_csv('/home/romoreira/VSCodeProject/5GNF_NoisyNeighbor/resources_stats/final/resources_stats_merged.csv', index=False)
print("Arquivo 'resources_stats_merged.csv' gerado com sucesso!")
