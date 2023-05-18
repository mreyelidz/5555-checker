import socket
import subprocess

def test_connection(ip):
    """Test connection to port 5555"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1) # timeout after 1 second
            result = sock.connect_ex((ip, 5555))
            return result == 0 # port is open
    except:
        return False # an error occurred

def check_adb_connection(ip):
    """Check adb connection to device"""
    try:
        output = subprocess.check_output(f'adb connect {ip}:5555', shell=True, stderr=subprocess.STDOUT)
        if b'unable to connect' in output:
            return False # unable to connect to device
        elif b'connected' in output:
            return True # connected to device
        else:
            return False # unknown response
    except subprocess.CalledProcessError as e:
        print(f'Error: {e.output.decode("utf-8").strip()}')
        return False
    except:
        print(f'Error: Unable to check ADB connection for {ip}.')
        return False

def test_ips(file_name):
    """Test connections to all IP addresses in the file"""
    live_ips = []
    with open(file_name, 'r') as f:
        ips = f.readlines()

    for ip in ips:
        ip = ip.strip() # remove newline character
        print(f'Testing connection to {ip}...')
        if test_connection(ip):
            print(f'{ip} is live!')
            print(f'Checking ADB connection to {ip}...')
            if check_adb_connection(ip):
                print(f'Success: Connected to {ip} via ADB.')
                live_ips.append(ip)
            else:
                print(f'Fail: Unable to connect to {ip} via ADB.')
        else:
            print(f'{ip} is down!')
    
    return live_ips

def write_ips(file_name, ips):
    """Write a list of IPs to a file"""
    with open(file_name, 'w') as f:
        for ip in ips:
            f.write(ip + '\n')

def main():
    """Main entry point of the script"""
    file_name = 'ips.txt'
    live_ip_file_name = 'live_ips.txt'

    live_ips = test_ips(file_name)
    write_ips(live_ip_file_name, live_ips)
    
    print('\nLive IP addresses:')
    for ip in live_ips:
        print(ip)

    print('\nDone!')

if __name__ == '__main__':
    main()
