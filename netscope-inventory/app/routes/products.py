from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.product import Product
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField
from wtforms.validators import DataRequired, NumberRange

bp = Blueprint('products', __name__)

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])

@bp.route('/')
def list_products():
    products = Product.query.order_by(Product.CreatedDate.desc()).all()
    return render_template('products/list.html', products=products)

@bp.route('/<int:id>')
def view_product(id):
    product = Product.query.get_or_404(id)
    return render_template('products/view.html', product=product)

@bp.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            Name=form.name.data,
            Description=form.description.data,
            Price=form.price.data,
            Quantity=form.quantity.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/form.html', form=form, title='Add Product')

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    
    # Pre-populate form with uppercase attribute names mapping to lowercase form fields
    if request.method == 'GET':
        form.name.data = product.Name
        form.description.data = product.Description
        form.price.data = product.Price
        form.quantity.data = product.Quantity

    if form.validate_on_submit():
        product.Name = form.name.data
        product.Description = form.description.data
        product.Price = form.price.data
        product.Quantity = form.quantity.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products.list_products'))
        
    return render_template('products/form.html', form=form, title='Edit Product', product=product)

@bp.route('/<int:id>/delete', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products.list_products'))
