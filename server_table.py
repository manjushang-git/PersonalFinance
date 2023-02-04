from flask import Flask, render_template, request,jsonify
import util

app = Flask(__name__)

@app.route('/')
def index():
    #db.create_all()
    #Model.initialise(app)
    return render_template('server_table.html', title='Server-Driven Table')

@app.route("/expense", methods=["POST","GET"])
def expense():
   
    return render_template("expense.html", title="Expense")

@app.route("/income",methods=["POST","GET"])
def income():
    return render_template("income.html", title="Income")

@app.route("/saving", methods=["POST","GET"])
def saving():
    return render_template("saving.html", title="Saving")

@app.route("/donation", methods=["POST","GET"])
def donation():
    return render_template("donation.html", title="Donation")

@app.route("/browsetransaction", methods=["POST","GET"])
def transaction():
    return render_template("browsetransaction.html", title="Transaction")

@app.route('/createexpense', methods = ['POST']) 
def createexpense(): 
    expense_name = request.form['expenseName']
    expense_amount = request.form['expenseAmount']
    expense_date = request.form['expenseDate']
    expense_category = request.form['expenseCategory']
    print('Printed eXPENSE ------ ' ,expense_name,expense_amount,expense_date,expense_category)
    util.createAdHocItem('Expense',expense_name,expense_amount,expense_date,expense_category);
    return "Expense submitted successfully!"

@app.route('/createincome', methods = ['POST']) 
def createincome(): 
    #return render_template("server_table.html") 
    income_name = request.form['incomeName']
    income_amount = request.form['incomeAmount']
    income_date = request.form['incomeDate']
    income_category = request.form['incomeCategory']
    print('Printed income ------ ' ,income_name,income_amount,income_date,income_category)
    util.createAdHocItem('Income',income_name,income_amount,income_date,income_category);
    return "Income submitted successfully!"

@app.route('/createsavings', methods = ['POST']) 
def createsavings(): 
      
    savings_name = request.form['savingsName']
    savings_amount = request.form['savingsAmount']
    savings_date = request.form['savingsDate']
    savings_category = request.form['savingsCategory']
    print('Printed savings ------ ' ,savings_name,savings_amount,savings_date,savings_category)
    util.createAdHocItem('Savings',savings_name,savings_amount,savings_date,savings_category);
    return "Savings submitted successfully!"

@app.route('/createdonation', methods = ['POST']) 
def createdonation(): 

    donation_name = request.form['donationName']
    donation_amount = request.form['donationAmount']
    donation_date = request.form['donationDate']
    donation_category = request.form['donationCategory']
    print('Printed donation ------ ' ,donation_name,donation_amount,donation_date,donation_category)
    util.createAdHocItem('Donation',donation_name,donation_amount,donation_date,donation_category);
   
    return "Donation submitted successfully!"

@app.route('/createbrowsetrans', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        vendor = request.form.get('Vendor')
        f.save(f.filename)  
       
        print(vendor)
        if vendor == 'BigBasket':
            util.insert_bigbasket_data(f)
        elif vendor == 'More':
            util.insert_more_data(f)
        
        print(f.filename)
        return "Donation submitted successfully!"
        #return render_template("server_table.html", name = f.filename)  


@app.route('/api/data')
def data():
    
   
    search = request.args.get('search[value]')
    
   
    # sorting
    order = []
    order_by={}
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        order_by[col_name]=descending
        print(order_by)
        i += 1
       
    
    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    #query = query.offset(start).limit(length)
    data,total_filtered,recordsTotal =util.getTransactions(search,order_by,start,length)
    # response
    
    return {
        'data':data,
        'recordsFiltered': total_filtered,
        'recordsTotal': recordsTotal,
        'draw': request.args.get('draw', type=int),
    }


@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    expenses = util.get_expenses()
    print(expenses)
    return jsonify(expenses)

@app.route('/api/expenses/<int:expense_id>', methods=['GET', 'PUT', 'DELETE'])
def expense_details(expense_id):
    print(' edit expense ',expense_id)
    if request.method == 'GET':
        expense = util.get_expense(expense_id)
        return jsonify(expense)
    elif request.method == 'PUT':
        expense = request.get_json()
        util.update_expense(expense_id, expense)
        return '', 204
    elif request.method == 'DELETE':
        util.delete_expense(expense_id)
        return '', 204
    
    
if __name__ == '__main__':
    app.run()
