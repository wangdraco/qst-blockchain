import requests,schedule,time,json

#r = requests.get('http://139.129.200.70:5000/device/dust/zthr-dust-data')

#print(r.json()['PM25'])

def run_scheduled_task():
    print('in auto dust--------------')
    schedule.every(10).seconds.do(run_auto_task)

    while 1:
        schedule.run_pending()
        time.sleep(5)


def run_auto_task():
    pm_confg = json.load(open('pm.json', 'r', encoding='utf-8'))
    pm_max = pm_confg['max']
    pm_min = pm_confg['min']

    r = requests.get('http://139.129.200.70:5000/device/dust/zthr-dust-data')

    pm25_realtime = int(float(r.json()['PM25']))
    pm10_realtiem = int(float(r.json()['PM10']))

    print('pm_max:{},min:{},25realtime:{}'.format(pm_max,pm_min,pm25_realtime))
    if pm25_realtime > pm_max: #start auto mechanism
        print('begin start auto dustelimination')
        #requests.post('http://139.129.200.70:5000/post/dm/9170/on') #1号门北侧围栏
        #requests.post('http://139.129.200.70:5000/post/dm/9171/on')  # 1号门西侧围栏
        #requests.post('http://139.129.200.70:5000/post/dm/9163/on')  # 3号门东侧围栏
        #requests.post('http://139.129.200.70:5000/post/dm/9167/on')  # 中间围栏
    elif pm25_realtime < pm_max-pm_min: #stop auto mechanism
        print('begin stop')
        #requests.post('http://139.129.200.70:5000/post/dm/9170/off')  # 1号门北侧围栏
        # requests.post('http://139.129.200.70:5000/post/dm/9171/off')  # 1号门西侧围栏
        # requests.post('http://139.129.200.70:5000/post/dm/9163/off')  # 3号门东侧围栏
        # requests.post('http://139.129.200.70:5000/post/dm/9167/off')  # 中间围栏




# def run_schedule():
#     schedule.every(10).seconds.do(run_auto_task)
#     while 1:
#         schedule.run_pending()
#         time.sleep(2)

#run_schedule()
#run_scheduled_task()