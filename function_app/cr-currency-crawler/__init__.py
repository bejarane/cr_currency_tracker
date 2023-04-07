import datetime
import logging
import requests
import uuid
import json
from bs4 import BeautifulSoup

import azure.functions as func


def main(mytimer: func.TimerRequest, dataoutput: func.Out[str]) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    ##Get ASPX page
    url = 'https://gee.bccr.fi.cr/indicadoreseconomicos/Cuadros/frmConsultaTCVentanilla.aspx'
    response = requests.get(url)
    logging.info(response.status_code)

    ##Parsing HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {"id": "Table2"})
    rows = table.find_all('tr')
    rows = rows[3:39]
    
    contador = 0

    data = []

    for row in rows:
        _date = row.find_all('td')[5].text
        _date = _date.replace('\xa0\xa0\xa0\xa0',' ') ##remove chars
        _date = _date.replace('.','') ##remove a.m. and p.m. periods
        _date = datetime.datetime.strptime(_date, "%d/%m/%Y %I:%M %p")
        _bank = row.find_all('td')[1].text
        _asset = "USD"
        _valbuyCRC = float(row.find_all('td')[2].text.replace(',','.'))
        _valsellCRC = float(row.find_all('td')[3].text.replace(',','.'))

        key = str(uuid.uuid4())
        ##logging.info(key)
        
        dataPoint = {
            "RowKey": key,
            "date": str(_date.date()),
            "bank": _bank,
            "asset": _asset,
            "valbuyCRC": _valbuyCRC,
            "valsellCRC": _valsellCRC
        }

        data.append(dataPoint)

        ##logging.info(str(_date.time()) +' '+str(contador))
        contador += 1

        ##logging.info(row.find_all('tr'))
    for point in data:
        logging.info(point)
        ##dataoutput.set(json.dumps(point))  
    
    dataoutput.set(json.dumps(data))
    logging.info(data)
