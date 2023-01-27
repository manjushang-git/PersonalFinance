from sqlalchemy import Column, String, Integer, Date,Float,ForeignKey,Identity
from sqlalchemy.orm import relationship
from base import Base

class TRANSACTION_MASTER(Base):
    __tablename__ = 'TRANSACTION_MASTER'
    trans_no =Column( Integer,Identity(start=1000000000, cycle=True),primary_key=True,autoincrement=True)
    trans_type = Column(String(1))
    invoice_no = Column(String(20))
    invoice_date =Column(Date) 
    vendor = Column(String(100))
    vendor_address = Column(String(250))
    trans_category = Column(String(20))
    trans_amount =Column(Float)
    trans_desc = Column(String(250))
    payment_mode = Column(String(20))
    payment_desc = Column(String(250))
    items = relationship('TRANSACTION_DETAILS',backref='trans')
    def __init__(self,trans_masterTO,items):
        self.trans_type=trans_masterTO.trans_type
        self.invoice_no=trans_masterTO.invoice_no
        self.invoice_date=trans_masterTO.invoice_date
        self.vendor=trans_masterTO.vendor
        self.vendor_address=trans_masterTO.vendor_address
        self.trans_category=trans_masterTO.trans_category
        self.trans_amount=trans_masterTO.trans_amount
        self.trans_desc=trans_masterTO.trans_desc
        self.payment_mode=trans_masterTO.payment_mode
        self.payment_desc=trans_masterTO.payment_desc
        self.items=items
    
    
    ''' def __init__(self,trans_type,invoice_no,invoice_date,vendor,vendor_address,trans_category,trans_amount,trans_desc,payment_mode,payment_desc,items): 
        self.trans_type=trans_type
        self.invoice_no=invoice_no
        self.invoice_date=invoice_date
        self.vendor=vendor
        self.vendor_address=vendor_address
        self.trans_category=trans_category
        self.trans_amount=trans_amount
        self.trans_desc=trans_desc
        self.payment_mode=payment_mode
        self.payment_desc=payment_desc
        self.items=items '''
    def to_dict(self):
        return {
            'trans_no':self.trans_no, 
            'trans_type':self.trans_type,     
            'invoice_no':self.invoice_no  ,   
            'invoice_date':self.invoice_date,    
            'vendor'  :self.vendor,         
            'vendor_address':self.vendor_address ,
            'trans_category':self.trans_category ,
            'trans_amount':self.trans_amount ,   
            'trans_desc':self.trans_desc ,    
            'payment_mode' :self.payment_mode ,  
            'payment_desc' :self.payment_desc  ,
        }
       
    def __repr__(self):
        my_list=[ 'trans_no: ',self.trans_no, 
                    'trans_type: ',self.trans_type,     
                    'invoice_no: ',self.invoice_no  ,   
                    #'invoice_date: ',self.invoice_date.strftime('%m/%d/%Y'),    
                    'vendor: '  ,self.vendor,         
                    'vendor_address: ',self.vendor_address ,
                    'trans_category: ',self.trans_category ,
                    'trans_amount: ',self.trans_amount ,   
                    'trans_desc: ',self.trans_desc ,    
                    'payment_mode: ' ,self.payment_mode ,  
                    'payment_desc: ' ,self.payment_desc ] 
        return "".join(filter(lambda x: x if x is not None else '', my_list))
   



class TRANSACTION_DETAILS(Base):
    __tablename__ = 'TRANSACTION_DETAILS'
    trans_no =Column( Integer,ForeignKey('TRANSACTION_MASTER.trans_no'),primary_key=True )
    item_code = Column(String(20),primary_key=True)
    item_name  = Column(String(250))
    item_categoty  = Column(String(250))
    item_unit_price =Column(Float)
    item_quantity =Column(Float)
    item_quantity_measure  = Column(String(20))
    item_net_amount =Column(Float)
    item_discount_value =Column(Float)
    item_total_amount  = Column(String(20))
    # trans = relationship('TRANSACTION_MASTER', back_populates = "items")
    def __init__(self,trans_detailsTO):
           
            self.item_code=trans_detailsTO.item_code
            self.item_name=trans_detailsTO.item_name
            self.item_categoty=trans_detailsTO.item_categoty
            self.item_unit_price=trans_detailsTO.item_unit_price
            self.item_quantity=trans_detailsTO.item_quantity
            self.item_quantity_measure=trans_detailsTO.item_quantity_measure
            self.item_net_amount=trans_detailsTO.item_net_amount
            self.item_discount_value=trans_detailsTO.item_discount_value
            self.item_total_amount=trans_detailsTO.item_total_amount
            #self.trans=trans
        
    def to_dict(self):
        return {
            'trans_no':self.trans_no,
            'item_code':self.item_code,
            'item_name':self.item_name,
            'item_categoty':self.item_categoty,
            'item_unit_price':self.item_unit_price,
            'item_quantity':self.item_quantity,
            'item_quantity_measure':self.item_quantity_measure,
            'item_net_amount':self.item_net_amount,
            'item_discount_value':self.item_discount_value,
            'item_total_amount':self.item_total_amount,
        }
    