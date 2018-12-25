import threading
import socket

class Tello:
    ANY_ADDR = '0.0.0.0'

    DEVICE_COMMAND_ADDR = '192.168.10.1'
    DEVICE_COMMAND_SEND_PORT = 8889
    DEVICE_COMMAND_RECV_PORT = 9000

    DEVICE_STATE_RECV_PORT = 8890

    DEVICE_VIDEO_RECV_PORT = 9000

    def __init__(self):
        self.deviceCommandSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.deviceCommandSocket.bind((Tello.ANY_ADDR, Tello.DEVICE_COMMAND_RECV_PORT))

        self.deviceStateSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.deviceStateSocket.bind((Tello.ANY_ADDR, Tello.DEVICE_STATE_RECV_PORT))

        self.__recvThreadQuit = False
        self.__recvThread = threading.Thread(target=self.__recv)
        self.__recvThread.start()

        self.__stateThreadQuit = False
        self.__stateThread = threading.Thread(target=self.__state)
        self.__stateThread.start()

    def __del__(self):
        self.deviceCommandSocket.close()

    def __recv(self):
        while not self.__recvThreadQuit:
            data, addr = self.deviceCommandSocket.recvfrom(128)
            if len(data) > 0:
                print("Last command received '%s' from %s" % (data, addr))
            else:
                print("Status received from %s" % addr)
        print("Done receiving")

    def __state(self):
        while not self.__stateThreadQuit:
            data, addr = self.deviceStateSocket.recvfrom(512)
            if len(data) > 0:
                print("From %s:" % addr[0])
                print("    %s" % data)
            else:
                print("Status received from %s" % addr)
        print("Done state")

    def testCmd(self):
        self.deviceCommandSocket.sendto('command', (Tello.DEVICE_COMMAND_ADDR, Tello.DEVICE_COMMAND_SEND_PORT))

    def release(self):
        print("Thread joining...")

        self.__recvThreadQuit = True
        self.__recvThread.join()

        self.__stateThreadQuit = True
        self.__stateThread.join()

        print("Thread joined")

if __name__ == "__main__":
    tello = Tello()
    tello.testCmd()
    tello.release()
