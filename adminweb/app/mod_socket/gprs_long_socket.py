from concurrent import futures as cf
import time,threading,schedule,socket,asyncio
from app import client_socket,client_id,log
from app.mod_protocalchannel.service import *


p_channels_list = select_by_clientAndIsactive(client_id,'Y')


def process_socket_server(**name):
    channel = name['channel']

    servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #关闭端口后立即释放
    print(f'================',channel.ipaddress,'--',channel.port)
    servsock.bind((channel.ipaddress, int(channel.port)))
    servsock.listen(2)
    servsock.settimeout(6)
    with cf.ThreadPoolExecutor(1) as e:
        try:
            # while True:,not while means just connecting once.
            # while True:

            new_sock, address = servsock.accept()
            print('连接上了---------------', channel.port, new_sock)
            # e.submit(get_connected_client, new_sock, address)
            _sock = {}
            _sock['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            _sock['status'] = True
            _sock['sock'] = new_sock
            _sock['channel'] = channel
            client_socket['gprs-socket' + str(channel.port)] = _sock
            print('put in the global var is ==================', client_socket)

        except KeyboardInterrupt:
            pass
        except socket.timeout:
            print(f'port=---serversocket timeout',channel.port, socket.timeout)
            _sock = {}
            _sock['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            _sock['status'] = False
            _sock['sock'] = None
            _sock['channel'] = channel
            client_socket['gprs-socket' + str(channel.port)] = _sock
            # servsock.shutdown()
            # wait_connect()
        except socket.error:
            _sock = {}
            _sock['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            _sock['status'] = False
            _sock['sock'] = None
            _sock['channel'] = channel
            client_socket['gprs-socket' + str(channel.port)] = _sock
            print('serversocket error', socket.error)
            # servsock.close()
        except Exception as ee:
            print('excetion occured', channel.port, ee)
        finally:
            # servsock.close()
            print('in the finally================')



async def process_long_gprs(channel):
    try:
        t = threading.Thread(target=process_socket_server,
                             kwargs={'channel': channel})

        t.start()
        time.sleep(0.1)
    except Exception as e:
        print('in process_long_gprs,',e)


async def main_long_gprs_task():
    for p in p_channels_list:
        if p.connettype == 'gprs' or p.connettype == 'gprs-l':
            await asyncio.gather(
                process_long_gprs(p))


def schedule_long_gprs_task():
    #系统启动的时候启动一次就可以，如果想定期启动，就放到while True里
    asyncio.run(main_long_gprs_task())

async def check_socket_status():

    for k,v in client_socket.items():
        if v["sock"] and not v["sock"]._closed:
            print(f'key={k},status={not v["sock"]._closed},保持连接状态....')
        else:
            print(f'socket {k},连接失败，，sock={v["sock"]}')
            log.error(f'socket {k},连接失败 ,时间={time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))}')
            #启动一个线程重新链接
            try:
                t = threading.Thread(target=process_socket_server,
                                     kwargs={'channel': v["channel"]})

                t.start()
            except Exception as e:
                log.error(f'{k},重新连接失败 ,错误={e},时间={time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))}')

    print('get socket status -----------------------------')

async def socket_status_task():
    await asyncio.gather(
        check_socket_status())

def schedule_socket_status():
    while 1:
        asyncio.run(socket_status_task())
        time.sleep(10)#这个时间要大于重新连接的timeout时间，否则容易堵塞

if '__main__' == __name__:
    pass
    # main()
    # run_gprs_connect()