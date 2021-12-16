from django.db import models
from numpy.random import random_sample

class CustomModel(models.Model):
    # Put your fields here

    def get_data(self):
        """ 
        Fake Method to generate random data.
        In the real case, this method should arrange
        data to be plotted according to model instance
        fields' values.
        """
        return random_sample(5)