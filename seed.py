from app import db
from models import Product

def seed():
    db.create_all()
    products = [
        {'name': 'Banan (1 kg)', 'description': 'Sog‘lom va shirin', 'price': 3.5, 'stock': 50, 'image': ''},
        {'name': 'Sut (1 L)', 'description': 'Toza sut', 'price': 1.2, 'stock': 100, 'image': ''},
        {'name': 'Non (1 dona)', 'description': 'Yangi pishirilgan', 'price': 0.5, 'stock': 200, 'image': ''},
    ]
    for p in products:
        prod = Product(name=p['name'], description=p['description'], price=p['price'], stock=p['stock'], image=p['image'])
        db.session.add(prod)
    db.session.commit()
    print("Seed completed.")

if __name__ == '__main__':
    seed()

