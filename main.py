from flask import Flask, render_template, request, redirect, url_for,flash,current_app
from Forms import CreateProductForm
from update_form import UpdateProduct
import shelve, User
from werkzeug.utils import secure_filename
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
import os , secrets



basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY']= "SECRETKET "
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir,'static/images')
photos = UploadSet('photos',IMAGES)
configure_uploads(app,photos)
patch_request_class(app)






@app.route("/")

@app.route("/Home")
def Home():
    return render_template("index.html", title="Home")




@app.route("/shop")
def shop():

    return render_template("shop.html")



@app.route("/product")
def product():
    return render_template("product-single.html")

###################################################################################################

@app.route('/createBooks', methods=['GET', 'POST'])
def createProducts():
    create_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_form.validate():
        usersDict = {}
        db = shelve.open('product.db', 'c')
        name = create_form.productName
        image_1 = photos.save(request.files.get('image_1'))
        image_2 = photos.save(request.files.get('image_2'))
        image_3 = photos.save(request.files.get('image_3'))
        try:
            usersDict = db['Users']
        except:
            print("Error in retrieving Users from product.db.")

        user = User.User(create_form.productName.data, create_form.author.data,create_form.publisher.data,create_form.genre.data
                          ,create_form.price.data,create_form.stocks.data,create_form.remarks.data,image_1=image_1,image_2=image_2,image_3=image_3)
        usersDict[user.get_userID()] = user
        db['Users'] = usersDict

        db.close()
        flash(f'The product {name} has been added to shelve', 'Success')
        return redirect(url_for('retrieveProducts'))
    return render_template('createproduct.html', form=create_form)









@app.route('/retrieveBooks')
def retrieveProducts():
    userDict = {}
    db = shelve.open('product.db', 'r')
    usersDict = db['Users']
    db.close()

    usersList = []
    for key in usersDict:
        user = usersDict.get(key)
        usersList.append(user)

    return render_template('retrieveproduct.html', usersList=usersList, count=len(usersList))


@app.route('/updateBooks/<int:id>/', methods=['GET', 'POST'])
def updateProduct(id):
    updateProductForm = CreateProductForm(request.form)
    if request.method == "POST" and updateProductForm.validate():
        userDict = {}
        db = shelve.open('product.db', "w")
        userDict = db["Users"]

        user = userDict.get(id)
        user.set_productName(updateProductForm.productName.data)
        user.set_author(updateProductForm.author.data)
        user.set_publisher(updateProductForm.publisher.data)
        user.set_genre(updateProductForm.genre.data)
        user.set_price(updateProductForm.price.data)
        user.set_stocks(updateProductForm.stocks.data)
        user.set_remarks(updateProductForm.remarks.data)






        db["Users"] = userDict

        db.close()

        return redirect(url_for('retrieveProducts'))
    else:
        userDict = {}
        db = shelve.open('product.db', 'r')
        userDict = db['Users']
        db.close()

        user = userDict.get(id)
        updateProductForm.productName.data = user.get_productName()
        updateProductForm.author.data = user.get_author()
        updateProductForm.publisher.data = user.get_publisher()
        updateProductForm.genre.data = user.get_genre()
        updateProductForm.stocks.data = user.get_stocks()
        updateProductForm.price.data = user.get_price()
        updateProductForm.remarks.data = user.get_remarks()

        return render_template('updateproduct.html', form=updateProductForm)


@app.route('/deleteBooks/<int:id>', methods=['POST'])
def deleteUser(id):
    usersDict = {}


    db = shelve.open('product.db', 'w')
    usersDict = db['Users']

    usersDict.pop(id)

    db['Users'] = usersDict
    db.close()

    return redirect(url_for('retrieveProducts'))

#######################################################################################################
#######################################################################################################
@app.route('/retrieveBooks/<string:category>/', methods=['GET', 'POST'])
def get_category(category):

    itemDict = {}
    db = shelve.open('product.db', 'r') # Opening product database
    itemDict = db['Users']
    db.close()


    itemList = []
    for key in itemDict:        # Looping data from itemDict
        user = itemDict.get(key)
        item_category = user.get_genre()  # item_category == "CH" ,"CR" , "F", "M"
        print(category, ':', item_category)
        if category == item_category :
            itemList.append(user)
    print(len(itemList))

    return render_template("displaying.html" , itemList=itemList,count=len(itemList),category= category)




@app.route('/Books/<int:id>/', methods=['GET', 'POST'])
def product_single(id):
    itemDict = {}
    db = shelve.open('product.db', 'r')  # Opening product database

    itemDict = db['Users']
    item = itemDict.get(id)
    db.close()

    usersList = []
    for key in itemDict:        # Looping data from itemDict
        user = itemDict.get(key)
        item_id = user.get_userID()  # item_category == "CH" ,"CR" , "F", "M"

        if id == item_id :
            usersList.append(user)


    return render_template('product_page.html', item = item, usersList=usersList)


#########################################################################################################

if __name__ == '__main__':
    app.run(debug=True)
