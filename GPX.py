import paramiko
import ipaddress
import pexpect
import netmiko
import time
import csv
import getpass

VOIP_ip = [str(ip) for ip in ipaddress.IPv4Network('10.0.16.0/22')]
<<<<<<< HEAD

user = getpass.getpass(prompt='Input username: ')
password = getpass.getpass(prompt='Input password: ')

=======

user = 'admin'
password = getpass.getpass(prompt='password:')
>>>>>>> b2acf142c9c30259231e077259a00bada23c58ae

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
                look_for_keys=False,
                allow_agent=False)
            with client.invoke_shell() as ssh:

                ssh.send('status\n')
                time.sleep(2)
                result = ssh.recv(1000).decode('ascii')
                index = result.find("IP")
                IP =result[index + 14: index + 25]
                index = result.find("Model:")
                MODEL = result[index +7: index + 16]
                index = result.find("Prog")
                FW = result[index +8: index + 17]
                print( "IP: " + IP.rstrip() +" Model: " + MODEL.rstrip() + " FW: " + FW.rstrip())
                info = " Model: " + MODEL.rstrip() + " FW: " + FW.rstrip()
                firm["IP: " + IP.rstrip()]=info

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
                telnet.close()
                index = result.find("IP")
                IP = result[index + 14: index + 25]
                index = result.find("Model:")
                MODEL = result[index +7: index + 16]
                index = result.find("Prog")
                FW = result[index +8: index + 17]
                info = " Model: " + MODEL.rstrip() + " FW: " + FW.rstrip()
                firm["IP: " + IP.rstrip()]=info
        except:
            pass


checkpass_by_SSH()
checkpass_by_telnet()
reboot_by_SSH()
reboot_by_telnet()
check_firm_by_SSH()
check_firm_by_telnet()

print('IP Phones with new pass:', new_pass)
print('IP Phones that was rebooted:', rebooted_phones)
print('Firmware list:',firm)


firm_file = open("firmware.csv", "w")

writer = csv.writer(firm_file)
for key, value in firm.items():
    writer.writerow([key, value])

firm_file.close()
