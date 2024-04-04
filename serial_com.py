import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    # return commPort
    # return "COM5"
    return "COM6"

if getPort != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    print(ser)

def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    warning = None
    distance = None
    # Gui nhiet do len server
    if splitData[0] == "TEMP":
        client.publish("cam_bien_nhiet_do", splitData[1])
    # Gui do am len server
    if splitData[2] == "HUMI":
        client.publish("cam_bien_do_am", splitData[3])
    # Gui canh bao len server
    if splitData[0] == "WARN":
        warning = splitData[1]
    if splitData[2] == "DIST":
        distance = int(splitData[3])
    warn_send = None
    if warning == "1" and distance < 60:
        data_warning = "CO NGUOI"
    else:
        data_warning = "KHONG CO NGUOI"
    if warn_send != data_warning:
        warn_send = data_warning
        client.publish("canh_bao", warn_send)
    if data_warning == "CO NGUOI":
        client.publish("cam_bien_khoang_cach", str(distance))
    # Gui thong bao tat quat
    if splitData[0] == "ON_FAN":
        client.publish("cong_tac_quat", splitData[1])
    if splitData[0] == "OFF_FAN":
        client.publish("cong_tac_quat", splitData[1])


mess = ""
def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

def writeData(data):
    ser.write(str(data).encode())