
# 1 - imports
from datetime import date


from base import Session, engine, Base
from Transaction_Master import TRANSACTION_MASTER
from Transaction_Master import TRANSACTION_DETAILS


session = Session()


td=[TRANSACTION_DETAILS('243','greengram','pulses','100',1,'kg',100,0,100)]
Tm = TRANSACTION_MASTER('C','ENTHE','10-JAN-2022','MANJUSHA','ADDRES','GROCERY',123.00,'DESC','CC','BII',td)




# 9 - persists data
session.add(Tm)


# 10 - commit and close session
session.commit()
session.close()