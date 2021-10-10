import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import *
from sqlalchemy import *

TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdMLU1zd3FCUngwUHZaRUZCbkw1YiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2hydXRpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGZkMzFhMjM1ODJiYzAwNjk0NjEwOGIiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYzMTIyMDA2OSwiZXhwIjoxNjMxMjI3MjY5LCJhenAiOiJvOGdMdzVJQTZjdHRGTGhGSnhMSU5WR29Rbm9oY21xWCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwibW9kaWZ5OmFjdG9ycyIsIm1vZGlmeTptb3ZpZXMiXX0.paUAByVyR35tM9U3po6PsO0T2nf7YOt6m8EI3t4arxxf3PV-Wq0qoOgLCfRIMsMzXo5mYIHpOTvpN0xCRl5lStb4ZrDlZ5S6pz0PUxKj-Y-O481Cc3s9ATy8nkpNdCkI_lUeGnIc_8yrd3y8hy0WXxQx9xlNqktPeBIIrrdDtYSigXRLHcar4rK5adP0PdQfAkKxwoxifaqAZsRvzqIV5kjhotrDqQWVAJGJAP2mNZlrDFamCQgkJN0cKjN4eyDQBDvkQbUZOC_pnFJ3Xd8ZDlfcGCOVkD_R4ldCzeSL3NbZhQmvXmEhFhcr3P5PNan0ph9lf9GB9tpsqcpOFACfaw'
TOKEN_EP = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkdMLU1zd3FCUngwUHZaRUZCbkw1YiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2hydXRpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGZkMzFhMjM1ODJiYzAwNjk0NjEwOGIiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYzMTE5ODkzNSwiZXhwIjoxNjMxMjA2MTM1LCJhenAiOiJvOGdMdzVJQTZjdHRGTGhGSnhMSU5WR29Rbm9oY21xWCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwibW9kaWZ5OmFjdG9ycyIsIm1vZGlmeTptb3ZpZXMiXX0.jfDJDLbiruiygri-GffG5u53qffhJH3hMyhhuswnOf1MsffuS57sxIJeu2yRxr0hKD_cdKpFG8N8UipQUnoNGzd0v56cpPPR74CaKkxB6mNN13wualQGonOmM4-SXIed8pIy5xuhIVScV_j2q6y89CtnXmkhawr77lwVOVphw-mGiARXnKmNW7Qu3RHyUmj8wxY_MzG8WeLLkQbtrv3-7_d-Z_mbSz6mOYDP1pvGGr-VU1TZ6E3VbowHwz9-YDEVQpB6RhNxNHn0xYIaD6LC8sEhRh4BbPEqeMA4x_dmWe11ZWkoWo_tnQqFV4EnAl-I4-nRbinrrKD7IVfcgDmMUg'

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"       
        self.database_path = os.environ.get('DATABASE_URL')
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
    def tearDown(self):
        """Executed after reach test"""
        pass
        
    def test_add_actor(self):
        """Test POST new actor."""

        json_add_actor = {
            
            'firstname' : 'Xyrisso',
            'lastname' : 'Mistry',
            'age' : 29,
            'gender':'male'
        } 
        
        
     
        res = self.client().post('/actors', json = json_add_actor, headers={
                                                            'Authorization': 'Bearer ' + TOKEN
                                                            })
       
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
    def test_get_actor(self):
        """Test GET  actor."""        
     
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
    def test_add_actor_401_error(self):
        """Test POST new actor."""

        json_add_actor = {
            'firstname' : 'Xyrisso',
            'lastname' : 'Mistry',
            'age' : 29,
            'gender':'male'
        } 
     
        res = self.client().post('/actors', json = json_add_actor, headers={
                                                            'Authorization': 'Bearer ' 
                                                            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
    def test_patch_actor(self):
        """Test PATCH existing actors"""
        new_age = {
            'age' : 11
        } 
        res = self.client().patch('/actors/30', json = new_age, headers={
                                                            'Authorization': 'Bearer ' + TOKEN
                                                            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
    def test_patch_actor_401(self):
        """Test PATCH existing actors with 401 ERROR"""
        new_age = {
            'age' : 26
        } 
        res = self.client().patch('/actors/30', json = new_age, headers={
                                                            'Authorization': 'Bearer ' 
                                                            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
        
    def test_z_delete_actor_401(self):
        """Test DELETE existing actors with 401 ERROR"""
        res = self.client().delete('/actors/30', headers={
                                                            'Authorization': 'Bearer ' 
                                                  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
        
    def test_z_delete_actor(self):
        """Test DELETE existing actors with 401 ERROR"""
        res = self.client().delete('/actors/30', headers={'Authorization': 'Bearer ' + TOKEN })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
        
    def test_add_movie(self):
        """Test POST new movie."""
    
        json_add_movie = {
            
            
            'title' : 'test movie xyz',
            'release_date' : '03-03-2021'
        } 
    
        res = self.client().post('/movies', json = json_add_movie, headers={
                                                            'Authorization': 'Bearer ' + TOKEN
                                                            })
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
    def test_get_movie(self):
        """Test GET  movie."""        
        
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
    def test_add_movie_401_error(self):
        """Test POST new movie."""
    
        json_add_movie = {
            
            'title' : 'test movie xyz abc',
            'release_date' : '03-03-2021'
        } 
    
        res = self.client().post('/movies', json = json_add_movie, headers={
                                                            'Authorization': 'Bearer ' 
                                                            })
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
    def test_z_patch_movie(self):
        """Test PATCH existing movies"""
        new_release_date = {
            'release_date' : '21-03-2021'
        } 
        res = self.client().patch('/movies/2', json = new_release_date, headers={
                                                            'Authorization': 'Bearer ' + TOKEN
                                                            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
    def test_patch_movie_401(self):
        """Test PATCH existing movies with 401 ERROR"""
        new_release_date = {
            'release_date' : '21-03-2021'
        } 
        res = self.client().patch('/movies/2', json = new_release_date, headers={
                                                            'Authorization': 'Bearer ' 
                                                            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
        
    def test_z_z_delete_movie_401(self):
        """Test DELETE existing movies with 401 ERROR"""
        res = self.client().delete('/movies/2', headers={
                                                            'Authorization': 'Bearer ' 
                                                            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
        
    def test_z_z_delete_movie(self):
        """Test DELETE existing movies with 401 ERROR"""
        res = self.client().delete('/movies/2', headers={'Authorization': 'Bearer ' + TOKEN })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
        
    
    