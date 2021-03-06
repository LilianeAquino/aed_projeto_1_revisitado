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
    'ceu claro': 'tempo bom',
    'sol': 'tempo bom',
    'nublado': 'nublado',
    'nevoeiro/neblina': 'nublado',
    'chuva': 'tempo ruim',
    'garoa/chuvisco': 'tempo ruim',
    'granizo': 'tempo ruim',
    'neve': 'tempo ruim',
    'vento': 'tempo ruim'
}


comportamental = [
 'desobediencia a sinalizacao',
 'desobediencia as normas de transito pelo condutor',
 'desobediencia as normas de transito pelo pedestre',
 'dormindo',
 'falta de atencao',
 'ingestao de alcool ou substancias psicoativas',
 'nao guardar distancia de seguranca',
 'ultrapassagem indevida',
 'velocidade incompativel'
 'trafegar com motocicleta (ou similar) entre as faixas',
 'transitar na calcada',
 'transitar na contramao',
 'transitar no acostamento',
 'acessar a via sem observar a presenca dos outros veiculos',
 'ausencia de reacao do condutor',
 'condutor deixou de manter distancia do veiculo da frente',
 'condutor desrespeitou a iluminacao vermelha do semaforo',
 'condutor usando celular',
 'conversao proibida',
 'deixar de acionar o farol da motocicleta (ou similar)',
 'desrespeitar a preferencia no cruzamento',
 'entrada inopinada do pedestre',
 'estacionar ou parar em local proibido',
 'frear bruscamente',
 'farois desregulados',
 'mal subito',
 'manobra de mudanca de faixa',
 'modificacao proibida',
 'pedestre andava na pista',
 'pedestre cruzava a pista fora da faixa',
 'reacao tardia ou ineficiente do condutor',
 'redutor de velocidade em desacordo',
 'retorno proibido',
 'participar de racha',
]


ambiental = [
 'acesso irregular',
 'acostamento em desnivel',
 'acumulo de agua sobre o pavimento',
 'acumulo de areia ou detritos sobre o pavimento',
 'acumulo de oleo sobre o pavimento',
 'afundamento ou ondulacao no pavimento',
 'agressao externa',
 'animais na pista',
 'area urbana sem a presenca de local apropriado para a travessia de pedestres',
 'ausencia de sinalizacao',
 'chuva',
 'curva acentuada',
 'declive acentuado',
 'demais falhas na via',
 'demais fenomenos da natureza', 
 'desvio temporario',
 'faixas de transito com largura insuficiente',
 'falta de acostamento',
 'falta de elemento de contencao que evite a saida do leito carrocavel',
 'fenomenos da natureza',
 'fumaca',
 'iluminacao deficiente',
 'neblina',
 'objeto estatico sobre o leito carrocavel',
 'obras na pista',
 'obstrucao na via',
 'pista em desnivel',
 'pista esburacada',
 'pista escorregadia',
 'restricao de visibilidade',
 'semaforo com defeito',
 'sinalizacao da via insuficiente ou inadequada',
 'sinalizacao encoberta',
 'sinalizacao mal posicionada',
 'sistema de drenagem ineficiente'    
]


veicular = [
 'avarias e/ou desgaste excessivo no pneu',
 'carga excessiva e/ou mal acondicionada',
 'defeito mecanico no veiculo',
 'defeito na via',
 'deficiencia do sistema de iluminacao/sinalizacao',
 'deficiencia ou nao acionamento do sistema de iluminacao/sinalizacao do veiculo',
 'demais falhas mecanicas ou eletricas',
 'problema com o freio',
 'problema na suspensao',
]


def cleaning(text:str) -> str:
    """
        M??todo principal que aplica a limpeza completa dos dados
    """
    cleanedText = str(text).lower()
    cleanedText = padronizaTexto(cleanedText)
    cleanedText = replaceBlanks(cleanedText)
    cleanedText = normalizeText(cleanedText)   
    return ' '.join(palavra.strip() for palavra in cleanedText.split())


def padronizaTexto(text:str) -> str:
    """
        M??todo respons??vel por padronizar os valores para algumas vari??veis
    """
    return text.replace('ignorada', 'ignorado')


def replaceBlanks(text:str) -> str:
    """
        Realiza as remo????o de marca????es de quebra de linha, 'carriage return' e espa??amento dos textos
    """
    text = text.replace(r'\r',' ')
    text = text.replace(r'\n', ' ')
    text = text.replace(r'\s', ' ')
    text = text.strip()
    return text


def normalizeText(text:str) -> str:
    """
        Realiza a normaliza????o dos textos
    """
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def padronizaDiaSemana(text:str) -> str:
    """
     M??todo respons??vel por padronizar os dias da semana
    """
    text = text.lower()
    text = text.strip()
    text = text.replace('segunda-feira', 'segunda')
    text = text.replace('ter??a-feira', 'terca')
    text = text.replace('ter??a', 'terca')
    text = text.replace('quarta-feira', 'quarta')
    text = text.replace('quinta-feira', 'quinta')
    text = text.replace('sexta-feira', 'sexta')
    text = text.replace('s??bado', 'sabado')
    return text


def padronizaCausaAcidente(text:str) -> str:
    """
     M??todo respons??vel por padronizar  as causas dos acidentes
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
     M??todo respons??vel por padronizar os tipos de acidentes
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
     M??todo respons??vel por padronizar os nomes das BRs
    """
    return text.replace('.0', '')


def padronizaUsoSolo(text:str) -> str:
    """
     M??todo respons??vel por padronizar as caracter??sticas do local do acidente
    """
    text = text.lower()
    text = text.strip()
    text = text.replace('n??o', 'rural')
    text = text.replace('sim', 'urbano')
    return text


def padronizaEstadoFisico(text:str) -> str:
    """
     M??todo respons??vel por padronizar o estado fisico
    """
    text = text.replace('lesoes graves', 'ferido grave')
    text = text.replace('lesoes leves', 'ferido leve')
    text = text.replace('obito', 'morto')
    return text


def padronizaTipoVeiculo(text:str) -> str:
    """
     M??todo respons??vel por padronizar os tipos de ve??culos
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
     M??todo respons??vel por padronizar o sexo biol??gico
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
     M??todo respons??vel por padronizar os nomes dos munic??pios
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
         M??todo respons??vel por mapear as esta????es do ano
    """
   
    dia = data.day
    mes = data.month
       
    if (mes == 12 and dia >= 21) or (mes < 3) or (mes == 3 and dia <= 20):
        return 'ver??o'
    if (mes == 3 and dia >= 21) or (mes > 3 and mes < 6) or (mes == 6 and dia <= 20):
        return 'outono'      
    if (mes == 6 and dia >= 21) or (mes > 6 and mes < 9) or (mes == 9 and dia <= 22):
        return 'inverno'
    return 'primavera'


def mapRegiaoPais(uf:str) -> str:
    """
     M??todo respos??vel por mapear as regi??es do Brasil
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


def mapTiposDeAcidentes(tipo_acidente:str) -> str:
    """
        M??todo respons??vel por mapear os tipos de acidentes
    """    
    if tipo_acidente in ['atropelamento de pedestre', 'atropelamento de pessoa']:
        return 'atropelamento de pessoas'
    elif tipo_acidente in ['capotamento', 'tombamento']:
        return 'capotamento/tombamento'
    elif tipo_acidente in ['queda de motocicleta / bicicleta / veiculo', 'queda de ocupante de veiculo']:
        return 'queda de ve??culo'
    elif tipo_acidente in ['saida de leito carrocavel', 'saida de pista']:
        return 'sa??da da pista'
    elif tipo_acidente in ['colisao com objeto', 'engavetamento', 'danos eventuais', 'incendio', 'derramamento de carga', 'eventos atipicos']:
        return 'outros'
    return tipo_acidente


def mapCausaAcidentes(text:str) -> str:
    """
        M??todo respons??vel por mapear as causas dos acidentes com base nas caracter??sticas
    """    
    if text in comportamental:
        return 'aspectos relacionados ao comportamento do condutor'
    elif text in ambiental:
        return 'aspectos relacionados a via ou ambiente'
    elif text in veicular:
        return 'aspectos relacionados ao ve??culo'
    return 'outros aspectos n??o identificados'


def mapDiasDaSemana(text:str) -> str:
    """
        M??todo respons??vel por mapear os dias da semana em ??teis ou final de semana
    """
    return 'final de semana' if text in ['sabado', 'domingo'] else 'dia ??til'


def mapTipoEnvolvido(veiculo:str, envolvido: str) -> str:
    """
        M??todo respons??vel por agrupar tipos de envolvidos por tipo de ve??culo
    """
    return 'ciclista' if veiculo in ['bicicleta', 'triciclo'] else envolvido


def mapTamanhoVeiculos(text:str) -> str:
    """
        M??todo respons??vel por mapear o porte dos ve??culos
    """
    if text in ['automovel', 'caminhonete', 'camioneta', 'utilitario']:
        return 'pequeno porte'
    elif text in ['motocicleta', 'motoneta', 'bicicleta', 'ciclomotor', 'triciclo', 'side-car']:
        return 'motociclista/ciclista'
    elif text in ['outros', 'carro-de-mao', 'carro de mao', 'carroca', 'carroca-charrete', 'charrete', 'quadriciclo']:
        return 'outros'
    return 'grande porte'


def mapCondicaoEnvolvimento(envolvido:str, tipo_veiculo: str) -> str:
    """
        M??todo respons??vel por mapear a forma como se deu a participa????o da v??tima no acidente
    """
    is_condutor_or_passageiro = ['condutor', 'passageiro']
    
    if envolvido in is_condutor_or_passageiro and tipo_veiculo in ['automovel', 'utilitario']:
        return 'ocupante de autom??veis'  
    if envolvido in is_condutor_or_passageiro and tipo_veiculo in ['caminhonete', 'camioneta']:
        return 'ocupante de caminhonete/camioneta'    
    elif envolvido in is_condutor_or_passageiro and tipo_veiculo in ['motocicleta', 'ciclomotor', 'triciclo', 'side-car']:
        return 'ocupante de motocicleta'
    elif envolvido in is_condutor_or_passageiro and tipo_veiculo == 'motoneta':
        return 'ocupante de motoneta'
    elif envolvido in is_condutor_or_passageiro and tipo_veiculo in ['caminhao-trator', 'caminhao', 'semireboque', 'caminhao-tanque', 'reboque']:
        return 'ocupante de caminh??o'
    elif envolvido in is_condutor_or_passageiro and tipo_veiculo in ['microonibus', 'onibus']:
        return 'ocupante de micro-??nibus/??nibus'    
    elif envolvido == 'pedestre':
        return 'pedestre'
    elif envolvido == 'ciclista':
        return 'ciclista'
    return 'outros'


def mapTracadoVia(tracado: str) -> str:
    """
        M??todo respons??vel por agrupar os tra??ados da via com poucos dados
    """
    return tracado if tracado in ['reta', 'curva', 'cruzamento'] else 'outros'


def mapHorarioAcidentes(hora:str) -> str:
    """
        M??todo respons??vel por mapear o hor??rio das ocorr??ncias
    """    
    if hora > '06:00:00' and hora <= '12:00:00':
        return 'manh??'
    elif hora > '12:00:00' and hora <= '18:00:00':
        return 'tarde'
    elif hora >= '00:00:00' and hora <= '06:00:00':
        return 'madrugada'
    elif hora > '18:00:00' and  hora <= '23:59:59':
        return 'noite'


feriados_fixos = {
    '01/01': 'ano novo',
    '21/04': 'tiradentes',
    '01/05': 'trabalhador',
    '07/09': 'independencia',
    '12/10': 'padroeira do brasil',
    '02/11': 'finados',
    '15/11': 'proclama????o da rep??blica',
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
        M??todo respons??vel por mapear os feriados nacionais
    """
    feriado = getFeriadoNacionalFixo(data)
    if feriado:
        return feriado
    return getFeriadoNacionalMovel(data)
    
    
def getFeriadoNacionalFixo(data:str) -> str:
    """
        M??todo respons??vel por mapear os feriados nacionais com datas fixas
    """
    data = data.strftime("%d/%m/%Y")[:5]
    if data in feriados_fixos.keys():
        return feriados_fixos[data]
    

def getFeriadoNacionalMovel(data:str) -> str:
    """
        M??todo respons??vel por mapear os feriados nacionais com datas mov??is
    """
    data = data.strftime("%d/%m/%Y")
    if data in feriados_moveis.keys():
        return feriados_moveis[data]
    

def mapFeriadoEnaoFeriado(text: str) -> str:
    """
        M??todo respons??vel por agrupar dias de feriados e n??o feriados
    """
    if text != 'sem feriado':
        return 'feriado'
    return text


def identifierConductorsOver100OrUnder10YearsOld(tipo_envolvido:str, idade: str) -> str:
    """
        M??todo respons??vel por identificar poss??veis outliers
    """
    if tipo_envolvido == 'condutor' and idade > 100 or idade < 10:
        return 'outlier'
    return 'n??o ?? outlier'