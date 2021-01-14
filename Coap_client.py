from coapthon.client.helperclient import HelperClient
from tkinter import *

host = "192.168.137.225"
port = 5683
path_observe = 'observe'

def tkinterclient(res):
    temp = 0 # 임시변수 temp
    print('쓰레기통 용량 :',res,'%') 
    response = float(res) # 받아온 payload값을 형변환시켜 저장
    window = Tk()
    if temp != response:  # 기존 값 temp와 받아온 쓰레기통 용량값이 같지 않을 때
        if response <0 or response >100: # 용량이 0%보다 작거나 100%보다 크게 나타날 경우
            print("out of length")
            image = PhotoImage(file = "trash default.png") # 비어있는 쓰레기통사진 출력
            label = Label(window, image = image)
            temp = response # 이전 값과 다음에 올 값을 비교하기 위해 temp에 용량값 저장
            window.title("default")
                
        elif response >= 0 and response <= 14: # 용량이 0%이상 14%이하 일 경우
            image = PhotoImage(file = "trash 10%.png") # 쓰레기통 용량이 10%차있는 사진출력
            label = Label(window,image = image)
            temp = response 
            window.title(str(response)+'%')
        elif response <= 34: # 용량이 15%이상 34%이하일 경우
            image = PhotoImage(file = "trash 30%.png") # 쓰레기통 용량이 30% 차있는 사진 출력
            label = Label(window,image = image)
            temp = response 
            window.title(str(response)+'%')
        elif response <= 54: # 용량이 35%이상 54% 이하일 경우
            image = PhotoImage(file = "trash 50%.png")  # 쓰레기통 용량이 50% 차있는 사진 출력
            label = Label(window,image = image)
            temp = response 
            window.title(str(response)+'%')
        elif response <= 74: # 용량이 55%이상 74% 이하일 경우
            image = PhotoImage(file = "trash 70%.png") # 쓰레기통 용량이 70% 차있는 사진 출력
            label = Label(window, image = image)
            temp = response 
            window.title(str(response)+'%')
        else:
            image = PhotoImage(file = "trash 90%.png") 
            label = Label(window, image = image) # 쓰레기통 용량 90% 사진 출력
            temp = response 
            window.title(str(response)+'%')
    else:
        print("Not changed") # temp와 용량값이 그대로일 경우
        image = None
        label = Label(window, image = image) # 아무사진도 표시해 주지 않음
    
    label.pack() # 위 조건문 중 하나의 조건을 만족하면 그 조건의 사진을 pack시킴
    window.update() 
    window.mainloop()
        
def OnReceiptionOfOserve(response):
    print("observe callback")
    res = response.payload  # 서버에서 받아온 쓰레기통 용량값을 res변수에 저장
    tkinterclient(res)  # tkinterclient함수에 res값을 보냄
    
client = HelperClient(server=(host, port))
response = client.get(path_observe)

observe = client.observe(path_observe, callback=OnReceiptionOfOserve)


