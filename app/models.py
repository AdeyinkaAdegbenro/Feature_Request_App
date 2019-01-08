from app import db


class FeatureRequest(db.Model):
    ''' this definition describes the Feature Request created by user '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    client_id = db.Column(
        db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship(
        'Client', backref='feature_requests', lazy=True)
    client_priority = db.Column(db.Integer)
    target_date = db.Column(db.DateTime)
    product_area_id = db.Column(
        db.Integer, db.ForeignKey('product_area.id'), nullable=False)
    product_area = db.relationship(
        'ProductArea', backref='feature_requests', lazy=True)

    def __repr__(self):
        return '<FeatureRequest {}>'.format(self.title)


class Client(db.Model):
    '''this model represents the Client selected by
    user when creating a feature request'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return '<Client {}>'.format(self.name)

    def get_client(self, name):
        return self.query.filter_by(name=name).first()


class ProductArea(db.Model):
    '''this model represents the Product Area
    selected by user when creating a feature request'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return '<ProductArea {}>'.format(self.name)
