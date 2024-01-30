import socket
import threading
from colorama import init, Fore
import time
init(autoreset=True)
PORT = 1234  # Change me
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

print(Fore.RED + "\n\n"+ascii_art1+"\n\n" + ascii_art2+"\n\n"+ "Type kill, to kill host connection\n[*] Starting SkullShell...")

def listen_for_connection():
    #Initilaizes socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', PORT))  # Bind to all available interfaces
        
    except socket.error as e:
        print(e)
        
    print(Fore.GREEN+"[*] Socket Created...")
    
    #Listens for one connection
    server_socket.listen(1)
    
    #Accept connection if found
    print(Fore.GREEN + f"[*] Waiting for a connection on port {PORT}")
    client_socket, client_addr = server_socket.accept()
    print(Fore.GREEN + f"[*] Connection established from {client_addr[0]}:{client_addr[1]}")
    
    #Start thread for recieving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        #Only every one second have input asked
        time.sleep(1)
        user_input = input("#")
        client_socket.send(user_input.encode())

#Recieve packets from shell
def receive_messages(client_socket):
    while True:
        data = client_socket.recv(2048).decode()
        print(Fore.RED +f"{data}")

if __name__ == "__main__":
    connection_thread = threading.Thread(target=listen_for_connection)
    connection_thread.start()
    #Makes sure threads run while alive
    while True:
        pass
