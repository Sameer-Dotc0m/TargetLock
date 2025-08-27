import os
import numpy as np
import tensorflow as tf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.conf import settings

# Load the Keras model once when the app starts
# This is more efficient than loading it on every request.
# The path must be relative to the BASE_DIR, which is the project root
model_path = os.path.join(settings.BASE_DIR, 'api', 'isac_model.keras')
model = tf.keras.models.load_model(model_path)
model._set_inputs(tf.TensorSpec(shape=(None, 10), dtype=tf.float32)) # Set the input shape

class PredictView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to the API. It expects a list of 10 features
        in the request body and returns a prediction.
        """
        try:
            # Get the features from the request body
            # The features should be sent as a list of numbers
            features = request.data.get('features')

            if not isinstance(features, list) or len(features) != 10:
                return Response(
                    {"error": "Invalid features format. Expected a list of 10 numbers."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Convert the list to a NumPy array with the correct shape for the model
            input_data = np.array([features], dtype=np.float32)

            # Make the prediction
            prediction = model.predict(input_data)

            # The prediction is a 2D array, so we extract the first (and only) row
            # and convert it back to a list to send as a JSON response.
            predicted_params = prediction[0].tolist()

            response_data = {
                "prediction": {
                    "range": predicted_params[0],
                    "velocity": predicted_params[1],
                    "azimuth": predicted_params[2]
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def frontend_view(request):
    """
    Renders the frontend HTML page.
    """
    return render(request, 'api/index.html')