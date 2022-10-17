import sys
import base64
import urllib.parse
import requests
import re


def handler(event, context):

    # производим раскодировку информации из анкеты на Tilda
    message = base64.b64decode(event['body']).decode('utf-8')

    # несколько команд print ниже для того, чтобы в логах на YCF
    # увидеть, как выглядит полученная информация после
    # преобразований
    print(message, file=sys.stderr)

    # в данном примере была использована на Tilda
    # стандартная страница-анкета, однако полученные данные
    # потребовали следующих преобразований при
    # доведении до удобного формата
    message_decode = urllib.parse.unquote(message)
    message_decode = urllib.parse.unquote_plus(message_decode)
    msg = str(message_decode)
    print(msg)
    msg_lst = list(re.findall(r'=([^=&]+)&', msg))
    # в итоге информации из анкеты на Tilda преобразована
    # в список
    print(msg_lst)

    # из полученного списка извлекаем имя и email получателя
    name = msg_lst[0]
    s_email = msg_lst[1]
    # в данном примере в анкете также надо было указать людей,
    # которые вдохновляют посетителя сайта - извлекаем эту информацию
    inspiring = msg_lst[2]
    # url согалсно методу отправки писем через Unisender
    url = 'https://api.unisender.com/ru/api/sendEmail?format=json'
    api_key = 'Токен (API ключ) который получили от Unisender'
    sender_email = 'email отправителя'
    sender_name = 'вдохновитель'

    post_info = (
            url + '&api_key=' + api_key + '&email=' + s_email + '&sender_name=' + sender_name +
            '&sender_email=' + sender_email + '&subject=Мыслим позитивно&body=' + name +
            ', люди, которые тебя вдохновляют и восхищают, на самом деле похожи на тебя! Между тобой и '
            + inspiring + ' есть много общего! Подумай, что вас объединяет&list_id=1')

    # собственно отправка письма
    requests.post(post_info)

    return {'statusCode': 200}
