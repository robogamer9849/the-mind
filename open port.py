

what = input("1.server\n2.client\n")

if(what == '1'):
    from server import *
    start_server()
elif(what == '2'):
    from client import *
    start_client(input("Enter your code: "))
