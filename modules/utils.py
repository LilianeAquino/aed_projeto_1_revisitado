import pandas as pd
import numpy as np


def getPivotTable(dados:pd.DataFrame, colunaForIndex:str, colunaForColumns:str, shapeToCalculatePercentage:int) -> pd.DataFrame:
    """
         Retorna a pivot table já formatada
    """
    pivot_table = generatePivotTable(dados, colunaForIndex, colunaForColumns)
    return formatPivotTable(pivot_table, shapeToCalculatePercentage)


def generatePivotTable(dados:pd.DataFrame, colunaForIndex:str, colunaForColumns:str) -> pd.DataFrame:
    """
        Método responsável por gerar as tabelas "pivot" do pandas
    """
    sample = dados[[colunaForIndex, colunaForColumns]]
    sample['count'] = 1    
    return pd.pivot_table(sample, values='count', index=colunaForIndex, columns=colunaForColumns, aggfunc=np.sum)


def formatPivotTable(pivot_table:pd.DataFrame, shapeToCalculatePercentage:int) -> pd.DataFrame:
    """
         Método responsável por formatar a tabela gerada 
    """
    for col in pivot_table.columns:
        pivot_table.fillna(0, inplace=True)
        pivot_table[col] = pivot_table[col].astype(int)
        pivot_table[col] = round((pivot_table[col]/shapeToCalculatePercentage)*100, 2)
    return pivot_table