import csv
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shipment_tracking.settings')
django.setup()

from shipments.models import Shipment

def import_csv(file_path):
    """Imports shipment data from a CSV file, adding all entries regardless of duplicates."""
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create a new Shipment object, even if it duplicates existing records
            shipment = Shipment.objects.create(
                tracking_number=row['tracking_number'],
                carrier=row['carrier'],
                sender_address=row['sender_address'],
                receiver_address=row['receiver_address'],
                article_name=row['article_name'],
                article_quantity=row['article_quantity'],
                article_price=row['article_price'],
                SKU=row['SKU'],
                status=row['status'],
            )
            print(f"Shipment with tracking number {row['tracking_number']} added.")

if __name__ == "__main__":
    file_path = 'track1.csv' 
    import_csv(file_path)
