# Pneumonia Detection System

A deep learning-based system for detecting pneumonia from chest X-ray images.

## Features

- Upload and analyze chest X-ray images
- Real-time prediction with confidence scores
- Detailed visualization of results
- User-friendly interface

## Deployment

This application is deployed on Streamlit. To run it locally:

1. Clone the repository:
```bash
git clone <your-repo-url>
cd pneumonia-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

- `app.py` - Main Streamlit application
- `requirements.txt` - Project dependencies
- `data/` - Dataset directory
- `models/` - Trained model files
- `.streamlit/` - Streamlit configuration

## API Integration

The application uses a REST API for predictions. Make sure to set the API URL in the application.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
