import socket

# function to test connection to port 5555
def test_connection(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # timeout after 1 second
        
        result = sock.connect_ex((ip, 5555))
        
        if result == 0:
            return True # port is open
        else:
            return False # port is closed
    except:
        return False # an error occurred

# read the ip's from a txt file
with open('ips.txt', 'r') as f:
    ips = f.readlines()

# test the connection to each ip
live_ips = []
for ip in ips:
    ip = ip.strip() # remove newline character
    
    print(f'Testing connection to {ip}...')
    if test_connection(ip):
        print(f'{ip} is live!')
        live_ips.append(ip)
    else:
        print(f'{ip} is down!')

# write live ips to a new file
with open('live_ips.txt', 'w') as f:
    for ip in live_ips:
        f.write(ip + '\n')
    
print('\nLive IP addresses:')
for ip in live_ips:
    print(ip)

print('\nAll done!')
