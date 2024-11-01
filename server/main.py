import random
import time

class Product:
    def __init__(self, id, name, price, style, material, color_palette, quality):
        self.id = id
        self.name = name
        self.price = price
        self.style = style
        self.material = material
        self.color_palette = color_palette
        self.quality = quality

# Example available products
available_products = [
    Product(1, "Sofa", 1500, "Modern", "Wood", "Neutral", "Standard"),
    Product(2, "Refrigerator", 800, "Modern", "Metal", "Neutral", "Standard"),
    Product(3, "Washing Machine", 600, "Modern", "Metal", "Neutral", "Standard"),
    Product(4, "Microwave Oven", 300, "Modern", "Metal", "Neutral", "Standard"),
    Product(5, "Television", 1200, "Modern", "Metal", "Neutral", "Standard"),
    Product(6, "Queen Bed Frame", 700, "Modern", "Wood", "Neutral", "Standard"),
    Product(7, "Office Desk", 400, "Modern", "Wood", "Neutral", "Standard"),
    Product(8, "Dining Table", 900, "Traditional", "Wood", "Neutral", "Standard"),
    Product(9, "Coffee Table", 250, "Modern", "Wood", "Neutral", "Standard"),
    Product(10, "Bookshelf", 350, "Modern", "Wood", "Neutral", "Standard"),
    Product(11, "Armchair", 600, "Traditional", "Fabric", "Dark", "Standard"),
    Product(12, "Nightstand", 150, "Modern", "Wood", "Neutral", "Standard"),
    Product(13, "Dresser", 700, "Modern", "Wood", "Neutral", "Standard"),
    Product(14, "Bed Mattress", 800, "Modern", "Foam", "Neutral", "Premium"),
    Product(15, "Desk Lamp", 100, "Modern", "Metal", "Neutral", "Standard"),
    Product(16, "Entertainment Center", 1000, "Modern", "Wood", "Neutral", "Standard"),
    Product(17, "Bar Stool", 200, "Modern", "Metal", "Neutral", "Standard"),
    Product(18, "Floor Lamp", 150, "Traditional", "Metal", "Dark", "Standard"),
    Product(19, "Area Rug", 300, "Modern", "Fabric", "Neutral", "Standard"),
    Product(20, "Wall Art", 200, "Modern", "Canvas", "Neutral", "Standard"),
    Product(21, "Shower Curtain", 30, "Modern", "Fabric", "Dark", "Standard"),
    Product(22, "Coffee Maker", 150, "Modern", "Metal", "Neutral", "Standard"),
    Product(23, "Toaster", 80, "Modern", "Metal", "Neutral", "Standard"),
    Product(24, "Blender", 120, "Modern", "Metal", "Neutral", "Standard"),
    Product(25, "Cookware Set", 200, "Modern", "Metal", "Neutral", "Standard"),
    Product(26, "Cutlery Set", 50, "Modern", "Metal", "Neutral", "Standard"),
    Product(27, "Pots and Pans Set", 250, "Modern", "Metal", "Neutral", "Standard"),
    Product(28, "Dishwasher", 1200, "Modern", "Metal", "Neutral", "Premium"),
    Product(29, "Vacuum Cleaner", 300, "Modern", "Plastic", "Neutral", "Standard"),
    Product(30, "Iron", 80, "Modern", "Metal", "Neutral", "Standard"),
    Product(31, "Curtains", 100, "Modern", "Fabric", "Neutral", "Standard"),
    Product(32, "Bedside Lamp", 75, "Modern", "Metal", "Neutral", "Standard"),
    Product(33, "Pet Bed", 100, "Modern", "Fabric", "Neutral", "Standard"),
    Product(34, "Wall Clock", 50, "Modern", "Wood", "Neutral", "Standard"),
    Product(35, "Fan", 150, "Modern", "Plastic", "Neutral", "Standard"),
    Product(36, "Air Purifier", 200, "Modern", "Plastic", "Neutral", "Standard"),
    Product(37, "Plant Pot", 25, "Modern", "Ceramic", "Neutral", "Standard"),
    Product(38, "Outdoor Patio Set", 1500, "Modern", "Wood", "Neutral", "Standard"),
    Product(39, "Fire Pit", 400, "Modern", "Metal", "Dark", "Standard"),
    Product(40, "Grill", 300, "Modern", "Metal", "Dark", "Standard"),
    Product(41, "Garden Tools Set", 100, "Modern", "Metal", "Dark", "Standard"),
    Product(42, "Storage Shed", 700, "Traditional", "Metal", "Dark", "Standard"),
]

# User input data
budget = 3000
essential_items = [
    "Sofa",
    "Queen Bed Frame",
    "Office Desk",
    "Dining Table",
    "Washing Machine",
    "Microwave Oven",
    "Television",
    "Armchair",
    "Nightstand",
    "Refrigerator"
]

# User preferences
user_preferences = {
    "style": "Modern",
    "material": "Wood, Metal, Fabric",
    "color_palette": "Neutral, Dark",
    "quality": "Premium"
}

# Prepare to store selected packages
packages = []
max_packages = 7
all_used_products = set()

# Function to calculate the score for a package
def calculate_package_score(package, user_preferences):
    total_matches = 0
    total_products = len(package)

    for product in package:
        matches = 0
        if product.style == user_preferences["style"]:
            matches += 1
        if product.material in user_preferences["material"].split(", "):
            matches += 1
        if product.color_palette in user_preferences["color_palette"].split(", "):
            matches += 1
        if product.quality == user_preferences["quality"]:
            matches += 1
        
        total_matches += matches

    if total_products > 0:
        average_score = (total_matches / (total_products * 4)) * 100
    else:
        average_score = 0  # No products means no score

    return average_score

def generate_package(available_products, essential_items, remaining_budget):
    selected_package = []
    used_products = set()

    # Randomize the order of essential items
    shuffled_essentials = essential_items.copy()
    random.shuffle(shuffled_essentials)

    for essential in shuffled_essentials:
        matching_products = []

        for product in available_products:
            # Check if product matches the essential item
            if product.name == essential and product.name not in all_used_products:
                matches = 0
                if product.style == user_preferences["style"]:
                    matches += 1
                if product.material in user_preferences["material"].split(", "):
                    matches += 1
                if product.color_palette in user_preferences["color_palette"].split(", "):
                    matches += 1
                if product.quality == user_preferences["quality"]:
                    matches += 1
                
                matching_products.append((product, matches))

        # Randomly select from products that have the highest match score
        if matching_products:
            max_matches = max(matches for _, matches in matching_products)
            best_products = [p for p, m in matching_products if m == max_matches]
            best_product = random.choice(best_products)

            if best_product.price <= remaining_budget:
                selected_package.append(best_product)
                remaining_budget -= best_product.price
                used_products.add(best_product.name)
                all_used_products.add(best_product.name)
                available_products.remove(best_product)

    # Randomize additional products selection
    remaining_products = [p for p in available_products 
                            if p.price <= remaining_budget 
                            and p.name not in used_products 
                            and p.name not in all_used_products]
    
    # Shuffle the remaining products
    random.shuffle(remaining_products)

    for product in remaining_products:
        if remaining_budget >= product.price:
            selected_package.append(product)
            remaining_budget -= product.price
            used_products.add(product.name)
            all_used_products.add(product.name)

    return selected_package, remaining_budget

def generate_all_packages(budget, essential_items, max_packages, available_products, user_preferences):
    packages = []
    all_used_products.clear()  # Reset the global set
    
    while len(packages) < max_packages:
        random.seed(time.time())
        remaining_budget = budget
        new_package, remaining_budget = generate_package(available_products.copy(), essential_items, remaining_budget)
        
        if not new_package:
            break
            
        packages.append(new_package)
    
    return packages

# Generate up to max_packages
packages = generate_all_packages(budget, essential_items, max_packages, available_products, user_preferences)
if __name__ == "__main__":
# Modify the final output section to help debug
    for idx, package in enumerate(packages):
        print(f"=== Package {idx + 1} ===")
        total_price = 0
        for item in package:
            print(f"Item: {item.name}, Price: ${item.price}")
            total_price += item.price
        score = calculate_package_score(package, user_preferences)
        print(f"Total Price: ${total_price}")
        print(f"Package similarity Score: {score:.2f}%") 
        print(f"Remaining Budget: ${budget - total_price}\n")

        # Print a summary of packages generated
    print(f"Total Packages Generated: {len(packages)}")