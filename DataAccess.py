
# 1 - imports
from datetime import date
from sqlalchemy import or_


from base import Session, engine, Base
from Model import TRANSACTION_MASTER
from Model import TRANSACTION_DETAILS
import Transaction_DetailsTO
import Transaction_MasterTO

def insert(trans_masterTO):
    session = Session()
    items=[]
    if trans_masterTO.items is not None:
        for details in trans_masterTO.items:
            items.append(TRANSACTION_DETAILS(details))
    trans_master=TRANSACTION_MASTER(trans_masterTO,items)
    print(trans_master)
    # 9 - persists data
    session.add(trans_master)
    # 10 - commit and close session
    session.commit()
    session.close()

def getTransactions(search,order_by,start,length):
    session = Session()
    print(''.join(['%',search,'%']),order_by,start,length)
    query = session.query(TRANSACTION_MASTER).filter(or_( TRANSACTION_MASTER.vendor.like(''.join(['%',search,'%'])),TRANSACTION_MASTER.invoice_no.like(''.join(['%',search,'%']))))
    order = []
    if not order_by:
        order_by = {'invoice_date': True}
        
    for col_name,desc in order_by.items():
        print(col_name,desc)
        col = getattr(TRANSACTION_MASTER, col_name)
        if desc:
            col = col.desc()
        order.append(col) 
    if order:
        query = query.order_by(*order)
    total_count=query.count()
    query = query.offset(start).limit(length)
    page_count=query.count()
    
    return [trans.to_dict() for trans in query],page_count,total_count