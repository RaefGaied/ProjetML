# Pneumonia Detection API

This API serves a deep learning model for pneumonia detection from chest X-ray images.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
- Copy `.env.example` to `.env`
- Update the variables in `.env` as needed

3. Make sure your model is in the correct location:
- Place your trained model at `models/pneumonia_model.h5`

## Running the API

1. Run locally:
```bash
python app.py
```

2. The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/health`
- Returns the status of the API

### Prediction
- **POST** `/predict`
- Accepts an image file in the request
- Returns prediction results in JSON format

Example request using curl:
```bash
curl -X POST -F "image=@path/to/your/image.jpg" http://localhost:5000/predict
```

Example response:
```json
{
    "pneumonia_probability": 0.85,
    "has_pneumonia": true,
    "confidence": "85.00%"
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 400: Bad Request (missing or invalid image)
- 500: Internal Server Error (processing error)

## Deployment

The API can be deployed to any platform that supports Python/Flask applications. For production:
1. Set `DEBUG=False` in `.env`
2. Use a production-grade WSGI server like Gunicorn
3. Set up proper security measures (HTTPS, authentication, etc.) 