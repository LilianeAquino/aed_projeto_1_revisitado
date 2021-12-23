from bs4 import BeautifulSoup
from unicodedata import normalize
from re import compile
from datetime import date
from datetime import datetime

punctuationRegex = compile(r'[^0-9a-zA-Z_]')


mapFase = {
    'amanhecer': 'dia', 
    'pleno dia': 'dia', 
    'anoitecer': 'noite', 
    'plena noite': 'noite'
}


mapClima = {
    'ceu claro': 'ensolarado',
    'sol': 'ensolarado',
    'nublado': 'nublado',
    'nevoeiro/neblina': 'nublado',
    'chuva': 'tempo ruim',
    'garoa/chuvisco': 'tempo ruim',
    'granizo': 'tempo ruim',
    'neve': 'tempo ruim',
    'vento': 'tempo ruim'
}


def cleaning(text:str) -> str:
    """
        Método principal que aplica a limpeza completa dos dados
    """
    cleanedText = str(text).lower()
    cleanedText = padronizaTexto(cleanedText)
    cleanedText = replaceBlanks(cleanedText)
    cleanedText = normalizeText(cleanedText)   
    return ' '.join(palavra.strip() for palavra in cleanedText.split())


def padronizaTexto(text:str) -> str:
    """
        Método responsável por padronizar os valores para algumas variáveis
    """
    return text.replace('ignorada', 'ignorado')


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


def padronizaDiaSemana(text:str) -> str:
    """
     Método responsável por padronizar os dias da semana
    """
    text = text.lower()
    text = text.strip()
    text = text.replace('segunda-feira', 'segunda')
    text = text.replace('terça-feira', 'terca')
    text = text.replace('terça', 'terca')
    text = text.replace('quarta-feira', 'quarta')
    text = text.replace('quinta-feira', 'quinta')
    text = text.replace('sexta-feira', 'sexta')
    text = text.replace('sábado', 'sabado')
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
    text = text.replace('colisao com objeto em movimento', 'colisao com objeto')
    text = text.replace('colisao com objeto estatico', 'colisao com objeto')
    text = text.replace('colisao lateral mesmo sentido', 'colisao lateral')
    text = text.replace('colisao lateral sentido oposto', 'colisao lateral')
    text = text.replace('atropelamento de pessoa', 'atropelamento de pedestre')
    return ' '.join(palavra.strip() for palavra in text.split())


def padronizaNomeBrs(text:str) -> str:
    """
     Método responsável por padronizar os nomes das BRs
    """
    return text.replace('.0', '')


def padronizaUsoSolo(text:str) -> str:
    """
     Método responsável por padronizar as características do local do acidente
    """
    text = text.lower()
    text = text.strip()
    text = text.replace('não', 'rural')
    text = text.replace('sim', 'urbano')
    return text


def padronizaEstadoFisico(text:str) -> str:
    """
     Método responsável por padronizar o estado fisico
    """
    text = text.replace('lesoes graves', 'ferido grave')
    text = text.replace('lesoes leves', 'ferido leve')
    text = text.replace('obito', 'morto')
    return text


def padronizaTipoVeiculo(text:str) -> str:
    """
     Método responsável por padronizar os tipos de veículos
    """
    text = text.lower()
    text = text.strip()
    text = text.replace('micro-onibus', 'microonibus')
    text = text.replace('motocicletas', 'motocicleta')
    text = text.replace('semi-reboque', 'semireboque')
    text = text.replace('carro-de-mao', 'carro de mao')
    return text


def padronizaSexo(text:str) -> str:
    """
     Método responsável por padronizar o sexo biológico
    """
    text = text.lower()
    text = text.strip()
    
    if text == 'f':
        text = 'feminino'
    elif text == 'm':
        text = 'masculino'
    elif text == 'i':
        text = 'ignorado'    
    
    text = text.replace('invalido', 'ignorado')
    text = text.replace('nao informado', 'ignorado')
    return text


def padronizaMunicipios(text:str) -> str:
    """
     Método responsável por padronizar os nomes dos municípios
    """
    return ' '.join(palavra.strip().capitalize() for palavra in text.split())


preprocessingFunctionsMap = {
    'dia_semana' : padronizaDiaSemana,
    'causa_acidente': padronizaCausaAcidente,
    'tipo_acidente': padronizaTipoAcidente,
    'br': padronizaNomeBrs,
    'uso_solo': padronizaUsoSolo,
    'estado_fisico': padronizaEstadoFisico,
    'tipo_veiculo' : padronizaTipoVeiculo,
    'sexo': padronizaSexo,
    'municipio': padronizaMunicipios
}


def mapEstacaoAno(data:date) -> str:
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


def mapRegiaoPais(uf:str) -> str:
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


def mapTiposDeAcidentes(text:str) -> str:
    """
        Método responsável por mapear os tipos de acidentes
    """    
    if text in ['atropelamento de animal', 'atropelamento de pedestre', 'atropelamento de pessoa']:
        return 'atropelamento'
    elif text in ['capotamento', 'tombamento']:
        return 'capotamento/tombamento'
    elif text in ['colisao com bicicleta', 'colisao com objeto', 'colisao frontal', 'colisao lateral', 'colisao transversal', 'colisao traseira']:
        return 'colisão'
    elif text in ['queda de motocicleta / bicicleta / veiculo', 'queda de ocupante de veiculo']:
        return 'queda'
    elif text in ['saida de leito carrocavel', 'saida de pista']:
        return 'saída pista/leito'
    return 'outros'


def mapDiasDaSemana(text:str) -> str:
    """
        Método responsável por mapear os dias da semana em úteis ou final de semana
    """
    return 'final de semana' if text in ['sábado', 'domingo'] else 'dia útil'


def mapTamanhoVeiculos(text:str) -> str:
    """
        Método responsável por mapear o porte dos veículos
    """
    if text in ['automovel', 'caminhonete', 'camioneta', 'utilitario']:
        return 'pequeno porte'
    elif text in ['motocicleta', 'motoneta', 'bicicleta', 'ciclomotor', 'triciclo', 'side-car']:
        return 'motociclista/ciclista'
    elif text in ['outros', 'carro-de-mao', 'carro de mao', 'carroca', 'carroca-charrete', 'charrete', 'quadriciclo']:
        return 'outros'
    return 'grande porte'



feriados_fixos = {
    '01/01': 'ano novo',
    '21/04': 'tiradentes',
    '01/05': 'trabalhador',
    '07/09': 'independencia',
    '12/10': 'padroeira do brasil',
    '02/11': 'finados',
    '15/11': 'proclamação da república',
    '25/12': 'natal'
}
    
feriados_moveis = {   
 '20/02/2007': 'carnaval',
 '01/04/2007': 'sexta santa',
 '07/06/2007': 'corpus christi',
 '05/02/2008': 'carnaval',
 '21/03/2008': 'sexta santa',
 '22/05/2008': 'corpus christi',
 '24/02/2009': 'carnaval',
 '10/04/2009': 'sexta santa',
 '11/06/2009': 'corpus christi',
 '16/02/2010': 'carnaval',
 '02/04/2010': 'sexta santa',
 '03/06/2010': 'corpus christi',
 '08/03/2011': 'carnaval',
 '22/04/2011': 'sexta santa',
 '23/06/2011': 'corpus christi',
 '21/02/2012': 'carnaval',
 '06/04/2012': 'sexta santa',
 '07/06/2012': 'corpus christi',
 '12/02/2013': 'carnaval',
 '29/03/2013': 'sexta santa',
 '30/05/2013': 'corpus christi',
 '04/03/2014': 'carnaval',
 '18/04/2014': 'sexta santa',
 '19/06/2014': 'corpus christi',
 '17/02/2015': 'carnaval',
 '03/04/2015': 'sexta santa',
 '04/06/2015': 'corpus christi',
 '09/02/2016': 'carnaval',
 '25/03/2016': 'sexta santa',
 '26/05/2016': 'corpus christi',
 '28/02/2017': 'carnaval',
 '14/04/2017': 'sexta santa',
 '15/06/2017': 'corpus christi',
 '13/02/2018': 'carnaval',
 '30/03/2018': 'sexta santa',
 '31/05/2018': 'corpus christi',
 '05/03/2019': 'carnaval',
 '19/04/2019': 'sexta santa',
 '20/06/2019': 'corpus christi',
 '25/02/2020': 'carnaval',
 '10/04/2020': 'sexta santa',
 '11/06/2020': 'corpus christi',
 '16/02/2021': 'carnaval',
 '02/04/2021': 'sexta santa',
 '03/06/2021': 'corpus christi'
}


def getFeriadoNacional(data:str) -> str:
    """
        Método responsável por mapear os feriados nacionais
    """
    feriado = getFeriadoNacionalFixo(data)
    if feriado:
        return feriado
    return getFeriadoNacionalMovel(data)
    
    
def getFeriadoNacionalFixo(data:str) -> str:
    """
        Método responsável por mapear os feriados nacionais com datas fixas
    """
    data = data.strftime("%d/%m/%Y")[:5]
    if data in feriados_fixos.keys():
        return feriados_fixos[data]
    

def getFeriadoNacionalMovel(data:str) -> str:
    """
        Método responsável por mapear os feriados nacionais com datas movéis
    """
    data = data.strftime("%d/%m/%Y")
    if data in feriados_moveis.keys():
        return feriados_moveis[data]
    

def mapFeriadoEnaoFeriado(text: str) -> str:
    """
        Método responsável por agrupar dias de feriados e não feriados
    """
    if text != 'sem feriado':
        return 'feriado'
    return text