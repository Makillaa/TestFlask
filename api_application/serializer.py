from api_application.models import ResultsModel


def response_serializer(result: ResultsModel):
    response = []
    for res in result:
        result_dict = {
            'id': res.id,
            'type': res.type,
            'operator': res.operator,
            'datetime': res.datetime,
            'result': res.result,
        }
        response.append(result_dict)
    return response
