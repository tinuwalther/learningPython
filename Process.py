# Process
import sys
sys.path.append('D:\DevOps\github.com\learningPython\Modules')
import PyNetTools
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
print(G+ PyNetTools.PyNet.__doc__ +W)
do = PyNetTools.PyNet()

# use some functions of the PyNet-class
collection = ['sbb.ch','crazy.domain.io']
for item in collection:
    print('digtest', item)
    digtest = do.dig(item)
    print(digtest)
    if(digtest['Succeeded'] == True):
        tping = do.tping(digtest['Resolved'], 443, 100) 
        print(G+ "TCP Port Test: " + digtest['Input'] + " -> " + digtest['Resolved']  + " -> " + str(tping['Succeeded']) +W)
        json_object = json.dumps(tping, indent = 4)
        print(json_object)
    else:
        print(Y+ "TCP Port Test: " + digtest['Resolved'] +W)
