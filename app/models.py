from app import db

class FeatureRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', backref='feature_requests', lazy=True)
    client_priority = db.Column(db.Integer)
    target_date = db.Column(db.DateTime)
    product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.id'), nullable=False)
    product_area = db.relationship('ProductArea', backref='feature_requests', lazy=True)

    def __repr__(self):
        # return '<FeatureRequest {}>'.format({
        #     'id': self.id,
        #     'title': self.title,
        #     'description': self.description,
        #     'client_id': self.client_id,
        #     'client': self.client,
        #     'client_priority': self.client_priority,
        #     'target_date': self.target_date,
        #     'product_area_id': self.product_area_id,
        #     'product_area': self.product_area
        # })
        return '<FeatureRequest client_id: {}: title:{}: client_priority: {}>'.format(self.client_id, self.title, self.client_priority)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return '<Client {}: {}: {}>'.format(self.name, self.feature_requests, self.id)
    
    def get_client(self, name):
        return self.query.filter_by(name=name).first()
        


class ProductArea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return '<ProductArea {}: {}: {}>'.format(self.name, self.feature_requests, self.id)