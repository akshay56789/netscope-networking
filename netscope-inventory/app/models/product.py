from datetime import datetime
from app import db

class Product(db.Model):
    __tablename__ = 'product'
    
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    Price = db.Column(db.Numeric(10, 2), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False, default=0)
    CreatedDate = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.Name}>'
        
    def to_dict(self):
        return {
            'Id': self.Id,
            'Name': self.Name,
            'Description': self.Description,
            'Price': float(self.Price) if self.Price else 0.0,
            'Quantity': self.Quantity,
            'CreatedDate': self.CreatedDate.isoformat() if self.CreatedDate else None
        }
