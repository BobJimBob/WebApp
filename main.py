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
    return 'you gay'

'''
Place for Hasan to put his codes
'''


if __name__ == '__main__':
    app.run(debug=True)
