
from aip import AipSpeech
from pydub import AudioSegment
import json
import requests
import pyaudio
import wave
import numpy as np
import webbrowser
import time
import pygame
import os
import urllib

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
IN1 = 6
IN2 = 13 

IN3 = 19  
IN4 = 26

IN5 = 21
IN6 = 20

def init():
    GPIO.setup(IN1, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN3, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN5, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN6, GPIO.OUT,initial=GPIO.LOW)

init()    
    
def up():
    
    GPIO.output(IN4, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    
    
def down():
   
    GPIO.output(IN3, GPIO.HIGH)  
    GPIO.output(IN4,GPIO.LOW)


def pull():
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    
def push():
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN1,GPIO.LOW)
    
def a_down():
    GPIO.output(IN5,GPIO.HIGH)
    GPIO.output(IN6,GPIO.LOW)
    
def a_up():
    GPIO.output(IN6,GPIO.HIGH)
    GPIO.output(IN5,GPIO.LOW)
    
    
    
def get_up():
    push()
    time.sleep(2.4)
    init()
    time.sleep(0.2)
    up()
    time.sleep(6)
    push()
    time.sleep(0.6)

    
def lay_down():
    down()    
    time.sleep(5.488)
    init()
    time.sleep(0.2)
    #pull()
    #time.sleep(3.6)
    pull()
    time.sleep(5.3)
    
def arm_down():
    a_down()
    time.sleep(6)
    
def arm_up():
    a_up()
    time.sleep(6)
   


class Family():
    def __init__(self,name=['JOJO'],per=1,speed=5,pit=5,vol=5,listen_time=5):
        self.name = name
        self.speed = speed
        self.per = per
        self.pit = pit
        self.vol = vol
        self.listen_time = listen_time
        self.man_wav = 'audio/man.wav'
        self.machine_mp3 = 'audio/machine.mp3'
        self.machine_wav = 'audio/machine.wav'#仅用于pygame的临时加载
        self.start_wav = 'audio/start.wav'
        self.sleep_wav = 'audio/sleep.wav'
        self.stop_wav = 'audio/stop.wav'
        self.questen = ''
        self.client = None
        self.listen = True
        self.work = not True
        self.stop = not True
        self.starttime = 0
        self.nowtime = 0
        self.test = True
    """下载音乐"""
    def DownloadMusic(self,name):
        res1 = requests.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1\
                            &cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w='+name)
        jm1 = json.loads(res1.text.strip('callback()[]'))['data']['song']['list'][0]

        mids=jm1['media_mid']
        songmids=jm1['songmid']
        songnames=jm1['songname']
        singers=jm1['singer'][0]['name']

        res2 = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&\
        jsonpCallback=MusicJsonCallback&cid=205361747&songmid='+songmids+'&filename=C400'+mids+'.m4a&guid=6612300644')
        jm2 = json.loads(res2.text)
        vkey = jm2['data']['items'][0]['vkey']
        srcs='http://dl.stream.qqmusic.qq.com/C400'+mids+'.m4a?vkey='+vkey+'&guid=6612300644&uin=0&fromtag=66'
        try:
            urllib.request.urlretrieve(srcs,'music/'+songnames+'.mp3')#.m4a
            return 1
        except:
            return 0
    """初始化pygame模块"""
    def pygame_init(self):
        pygame.mixer.init()
    """播放音频"""
    def play(self,file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
    """pygame是否正忙"""
    def get_busy(self):
        return pygame.mixer.music.get_busy()
    """以二进制格式打开文件"""
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    """播放WAV"""
    def play_wav(self,file):
        """参数：wav文件绝对路径"""
        """阻塞，直到播放完成"""
        CHUNK = 1024
        wf = wave.open(file, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    """sizhi机器人"""
    def answer(self):
        """参数：中文问题；返回：JSON格式回答信息"""
        data = {
            "appid": "c91e8ed614ad2bd412ff3b2542b4888e",
            "userid": "JOJO",
            "spoken": self.questen
        }
        resp = requests.post("https://api.ownthink.com/bot", data )
        resp.encoding ='utf-8'
        result = resp.json()
        print(result)
        answer = result['data']['info']['text']
        return answer

    def wav_to_pcm(self,wav_file):
        pcm_file = "%s.pcm" % (wav_file.split(".")[0])

        # 就是此前我们在cmd窗口中输入命令,这里面就是在让Python帮我们在cmd中执行命令
        os.system("ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s" % (wav_file, pcm_file))
        return pcm_file


    """MP3文件转WAV文件"""
    def mp3_to_wav(self,mp3,wav):
        """参数：MP3文件绝对路径，WAV文件绝对路径"""
        """输出：WAV文件"""
        sound = AudioSegment.from_mp3(mp3)  #加载mp3文件
        sound.export(wav, format="wav")  #转换格式
    
    """有声音就录音"""
    def recodeing(self,t):
        """参数：录音阈值，正常1500"""
        """阻塞，直到录音完成"""
        CHUNK = 1024 #每次读取的音频流长度
        FORMAT = pyaudio.paInt16  #语音文件的格式
        CHANNELS = 2  #声道数，百度语音识别要求单声道
        RATE = 16000  #采样率， 8000 或者 16000， 推荐 16000 采用率
        wait = True  #录音等待
        LEVEL = 1000
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        print("start recording")
        while wait:
            data = stream.read(CHUNK)
            audio_data = np.fromstring(data, dtype=np.short)
            temp = np.max(audio_data)
            if temp >t:
                wait = not True
                print("end recording")
        large_count = np.sum( audio_data > LEVEL )
        while large_count>10:
            frames.append(data) 
            data = stream.read(CHUNK)
            audio_data = np.fromstring(data, dtype=np.short)
            large_count = np.sum( audio_data > LEVEL )
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(self.man_wav, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print('录音完毕...')
        self.wav_to_pcm(self.man_wav)


    def login(self):
        APP_ID = '18308446'
        API_KEY = 'ZCU9ew1M7cxIVnMn7FOSjlAz'
        SECRET_KEY = 'XUXRO2Pa6oF3Cp0XN4IqrnBzGrhvhcqF'
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    def awake(self):
        while self.listen:
            self.recodeing(1500)
            pcm_file = self.wav_to_pcm(self.man_wav)
            print("开始上传音频数据...")
            result_text = self.client.asr(self.get_file_content(pcm_file), 'pcm',16000, {'dev_pid': '1537', })
            print('语音识别结果：')
            print(result_text)
            if 'result' in result_text.keys():
                info = result_text["result"][0][:-1]
                if self.test:
                    print('唤醒音识别结果：'+info)
                if info in self.name:
                    self.listen = not True
                    self.work = True
                    self.stop = not True
                    break
            else:
                if self.test:
                    print('识别失败')
    def working(self):
        self.play_wav(self.start_wav)
        self.starttime = time.time()
        while self.work:
            CHUNK = 1024  #每次读取的音频流长度
            FORMAT = pyaudio.paInt16  #语音文件的格式
            CHANNELS = 2  #声道数，百度语音识别要求单声道
            RATE = 16000  #采样率， 8000 或者 16000， 推荐 16000 采用率
            wait = True  #录音等待
            LEVEL = 1000
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,\
                            frames_per_buffer=CHUNK)
            frames = []
            print("start recording")
            while wait:
                data = stream.read(CHUNK)
                audio_data = np.fromstring(data, dtype=np.short)
                temp = np.max(audio_data)
                if temp >1500:
                    wait = not True
                    break
                self.nowtime = time.time()
                if self.nowtime-self.starttime>self.listen_time:
                    self.listen = True
                    self.work = not True
                    self.stop = not True
                    self.play_wav(self.stop_wav)
                    break
            if self.work:
                large_count = np.sum( audio_data > LEVEL )
                while large_count>8:
                    frames.append(data) 
                    data = stream.read(CHUNK)
                    audio_data = np.fromstring(data, dtype=np.short)
                    large_count = np.sum( audio_data > LEVEL )
                stream.stop_stream()
                stream.close()
                p.terminate()
                wf = wave.open(self.man_wav, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()

                pcm_file = self.wav_to_pcm(self.man_wav)

                #录音结束
                print("开始上传音频数据...")
                result_text = self.client.asr(self.get_file_content(pcm_file), 'pcm',16000, {'dev_pid': '1537',})
                if 'result' in result_text.keys():
                    self.questen = result_text["result"][0][:-1]
                    if self.test:
                        print('语音输入识别结果：'+self.questen)
                    if self.questen in ['机电了','点了','机电','电缆','电了','现在几点了']:#对时间的处理，‘几点了’的识别结果很无奈
                        now_time = time.localtime()
                        tm_hour = now_time.tm_hour
                        if tm_hour >= 12:
                            tm_hour -= 12
                        tm_min = now_time.tm_min
                        tm_sec = now_time.tm_sec
                        turing_answer_text = str(tm_hour)+'点'+str(tm_min)+'分'+str(tm_sec)+'秒'
                    elif self.questen in ['今天几号','今天多少号']:#对日期的处理
                        now_time = time.localtime()
                        tm_mon = now_time.tm_mon
                        tm_mday = now_time.tm_mday
                        turing_answer_text = str(tm_mon)+'月'+str(tm_mday)+'号'
                    elif self.questen in ['今天星期几']:#对星期的处理
                        now_time = time.localtime()
                        tm_wday = now_time.tm_wday+1
                        if tm_wday <= 6:
                            turing_answer_text = '星期'+str(tm_wday)
                        else:
                            turing_answer_text = '星期日'
                            
                    elif self.questen in ['扶我起来','服务我起来','如果起来','起来']:
                        turing_answer_text = '好的'
                        
                        time.sleep(0.5)
                        init()
                        get_up()
                        
                        
                    elif self.questen in ['躺下']:
                        turing_answer_text = '好的'
                        time.sleep(0.5)
                        init()
                        lay_down()
                        init()
                        
                    
                    elif self.questen in ['手臂放下']:
                        turing_answer_text = '好的'
                        
                        time.sleep(0.5)
                        init()
                        arm_down()
                        init()
                        
                    elif self.questen in ['手臂抬起','手臂抬起业']:
                        turing_answer_text = '好的'
                        
                        time.sleep(0.5)
                        init()
                        arm_up()
                        init()
                        
                    elif self.questen in self.name:
                        turing_answer_text = '嗯！这儿了'
                        
                    elif '播放' in self.questen:#对唱歌的处理
                        try:
                            self.play('music/'+self.questen[2:]+'.mp3')
                            continue
                        except:
                            turing_answer_text = '咱还没有下载这首歌呢'
                    elif '下载' in self.questen:#对唱歌的处理
                        self.play_wav(self.start_wav)
                        down_ok_or_not = self.DownloadMusic(self.questen[2:])
                        if down_ok_or_not:
                            turing_answer_text = '好了'
                        else:
                            turing_answer_text = '不好意思，我没有权限'
                    elif self.questen in ['说话快一点']:#对语速的处理
                        if self.speed < 9:
                            self.speed += 1
                        turing_answer_text = '好的，快了'
                    elif self.questen in ['说话慢一点']:#对语速的处理
                        if self.speed > 0:
                            self.speed -= 1
                        turing_answer_text = '好的，慢了'
                    elif self.questen in ['语调高一点','调高一点','音调高一点']:#对语调的处理
                        if self.pit < 9:
                            self.pit += 1
                        turing_answer_text = '好的，高了'
                    elif self.questen in ['语调低一点','调低一点','音调低一点']:#对语调的处理
                        if self.pit > 0:
                            self.pit -= 1
                        turing_answer_text = '好的，低了'
                    elif self.questen in ['打开即可供房','打开即刻供房','打开即刻供方']:#加入对网页的处理
                        webbrowser.open('http://www.geek-workshop.com/forum.php')
                        turing_answer_text = '好的'
                    elif self.questen in ['打开电影天堂']:#加入对网页的处理
                        webbrowser.open('http://www.dytt8.net/')
                        turing_answer_text = '好的'
                    elif self.questen in ['打开博客','打开CSDN博客','CSDN博客']:#加入对网页的处理
                        webbrowser.open('https://blog.csdn.net/Lingdongtianxia')
                        turing_answer_text = '好的'
                    elif '搜索' in self.questen:#加入对网页的处理
                        webbrowser.open('https://www.baidu.com/baidu?ie=utf-8&wd='+self.questen[2:])
                        turing_answer_text = '好的'
                    elif self.questen in ['打开CSDN下载','CSDN下载']:#加入对网页的处理
                        webbrowser.open('https://download.csdn.net/my')
                        turing_answer_text = '好的'
                    elif self.questen in ['打开木可','打开中国大学慕课']:#加入对网页的处理
                        webbrowser.open('https://www.icourse163.org/')
                        turing_answer_text = '好的'
                    elif self.questen in ['打开我的课程','我要当学霸','我要做学霸','我要学习']:#加入对网页的处理
                        webbrowser.open('https://www.icourse163.org/home.htm?userId=1019112339#/home/course')
                        turing_answer_text = '好的'
                    elif self.questen in ['打开截图','截图','打开截屏','截屏']:#加入对软件的处理
                        os.system(r"start D:\快速截图\FSCapture_单文件.exe")
                        turing_answer_text = '好的'
                    elif self.questen in ['打开微信','微信']:#加入对软件的处理
                        os.system(r"start D:\微信\WeChat\WeChat.exe")
                        turing_answer_text = '好的'
                    elif self.questen in ['打开邮箱','邮箱']:#加入对软件的处理
                        webbrowser.open("https://mail.qq.com")
                        turing_answer_text = '好的'
                    elif self.questen in ['打开迅雷','迅雷']:#加入对软件的处理
                        os.system(r"start D:\迅雷\Program\Thunder.exe")
                        turing_answer_text = '好的'
                    else:
                        turing_answer_text = self.answer()
                        #turing_answer_text = turing_answer['text']
                        # if 'url' in turing_answer.keys():
                        #     webbrowser.open(turing_answer['url'])
                        # if 'list' in turing_answer.keys():
                        #     webbrowser.open(turing_answer['list'][0]['detailurl'])
                        #     webbrowser.open(turing_answer['list'][1]['detailurl'])
                    if self.test:
                        print('机器人的回答：'+turing_answer_text)
                    result  = self.client.synthesis(str(turing_answer_text), 'zh', 1,{'vol':self.vol,'spd':self.speed,'per':self.per,'pit':self.pit})
                    if not isinstance(result, dict):  
                        with open(self.machine_mp3, 'wb') as f:
                            f.write(result)
                    #self.mp3_to_wav(self.machine_mp3, self.machine_wav)
                    self.play(self.machine_mp3)
                    while self.get_busy():
                        time.sleep(0.2)
                    pygame.mixer.music.load(self.machine_wav)#使用pygame加载一个别的音频，释放掉self.machine_mp3，不然权限出错
                    time.sleep(0.2)#防止扬声器对麦克风的干扰
                    self.starttime = time.time()
    def run(self):
        self.pygame_init()
        try:
            self.login()
            print("登录成功...")
        except:
            print("登录失败...")
        while True:
            self.awake()
            print("录音完毕...")
            self.working()

