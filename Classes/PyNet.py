#region Classes
class PyNet:

    '''
---------------------------------------------------
        Network tests with a python-class        
---------------------------------------------------
Included functions:
- digtest()
- tping()
---------------------------------------------------
    '''

    pass

    # Constructor   
    def __init__(self) -> None:
        pass
        
    def digtest(self, input):

        '''DigTests with python: digtest(hostname | ip address)'''

        import socket
        import re

        ipv4 = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
        ipv6 = '^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'
        result = dict()

        try: 
            
            if(re.match(ipv4, input)):
                # input is an ipv4 address
                resolved = socket.gethostbyaddr(input)[0]
                result['Function']  = 'digtest'
                result['Input']     = input
                result['Resolved']  = resolved
                result['Succeeded'] = True
            else:
                if(re.match(ipv6, input)):
                    # input is an ipv6 address
                    resolved = socket.gethostbyaddr(input)[0]
                    result['Function']  = 'digtest'
                    result['Input']     = input
                    result['Resolved']  = resolved
                    result['Succeeded'] = True
                    
                else:
                    # input is a hostname
                    resolved = socket.gethostbyname(input)
                    result['Function']  = 'digtest'
                    result['Input']     = input
                    result['Resolved']  = resolved
                    result['Succeeded'] = True

        except: 
            result['Function']  = 'digtest'
            result['Input']     = input
            result['Resolved']  = f'Could not resolve {input}'
            result['Succeeded'] = False

        return result
        
    def tping(self, host, port, timeout):

        '''TcpTests with python: tping(hostname, tcp port, timeout)'''

        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = dict()

        try:
            # tries to connect to the host
            s.connect((host, port))

        except ConnectionRefusedError:
            # if failed to connect
            result['Function']  = 'tping'
            result['Computer']  = host
            result['Port']      = port
            result['Succeeded'] = False
            s.close()

        while True:
            # if connected to host
            result['Function']  = 'tping'
            result['Computer']  = host
            result['Port']      = port
            result['Succeeded'] = True
            s.close()
            return result
#endregion

# Process
import json

# Colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
Y  = '\033[93m' # yellow

# create an instance of PyNet-class and run some functions
print(G+PyNet.__doc__+W)
do = PyNet()

# use some functions of the PyNet-class
collection = ['sbb.ch','crazy.domain.io']
for item in collection:
    print('digtest', item)
    digtest = do.digtest(item)
    if(digtest['Succeeded'] == True):
        tping = do.tping(item, 443, 100) 
        json_object = json.dumps(tping, indent = 4)
        print(json_object)
    else:
        print(Y+'WARNING:' + digtest['Resolved']+W)

