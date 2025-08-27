from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class PredictViewTests(TestCase):
    def test_valid_prediction_request(self):
        """
        Tests if a valid POST request to the API returns a 200 OK status
        and a prediction with the correct keys.
        """
        url = reverse('predict_api')
        valid_features = [0.1, -0.5, 1.2, 0.8, 0.3, -0.2, 1.0, 0.4, -0.6, 0.9]
        response = self.client.post(url, {'features': valid_features}, format='json')
        
        # Check that the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the prediction keys are present in the response data
        self.assertIn('prediction', response.data)
        self.assertIn('range', response.data['prediction'])
        self.assertIn('velocity', response.data['prediction'])
        self.assertIn('azimuth', response.data['prediction'])
        
    def test_invalid_features_count(self):
        """
        Tests if an invalid number of features returns a 400 Bad Request status.
        """
        url = reverse('predict_api')
        invalid_features = [0.1, 0.2] # Only 2 features instead of 10
        response = self.client.post(url, {'features': invalid_features}, format='json')
        
        # Check that the request fails with a 400 status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        # python manage.py test