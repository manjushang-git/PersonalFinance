
class Transaction_MasterTO:
   
    def __init__(self,**kwargs) -> None:
        self.trans_type=kwargs["trans_type"]
        self.invoice_no=kwargs["invoice_no"]
        self.invoice_date=kwargs["invoice_date"]
        self.vendor=kwargs["vendor"]
        self.vendor_address=kwargs["vendor_address"]
        self.trans_category=kwargs["trans_category"]
        self.trans_amount=kwargs["trans_amount"]
        self.trans_desc=kwargs["trans_desc"]
        self.payment_mode=kwargs["payment_mode"]
        self.payment_desc=kwargs["payment_desc"]
        self.items=kwargs["items"]
    def to_dict(self):
        return {
            
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


