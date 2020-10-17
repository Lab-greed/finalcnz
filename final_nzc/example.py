'''
name：唤醒音，列表参数
per：发音人选择, 0为普通女声，1为普通男生，
     3为情感合成-度逍遥，4为情感合成-度丫丫，
     默认为普通女声
speed：语速，取值0-9，默认为5中语速
pit：音调，取值0-9，默认为5中语调
vol：音量，取值0-15，默认为5中音量
listen_time：从唤醒开始保持唤醒的时间，默认为5
'''
from family import Family

a = Family(name=['古尔丹'],per=3,speed=4,pit=0,vol=10,listen_time=60)
a.run()