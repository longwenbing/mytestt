from handle_message import handle_mes
from save_data import data2mysql


def response(flow):
    if 'api/DealerShows/hyxq'in flow.request.url:
       mes=flow.response.text
       info = handle_mes(mes)
       data2mysql(info)
