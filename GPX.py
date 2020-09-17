import paramiko
import ipaddress
import pexpect
import netmiko
import time
import csv

#VOIP_ip = [str(ip) for ip in ipaddress.IPv4Network('10.0.16.0/22')]
VOIP_ip = ['10.0.16.2', '10.0.16.29']
user = 'admin'
password = 'admin0'

new_pass = []
rebooted_phones = []
firm = {}
def checkpass_by_SSH():
    for ip in VOIP_ip:
            try:
                print('Connection to device {}'.format(ip))
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                client.connect(
                    hostname=ip,
                    port='22',
                    username=user,
                    password=password,
                    look_for_keys=False,
                    allow_agent=False)
                with client.invoke_shell() as ssh:

                    ssh.send('help\n')
                    time.sleep(0.5)
                    result = ssh.recv(100).decode('ascii')
                    #print(result)

                new_pass.append(ip)
            except:
                pass


def checkpass_by_telnet():
    for ip in VOIP_ip:
        try:
            print('Connection to device {}'.format(ip))
            with pexpect.spawn('telnet {}'.format( ip)) as telnet:

                telnet.expect('Password:')
                telnet.sendline(password)

                telnet.expect('[>]')
                telnet.sendline('help')
                telnet.expect('[>]')
                result = telnet.before.decode('ascii')
                #print(result)

                telnet.close()
                new_pass.append(ip)
        except:
            pass

def reboot_by_SSH():
    for ip in VOIP_ip:
        try:
            print('Connection to device {}'.format(ip))
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(
                hostname=ip,
                port='22',
                username=user,
                password=password,
                look_for_keys=False,
                allow_agent=False)
            with client.invoke_shell() as ssh:

                ssh.send('reboot\n')
                time.sleep(2)
                result = ssh.recv(100).decode('ascii')
                time.sleep(2)
                #print(result)

                rebooted_phones.append(ip)
        except:
            pass

def reboot_by_telnet():
    for ip in VOIP_ip:
        try:
            print('Connection to device {}'.format(ip))
            with pexpect.spawn('telnet {}'.format( ip)) as telnet:

                telnet.expect('Password:')
                telnet.sendline(password)

                telnet.expect('[>]')
                telnet.sendline('reboot')
                telnet.expect('[...]')
                result = telnet.before.decode('ascii')
                #print(result)
                time.sleep(5)
                telnet.close()
                rebooted_phones.append(ip)
        except:
            pass


def check_firm_by_SSH():
    for ip in VOIP_ip:
        try:
            print('Connection to device {} by ssh'.format(ip))
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(
                hostname=ip,
                port='22',
                username=user,
                password=password,
#                timeout='1',
 #               banner_timeout='5',
#                auth_timeout='5',
                look_for_keys=False,
                allow_agent=False)
            with client.invoke_shell() as ssh:

                ssh.send('status\n')
                time.sleep(2)
                result = ssh.recv(1000).decode('ascii')
                index = result.find("IP")
                #print(index)
                IP = result[index + 14: index + 25]
                #print(IP)
                index = result.find("Prog")
                #print(index)
                FW = result[index +8: index + 17]
                print(IP.rstrip() +" fw " + FW.rstrip())
                #firm.append(result)
                firm[IP.rstrip()]="fw " + FW.rstrip()

        except:
            pass

def check_firm_by_telnet():
    for ip in VOIP_ip:
        try:
            print('Connection to device {} by telnet'.format(ip))
            with pexpect.spawn('telnet {}'.format( ip)) as telnet:

                telnet.expect('Password:')
                telnet.sendline(password)

                telnet.expect('[>]')
                telnet.sendline('status')
                telnet.expect('[>]')
                result = telnet.before.decode('ascii')
                #print(result)
                #time.sleep(1)
                telnet.close()
                index = result.find("IP")
                IP = result[index + 14: index + 25]
                #print(IP)
                index = result.find("Prog")
                FW = result[index + 8: index + 17]
                #print(IP + FW)
                print(IP.rstrip() +" fw " + FW.rstrip())
                firm[IP.rstrip()]="fw " + FW.rstrip()
                #rebooted_phones.append(ip)
        except:
            pass


checkpass_by_SSH()
checkpass_by_telnet()
check_firm_by_SSH()
check_firm_by_telnet()
reboot_by_SSH()
reboot_by_telnet()

print('IP Phones with new pass:', new_pass)
print('IP Phones that was rebooted:', rebooted_phones)
#print(firm)


firm_file = open("firmware.csv", "w")

writer = csv.writer(firm_file)
for key, value in firm.items():
    writer.writerow([key, value])

firm_file.close()