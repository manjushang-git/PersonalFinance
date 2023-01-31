



DROP TABLE   "OHM"."TRANSACTION_DETAILS" ;



DROP TABLE  "OHM"."TRANSACTION_MASTER" ;
  CREATE TABLE "OHM"."TRANSACTION_MASTER" 
   (	"TRANS_TYPE"  varchar2(15), 
	"INVOICE_NO" VARCHAR2(20 BYTE), 
	"INVOICE_DATE" DATE, 
	"VENDOR" VARCHAR2(100 BYTE), 
	"VENDOR_ADDRESS" VARCHAR2(250 BYTE), 
	"TRANS_CATEGORY" VARCHAR2(20 BYTE), 
	"TRANS_AMOUNT" NUMBER, 
	"TRANS_DESC" VARCHAR2(250 BYTE), 
	"PAYMENT_MODE" VARCHAR2(20 BYTE), 
	"PAYMENT_DESC" VARCHAR2(250 BYTE), 
	"TRANS_NO" NUMBER  GENERATED ALWAYS AS IDENTITY (START WITH 1000000000 
 INCREMENT BY 1 
NOCYCLE), 
	"TRANS_AMOUNT_WORDS" VARCHAR2(500 BYTE), 
	"VENDOR_EMAIL" VARCHAR2(50 BYTE), 
	 CONSTRAINT "TRANSACTION_MASTER_PK" PRIMARY KEY ("TRANS_NO")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "USERS"  ENABLE
   ) SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "USERS" ;


  CREATE TABLE "OHM"."TRANSACTION_DETAILS" 
   (	"TRANS_NO" NUMBER NOT NULL ENABLE, 
	"ITEM_CODE" VARCHAR2(20 BYTE) NOT NULL ENABLE, 
	"ITEM_NAME" VARCHAR2(250 BYTE), 
	"ITEM_CATEGOTY" VARCHAR2(250 BYTE), 
	"ITEM_UNIT_PRICE" NUMBER, 
	"ITEM_QUANTITY" NUMBER, 
	"ITEM_QUANTITY_MEASURE" VARCHAR2(20 BYTE), 
	"ITEM_NET_AMOUNT" NUMBER, 
	"ITEM_DISCOUNT_VALUE" NUMBER, 
	"ITEM_TOTAL_AMOUNT" VARCHAR2(20 BYTE), 
	 CONSTRAINT "TRANSACTION_DETAILS_PK" PRIMARY KEY ("TRANS_NO", "ITEM_CODE")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  TABLESPACE "USERS"  ENABLE, 
	 CONSTRAINT "TRANSACTION_DETAILS_FK1" FOREIGN KEY ("TRANS_NO")
	  REFERENCES "OHM"."TRANSACTION_MASTER" ("TRANS_NO") ON DELETE CASCADE ENABLE
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;

   COMMENT ON COLUMN "OHM"."TRANSACTION_DETAILS"."TRANS_NO" IS 'FOREIGN KEY';



CREATE OR REPLACE VIEW transactionS (
    trans_no,
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
) AS
    SELECT
        tm.trans_no,
        tm.trans_type,
        tm.invoice_no,
        tm.invoice_date,
        tm.vendor,
        tm.vendor_address,
        tm.trans_category,
        tm.trans_amount,
        tm.trans_desc,
        tm.payment_mode,
        tm.payment_desc,
        tm.trans_amount_words,
        tm.vendor_email,
        td.item_code,
        td.item_name,
        td.item_categoty,
        td.item_unit_price,
        td.item_quantity,
        td.item_quantity_measure,
        td.item_net_amount,
        td.item_discount_value,
        td.item_total_amount
    FROM
        transaction_master  tm
        LEFT OUTER JOIN transaction_details td ON tm.trans_no = td.trans_no;

CREATE OR REPLACE TRIGGER transaction_insert_trg INSTEAD OF
    INSERT ON transactions
    FOR EACH ROW
DECLARE
    l_trans_no NUMBER;
BEGIN
    -- insert a new customer first
    BEGIN
        SELECT
            trans_no
        INTO l_trans_no
        FROM
            transaction_master
        WHERE
                invoice_no = :new.invoice_no
                and invoice_date=:new.invoice_date
            AND vendor = :new.vendor
            AND trans_amount = :new.trans_amount
        FETCH FIRST 1 ROW ONLY;

    EXCEPTION
        WHEN no_data_found THEN
            INSERT INTO transaction_master (
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
                vendor_email
            ) VALUES (
                :new.trans_type,
                :new.invoice_no,
                :new.invoice_date,
                :new.vendor,
                :new.vendor_address,
                :new.trans_category,
                :new.trans_amount,
                :new.trans_desc,
                :new.payment_mode,
                :new.payment_desc,
                :new.trans_amount_words,
                :new.vendor_email
            ) RETURNING trans_no INTO l_trans_no;

    END;
    -- insert the contact
    DELETE FROM transaction_details
    WHERE
            trans_no = l_trans_no
        AND item_code = :new.item_code;

    INSERT INTO transaction_details (
        trans_no,
        item_code,
        item_name,
        item_categoty,
        item_unit_price,
        item_quantity,
        item_quantity_measure,
        item_net_amount,
        item_discount_value,
        item_total_amount
    ) VALUES (
        l_trans_no,
        :new.item_code,
        :new.item_name,
        :new.item_categoty,
        :new.item_unit_price,
        :new.item_quantity,
        :new.item_quantity_measure,
        :new.item_net_amount,
        :new.item_discount_value,
        :new.item_total_amount
    );

END;

INSERT INTO transactions (
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
) VALUES (
    'e',
    '234',
    sysdate,
    'more',
    'moremegastore',
    'gloceries',
    3450,
    'desci',
    'cc',
    'mu hdfc',
    'one thousand',
    'more@more.com',
    '12334',
    'banana',
    'veggies',
    122,
    1,
    'kg',
    '222',
    0,
    333
);


alter table transaction_master modify TRANS_TYPE varchar2(15)