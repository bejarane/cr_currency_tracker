import logging
import json
import azure.functions as func


def main(req: func.HttpRequest, datainput) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    message = json.loads(datainput)

    return func.HttpResponse(f"{datainput}")
