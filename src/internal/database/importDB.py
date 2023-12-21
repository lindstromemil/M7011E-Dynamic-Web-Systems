import csv
import os

from src.internal.models.beverage import Beverage
from src.internal.models.brand import Brand


def insert_brand_from_csv():
    filepath = os.getcwd() + "/src/internal/database/brand_db.csv"
    with open(filepath, "r", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        for row in reader:
            try:
                existingBrand = Brand.objects.get(name=row["name"])

            except Brand.DoesNotExist:
                brand = Brand(name=row["name"], description=row["description"])
                brand.save()


def insert_beverage_from_csv():
    filepath = os.getcwd() + "/src/internal/database/beverage_db.csv"
    with open(filepath, "r", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        for row in reader:
            try:
                existingBrand = Brand.objects.get(name=row["brand"])
            except Brand.DoesNotExist:
                print("Brand does not exist", row["brand"])
                print(f"Add brand {row['brand']} to database first")
                continue
            try:
                existingBeverage = Beverage.objects.get(name=row["name"], brand_id=existingBrand)
            except Beverage.DoesNotExist:
                beverage = Beverage(
                    name=row["name"],
                    description=row["description"],
                    image_path=row["image_path"],
                    bitterness=row["bitterness"],
                    fullness=row["fullness"],
                    sweetness=row["sweetness"],
                    abv=row["abv"],
                    beverageType=row["beverageType"],
                    country=row["country"],
                    brand_id=existingBrand,
                )
                beverage.save()


def insert_db_from_csv():
    print("Inserting brands...")
    insert_brand_from_csv()
    print("Inserting beverages...")
    insert_beverage_from_csv()
    print("Done!")


if __name__ == "__main__":
    insert_db_from_csv()
