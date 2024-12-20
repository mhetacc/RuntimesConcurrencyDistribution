import xmlrpc.client
import time

# used to test if th_looping_serverPOC.py can respond to 
# requests while its looping timer runs and calls the callback (it can)
with xmlrpc.client.ServerProxy('http://localhost:8080', allow_none=True) as server:
    i = 0
    while True:
        time.sleep(1)
        print(server.just_return(i))
        i+=1