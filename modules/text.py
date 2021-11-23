from bs4 import BeautifulSoup
from unicodedata import normalize
from re import compile
from datetime import date


punctuationRegex = compile(r'[^0-9a-zA-Z_]')

mapaEstacao = {'outono' : 1,'inverno': 2, 'verão': 3, 'primavera': 4}

mapaClima = {
    'sol' :   1,
    'chuva' : 2,
    'nublado' : 3,
    'céu claro' : 4,
    'vento' : 5,
    'neve' : 6,
    'nevoeiro/neblina' : 7, 
    'granizo' : 8, 
    'garoa/chuvisco': 9
}


def cleaning(text:str) -> str:
    """
        Método principal que aplica a limpeza completa dos dados
    """
    cleanedText = str(text).lower()
    cleanedText = padronizaTexto(cleanedText)
    cleanedText = replaceBlanks(cleanedText)
    cleanedText = normalizeText(cleanedText)
    cleanedText = removePunctuation(cleanedText)    
    return cleanedText



def replaceBlanks(text:str) -> str:
    """
        Realiza as remoção de marcações de quebra de linha, 'carriage return' e espaçamento dos textos
    """
    text = text.replace(r'\r',' ')
    text = text.replace(r'\n', ' ')
    text = text.replace(r'\s', ' ')
    text = text.strip()
    return text


def normalizeText(text:str) -> str:
    """
        Realiza a normalização dos textos
    """
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def removePunctuation(text:str) -> str:
    """
        Realiza a remoção da pontuação dos textos
    """
    text = punctuationRegex.sub(' ', text)     
    return text


def padronizaTexto(text:str) -> str:
    """
        Método responsável por padronizar os valores para algumas variáveis
    """
    text = text.replace('ignorado', 'ignorada')
    text = text.replace(',', '.')
    return text


def estacaoAno(data:date) -> str:
    """
         Método responsável por mapear as estações do ano
    """
   
    dia = data.day
    mes = data.month
       
    if mes < 3 or mes == 3 and dia <= 19 or mes == 12 and dia >= 22:
        estacao = 'verão'
    if mes == 3 and dia >= 20 or mes < 6 and mes > 3 or mes == 6 and dia <= 20:
        estacao = 'outono'      
    if mes == 6 and dia >= 21 or mes < 9 and mes > 6 or mes == 9 and dia <= 22:
        estacao = 'inverno'
    else:
        estacao = 'primavera'
    return estacao


def diaSemana(data: date) -> str:
    """
         Método responsável por mapear os dias da semana
    """
    dias = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']
    
    data = date(year=data.year, month=data.month, day=data.day)
    indice_da_semana = data.weekday()
    diaSemana = dias[indice_da_semana]
    return diaSemana


def regiaoPais(uf:str) -> str:
    """
     Método resposável por mapear as regiões do Brasil
    """
    norte = ['AM', 'AC', 'RO', 'RR', 'AP', 'PA', 'TO']
    nordeste = ['MA', 'PI', 'RN', 'CE', 'PB', 'BA', 'PE', 'AL', 'SE']
    centroOeste = ['MS', 'MT', 'GO', 'DF']
    sudeste = ['MG', 'ES', 'RJ', 'SP']   
 
    if uf in norte:
        regiao = 'norte'        
    elif uf in nordeste:
        regiao = 'nordeste'        
    elif uf in centroOeste:
        regiao = 'centro-oeste'   
    elif uf in sudeste:
        regiao = 'sudeste'        
    else:
        regiao = 'sul'    
    return regiao