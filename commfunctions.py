from mysocket import Mysocket
from telling import Telling
from tellingproduct import TellingProduct

SERVER='192.168.0.22'
PORT=7893

def getTellingList():
    tellinglist=[]
    #create the socket
    sock = Mysocket()
    sock.connect(SERVER,PORT)
    sock.mysend('i')
    sock.mysend(';')
    # read the response
    bit=''
    while(bit!=';'):
        bit = sock.myreceive(1)
    nrtellings=''
    bit=sock.myreceive(1)
    while(bit!=';'):
        nrtellings=nrtellings+bit
        bit = sock.myreceive(1)
    nrtellings=eval(nrtellings) # convert to number

    # read the tellings
    for i in range(0,nrtellings):
        current=Telling()
        current.id=''
        current.datechange=''
        current.datecreation=''
        bit = sock.myreceive(1)
        while (bit!='|'):
            current.id=current.id+bit
            bit=sock.myreceive(1)
        bit=sock.myreceive(1)
        while (bit!='|'):
            current.datecreation=current.datecreation+bit
            bit=sock.myreceive(1)
        bit=sock.myreceive(1)
        while (bit!=';'):
            current.datechange=current.datechange+bit
            bit=sock.myreceive(1)

        tellinglist.append(current)
        # eat the \r \n
        bit=sock.myreceive(2)
    return tellinglist


def getMissedProducts(tellingid):
    # get the missed products for the telling
    productlist=[]
    #create the socket
    sock = Mysocket()
    sock.connect(SERVER,PORT)
    sock.mysend('m')
    sock.mysend(';')
    for c in tellingid:
        sock.mysend(c)
    sock.mysend(';')
    # read the response
    bit=''
    while(bit!=';'):
        bit = sock.myreceive(1)
    nrproducts=''
    bit=sock.myreceive(1)
    while(bit!=';'):
        nrproducts=nrproducts+bit
        bit = sock.myreceive(1)
    nrproducts=eval(nrproducts) # convert to number
    # read the products
    for i in range(0,nrproducts):
        current=TellingProduct()
        current.id=''
        current.quantity_original=''
        current.quantity_new=''
        current.datechange=''
        bit = sock.myreceive(1)
        while (bit!='|'):
            current.id=current.id+bit
            bit=sock.myreceive(1)
            
        bit=sock.myreceive(1)
        while (bit!='|'):
            current.name=current.name+bit
            bit=sock.myreceive(1)

        bit=sock.myreceive(1)
        while (bit!=';'):
            current.quantity_original=current.quantity_original+bit
            bit=sock.myreceive(1)
            
        productlist.append(current)
        # eat the \r \n
        bit=sock.myreceive(2)
    return productlist

def markProductsAsCounted(tellingid,products):
    #create the socket
    sock = Mysocket()
    sock.connect(SERVER,PORT)
    sock.mysend('a')
    sock.mysend(';')
    for c in tellingid:
        sock.mysend(c)
    sock.mysend(';')
    #send the products
    for prodid, q in products.iteritems():
        sock.mysend(prodid)
        sock.mysend('|')
        sock.mysend(q)
        sock.mysend('|')
    sock.mysend(';')
    
    # read the response
    bit=''
    while(bit!=';'):
        bit = sock.myreceive(1)
    succeeded=''
    bit=sock.myreceive(1)
    while(bit!=';'):
        succeeded=succeeded+bit
        bit = sock.myreceive(1)
    succeeded=eval(succeeded) # convert to number
    return succeeded

	
def getTelling(tellingid):
    # get the products for the telling
    productlist=[]
    #create the socket
    sock = Mysocket()
    sock.connect(SERVER,PORT)
    sock.mysend('k')
    sock.mysend(';')
    for c in tellingid:
        sock.mysend(c)
    sock.mysend(';')
    # read the response
    bit=''
    while(bit!=';'):
        bit = sock.myreceive(1)
    nrproducts=''
    bit=sock.myreceive(1)
    while(bit!=';'):
        nrproducts=nrproducts+bit
        bit = sock.myreceive(1)
    nrproducts=eval(nrproducts) # convert to number

    # read the products
    for i in range(0,nrproducts):
        current=TellingProduct()
        current.id=''
        current.quantity_original=''
        current.quantity_new=''
        current.datechange=''
        bit = sock.myreceive(1)
        while (bit!='|'):
            current.id=current.id+bit
            bit=sock.myreceive(1)
            
        bit=sock.myreceive(1)
        while (bit!='|'):
            current.name=current.name+bit
            bit=sock.myreceive(1)

            
        bit=sock.myreceive(1)
        while (bit!='|'):
            current.quantity_original=current.quantity_original+bit
            bit=sock.myreceive(1)
            
        bit=sock.myreceive(1)
        while (bit!='|'):
            current.quantity_new=current.quantity_new+bit
            bit=sock.myreceive(1)
            
        bit=sock.myreceive(1)
        while (bit!=';'):
            current.datechange=current.datechange+bit
            bit=sock.myreceive(1)

        productlist.append(current)
        # eat the \r \n
        bit=sock.myreceive(2)
    return productlist
