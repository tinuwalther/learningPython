#region Classes
class pynet:

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
        
    def dig(self, input):

        '''DigTests with python: digtest(hostname | ip address)'''

        import socket
        import re

        function_name = self.dig.__name__
        ipv4 = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
        ipv6 = '^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'
        result = dict()

        try: 
            
            if(re.match(ipv4, input)):
                # input is an ipv4 address
                resolved = socket.gethostbyaddr(input)[0]
                result['Function']  = function_name
                result['Input']     = input
                result['Resolved']  = resolved
                result['Succeeded'] = True
            else:
                if(re.match(ipv6, input)):
                    # input is an ipv6 address
                    resolved = socket.gethostbyaddr(input)[0]
                    result['Function']  = function_name
                    result['Input']     = input
                    result['Resolved']  = resolved
                    result['Succeeded'] = True
                    
                else:
                    # input is a hostname
                    resolved = socket.gethostbyname(input)
                    result['Function']  = function_name
                    result['Input']     = input
                    result['Resolved']  = resolved
                    result['Succeeded'] = True

        except: 
            result['Function']  = function_name
            result['Input']     = input
            result['Resolved']  = f'Could not resolve {input}'
            result['Succeeded'] = False

        return result
        
    def tping(self, host, port, timeout):

        '''TcpTests with python: tping(hostname, tcp port, timeout)'''

        import socket

        function_name = self.tping.__name__
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = dict()

        try:
            # tries to connect to the host
            s.connect((host, port))

        except ConnectionRefusedError:
            # if failed to connect
            result['Function']  = function_name
            result['Computer']  = host
            result['Port']      = port
            result['Succeeded'] = False
            s.close()

        while True:
            # if connected to host
            result['Function']  = function_name
            result['Computer']  = host
            result['Port']      = port
            result['Succeeded'] = True
            s.close()
            return result
#endregion
