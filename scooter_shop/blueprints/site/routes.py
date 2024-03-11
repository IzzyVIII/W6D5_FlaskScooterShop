from flask import Blueprint, flash, redirect, render_template, request 


from scooter_shop.models import Product, Customer, Order, db 
from scooter_shop.forms import ProductForm

site = Blueprint('site', __name__, template_folder='site_templates')


@site.route('/')
def shop():

    allprods = Product.query.all()
    allcustomers = Customer.query.all()
    allorders = Order.query.all()

    shop_stats = {
        'products' : len(allprods),
        'sales' : sum([order.order_total for order in allorders]),
        'customers' : len(allcustomers)
    }


    return render_template('shop.html', shop=allprods, stats=shop_stats)


@site.route('/shop/create', methods= ['GET', 'POST'])
def create():

    #instantiate our productform

    createform = ProductForm()

    if request.method == 'POST' and createform.validate_on_submit():
        #grab our data from our form
        name = createform.name.data
        image = createform.image.data
        prod_type = createform.prod_type.data
        price = createform.price.data
        quantity = createform.quantity.data
        color = createform.color.data

        #instantiate that class as an object passing in our arguments to replace our parameters 
        
        product = Product(name, prod_type, price, quantity, image, color)

        db.session.add(product) #adding our new instantiating object to our database
        db.session.commit()

        flash(f"You have successfully created product {name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/shop/create')
    

    return render_template('create.html', form=createform )


@site.route('/shop/update/<id>', methods=['GET', 'POST']) #<parameter> this is how pass parameters to our routes 
def update(id):

    #lets grab our specific product we want to update
    product = Product.query.get(id) #this should only ever bring back 1 item/object
    updateform = ProductForm()

    if request.method == 'POST' and updateform.validate_on_submit():

        product.name = updateform.name.data 
        product.image = product.set_image(updateform.image.data, updateform.name.data)
        product.prod_type = updateform.prod_type.data 
        product.price = updateform.price.data 
        product.quantity = updateform.quantity.data
        product.color = updateform.color.data

        #commit our changes
        db.session.commit()

        flash(f"Product successfully updated {product.name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("Unable to process request", category='warning')
        return redirect(f'/')
    
    return render_template('update.html', form=updateform, product=product )


@site.route('/shop/delete/<id>')
def delete(id):

    #query our database to find that object we want to delete
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return redirect('/')