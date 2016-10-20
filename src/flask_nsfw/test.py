#!/usr/bin/env python2

from .app import app
import unittest
from json import loads
from os import path

MODEL_DEF = '../open_nsfw/nsfw_model/deploy.prototxt'
PRETRAINED_MODEL = '../open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel'

def rel (name):
    return path.join(path.dirname(__file__), name)

class TestCase (unittest.TestCase):

    def setUp (self):
        app.config['TESTING'] = False
        self.app = app.test_client()

    def tearDown (self):
        pass

    def test_get (self):
        r = self.app.get('/')
        assert r.status_code == 200
        assert len(r.data) == 438

    def test_post_empty (self):
        r = self.app.post('/')
        assert r.status_code == 400
        r = loads(r.data)
        assert r['message'] == 'No image submitted'

    def test_post_valid_image (self):
        data = { "image": open(rel('../test_data/image.jpg'), 'r') }
        r = self.app.post('/', data=data)
        assert r.status_code == 200
        r = loads(r.data)
        assert r == '0.9039807915687561'

    def test_post_valid_image_and_model (self):
        data = {
            "image": open(rel('../test_data/image.jpg'), 'r'),
            "model_def": open(rel(MODEL_DEF), 'r'),
            "pretrained_model": open(rel(PRETRAINED_MODEL), 'r')
        }
        r = self.app.post('/', data=data)
        assert r.status_code == 200
        r = loads(r.data)
        assert r == '0.9039807915687561'

    def test_post_invalid_image (self):
        data = { "image": open(rel('../test_data/not_an_image.jpg'), 'r') }
        r = self.app.post('/', data=data)
        assert r.status_code == 400
        r = loads(r.data)
        assert r['message'] == 'Could not process image'

    def test_post_only_model (self):
        data = {
            "model_def": open(rel(MODEL_DEF), 'r'),
            "pretrained_model": open(rel(PRETRAINED_MODEL), 'r')
        }
        r = self.app.post('/', data=data)
        assert r.status_code == 400
        r = loads(r.data)
        assert r['message'] == 'No image submitted'

if __name__ == '__main__':
    unittest.main()
