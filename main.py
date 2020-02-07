from flask import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


from Forms import *
from cartentry import *
import order_data
from create_form import createForm
from alert_form import alertForm
from verification_form import verification_form
from remarks_form import remarksForms


app = Flask(__name__)
app.config['SECRET_KEY'] = 'peepee'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config["SECURITY_REGISTERABLE"] = True
app.config["SECURITY_LOGIN_URL"] = "/login.html"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
admin = Admin(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.html'

'''
bryans stuff
'''

roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                       db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
                       )


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

    def __repr__(self):
        return '<Role %r>' % (self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean)
    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic"))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    postal = db.Column(db.String(6))
    country = db.Column(db.String(100))


class SecurityQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000))
    answer = db.Column(db.String(100))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_first_request
def before_first_request():
    db.create_all()
    user_datastore.find_or_create_role(name='admin')
    user_datastore.find_or_create_role(name='end-user')
    user_datastore.find_or_create_role(name='delivery')
    encrypted_password = generate_password_hash('password')
    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(email='admin@example.com', password=encrypted_password)
    db.session.commit()
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    db.session.commit()


class myModel(ModelView):
    can_delete = False
    column_display_pk = True
    column_exclude_list = ("password")

    def is_accessible(self):
        return current_user.has_role('admin')


admin.add_view(myModel(User, db.session))
admin.add_view(myModel(Role, db.session))
admin.add_view(myModel(Address, db.session))
admin.add_link(MenuLink("Back to home", "/", "home"))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

security = Security(app, user_datastore)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return render_template("home.html")
        flash("Invalid email or password")
        return render_template("login.html", form=form)

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("Username already exists")
            return render_template('signup.html', form=form)
        elif email:
            flash("Email already exists")
            return render_template('signup.html', form=form)

        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user_datastore.create_user(username=form.username.data, email=form.email.data, password=hashed_password)
        user_datastore.add_role_to_user(form.email.data, "end-user")
        db.session.commit()
        flash("Your account has been created")
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)


@app.route('/userpage')
@login_required
def userpage():
    orderdb = shelve.open('orderdatabase.db')
    id = current_user.id
    id = str(id)
    orderinfo = orderdb[id]
    exists = db.session.query(User.query.filter(Address.id == current_user.id).exists()).scalar()
    exists2 = db.session.query(User.query.filter(SecurityQ.id == current_user.id).exists()).scalar()
    if exists and exists2 is True:
        userAddress = Address.query.filter_by(id=current_user.id).first()
        address = userAddress.address
        postal = userAddress.postal
        country = userAddress.country
        return render_template("userpage.html", name=current_user.username, email=current_user.email,
                               id=current_user.id, address=address, postal=postal, country=country, haveaddress=True,
                               havequestion=True,orderinfo=orderinfo)
    elif exists is True:
        userAddress = Address.query.filter_by(id=current_user.id).first()
        address = userAddress.address
        postal = userAddress.postal
        country = userAddress.country
        return render_template("userpage.html", name=current_user.username, email=current_user.email,
                               id=current_user.id, address=address, postal=postal, country=country, haveaddress=True)
    elif exists2 is True:
        return render_template("userpage.html", name=current_user.username, email=current_user.email,
                               id=current_user.id, havequestion=True)

    return render_template('userpage.html', name=current_user.username, email=current_user.email, id=current_user.id)


@app.route('/changeinfo', methods=['GET', 'POST'])
@login_required
def changeinfo():
    form = ChangeForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.newpassword.data, method='sha256')
        user = User.query.filter_by(email=current_user.email).first()
        if check_password_hash(user.password, form.oldpassword.data):
            user.password = hashed_password
            db.session.commit()

            flash("Your password has been changed")

            return redirect(url_for('home'))
        flash("wrong password")
        return redirect(url_for("changeinfo"))
    return render_template('changeinfo.html', form=form)


@app.route('/addressinfo', methods=['GET', 'POST'])
@login_required
def addressinfo():
    form = AddressForm()
    if form.validate_on_submit():
        newaddress = Address(id=current_user.id, address=form.address.data, postal=form.postal_code.data,
                             country=form.country.data)
        db.session.add(newaddress)
        db.session.commit()

        flash("your information has been added")
        return redirect(url_for("userpage"))
    return render_template("addressinfo.html", form=form)


@app.route("/changeaddress", methods=['GET', 'POST'])
@login_required
def changeaddress():
    form = AddressForm()
    if form.validate_on_submit():
        newaddress = Address.query.filter_by(id=current_user.id).first()
        newaddress.question = form.address.data
        newaddress.postal = form.postal_code.data
        newaddress.country = form.country.data
        db.session.commit()
        flash("Your address has been changed")
        return redirect(url_for("userpage"))
    return render_template("changeaddress.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    form = ForgotForm()
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        if email:
            user = User.query.filter_by(email=form.email.data).first()
            userid = user.id
            mail = SecurityQ.query.filter_by(id=userid).first()
            mailid = mail.id
            if userid == mailid:
                login_user(user)
                return redirect(url_for("question"))
            flash("question not set")
        flash("email not linked to account")
    return render_template('forgotpassword.html', form=form)


@app.route('/setquestion', methods=['GET', 'POST'])
@login_required
def setquestion():
    form = SQuestionForm()
    if form.validate_on_submit():
        question = SecurityQ(id=current_user.id, question=form.question.data, answer=form.answer.data)
        db.session.add(question)
        db.session.commit()

        flash("your information has been added")
        return redirect(url_for("userpage"))
    return render_template('setquestion.html', form=form)


# @app.route("/changequestion", methods=['GET','POST'])
# @login_required
# def changequestion():
#    form = SQuestionForm()
# if form.validate_on_submit():
#  newanswer =SecurityQ.query.filter_by(id=current_user.id).first()
#  newanswer.question = form.question.data
#  newanswer.answer = form.answer.data
#  db.session.commit()
#  flash("Your question has been changed")
#  return redirect(url_for("userpage"))
# return render_template("changequestion.html",form=form)

@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    form = QuestionForm()
    question = SecurityQ.query.filter_by(id=current_user.id).first()
    answer = question.answer
    questionused = question.question
    if form.validate_on_submit():
        if answer == form.answer.data:
            return redirect(url_for('resetchangeinfo'))
        flash("Wrong answer")
    return render_template("question.html", form=form, question=questionused)


@app.route('/resetchangeinfo', methods=['GET', 'POST'])
@login_required
def resetchangeinfo():
    form = ResetChangeForm()
    if form.validate_on_submit():
        if form.newpassword.data == form.confirmpassword.data:
            hashed_password = generate_password_hash(form.confirmpassword.data, method='sha256')
            current_user.password = hashed_password
            db.session.commit()

            flash("Your Password has been changed")
            return redirect(url_for("logout"))
        flash("Passwords are not the same")
    return render_template("resetchangeinfo.html", form=form)


'''
end of bryans shit
'''


'''
hasans stuff
'''
@app.route('/deliveryStatus')
def delivery_status():
    userorders = {}
    orderdb = shelve.open('orderdatabase.db')
    userID = str(current_user.id)
    userorders = orderdb[userID]
    #orderDict = db['Orders']
    orderdb.close()

    orderList = []
    for key in userorders:
        order = userorders.get(key)
        orderList.append(order)
    return render_template("delivery_status.html", orderList=orderList, count=len(orderList))
    # return render_template("delivery_status.html", orderList=orderList, count=len(orderList),posts=posts)


@app.route('/alertUser/<id>', methods=['GET', 'POST'])
def alert_user(id):
    alertChangeForm = alertForm(request.form)
    if request.method == 'POST' and alertChangeForm.validate():
        #orderDict = {}
        #db = shelve.open('order.db', 'w')
        #orderDict = db['Orders']
        userorders = {}
        orderdb = shelve.open('orderdatabase.db')
        userID = str(current_user.id)
        userorders = orderdb[userID]
        order = userDict.get(id)
        #order = orderDict.get(id)
        #order.set_date_received(alertChangeForm.newReceiveDate.data)
        #order.set_delivery_types(alertChangeForm.newDeliveryTypes.data)
        order.set_delivery_status(alertChangeForm.deliveryStatus.data)
        #order.set_admin_remarks(alertChangeForm.remarks.data)
        orderdb[userID] = userorders
        #db['Orders'] = orderDict
        orderdb.close()

        return redirect(url_for('delivery_status'))
    else:
        #orderDict = {}
        #db = shelve.open('order.db', 'r')
        #orderDict = db['Orders']
        #db.close()
        userorders = {}
        orderdb = shelve.open('orderdatabase.db')
        userID = str(current_user.id)
        userorders = orderdb[userID]
        orderdb.close()
        #order = orderDict.get(id)
        order = userorders.get(id)
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
    userorders = {}
    orderdb = shelve.open('orderdatabase.db')
    userID = str(current_user.id)
    userorders = orderdb[userID]
    orderdb.close()
    #orderDict = {}
    #db = shelve.open('order.db', 'r')
    #orderDict = db['Orders']
    #db.close()
    #order = orderDict.get(id)
    order = userorders.get(id)
    orderList = []
    orderList.append(order)
    return render_template('view_more_admin.html', orderList=orderList)


@app.route('/allOrders')
def all_orders():
    userorders = {}
    orderdb = shelve.open('orderdatabase.db')
    userID = str(current_user.id)
    userorders = orderdb[userID]
    orderdb.close()
    #orderDict = {}
    #db = shelve.open('order.db', 'r')
    #orderDict = db['Orders']
    #db.close()

    orderList = []
    for key in userorders:
        order = userorders.get(key)
        orderList.append(order)
    return render_template('all_orders.html', orderList=orderList)


@app.route('/verification/<id>', methods=['GET', 'POST'])
def verification(id):
    updateStatusForm = verification_form(request.form)
    if request.method == 'POST' and updateStatusForm.validate():
        userorders = {}
        orderdb = shelve.open('orderdatabase.db')
        userID = str(current_user.id)
        userorders = orderdb[userID]
        orderdb.close()
        #orderDict = {}
        #db = shelve.open('order.db', 'w')
        #orderDict = db['Orders']
        #order = orderDict.get(id) #change the codes here
        order = userorders.get(id)
       #print(order.get_verification(), updateStatusForm.verifyDelivery.data)
        if order.get_verification() == updateStatusForm.verifyDelivery.data:
            order.set_status('D')
        # order.set_received_date
        #order.set_delivery_status(updateStatusForm.verifyDelivery.data)
            orderdb[userID] = userorders
            orderdb.close()
            return redirect(url_for('all_orders'))
        else:
            return 'Verification Code does not match'
        # return redirect(url_for('error_page'))
    else:
        #orderDict = {}
        #db = shelve.open('order.db', 'r')
        #orderDict = db['Orders']
        #db.close()
        userorders = {}
        orderdb = shelve.open('orderdatabase.db')
        userID = str(current_user.id)
        userorders = orderdb[userID]
        orderdb.close()

        order = userorders.get(id)
        #order = orderDict.get(id)
        orderList = []
        orderList.append(order)
        #add in something here

        return render_template('veri_code.html', orderList=orderList, form=updateStatusForm)


@app.route('/view_more_delivery/<id>', methods=['GET', 'POST']) #continue making this
def view_more__delivery(id):
    deliveryRemarkForm = remarksForms(request.form)
    if request.method == 'POST' and deliveryRemarkForm.validate():
        userorders = {}
        orderdb = shelve.open('orderdatabase.db')
        userID = str(current_user.id)
        userorders = orderdb[userID]
        #orderDict = {}
        #db = shelve.open('order.db', 'w')
        #orderDict = db['Orders']
        #order = orderDict.get(id)
        order = userorders.get(id)
        #order.set_delivery_remarks(deliveryRemarkForm.remarks.data)
        orderdb[userID] = userorders
        orderdb.close()
        return redirect(url_for('all_orders'))
    else:
        userorders = {}
        orderdb = shelve.open('orderdatabase.db')
        userID = str(current_user.id)
        userorders = orderdb[userID]
        #orderDict = {}
        #db = shelve.open('order.db', 'r')
        #orderDict = db['Orders']
        orderdb.close()
        order = userorders.get(id)
        #order = orderDict.get(id)
        orderList = []
        orderList.append(order)
        return render_template('view_more_delivery.html', orderList=orderList, form=deliveryRemarkForm)

'''
end of hasans stuff
'''
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
@login_required
def checkout():
    checkoutForm = CheckoutForm(request.form)
    if request.method == 'POST' and checkoutForm.validate():
        return redirect(url_for('receipt'))
    return render_template('checkout.html', form=checkoutForm)


@app.route('/receipt')
@login_required
def receipt():
    ordergenerate()

    grandtotal = session.get('grandtotal', None)
    deleteallItem()
    return render_template("receipt.html", grandtotal=grandtotal)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    verification = str(uuid.uuid4())
    feedbackForm = FeedbackForm(request.form)
    if request.method == 'POST' and feedbackForm.validate():
        return redirect(url_for('home'))
    return render_template('feedback.html', form=feedbackForm, verification=verification)



def ordergenerate():

    orderinfo = {}
    orderdb = shelve.open('orderdatabase.db')
    cartitemdb = shelve.open('cartstorage.db')
    userID = str(current_user.id)
    trackingnum = str(uuid.uuid4())
    orderID = str(userID) + str(len(orderdb.keys()))
    userorders = orderinfoC(orderID, cartitemdb, trackingnum)
    orderinfo[userorders.get_orderID()] = {userorders}

    orderdb[str(current_user.id)] = orderinfo


    orderdb.close()
    cartitemdb.close()


if __name__ == '__main__':
    app.run(debug=True)
