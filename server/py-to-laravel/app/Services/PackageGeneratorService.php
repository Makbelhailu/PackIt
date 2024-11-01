<?php

namespace App\Services;

use App\Models\Product;
use Illuminate\Support\Collection;

class PackageGeneratorService
{
    private $allUsedProducts = [];
    private $maxPackages = 7;

    public function generatePackages(
        float $budget,
        array $essentialItems,
        array $userPreferences,
        Collection $availableProducts
    ): array {
        $this->allUsedProducts = [];
        $packages = [];

        while (count($packages) < $this->maxPackages) {
            // Set new random seed
            mt_srand((int) (microtime(true) * 1000000));
            
            $remainingBudget = $budget;
            $newPackage = $this->generatePackage($availableProducts, $essentialItems, $remainingBudget, $userPreferences);
            
            if (empty($newPackage['items'])) {
                break;
            }

            // Only add package if similarity score is >= 70%
            if ($newPackage['score'] >= 70) {
                $packages[] = $newPackage;
            }
        }

        return $packages;
    }

    private function generatePackage(
        Collection $availableProducts,
        array $essentialItems,
        float $remainingBudget,
        array $userPreferences
    ): array {
        $selectedPackage = [];
        $usedProducts = [];

        // Randomize essential items
        $shuffledEssentials = $essentialItems;
        shuffle($shuffledEssentials);

        foreach ($shuffledEssentials as $essential) {
            $matchingProducts = [];

            foreach ($availableProducts as $product) {
                if ($product->name === $essential && !in_array($product->name, $this->allUsedProducts)) {
                    $matches = 0;
                    if ($product->style === $userPreferences['style']) $matches++;
                    if (in_array($product->material, explode(', ', $userPreferences['material']))) $matches++;
                    if (in_array($product->color_palette, explode(', ', $userPreferences['color_palette']))) $matches++;
                    if ($product->quality === $userPreferences['quality']) $matches++;

                    $matchingProducts[] = ['product' => $product, 'matches' => $matches];
                }
            }

            if (!empty($matchingProducts)) {
                $maxMatches = max(array_column($matchingProducts, 'matches'));
                $bestProducts = array_filter($matchingProducts, fn($p) => $p['matches'] === $maxMatches);
                $bestProduct = $bestProducts[array_rand($bestProducts)]['product'];

                if ($bestProduct->price <= $remainingBudget) {
                    $selectedPackage[] = $bestProduct;
                    $remainingBudget -= $bestProduct->price;
                    $usedProducts[] = $bestProduct->name;
                    $this->allUsedProducts[] = $bestProduct->name;
                }
            }
        }

        // Add additional products
        $remainingProducts = $availableProducts->filter(function ($product) use ($remainingBudget, $usedProducts) {
            return $product->price <= $remainingBudget 
                && !in_array($product->name, $usedProducts)
                && !in_array($product->name, $this->allUsedProducts);
        })->shuffle();

        foreach ($remainingProducts as $product) {
            if ($remainingBudget >= $product->price) {
                $selectedPackage[] = $product;
                $remainingBudget -= $product->price;
                $usedProducts[] = $product->name;
                $this->allUsedProducts[] = $product->name;
            }
        }

        return [
            'items' => $selectedPackage,
            'remaining_budget' => $remainingBudget,
            'score' => $this->calculatePackageScore($selectedPackage, $userPreferences)
        ];
    }

    private function calculatePackageScore(array $package, array $userPreferences): float
    {
        $totalMatches = 0;
        $totalProducts = count($package);

        foreach ($package as $product) {
            $matches = 0;
            if ($product->style === $userPreferences['style']) $matches++;
            if (in_array($product->material, explode(', ', $userPreferences['material']))) $matches++;
            if (in_array($product->color_palette, explode(', ', $userPreferences['color_palette']))) $matches++;
            if ($product->quality === $userPreferences['quality']) $matches++;

            $totalMatches += $matches;
        }

        return $totalProducts > 0 
            ? ($totalMatches / ($totalProducts * 4)) * 100 
            : 0;
    }
} 