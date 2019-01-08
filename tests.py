import os
import unittest
from config import basedir
from app import app, db
from app.models import FeatureRequest, ProductArea, Client
from datetime import datetime
from flask import url_for
import json


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
         'sqlite:///' + os.path.join(basedir, 'test.db')
        with app.app_context():
            self.app = app.test_client()
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_landing_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_feature_request(self):
        # check that post request for creating  feature request
        # is successful
        form_values = [{'name': 'title',
                        'value': 'social media share button'},
                       {'name': 'description',
                        'value': 'a button that allows'
                        ' sharing on social media'},
                       {'name': 'client', 'value': 'Client A'},
                       {'name': 'client_priority', 'value': 1},
                       {'name': 'target_date', 'value': '2018-01-30'},
                       {'name': 'product_area', 'value': 'Policies'}]
        response = self.app.post('/',
                                 data=json.dumps(form_values),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # check ProductArea was created
        product_area = ProductArea.query.first()
        self.assertNotEqual(product_area, None)
        # check Client was created
        client = Client.query.first()
        self.assertNotEqual(client, None)

        # check all data are correct
        feature_request = FeatureRequest.query.first()
        self.assertNotEqual(feature_request, None)
        self.assertEqual(feature_request.title, 'social media share button')
        self.assertEqual(feature_request.description,
                         'a button that allows sharing on social media')
        self.assertEqual(feature_request.client.name, 'Client A')
        self.assertEqual(feature_request.client_priority, 1)
        self.assertEqual(feature_request.target_date,
                         datetime.strptime('2018-01-30', '%Y-%m-%d'))
        self.assertEqual(feature_request.product_area.name, 'Policies')

    def test_client_priority_shifts_with_same_client_same_priority_num(self):
        form_values = [{'name': 'title',
                        'value': 'social media share button'},
                       {'name': 'description',
                        'value': 'a button that allows '
                        'sharing on social media'},
                       {'name': 'client', 'value': 'Client A'},
                       {'name': 'client_priority', 'value': 1},
                       {'name': 'target_date', 'value': '2018-01-30'},
                       {'name': 'product_area', 'value': 'Policies'}]
        # create feature request by client A with client priority of 1
        response = self.app.post('/', data=json.dumps(form_values))
        self.assertEqual(response.status_code, 200)

        form_values2 = [{'name': 'title', 'value': 'Analytics Page'},
                        {'name': 'description',
                         'value': 'a page that show an analysis of users'},
                        {'name': 'client', 'value': 'Client A'},
                        {'name': 'client_priority', 'value': 1},
                        {'name': 'target_date', 'value': '2018-01-31'},
                        {'name': 'product_area', 'value': 'Policies'}]

        # create feature request by client A with client priority of 1
        response = self.app.post('/', data=json.dumps(form_values2))
        self.assertEqual(response.status_code, 200)

        # check that FeatureRequests created are two
        self.assertEqual(FeatureRequest.query.count(), 2)

        request1 = FeatureRequest.query.filter_by(id=1).one()
        request2 = FeatureRequest.query.filter_by(id=2).one()
        # check feature request 1 has client priority of 2
        self.assertEqual(request1.client_priority, 2)
        # check feature request 2 has client priority of 1
        self.assertEqual(request2.client_priority, 1)

    def test_same_client_priority_doesnt_shift_with_different_priority_num(self):
        form_values = [{'name': 'title', 'value': 'social media share button'},
                       {'name': 'description',
                        'value': 'a button that allows'
                        ' sharing on social media'},
                       {'name': 'client', 'value': 'Client A'},
                       {'name': 'client_priority', 'value': 1},
                       {'name': 'target_date', 'value': '2018-01-30'},
                       {'name': 'product_area', 'value': 'Policies'}]
        # create feature request by client A with client priority of 1
        response = self.app.post('/', data=json.dumps(form_values))
        self.assertEqual(response.status_code, 200)

        form_values2 = [{'name': 'title', 'value': 'Settings Page'},
                        {'name': 'description',
                         'value': 'a page that show settings'},
                        {'name': 'client', 'value': 'Client A'},
                        {'name': 'client_priority', 'value': 2},
                        {'name': 'target_date', 'value': '2018-01-31'},
                        {'name': 'product_area', 'value': 'Policies'}]
        # create feature request by client A with client priority of 2
        response = self.app.post('/', data=json.dumps(form_values2))
        self.assertEqual(response.status_code, 200)

        # check that FeatureRequests created are two
        self.assertEqual(FeatureRequest.query.count(), 2)

        # check feature request 1 has client priority of 1
        request1 = FeatureRequest.query.filter_by(id=1).one()
        self.assertEqual(request1.client_priority, 1)

        # check feature request 2 has client priority of 2
        request2 = FeatureRequest.query.filter_by(id=2).one()
        self.assertEqual(request2.client_priority, 2)

    def test_different_client_doesnt_shift_when_same_priority_num(self):
        # create feature request by client A with client priority of 1
        form_values = [{'name': 'title', 'value': 'social media share button'},
                       {'name': 'description',
                        'value': 'a button that allows '
                        'sharing on social media'},
                       {'name': 'client', 'value': 'Client A'},
                       {'name': 'client_priority', 'value': 1},
                       {'name': 'target_date', 'value': '2018-01-30'},
                       {'name': 'product_area', 'value': 'Policies'}]

        response = self.app.post('/', data=json.dumps(form_values),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # create feature request by client B with client priority of 1
        form_values2 = [{'name': 'title', 'value': 'Settings Page'},
                        {'name': 'description',
                         'value': 'a page that show settings'},
                        {'name': 'client', 'value': 'Client B'},
                        {'name': 'client_priority', 'value': 1},
                        {'name': 'target_date', 'value': '2018-01-31'},
                        {'name': 'product_area', 'value': 'Policies'}]
        response = self.app.post('/', data=json.dumps(form_values2),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # check feature request 1 by client A has client priority of 1
        request1 = FeatureRequest.query.filter_by(id=1).one()
        self.assertEqual(request1.client_priority, 1)

        # check feature request 2 by client B has client priority of 1
        request2 = FeatureRequest.query.filter_by(id=2).one()
        self.assertEqual(request2.client_priority, 1)


if __name__ == "__main__":
    unittest.main()
