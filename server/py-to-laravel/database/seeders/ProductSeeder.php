<?php

namespace Database\Seeders;

use App\Models\Product;
use Illuminate\Database\Seeder;

class ProductSeeder extends Seeder
{
    public function run()
    {
        $products = [
            ["Sofa", 1500, "Modern", "Wood", "Neutral", "Standard"],
            ["Refrigerator", 800, "Modern", "Metal", "Neutral", "Standard"],
            // ... Add all other products here
        ];

        foreach ($products as $product) {
            Product::create([
                'name' => $product[0],
                'price' => $product[1],
                'style' => $product[2],
                'material' => $product[3],
                'color_palette' => $product[4],
                'quality' => $product[5],
            ]);
        }
    }
} 