#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------
# Projeto Soluções de Mineração de Dados
# ----------------------------------------
# ********** Pré-processamento **********

# Base de dados: 
# Activity recognition with healthy older people using a batteryless
# wearable sensor Data Set

#%%********************************
# *** Importação de bibliotecas ***
# *********************************

import glob
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier

#%%*******************************
# *** Leitura da base de dados ***
# ********************************

# Salvar todos os data paths dos arquivos
data_path_arquivos = sorted(glob.glob('S*_Dataset/d*'))

df = pd.DataFrame()

# Nome dos atributos dos arquivos da base de dados
colunas = ['tempo', 'frontal', 'vertical', 'lateral', 'antena', 'rssi', 
           'fase', 'frequencia', 'atividade']

for data_path in data_path_arquivos:
    pasta = data_path[0:11]         # Salva o nome da pasta, 'S1_Dataset/'
    nome_arquivo = data_path[11:]   # Salva o nome do arquivo, ex.: 'd1p01M'
    
    if nome_arquivo != 'README.txt':
        # Leitura do arquivo
        data = pd.read_csv(data_path, header=None, names=colunas)
        
        # Substituir diretamente os caracteres por valores numéricos, para
        # criação das colunas 'sala' e 'sexo':
        data['sala'] = (0, 1)[nome_arquivo.startswith('d2')] # S1: 0 / S2:1
        data['sexo'] = (0, 1)[nome_arquivo.endswith('F')] # 'M':0 / 'F':1
        
        # Juntando todos os arquivos lidos em um mesmo dataframe
        df = df.append(data, ignore_index=True)

# Reordenamento das colunas
df = df[['sala', 'sexo', 'tempo', 'frontal', 'vertical', 'lateral', 'antena', 
         'rssi', 'fase', 'frequencia', 'atividade']]

# Separação dos dados em atributos e classe
X = df.values[:, 0:-1]
y = df.values[:, -1]

#%% **************************************
# *** Separação dos dados treino/teste ***
# ****************************************

seed = 75128
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, 
                                                        random_state=seed)

# Fixando as dimensões das classes como (n_exemplos x 1)
y_treino = np.reshape(y_treino, (y_treino.shape[0], 1))
y_teste = np.reshape(y_teste, (y_teste.shape[0], 1))

#%% ****************************
# *** Normalização dos dados ***
# ******************************

MinMax = MinMaxScaler(feature_range=(0, 1))

# É importante que o fit seja realizado somente nos dados de treino
MinMax.fit(X_treino)

# Depois de determinados os parâmetros da normalização, aplicar nos
# dados de treino e teste
X_treino_escalonado = MinMax.transform(X_treino)
X_teste_escalonado = MinMax.transform(X_teste)

#%% **************************
# *** Seleção de Atributos ***
# ****************************

# Usar o RandomForest para ver importância de features na classificação

clf = RandomForestClassifier(n_estimators=1000, random_state=seed, n_jobs=-1)

clf.fit(X_treino_escalonado, y_treino)

importancia_atributos = []

plt.rcParams['figure.figsize'] = 12, 8

# Lista com importância de cada feature
for feature in zip(df.columns, clf.feature_importances_):
    plt.bar(feature[0], feature[1])
    plt.title('Importância dos atributos usando Random Forest', size=16)
    plt.xlabel('Atributos')
    plt.ylabel('Nível de importância')
    importancia_atributos.append(feature)

plt.show()

importancia_atributos = sorted(importancia_atributos, key=lambda x:x[1], 
                               reverse=True)

#%% ************************
# *** Salvar os arquivos ***
# **************************

tipos_dados = ['%d', '%d', '%10.9f', '%10.9f', '%10.9f', '%10.9f', '%10.9f', 
               '%10.9f', '%10.9f', '%10.9f', '%d']

# Salvar os dados de treino e teste em arquivos .csv
np.savetxt("Dataset_processado/dataset_treino_processado.csv", 
           np.hstack((X_treino_escalonado, y_treino)), comments='',
           fmt=tipos_dados, delimiter=",", header=','.join(df.columns))
np.savetxt("Dataset_processado/dataset_teste_processado.csv", 
           np.hstack((X_teste_escalonado, y_teste)), comments='',
           fmt=tipos_dados, delimiter=",", header=','.join(df.columns))

#%% ***************************************
# *** Análise de Componentes Principais ***
# *****************************************

pca = PCA().fit(X_treino_escalonado)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Número de componentes')
plt.ylabel('Variância explicada cumulativa')
plt.title('Análise da variância explicada com PCA\n(normalização MinMax)', 
          size=16)
plt.show()