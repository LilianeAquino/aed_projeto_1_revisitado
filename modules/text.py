from bs4 import BeautifulSoup
from unicodedata import normalize
from re import compile
from datetime import date

punctuationRegex = compile(r'[^0-9a-zA-Z_]')

mapaEstacao = {'outono' : 1,'inverno': 2, 'verão': 3, 'primavera': 4}

mapaClima = {
    'sol': 0, 
    'chuva': 1, 
    'ignorada': 2, 
    'ceu claro': 3, 
    'nublado': 4, 
    'vento': 5,
    'neve': 6, 
    'nevoeiro/neblina': 7, 
    'granizo': 8, 
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


def padronizaTexto(text:str) -> str:
    """
        Método responsável por padronizar os valores para algumas variáveis
    """
    text = text.replace('ignorado', 'ignorada')
    text = text.replace(',', '.')
    return text


def padronizaDiaSemana(text:str) -> str:
    """
     Método responsável por padronizar os dias da semana
    """
    text = text.lower()
    text = text.replace('segunda-feira', 'segunda')
    text = text.replace('terça-feira', 'terça')
    text = text.replace('quarta-feira', 'quarta')
    text = text.replace('quinta-feira', 'quinta')
    text = text.replace('sexta-feira', 'sexta')
    return text


def padronizaCausaAcidente(text:str) -> str:
    """
     Método responsável por padronizar  as causas dos acidentes
    """
    text = text.lower()
    
    if text == 'ingestao de alcool' or text=='ingestao de substancias psicoativas':
        text = 'ingestao de alcool ou substancias psicoativas'
    
    text = text.replace('defeito mecanico em veiculo', 'defeito mecanico no veiculo')
    text = text.replace('falta de atencao a conducao', 'falta de atencao')
    text = text.replace('falta de atencao do pedestre', 'falta de atencao')
    text = text.replace('mal subito do condutor', 'mal subito')
    text = text.replace('restricao de visibilidade em curvas horizontais', 'restricao de visibilidade')
    text = text.replace('restricao de visibilidade em curvas verticais', 'restricao de visibilidade')
    text = text.replace('condutor dormindo', 'dormindo')
    text = text.replace('ingestao de alcool pelo condutor', 'ingestao de alcool ou substancias psicoativas')
    text = text.replace('ingestao de alcool ou substancias psicoativas pelo condutor', 'ingestao de alcool ou substancias psicoativas')
    text = text.replace('ingestao de alcool e/ou substancias psicoativas pelo pedestre', 'ingestao de alcool ou substancias psicoativas')
    text = text.replace('ingestao de alcool ou de substancias psicoativas pelo pedestre', 'ingestao de alcool ou substancias psicoativas')
    text = text.replace('ingestao de substancias psicoativas pelo condutor', 'ingestao de alcool ou substancias psicoativas')
    return ' '.join(palavra.strip() for palavra in text.split())


def padronizaTipoAcidente(text:str) -> str:
    """
     Método responsável por padronizar os tipos de acidentes
    """
    text = text.lower()   
    text = text.replace('colisao com objeto fixo', 'colisao com objeto')
    text = text.replace('colisao com objeto movel', 'colisao com objeto')
    text = text.replace('colisao lateral mesmo sentido', 'colisao lateral')
    text = text.replace('colisao lateral sentido oposto', 'colisao lateral')
    return ' '.join(palavra.strip() for palavra in text.split())


def padronizaNomeBrs(text:str) -> str:
    """
     Método responsável por padronizar os nomes das BRs
    """
    return text.replace('.0', '')


def estacaoAno(data:date) -> str:
    """
         Método responsável por mapear as estações do ano
    """
   
    dia = data.day
    mes = data.month
       
    if (mes == 12 and dia >= 21) or (mes < 3) or (mes == 3 and dia <= 20):
        return 'verão'
    if (mes == 3 and dia >= 21) or (mes > 3 and mes < 6) or (mes == 6 and dia <= 20):
        return 'outono'      
    if (mes == 6 and dia >= 21) or (mes > 6 and mes < 9) or (mes == 9 and dia <= 22):
        return 'inverno'
    return 'primavera'


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