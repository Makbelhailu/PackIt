from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import random
import time
from main import Product, calculate_package_score, generate_package, generate_all_packages

app = FastAPI()

# Define request models using Pydantic
class Preferences(BaseModel):
    style: str
    material: List[str]
    color_palette: List[str]
    quality: str

class PackageRequest(BaseModel):
    budget: float
    essential_items: List[str]
    preferences: Preferences

# Available products
available_products = [
    Product(1, "Sofa", 40000, "Modern", "Wood", "Neutral", "Standard"),
    Product(2, "Refrigerator", 30000, "Modern", "Metal", "Neutral", "Standard"),
    Product(3, "Washing Machine", 44000, "Modern", "Metal", "Neutral", "Standard"), 
    Product(4, "Microwave Oven", 3000, "Modern", "Metal", "Neutral", "Standard"),
    Product(5, "Television", 24000, "Modern", "Metal", "Neutral", "Standard"),
    Product(6, "Queen Bed Frame", 17000, "Modern", "Wood", "Neutral", "Standard"),
    Product(7, "Office Desk", 9000, "Modern", "Wood", "Neutral", "Standard"),
    Product(8, "Dining Table", 12000, "Traditional", "Wood", "Neutral", "Standard"),
    Product(9, "Coffee Table", 5500, "Modern", "Wood", "Neutral", "Standard"),
    Product(10, "Bookshelf", 3500, "Modern", "Wood", "Neutral", "Standard"),
    Product(11, "Armchair", 10000, "Traditional", "Fabric", "Dark", "Standard"),
    Product(12, "Nightstand", 4000, "Modern", "Wood", "Neutral", "Standard"),
    Product(13, "Dresser", 15000, "Modern", "Wood", "Neutral", "Standard"),
    Product(14, "Bed Mattress", 8000, "Modern", "Foam", "Neutral", "Premium"),
    Product(15, "Desk Lamp", 2000, "Modern", "Metal", "Neutral", "Standard"),
    Product(16, "Entertainment Center", 3000, "Modern", "Wood", "Neutral", "Standard"),
    Product(17, "Bar Stool", 1000, "Modern", "Metal", "Neutral", "Standard"),
    Product(18, "Floor Lamp", 1500, "Traditional", "Metal", "Dark", "Standard"),
    Product(19, "Area Rug", 6000, "Modern", "Fabric", "Neutral", "Standard"),
    Product(20, "Wall Art", 2000, "Modern", "Canvas", "Neutral", "Standard"),
    Product(21, "TV Mount", 2500, "Modern", "Metal", "Neutral", "Standard"),
    Product(22, "Console Table", 6000, "Modern", "Wood", "Neutral", "Standard"),
    Product(23, "Throw Blanket", 1500, "Modern", "Fabric", "Neutral", "Premium"),
    Product(24, "Decorative Pillows Set", 2000, "Modern", "Fabric", "Neutral", "Standard"),
    Product(25, "Media Storage Unit", 7000, "Modern", "Wood", "Neutral", "Standard"),
    Product(26, "Bed Sheets Set", 3000, "Modern", "Fabric", "Neutral", "Premium"),
    Product(27, "Comforter Set", 5000, "Modern", "Fabric", "Neutral", "Premium"),
    Product(28, "Pillows Set", 2500, "Modern", "Foam", "Neutral", "Premium"),
    Product(29, "Bedroom Bench", 8000, "Modern", "Fabric", "Neutral", "Standard"),
    Product(30, "Under-bed Storage", 3500, "Modern", "Fabric", "Neutral", "Standard"),
    Product(31, "Dining Chairs Set", 15000, "Modern", "Wood", "Neutral", "Standard"),
    Product(32, "Table Runner", 1000, "Modern", "Fabric", "Neutral", "Standard"),
    Product(33, "Placemats Set", 1500, "Modern", "Fabric", "Neutral", "Standard"),
    Product(34, "Serving Cart", 7000, "Modern", "Metal", "Neutral", "Standard"),
    Product(35, "China Cabinet", 25000, "Modern", "Wood", "Neutral", "Premium"),
    Product(36, "Ergonomic Chair", 12000, "Modern", "Fabric", "Neutral", "Premium"),
    Product(37, "Desk Pad", 1000, "Modern", "Fabric", "Neutral", "Standard"),
    Product(38, "Cable Management Set", 1500, "Modern", "Plastic", "Neutral", "Standard"),
    Product(39, "Monitor Stand", 2500, "Modern", "Metal", "Neutral", "Standard"),
    Product(40, "Desk Drawer Unit", 5000, "Modern", "Wood", "Neutral", "Standard"),
    Product(41, "Spice Rack", 1500, "Modern", "Metal", "Neutral", "Standard"),
    Product(42, "Kitchen Storage Set", 3000, "Modern", "Plastic", "Neutral", "Standard"),
    Product(43, "Paper Towel Holder", 500, "Modern", "Metal", "Neutral", "Standard"),
    Product(44, "Dish Drying Rack", 2000, "Modern", "Metal", "Neutral", "Standard"),
    Product(45, "Kitchen Mat Set", 2500, "Modern", "Fabric", "Neutral", "Standard"),
    Product(46, "Laundry Sorter", 3000, "Modern", "Fabric", "Neutral", "Standard"),
    Product(47, "Drying Rack", 2500, "Modern", "Metal", "Neutral", "Standard"),
    Product(48, "Laundry Storage Cabinet", 8000, "Modern", "Wood", "Neutral", "Standard"),
    Product(49, "Laundry Counter Top", 5000, "Modern", "Wood", "Neutral", "Standard"),
    Product(50, "Lint Roller Set", 500, "Modern", "Plastic", "Neutral", "Standard"),
    Product(51, "Floating Shelves Set", 3500, "Modern", "Wood", "Neutral", "Standard"),
    Product(52, "Storage Ottoman", 4500, "Modern", "Fabric", "Neutral", "Standard"),
    Product(53, "Drawer Organizers Set", 2000, "Modern", "Plastic", "Neutral", "Standard"),
    Product(54, "Closet System", 12000, "Modern", "Wood", "Neutral", "Premium"),
    Product(55, "Storage Baskets Set", 2500, "Modern", "Fabric", "Neutral", "Standard"),
    Product(56, "Ceiling Fan with Light", 8000, "Modern", "Metal", "Neutral", "Premium"),
    Product(57, "Wall Sconces Set", 4500, "Modern", "Metal", "Neutral", "Standard"),
    Product(58, "LED Strip Lighting", 2000, "Modern", "Plastic", "Neutral", "Standard"),
    Product(59, "Table Lamp Set", 5000, "Modern", "Metal", "Neutral", "Standard"),
    Product(60, "Reading Light", 1500, "Modern", "Metal", "Neutral", "Standard"),
    Product(61, "Key and Mail Organizer", 1500, "Modern", "Wood", "Neutral", "Standard"),
    Product(62, "Shoe Storage Bench", 7000, "Modern", "Wood", "Neutral", "Standard"),
    Product(63, "Coat Rack", 3000, "Modern", "Metal", "Neutral", "Standard"),
    Product(64, "Magazine Rack", 2000, "Modern", "Metal", "Neutral", "Standard"),
    Product(65, "Umbrella Stand", 1500, "Modern", "Metal", "Neutral", "Standard"),
    Product(66, "Decorative Mirrors Set", 8000, "Modern", "Glass", "Neutral", "Premium"),
    Product(67, "Indoor Plants Set", 5000, "Modern", "Ceramic", "Neutral", "Standard"),
    Product(68, "Wall Shelves Set", 6000, "Modern", "Wood", "Neutral", "Standard"),
    Product(69, "Bookends Set", 1500, "Modern", "Metal", "Neutral", "Standard"),
    Product(70, "Photo Frames Set", 3000, "Modern", "Wood", "Neutral", "Standard")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*']
    )

@app.post("/api/generate-package")
async def generate_packages(request: PackageRequest):
    try:
        # Convert preferences to the format expected by the original code
        user_preferences = {
            "style": request.preferences.style,
            "material": ", ".join(request.preferences.material),
            "color_palette": ", ".join(request.preferences.color_palette),
            "quality": request.preferences.quality
        }

        # Generate packages using the function from main.py
        packages = generate_all_packages(
            request.budget,
            request.essential_items,
            7,  # max_packages
            available_products,
            user_preferences
        )

        # Format the response
        formatted_packages = []
        for package in packages:
            total_price = sum(item.price for item in package)
            score = calculate_package_score(package, user_preferences)
            
            formatted_packages.append({
                "items": [
                    {
                        "id": item.id,
                        "name": item.name,
                        "price": item.price,
                        "style": item.style,
                        "material": item.material,
                        "color_palette": item.color_palette,
                        "quality": item.quality
                    } for item in package
                ],
                "total_price": total_price,
                "similarity_score": round(score, 2),
                "remaining_budget": request.budget - total_price
            })

        return {
            "status": "success",
            "packages": formatted_packages,
            "total_packages": len(formatted_packages)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
