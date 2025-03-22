def find_code():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def get_min() :
    min_num = 100
    for i in nums:
        if i + 1 < min_num:
            min_num = i
    return min_num



