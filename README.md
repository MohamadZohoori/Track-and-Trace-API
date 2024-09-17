# Shipment Tracking API

This is a Django-based API for tracking shipments. It allows users to search for shipments by carrier and tracking number and also provides weather information for the receiver's location.

## Features

- Track shipments by carrier and tracking number.
- View weather data for the receiver's location.
- Caching for weather data to improve performance and reduce external API calls.

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Django 5.x
- pip (Python package installer)
- A `.env` file containing the `WEATHER_API_KEY` (for OpenWeatherMap API)

## Installation

1. **Clone the repository**:

```
git clone <repository-url>
cd shipment_tracking
```

2. **Set up a virtual environment:**:

```
python -m venv venv
source venv/bin/activate  
```

3. **Install the dependencies:**:

```
pip install -r requirements.txt
```


4. **Set up the .env file**:

Create a .env file in the project root with the following content:

```
WEATHER_API_KEY=262d64514ac83c4ea42fb0abb9097730
```

5. **Run the migrations**:

```
python manage.py makemigrations
python manage.py migrate
```
6. **Run the import-data file to import the csv data**:

```
python import_data.py
```

7. **Optional: You can run the tests**:

```
python manage.py test
```

## API Endpoints

### Get Shipments

- **URL**: `/shipments/<carrier>/<tracking_number>/`
- **Method**: `GET`
- **Description**: Fetches all shipments for the given carrier and tracking number. Also retrieves weather data for the receiver's location.

#### Example Request

```bash
GET /shipments/DHL/TN12345678/
