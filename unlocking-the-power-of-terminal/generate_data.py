import csv
import argparse
from faker import Faker
import numpy as np

# Initialize Faker
fake = Faker()

# Set a seed for reproducibility
SEED = 42  # You can choose any integer value
fake.seed_instance(SEED)
np.random.seed(SEED)

# Define column names
column_names = [
    "event_time",
    "event_type",
    "product_id",
    "category_id",
    "category_code",
    "brand",
    "price",
    "user_id",
    "user_session",
]

# Define weighted probabilities for brands and categories
brands = ["apple", "samsung", "xiaomi", "lenovo", "lg"]
brand_weights = [
    0.5,
    0.3,
    0.1,
    0.05,
    0.05,
]  # Apple is the most popular, followed by Samsung, etc.

categories = [
    "electronics.smartphone",
    "appliances.sewing_machine",
    "computers.laptop",
    "electronics.television",
    "appliances.washing_machine",
]
category_weights = [0.4, 0.1, 0.3, 0.1, 0.1]  # Smartphones and laptops are more common.


# Use generator with `yield` to generate fake data with skewed price and weighted probabilities
def generate_fake_data(num_records):
    event_types = ["view", "cart", "purchase"]

    for _ in range(num_records):
        yield [
            fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
            fake.random.choice(event_types),
            fake.random_int(min=1000000, max=9999999),
            fake.random_int(min=1000000000000000000, max=9999999999999999999),
            np.random.choice(categories, p=category_weights),  # Weighted categories
            np.random.choice(brands, p=brand_weights),  # Weighted brands
            round(
                np.random.lognormal(mean=3, sigma=0.75), 2
            ),  # Left-skewed price distribution
            fake.random_int(min=100000000, max=999999999),
            fake.uuid4(),
        ]


# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate a CSV file with fake data.")

    # Add arguments
    parser.add_argument(
        "-n",
        "--num_records",
        type=int,
        default=10,
        help="Number of records to generate. Default is 10.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="data.csv",
        help="Output file name. Default is 'data.csv'.",
    )

    return parser.parse_args()


# Main function
def main():
    # Get command-line arguments
    args = parse_arguments()

    # Number of records and output file name from arguments
    num_records = args.num_records
    output_file = args.output

    # Write to CSV file while using `yield` to generate data on the fly
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)

        # Write column headers
        writer.writerow(column_names)

        # Generate data row by row and write it to the file
        for row in generate_fake_data(num_records):
            writer.writerow(row)

    print(f"CSV file '{output_file}' generated with {num_records} records.")


# Run the script
if __name__ == "__main__":
    main()
