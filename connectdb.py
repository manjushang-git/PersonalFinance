import cx_Oracle
def get_connction():
    constr ='OHM/OHM@localhost:1521/PER_FIN'
    conn=cx_Oracle.connect(constr)
    return conn
   
    

def get_random_record():
    conn=get_connction()
    cur2=conn.cursor()
    querytext='select * from TRANSACTIONS order by trans_no desc fetch first 1 row only '
    cur2.execute(querytext)
    record=cur2.fetchall()
    cur2.close()
    return record
  
def insert_data(items):
    conn=get_connction()
    
    cur1=conn.cursor()

    sqltext=''' INSERT INTO transactions (
        trans_type,
        invoice_no,
        invoice_date,
        vendor,
        vendor_address,
        trans_category,
        trans_amount,
        trans_desc,
        payment_mode,
        payment_desc,
        trans_amount_words,
        vendor_email,
        item_code,
        item_name,
        item_categoty,
        item_unit_price,
        item_quantity,
        item_quantity_measure,
        item_net_amount,
        item_discount_value,
        item_total_amount
    )
       
    VALUES( :trans_type,
        :invoice_no,
        :invoice_date,
        :vendor,
        :vendor_address,
        :trans_category,
        :trans_amount,
        :trans_desc,
        :payment_mode,
        :payment_desc,
        :trans_amount_words,
        :vendor_email,
        :item_code,
        :item_name,
        :item_categoty,
        :item_unit_price,
        :item_quantity,
        :item_quantity_measure,
        :item_net_amount,
        :item_discount_value,
        :item_total_amount ) 
    ''' 
    cur1.executemany(sqltext,items)

    conn.commit()
    cur1.close()
    


if __name__ == '__main__':
    print('in util..')