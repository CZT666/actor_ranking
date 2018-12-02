# coding: utf-8
import os
import json

def load_actor_list():
    """
    将演员姓名存入列表
    :return: actor_list
    """
    actor_list = []
    with open("./actor.txt","r") as r:
        lines = r.readlines()
        for line in lines:
            line = line.strip('\n')
            actor_list.append(line)
    # print(actor_list)
    return actor_list

def load_totaloffice_attributes(actor_list):
    """
    计算演员经验值指标
    :param actor_list:
    :return: actor_experience
    """
    actor_experience = {}
    experience = {}
    for name in actor_list:
        filename = "./actor_office/" + name + ".json"
        if os.path.exists(filename):
            with open(filename,"r") as r:
                count = 0
                per_acotr = json.load(r)
                # print(per_acotr)
                for per_movie in per_acotr:
                    office = per_movie['office']
                    if office == 'null':
                        office = 0
                    else:
                        office = int(office.replace("万",""))
                    count += office
                actor_experience[name] = count
    # print(actor_experience)
    max_office,min_office = evaluate(actor_experience)
    for name in actor_experience.keys():
        sorce = normalized(actor_experience[name],max_office,min_office)
        experience[name] = sorce
    print("Empirical indicator: \n")
    print(experience)
    return experience



def load_time_attributes(star,end,actor_list):
    """
    计算时效性指标
    :param star:
    :param end:
    :param actor_list:
    :return:
    """
    # 获取该段时间内设计该演员的新闻数量
    actor_new = {}
    for name in actor_list:
        filename = "./new/" + name + ".txt"
        if os.path.exists(filename):
            count = 0
            with open(filename,"r") as r:
                news = r.readlines()
                for new in news:
                    new = new.strip('\n')
                    year = new.split('\t')[0]
                    num = new.split('\t')[1]
                    if int(year) >= star and int(year) <= end:
                        count += int(num)
                actor_new[name] = count

    # 获取该段时间内演员的票房数量
    actor_office = {}
    for name in  actor_list:
        filename = "./actor_office/" + name + ".json"
        if os.path.exists(filename):
            count = 0
            with open(filename,"r") as r:
                per_actor = json.load(r)
                for per_movie in per_actor:
                    if per_movie['year'] >= star and per_movie['year'] <= end:
                        office = per_movie['office']
                        if office == 'null':
                            office = 0
                        else:
                            office = int(office.replace("万", ""))
                        count += office
                actor_office[name] = count

    # 计算时效性指标
    max_office, min_office = evaluate(actor_office)
    max_new, min_new = evaluate(actor_new)
    time = {}
    for name in actor_list:
        if name in actor_office.keys() and name in actor_new.keys():
            sorce_office = normalized(actor_office[name],max_office,min_office)
            sorce_new = normalized(actor_new[name],max_new,min_new)
            time[name] = sorce_office + sorce_new
    print("Timeliness indicator: \n")
    print(time)
    return time

def load_actieve(actor_list,star,end):
    baidu = {}
    actieve = {}
    with open("./record.txt","r") as r:
        lines = r.readlines()
        for line in lines:
            line = line.strip('\n')
            flag = line.split(' ')[-1]
            names = line.split(' ')[0:-1]
            name = ''
            for i in names:
                name += i
            baidu[name] = flag
    # print(baidu)
    for name in actor_list:
        filename = "./演员活跃度/" + name + '.txt'
        if os.path.exists(filename) and name in baidu.keys():
            with open(filename, "r") as r:
                sorce = 0
                wei = 0
                aware = 0
                bai = 0
                lines = r.readlines()
                for line in lines:
                    line = line.strip('\n')
                    weibo = line.split(',')[0]

                    if weibo == "1":
                        wei = 1
                    awares = line.split(',')[1:]

                    for i in awares:
                        if int(i) >= star and int(i) <= end:
                            aware = 1
                    if baidu[name] == "1":
                        bai = 1
                sorce = (wei + bai + aware) * 0.3
                actieve[name] = sorce
    print("Character indicator: \n")
    print(actieve)
    return actieve



def evaluate(dict):
    Max = max(dict.values())
    Min = min(dict.values())
    return Max,Min

def normalized(value,Max,Min):
    return 0.5/(Max - Min)*(value - Min)

def ranking(actor_list,experience,time,actieve):
    total = {}
    for name in actor_list:
        if name in experience.keys() and name in time.keys() and name in actieve.keys():
            total[name] = experience[name] + time[name] + actieve[name]
    # with open("./actor_ranking_2015-2018.json","w") as w:
    #     json.dump(total,w)
    print(total)
    dict = sorted(total.items(), key=lambda d: d[1], reverse=True)
    for i in dict:
        print(str(i) + '\n')
if __name__ == '__main__':
    actor_list = load_actor_list()
    experience = load_totaloffice_attributes(actor_list)
    time = load_time_attributes(2015,2018,actor_list)
    actieve = load_actieve(actor_list,2011,2015)
    ranking(actor_list,experience,time,actieve)