from flask import Flask, escape, render_template, request,jsonify
import util
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    return render_template('add_data.html')
    
@app.route('/temp')
def home():
    return render_template('PersonalFinanceHome.html')
   
@app.route('/')
def index():
    return render_template('server_table.html', title='Manjusha Table')


@app.route('/Bills')
def Bills():
     return render_template('Bills.html')

@app.route('/about')
def about():
     return render_template('about.html')

@app.route('/Manjusha')
def hello_manjusha():
    return 'Hello Manjusha, you will achieve this!'
    
@app.route('/get_a_randam_record', methods=['GET', 'POST'])
def get_a_randam_record():
    response = jsonify({
        'data': util.get_random_record()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/insert_more_data', methods=['GET', 'POST'])
def insert_more_data():
    
    resp = util.insert_more_data()
    

    return 'Hello Manjusha, you will achieve this!'

@app.route('/insert_bb_data', methods=['GET', 'POST'])
def insert_bb_data():
    
    response = util.insert_bb_data()
 
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
    

@app.route('/api/data')
def data():
    query = util.get_random_record()

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            User.name.like(f'%{search}%'),
            User.email.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['name', 'age', 'email']:
            col_name = 'name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(User, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': User.query.count(),
        'draw': request.args.get('draw', type=int),
    }
    
if __name__ == '__main__':
    app.run()
