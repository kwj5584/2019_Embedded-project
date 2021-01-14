from coapthon.server.coap import CoAP
import Resource_PIR_Observe
import RPi.GPIO as GPIO

red=21
green=20
blue=16
motor = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor,GPIO.OUT)
p = GPIO.PWM(motor,50)

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('observe/', Resource_PIR_Observe.ObservableResource(coap_server=self))
    

def main():
    server = CoAPServer("192.168.137.225", 5683) # 서버연결
    try:
        server.listen(10)
    except KeyboardInterrupt: # ctrl+c를 누를 경우
        GPIO.output(red,False) 
        GPIO.output(green,False)
        GPIO.output(blue,False) # led모듈 모든 색을 꺼줌
        p.stop() # 서보모터 중단시킴
        GPIO.cleanup()

        print("Server Shutdown")
        server.close()
        print("Exiting...")

if __name__ == '__main__':
    main()
