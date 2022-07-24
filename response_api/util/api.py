
import sys
import time


def time_second():
    return time.time()


def time_count(_time):
    return round(time_second() - _time, 10)


def exc_info():
    type_, value, tb = sys.exc_info()
    return type_, value


def get_dict(output: list) -> list:
    temp_list = []
    for item in output:
        score, spoofing, message = _get_item(item)
        temp_list.append({
            "codigoIdentificadorSolicitacao": item.token_service,
            "codigoIdentificadorSistemaConsumidor": item.client_identifier,
            "codigoEstadoRetorno": item.response_status,
            "textoMensagemRetorno": message,
            "listaIdentificacaoFraude": [{
                "textoIdentificadorFotografiaFraude": str(spoofing),
                "valorProbabilidadeFraude": score
            }]
        })
    return temp_list


def _get_item(item):
    score, spoofing, message = 0, "None", str(item.response_service)
    if "is_spoofed" in item.response_service:
        score = item.response_service["trust"]
        spoofing = item.response_service["is_spoofed"]
        message = "SUCCESS"
    return score, spoofing, message
