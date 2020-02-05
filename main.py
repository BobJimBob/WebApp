from flask import *
import shelve
from feedbackforms import *
from cartentry import *

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
@app.route('/home')
@app.route('/shop')
def home():
    db = shelve.open('inventory.db')

    product_list = []
    for key in db:
        product = db.get(key)
        product_list.append(product)
    db.close()
    return render_template("shop.html", product_list=product_list)


@app.route('/init')
def init():
    initdb()
    print('db initialised')
    return 'bruh'


@app.route('/product-single/<string:id>')
def product_single(id):

    db = shelve.open('inventory.db')
    product = db.get(id)
    db.close()
    return render_template("product-single.html", product=product)

@app.route('/additem/')
@app.route('/additem/<string:id>', methods=['GET', 'POST'])
def additem(id):
    cartDict = {}
    cartadd = int(request.form.get('quantity'))


    # init db#
    dbinv = shelve.open('inventory.db')
    dbcart = shelve.open('cartstorage.db')

    retrieveitem = dbinv.get(id)
    itemtobeadded = CartEntry(retrieveitem.get_itemID(), retrieveitem.get_image(), retrieveitem.get_name(),
                              retrieveitem.get_price(), cartadd)

    dbcart[itemtobeadded.get_itemID()] = itemtobeadded

    print(itemtobeadded.get_name(), itemtobeadded.get_itemID(), "was stored in cart successfully")

    dbcart.close()
    dbinv.close()
    return redirect(url_for('displaycart'))


@app.route('/cart', methods=['GET', 'POST'])
def displaycart():
    grandtotal = 0
    cartitemDict = {}
    db = shelve.open('cartstorage.db')
    itemList = []
    for id in db:
        cartdisplay = db.get(id)
        grandtotal += cartdisplay.get_total()
        itemList.append(cartdisplay)
    db.close()
    session['grandtotal'] = grandtotal
    return render_template('cart.html', itemList=itemList, count=len(itemList), grandtotal=grandtotal)


@app.route('/deletecartItem/<string:id>', methods=['POST'])
def deleteItem(id):
    db = shelve.open('cartstorage.db')
    db.pop(id)
    db.close()
    return redirect(url_for('displaycart'))


@app.route('/deletecartAll', methods=['POST'])
def deleteallItem():
    cartitemDict = {}
    db = shelve.open('cartstorage.db')
    db.clear()
    db.close()
    return redirect(url_for('displaycart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    checkoutForm = CheckoutForm(request.form)
    if request.method == 'POST' and checkoutForm.validate():
        return redirect(url_for('receipt'))
    return render_template('checkout.html', form=checkoutForm)


@app.route('/receipt')
def receipt():
    orderdb = shelve.open('orderdatabase')   
    grandtotal = session.get('grandtotal', None)
    return render_template("receipt.html", grandtotal=grandtotal)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    verification = str(uuid.uuid4())
    feedbackForm = FeedbackForm(request.form)
    if request.method == 'POST' and feedbackForm.validate():
        return redirect(url_for('home'))
    return render_template('feedback.html', form=feedbackForm, verification = verification)

@app.route('/createorder', methods=['GET', 'POST'])
def ordergenerate():
    return 'generate order details'

'''
Place for Hasan to put his codes
'''
'''
@app.route('/deliveryStatus')
def delivery_status():
    # posts = Post.query.all()
    orderDict = {}
    db = shelve.open('order.db', 'r')
    orderDict = db['Orders']
    db.close()

    orderList = []
    for key in orderDict:
        order = orderDict.get(key)
        orderList.append(order)
    return render_template("delivery_status.html", orderList=orderList, count=len(orderList))
    # return render_template("delivery_status.html", orderList=orderList, count=len(orderList),posts=posts)


@app.route('/alertUser/<id>', methods=['GET', 'POST'])
def alert_user(id):
    alertChangeForm = alertForm(request.form)
    if request.method == 'POST' and alertChangeForm.validate():
        orderDict = {}
        db = shelve.open('order.db', 'w')
        orderDict = db['Orders']
        print('something')
        order = orderDict.get(id)
        order.set_date_received(alertChangeForm.newReceiveDate.data)
        order.set_delivery_company(alertChangeForm.newDeliveryCompany.data)
        order.set_delivery_status(alertChangeForm.deliveryStatus.data)
        order.set_admin_remarks(alertChangeForm.remarks.data)
        print('something 2')
        db['Orders'] = orderDict
        db.close()

        return redirect(url_for('delivery_status'))
    else:
        orderDict = {}
        db = shelve.open('order.db', 'r')
        orderDict = db['Orders']
        db.close()
        print('failed')
        order = orderDict.get(id)
        orderList = []
        orderList.append(order)
        # takes info from dictionary
        # alertChangeForm.orderID.data = order.get_orderID()
        #alertChangeForm.newReceiveDate.data = order.get_date_received()
        #alertChangeForm.newDeliveryCompany.data = order.get_delivery_company()
        #alertChangeForm.deliveryStatus.data = order.get_delivery_status()
        #alertChangeForm.remarks.data = order.get_remarks()

        return render_template("alertuser.html", orderList=orderList, form=alertChangeForm)

@app.route('/view_more_admin/<id>', methods=['GET','POST'])
def view_more_admin(id):
    orderDict = {}
    db = shelve.open('order.db', 'r')
    orderDict = db['Orders']
    db.close()
    order = orderDict.get(id)
    orderList = []
    orderList.append(order)
    return render_template('view_more_admin.html', orderList=orderList)


'''
add in code from app dev project 2
'''
@app.route('/allOrders')
def all_orders():
    orderDict = {}
    db = shelve.open('order.db', 'r')
    orderDict = db['Orders']
    db.close()

    orderList = []
    for key in orderDict:
        order = orderDict.get(key)
        orderList.append(order)
    return render_template('all_orders.html', orderList=orderList)


@app.route('/verification/<id>', methods=['GET', 'POST'])
def verification(id):
    updateStatusForm = verification_form(request.form)
    if request.method == 'POST' and updateStatusForm.validate():
        orderDict = {}
        db = shelve.open('order.db', 'w')
        orderDict = db['Orders']
        order = orderDict.get(id) #change the codes here
       #print(order.get_verification(), updateStatusForm.verifyDelivery.data)
        if order.get_verification() == updateStatusForm.verifyDelivery.data:
            order.set_delivery_status('D')
        # order.set_received_date
        #order.set_delivery_status(updateStatusForm.verifyDelivery.data)
            db['Orders'] = orderDict
            db.close()
            return redirect(url_for('all_orders'))
        else:
            return 'Verification Code does not match'
        # return redirect(url_for('error_page'))
    else:
        orderDict = {}
        db = shelve.open('order.db', 'r')
        orderDict = db['Orders']
        db.close()

        order = orderDict.get(id)
        orderList = []
        orderList.append(order)
        #add in something here

        return render_template('veri_code.html', orderList=orderList, form=updateStatusForm)


@app.route('/view_more_delivery/<id>', methods=['GET', 'POST']) #continue making this
def view_more__delivery(id):
    deliveryRemarkForm = remarksForms(request.form)
    if request.method == 'POST' and deliveryRemarkForm.validate():
        orderDict = {}
        db = shelve.open('order.db', 'w')
        orderDict = db['Orders']
        order = orderDict.get(id)
        order.set_delivery_remarks(deliveryRemarkForm.remarks.data)
        db['Orders'] = orderDict
        db.close()
        return redirect(url_for('all_orders'))
    else:
        orderDict = {}
        db = shelve.open('order.db', 'r')
        orderDict = db['Orders']
        db.close()
        order = orderDict.get(id)
        orderList = []
        orderList.append(order)
        return render_template('view_more_delivery.html', orderList=orderList, form=deliveryRemarkForm)



'''

if __name__ == '__main__':
    app.run(debug=True)
