
class Transaction_DetailsTO:
    def __init__(self,**kwargs):
        self.item_code=kwargs["item_code"]
        self.item_name=kwargs["item_name"]
        self.item_categoty=kwargs["item_categoty"]
        self.item_unit_price=kwargs["item_unit_price"]
        self.item_quantity=kwargs["item_quantity"]
        self.item_quantity_measure=kwargs["item_quantity_measure"]
        self.item_net_amount=kwargs["item_net_amount"]
        self.item_discount_value=kwargs["item_discount_value"]
        self.item_total_amount=kwargs["item_total_amount"]
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
    