import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

res = client.post(
    '/plan',
    json={
        'event_type': 'Wedding',
        'location': 'Bangalore',
        'budget': 450000,
        'guest_count': 150,
        'preferences': {'cuisine': 'North Indian', 'decor_style': 'Royal'},
    },
).json()

recs = res.get('recommendations', {})
all_names = []
print("=" * 60)
print("FETCHED VENDOR RECOMMENDATIONS BY CATEGORY")
print("=" * 60)

for cat, vendors in recs.items():
    print(f"\n[{cat.upper()}] ({len(vendors)} options)")
    cat_names = []
    for idx, v in enumerate(vendors, 1):
        name = v.get("name")
        rating = v.get("rating")
        price = v.get("price")
        print(f"  {idx}. {name} | {rating} Stars | INR {price:,.2f}")
        all_names.append(name)
        cat_names.append(name)
    assert len(cat_names) == len(set(cat_names)), f"Duplicates in {cat}: {cat_names}"

print("\n" + "=" * 60)
print(f"Total Vendors: {len(all_names)} | Unique Names: {len(set(all_names))}")
print("=" * 60)
assert len(all_names) == len(set(all_names)), "Duplicate vendor names found across categories!"
print("RESULT: ALL VENDOR NAMES ARE 100% DISTINCT AND UNIQUE! [OK]")
