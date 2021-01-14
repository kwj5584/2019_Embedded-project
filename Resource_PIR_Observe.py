import RPi.GPIO as GPIO
from coapthon.resources.resource import Resource
import threading
import logging as logger
import time

trig=2
echo=3
red=21
green=20
blue=16
pir = 7
motor = 17
trash = 10

class ObservableResource(Resource):
    def __init__(self, name="Obs", coap_server=None):
        super(ObservableResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=False)
        
        self.period = 5

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pir, GPIO.IN) #pir센서 연결
        GPIO.setup(motor,GPIO.OUT) # 서보모터 연결
        GPIO.setup(red,GPIO.OUT) # rgc모듈 red 연결
        GPIO.setup(green,GPIO.OUT) # rgb모듈 green 연결
        GPIO.setup(blue,GPIO.OUT) # rgb모듈 blue 연결
        GPIO.setup(trig,GPIO.OUT) # 초음파센서 
        GPIO.setup(echo,GPIO.IN)  # 초음파센서
        self.update(True)
        

    def render_GET(self, request):
        return self

    def render_POST(self, request):
        self.payload = request.payload
        return self

    def render_DELETE(self, request):
        return True


    def update(self, first=False):
        if not self._coap_server.stopped.isSet():
            timer = threading.Timer(self.period, self.update)
            timer.setDaemon(True)
            timer.start()

            if not first and self._coap_server is not None:
                p = GPIO.PWM(motor,50)    
                p.start(0)
                if GPIO.input(pir) == GPIO.HIGH: # pir센서가 움직임을 감지하면
                    print("Detected") 
                    time.sleep(0.5)
                    p.ChangeDutyCycle(2.5) # 서보모터를 90도 돌려줌으로 쓰레기통 열어줌
                    time.sleep(4)
                    p.ChangeDutyCycle(7.5) # 반대방향 90도로 돌려줌으로 쓰레기통 닫아줌
                    time.sleep(0.5)
                else:
                    print("Not Detected")

                GPIO.output(trig,False)
                time.sleep(0.5)
                GPIO.output(trig,True)
                time.sleep(0.01)
                GPIO.output(trig,False)

                while GPIO.input(echo) == 0:
                    start = time.time() # echo에 초음파가 인식이 안될때 시간
                while GPIO.input(echo) == 1:
                    end = time.time() # echo에 초음파가 인식이 될때 시간

                duration = end-start # 수신시간에서 전송시간을 빼서 도달 시간 선정
                distance = duration * 17000 # 음파의 초당 이동속도를 이용하여 거리 계산
                distance = round(distance,2) # 거리의 소수점 2자리에서 반올림
                percent = round(((trash-distance)/trash),2) # 쓰레기통 용량 차있는 만큼 퍼센트 계산
                if distance <= 3:
                    GPIO.output(blue,False)
                    GPIO.output(green,False) 
                    GPIO.output(red,True) # 거리가 3cm 이하일 때 빨간불 출력 나머지 불 꺼줌
                    print("거리 :",distance,"cm")
                    self.payload = str(percent*100) # 페이로드에 percent 변수 대입
                    self._coap_server.notify(self) # 서버에서 payload값을 notify 해줌
                    self.observe_count += 1 # 옵저브 카운트 1증가 

                 elif distance <= 5 :
                     GPIO.output(blue,False)
                     GPIO.output(red,True)
                     GPIO.output(green,True) # 거리가 3cm 이상 5cm 이하일 때 노란불 출력
                     print('거리 : ',distance,'cm')
                     self.payload = str(percent*100)
                     self._coap_server.notify(self)
                     self.observe_count +=1
                else:                   
                    GPIO.output(red,False)
                    GPIO.output(green,False)
                    GPIO.output(blue,True) # 거리가 6cm 이상일 때 파랑불 출력
                    self.payload = str(percent*100)
                    self._coap_server.notify(self)
                    self.observe_count +=1
                    print("거리 : ",distance, "cm")
