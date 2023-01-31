
import pdfplumber
import re
from dateutil import parser
import connectdb
import DataAccess
import Transaction_DetailsTO as DetailsTO
import Transaction_MasterTO as MasterTO

def Extract_items(text,*trans_details):
    items=[]
    items_def=re.compile(r'^\d{9} [A-Z].*')  
    ''' ^ starting line
    d{9}- 9 digits
    followed by a space
    followed by uppercase a to z
    then anything '''
     
    for line in text.split('\n'):
        if items_def.match(line):
            itemnum,*iteminfo =line.split()
            totalamount=iteminfo.pop()
            discountvalue=iteminfo.pop()
            netamount=iteminfo.pop()
            Qtymeasure =iteminfo.pop()
            quantity=iteminfo.pop()
            unitprice=iteminfo.pop()
            description =" ".join (iteminfo)
           
            #item_details = list(trans_details)
            #item_details.extend([itemnum,description,' ',unitprice,quantity,Qtymeasure,netamount,discountvalue,totalamount])   
            #trans_det= TRANSACTION_DETAILS(itemnum,description,'',unitprice,quantity,Qtymeasure,netamount,discountvalue,totalamount)
            trans_detTO=DetailsTO.Transaction_DetailsTO(   
                item_code=itemnum,
                item_name=description,
                item_categoty='',
                item_unit_price=unitprice,
                item_quantity=quantity,
                item_quantity_measure=Qtymeasure,
                item_net_amount=netamount,
                item_discount_value=discountvalue,
                item_total_amount=totalamount
             )
            #items.append(tuple(item_details )) 
            items.append(trans_detTO) 
           
    return items

def extract_invoice_no(text):
    invoiceno_m=re.compile(r'Invoice No')  
    for line in text.split('\n'):
        if invoiceno_m.match(line):
            invoiceno= line.split(':')[1]
    return invoiceno
def extract_invoice_date(text):
    for line in text.split('\n'):
        if re.search( r'Invoice Date',line):
            invoicedate= line.split('Invoice Date:')[1]
    return invoicedate
def extract_vendor_email(text):
    for line in text.split('\n'):
        if re.search( r'Email',line):
            Email= line.split(':')[1]
    return Email

def extract_Amount(text):
    for line in text.split('\n'):
        if re.search( r'Amount in Words',line):
            AmountinWords= line.split(':')[1]
        if re.search( r'Total :',line):
            Amount= line.split(':')[1]
    return Amount,AmountinWords

def extract_address(text):
    for index, line in enumerate(text.split('\n')):
         if re.search( r'Store',line):
            address = text.split('\n')[index+1]
    return address

def extract_vendor_name(text):
    return text.split('\n')[0]
    
def get_random_record():
    return connectdb.get_random_record()

   
def Extract_bb_items(text,word,*trans_details):
    items=[]
    items_def=re.compile(word)  
    ''' ^ starting line
    d{9}- 9 digits
    followed by a space
    followed by uppercase a to z
    then anything '''
    itemnum=None 
    for line in text.split('\n'):
        if items_def.match(line):
            #print(str.strip(line))
            iteminfo =line.split('Rs.')
            #print(iteminfo,'---->',len(iteminfo))
            if len(iteminfo)>2:
                itemnum,*itemdesc=iteminfo[0].split(' ')
                description= " ".join(itemdesc)
                #print(itemnum,'---->',description)
                unitprice=str.strip(iteminfo[1]).split(' ')[0]
                #print('unitprice---->',unitprice)
                qty=str.strip(iteminfo[1]).split(' ')
                if len(qty)==4:
                    quantity =qty[-2].strip('()')
                    Qtymeasure=qty[-1].strip('()')
                    #print('quantity---->',quantity)
                    #print('Qtymeasure---->',Qtymeasure)
                if len(qty)==2:
                    quantity = qty[-1]
                    Qtymeasure='Pkt/Cnt'
                    #print('quantity---->',quantity)
                    #print('Qtymeasure---->',Qtymeasure)
                totalamount=str.strip(iteminfo[2])
                #print('totalamount---->',totalamount)
                if len(iteminfo)==4:
                    discountvalue=str.strip(iteminfo[3])
                else:
                    discountvalue='0'
                #print('discountvalue---->',discountvalue)
                item_details = list(trans_details)
                netamount=0
                item_details.extend([itemnum,description,' ',unitprice,quantity,Qtymeasure,netamount,discountvalue,totalamount])   
                items.append(tuple(item_details )) 
            
    return items

def extract_value(text,word,seperator,starting,ending):
    invoiceno_m=re.compile(word) 
   
    invoiceno=None
    for line in text.split('\n'):
        if invoiceno_m.match(line):
            #print(line)
            invoiceno= line.split(seperator)[starting:ending]
    return ' '.join(invoiceno)


    
def insert_more_data(f):
    text=""
    with pdfplumber.open(f) as pdf:
        for page in pdf.pages:
            text+= page.extract_text()
        invoiceno=extract_invoice_no(text)
        invoice_date=parser.parse(str.strip(extract_invoice_date(text))) 
        vendor_email = extract_vendor_email(text)
        Amount,AmountinWords= extract_Amount(text)
        address = extract_address(text)
        vendor_name=extract_vendor_name(text)
        items=Extract_items(text,'E',invoiceno,invoice_date,vendor_name,address,'Grocery',Amount,'More','CreditCard','hdfc muraleedas',AmountinWords,vendor_email)
        #trans_type,invoice_no,invoice_date,vendor,vendor_address,trans_category,trans_amount,trans_desc,payment_mode,payment_desc,items
        #trans=TRANSACTION_MASTER('C',invoiceno,invoice_date,vendor_name,address,'Grocery',Amount,'DESC','CC','BII',items)
        trans_masterTO=MasterTO.Transaction_MasterTO(  
                trans_type='C',
                invoice_no=invoiceno,
                invoice_date=invoice_date,
                vendor=vendor_name,
                vendor_address=address,
                trans_category='Grocery',
                trans_amount=Amount,
                trans_desc='DESC',
                payment_mode='CC',
                payment_desc='BB',
                items=items
            )
        #connectdb.insert_data(items)
        DataAccess.insert(trans_masterTO)
        return trans_masterTO.to_dict()
    
def insert_bb_data():  
    text=""
    with pdfplumber.open("C:/Manjusha/Projects/bills/MMYO-275961754-271122.pdf") as pdf:
        for page in pdf.pages:
            text+= page.extract_text()
    invoiceno=extract_value(text,'GST Invoice No',' ',3,4)
    invoice_date=parser.parse(str.strip(extract_value(text,'Slot',' ',1,5)))
    Amount=extract_value(text,'Sub Total Rs.',' ',3,4)
    address=extract_value(text,'Source',' ',1,2)
    vendor_email =''
    AmountinWords=''
    vendor_name=address
    PaymentBy =extract_value(text,'Payment By',' ',2,3)
    items=Extract_bb_items(text,'^\d{1}.*','E',invoiceno,invoice_date,vendor_name,address,'Grocery',Amount,address,PaymentBy,PaymentBy,AmountinWords,vendor_email)
    print('items---->',items)
    connectdb.insert_data(items)
    return items

def insert_bigbasket_data(f):  
    text=""
    with pdfplumber.open(f) as pdf:
        for page in pdf.pages:
            text+= page.extract_text()
    invoiceno=extract_value(text,'GST Invoice No',' ',3,4)
    invoice_date=parser.parse(str.strip(extract_value(text,'Slot',' ',1,5)))
    Amount=extract_value(text,'Sub Total Rs.',' ',3,4)
    address=extract_value(text,'Source',' ',1,2)
    vendor_email =''
    AmountinWords=''
    vendor_name=address
    PaymentBy =extract_value(text,'Payment By',' ',2,3)
    items=Extract_bb_items(text,'^\d{1}.*','E',invoiceno,invoice_date,vendor_name,address,'Grocery',Amount,address,PaymentBy,PaymentBy,AmountinWords,vendor_email)
    print('items---->',items)
    connectdb.insert_data(items)
    return items
def getTransactions(search,order_by,start,length):
    return DataAccess.getTransactions(search,order_by,start,length)
    
def createAdHocItem(transtype,transdesc,Amount,pDate,transcategory):
    
    trans_masterTO=MasterTO.Transaction_MasterTO(  
                trans_type=transtype,
                invoice_no=None,
                invoice_date=parser.parse(str.strip(pDate)) ,
                vendor=transdesc,
                vendor_address=transdesc,
                trans_category=transcategory,
                trans_amount=Amount,
                trans_desc=transdesc,
                payment_mode='Cash',
                payment_desc='Cash',
                items=None
            )
        #connectdb.insert_data(items)
    DataAccess.insert(trans_masterTO)
    return trans_masterTO.to_dict()
    
 
    


if __name__ == '__main__':
    print('in util..')