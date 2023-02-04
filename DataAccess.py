
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

def getExpense():
    session = Session()
    query = session.query(TRANSACTION_MASTER).with_entities(TRANSACTION_MASTER.trans_no,TRANSACTION_MASTER.trans_desc,TRANSACTION_MASTER.trans_amount,TRANSACTION_MASTER.invoice_date,TRANSACTION_MASTER.trans_category).all()
   
    total_count=len(query)
    print('  total_count   ====',total_count)
    query = query[1:11]
    page_count=len(query)
    
    result = []
    for trans in query:
        trans_dict = {}
        trans_dict['id'] = trans.trans_no
        trans_dict['name'] = trans.trans_desc
        trans_dict['amount'] = trans.trans_amount
        trans_dict['date'] =trans.invoice_date
        trans_dict['category'] = trans.trans_category
        result.append(trans_dict)
    
    return result,page_count,total_count