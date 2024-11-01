<?php

namespace App\Http\Controllers;

use App\Models\Product;
use App\Services\PackageGeneratorService;
use Illuminate\Http\Request;

class PackageController extends Controller
{
    private $packageGenerator;

    public function __construct(PackageGeneratorService $packageGenerator)
    {
        $this->packageGenerator = $packageGenerator;
    }

    public function generate(Request $request)
    {
        $budget = 3000;
        $essentialItems = [
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
        ];

        $userPreferences = [
            "style" => "Modern",
            "material" => "Wood, Metal, Fabric",
            "color_palette" => "Neutral, Dark",
            "quality" => "Premium"
        ];

        $availableProducts = Product::all();

        $packages = $this->packageGenerator->generatePackages(
            $budget,
            $essentialItems,
            $userPreferences,
            $availableProducts
        );

        return response()->json([
            'packages' => array_map(function ($package) use ($budget) {
                $totalPrice = collect($package['items'])->sum('price');
                return [
                    'items' => $package['items'],
                    'total_price' => $totalPrice,
                    'similarity_score' => round($package['score'], 2),
                    'remaining_budget' => $budget - $totalPrice
                ];
            }, $packages),
            'total_packages' => count($packages)
        ]);
    }
} 