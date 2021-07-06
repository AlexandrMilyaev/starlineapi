#!/usr/bin/python3
import logging
import argparse
import time
import datetime as dt
import requests
import xlsxwriter as xls
import pytz

from get_device_data import get_device_data

__author__ = "Milyaev Aleksandr <milyaev.alexandr@aac-kharkov.com>"
__date__ = "29.06.2021"


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", dest="date", help="final report time", default="")
    parser.add_argument("-c", "--hours", dest="hours", help="report hours period", default="24")
    parser.add_argument("-m", "--min", dest="min", help="report minutes period", default="00")
    parser.add_argument("-s", "--sec", dest="sec", help="report seconds period", default="00")
    parser.add_argument("-i", "--imei", dest="imei", help="imei object for report", default="", required=True)
    parser.add_argument("-t", "--slid_token", dest="slidToken", help="StarLineID Token", default="", required=True)
    parser.add_argument("-p", "--path", dest="path", help="path", default="")
    parser.add_argument("-n", "--file_name", dest="file_name", help="Name of file")
    args = parser.parse_args()
    # logging.info('appId: {}, appSecret: {}, login: {}, password: {}'.format(args.appId, args.appSecret, args.login,
                                                                            # args.password))
    return args


args = get_args()
if args.file_name is None:
    name_file = f'{args.imei}'
else:
    name_file = f'{args.file_name}'
if args.path == '':
    workbook = xls.Workbook(f'./{name_file}.xlsx')
else:
    workbook = xls.Workbook(f'{args.path}/{name_file}.xlsx')
statistic = workbook.add_worksheet('Статистика')
trips = workbook.add_worksheet('Поездки')
ins = workbook.add_worksheet('Нарушения')
format_time = workbook.add_format()
format_time.set_num_format('hh:mm:ss')
format_km = workbook.add_format()
format_km.set_num_format('#,##0"км"')
format_km_h = workbook.add_format()
format_km_h.set_num_format('#,##0"км/ч"')

tz = pytz.timezone("Europe/Kiev")
tz_offset = tz.utcoffset(dt.datetime.now()).total_seconds()


def get_name_device(device_id, slenet_token):
    data = get_device_data(device_id=device_id, slnet_token=slenet_token)
    return data['data']['alias']


def proc_statistic(name_object: str, time_begin: str, time_end: str,
                   track: dict):
    '''
    Функция возвращает подготовленный словарь значений для записи в лист "статистика"
    :param name_object: имя обьекта
    :param time_begin: начало интервала
    :param time_end: конец интервала
    :param track: можно получить с помощью функции .device_ways
    :param ins_data: можно получить с помощью функции .device_ins_data
    :return:
    '''

    def moving_time():
        mt = track['moving_time']
        return dt.timedelta(seconds=mt)

    def waiting_time():
        wt = track['waiting_time']

        return dt.timedelta(seconds=wt)

    def mileage():
        m = track['mileage']
        return track['mileage'] / 1000

    def max_speed():
        speed = list()
        try:
            for data in track['way']:
                if data['type'] == 'TRACK':
                    for nodes in data['nodes']:
                        speed.append(nodes['s'])
            return max(speed)
        except Exception as e:
            print(e.args)
            return 0

    def avr_speed():
        try:
            avr = track['mileage'] / track['moving_time']
            avr *= 3.6
            return avr
        except Exception as e:
            print(e.args)
            return 0

    statistic_cells = {
        'Обьект': name_object,
        'Начало периода': time_begin,
        'Конец периода': time_end,
        'Время в движении': moving_time(),
        'Время стоянки': waiting_time(),
        'Пройденный путь': mileage(),
        'Максимальная скорость': max_speed(),
        'Средняя скорость': avr_speed()
    }
    counter = 0
    for key, value in statistic_cells.items():

        statistic.write(counter, 0, key)
        if key == 'Время в движении' or key == 'Время стоянки':
            statistic.write(counter, 1, value, format_time)
        elif key == 'Пройденный путь':
            statistic.write(counter, 1, value, format_km)
        elif key == 'Максимальная скорость' or key == 'Средняя скорость':
            statistic.write(counter, 1, value, format_km_h)
        elif key == 'Обьект' or key == 'Начало периода' or key == 'Конец периода':
            statistic.write(counter, 1, value)
        counter += 1


def proc_trip(track: dict):
    trips_columns = ('Номер поездки', 'Длительность стоянки', 'Начало поездки', 'Начальное положение',
                     'Конец поездки', 'Конечное положение', 'Пройденый путь', 'Длительность поездки',
                     'Средняя скорость', 'Максимальная скорость', 'Количество нарушений')
    for columns in range(len(trips_columns)):
        trips.write(0, columns, trips_columns[columns])

    try:
        line = 1
        for weys in track['way']:
            if weys['type'] == 'STOP':
                wt = dt.timedelta(seconds=weys['waiting_time'])
                trips.write(line, trips_columns.index('Длительность стоянки'), wt, format_time)
            elif weys['type'] == 'TRACK':
                trips.write(line, trips_columns.index('Номер поездки'), line)
                mt = dt.timedelta(seconds=weys['moving_time'])
                trips.write(line, trips_columns.index('Длительность поездки'), mt, format_time)
                m = weys['mileage'] / 1000
                trips.write(line, trips_columns.index('Пройденый путь'), m, format_km)
                start = f'{weys["nodes"][0]["x"]}, {weys["nodes"][0]["y"]}'
                trips.write(line, trips_columns.index('Начальное положение'), start)
                end = f'{weys["nodes"][-1]["x"]}, {weys["nodes"][-1]["y"]}'
                trips.write(line, trips_columns.index('Конечное положение'), end)
                ts = weys["nodes"][0]["t"]
                ts = dt.datetime.utcfromtimestamp(ts + tz_offset).strftime('%Y-%m-%d %H:%M:%S')
                trips.write(line, trips_columns.index('Начало поездки'), ts)
                te = weys["nodes"][-1]["t"]
                te = dt.datetime.utcfromtimestamp(te + tz_offset).strftime('%Y-%m-%d %H:%M:%S')
                trips.write(line, trips_columns.index('Конец поездки'), te)
                avr_speed = weys['mileage'] / weys['moving_time'] * 3.6
                trips.write(line, trips_columns.index('Средняя скорость'), avr_speed, format_km_h)
                max_speed = list()
                for nodes in weys['nodes']:
                    max_speed.append(nodes['s'])
                trips.write(line, trips_columns.index('Максимальная скорость'), max(max_speed), format_km_h)
                count_ins = 0

                for ins_ in weys['nodes']:
                    try:
                        data = ins_['ins_data']
                        count_ins += 1
                    except:
                        pass
                trips.write(line, trips_columns.index('Количество нарушений'), count_ins)
                line += 1
    except Exception as e:
        print(e.args)
        print('Error')


def proc_ins(ins_data: dict):
    ins_columns = ('№', 'Тип нарушения', 'Время нарушения', 'Координаты нарушения',
                   'Максимальное ускорение', 'Среднее ускорение')
    ins_type = ('Резкое ускорение', 'Резкое торможение', 'Резкий поворот направо',
                'Резкий поворот налево', 'Резкий подьем', 'Резкое снижение')
    for columns in range(len(ins_columns)):
        ins.write(0, columns, ins_columns[columns])
    line = 1
    for ins_ in ins_data['way']:
        if ins_['type'] == 'TRACK':
            for nodes in ins_['nodes']:

                try:
                    data = nodes['ins_data']

                    ins.write(line, ins_columns.index('№'), line)
                    it = ins_type[data['side']]

                    ins.write(line, ins_columns.index('Тип нарушения'), it)
                    ts = nodes['t']

                    ts = dt.datetime.utcfromtimestamp(ts + tz_offset).strftime('%Y-%m-%d %H:%M:%S')
                    ins.write(line, ins_columns.index('Время нарушения'), ts)
                    coord = f'{nodes["x"]}, {nodes["y"]}'
                    ins.write(line, ins_columns.index('Координаты нарушения'), coord)
                    max_acc = data['max'] / 256
                    ins.write(line, ins_columns.index('Максимальное ускорение'), max_acc)
                    avg_acc = data['avg'] / 256
                    ins.write(line, ins_columns.index('Среднее ускорение'), avg_acc)

                    line += 1
                except:
                    pass


def device_ways(slnet_token, devise_id: int, begin_track: int, end_track: int, **kwargs) -> dict:
    '''
    :param self:
    :param devise_id: идентификатор устройства
    :param begin_track: unix-время начала запрашиваемого трека
    :param end_track: unix-время конца запрашиваемого трека
    :return: возвращаем масив точек
    '''

    url = "https://prod-mobapp.starline.ru/json/v1/device/{}/ways".format(devise_id)
    # logging.info('execute request: {}'.format(url))
    cookies = "slnet={}".format(slnet_token)
    data = {"begin": begin_track, "end": end_track}
    data.update(kwargs)

    r = requests.post(url, headers={"Cookie": cookies}, json=data)
    response = r.json()
    r.close()
    # logging.info('payload : {}'.format(payload))
    # logging.info('response info: {}'.format(r))
    # logging.info('response data: {}'.format(response))
    return response


def create_report(slidToken, date, hours, min, sec, imei):

    try:
        time_end_int = int(date)
    except:
        time_end_int = int(time.time())
    time_begin_int = int(sec) + int(min) * 60 + int(hours) * 3600
    time_begin_int = time_end_int - time_begin_int
    track = device_ways(slidToken, int(imei), time_begin_int, time_end_int, has_properties=True)
    time_end_str = dt.datetime.utcfromtimestamp(time_end_int + tz_offset).strftime('%Y-%m-%d %H:%M:%S')
    time_begin_str = dt.datetime.utcfromtimestamp(time_begin_int + tz_offset).strftime('%Y-%m-%d %H:%M:%S')
    name_device = get_name_device(device_id=imei, slenet_token=slidToken)
    proc_statistic(name_device, time_begin_str, time_end_str, track)
    proc_trip(track)
    proc_ins(track)

    workbook.close()

def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    create_report(slidToken=args.slidToken,
                  date=args.date,
                  hours=args.hours,
                  min=args.min,
                  sec=args.sec,
                  imei=args.imei)


if __name__ == "__main__":
    try:
        main()
        print('Ok')
    except Exception as e:
        logging.error(e)
