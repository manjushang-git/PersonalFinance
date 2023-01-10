from flask import Flask, render_template, request
import util

app = Flask(__name__)

@app.route('/')
def index():
    #db.create_all()
    #Model.initialise(app)
    return render_template('server_table.html', title='Server-Driven Table')

@app.route('/createnew', methods = ['POST']) 
def createnew(): 
    if request.method == 'POST': 
        Category = request.form.get('Category')
        Amount = request.form.get('Amount')
        print('Manjusha  Create new-----------------------------------------'+Category+Amount)
    return render_template("server_table.html") 
@app.route('/browse', methods = ['POST'])  
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
        return render_template("server_table.html", name = f.filename)  


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


if __name__ == '__main__':
    app.run()
