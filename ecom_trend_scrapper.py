# ecom_trend_scraper.py
import os
from scrapegraphai import SmartScraper
import pandas as pd
from datetime import datetime
import json
import re
import streamlit as st

class EcomTrendScraper:
    def __init__(self):
        self.config = {
            "llm": {
                "api_key": os.getenv("GEMINI_API_KEY"),
                "model": "gemini-2.5-pro-exp",
            },
        }
        
        self.trend_prompts = {
            "amazon": """
            Analyze trending fashion products and extract:
            - Product names and descriptions
            - Design patterns (stripes, solids, prints, etc.)
            - Color schemes
            - Material/fabric types
            - Price points
            - Customer ratings and reviews summary
            - Key features and unique selling points
            - Target audience (men, women, kids)
            - Seasonality indications
            Return as structured JSON with design insights for manufacturing.
            """,
            
            "myntra": """
            Extract fashion trend data focusing on:
            - Current popular styles and silhouettes
            - Fabric compositions and materials
            - Color trends and combinations
            - Pattern types (floral, geometric, abstract)
            - Neckline and sleeve styles
            - Occasion wear trends
            - Brand positioning and pricing
            - Customer preference indicators
            Format as JSON suitable for apparel manufacturing planning.
            """,
            
            "flipkart": """
            Analyze fashion trends with emphasis on:
            - Product categories and subcategories
            - Price segmentation
            - Design elements and features
            - Material quality indicators
            - Seasonal trends
            - Customer rating patterns
            - Value propositions
            Return structured data for manufacturing decision making.
            """,
            
            "nykaa": """
            Focus on fashion accessories and apparel:
            - Style trends in fashion category
            - Color palettes
            - Material preferences
            - Price ranges for different segments
            - Customer satisfaction indicators
            - Emerging trends
            Provide JSON output for manufacturing insights.
            """
        }
    
    def scrape_trends_for_manufacturing(self, sites, categories, max_products=20, price_range=(0, 10000), min_rating=4.0):
        """Enhanced scraping specifically for manufacturing insights"""
        
        all_trends = {
            'all_products': [],
            'design_analysis': {},
            'color_analysis': [],
            'price_analysis': {},
            'manufacturing_recommendations': {},
            'competitor_pricing': {}
        }
        
        for site in sites:
            try:
                st.write(f"🔍 Analyzing {site}...")
                
                # Simulated scraping - replace with actual URLs
                mock_url = f"https://{site}.com/trending-fashion"
                prompt = self.trend_prompts.get(site, self.trend_prompts["amazon"])
                
                scraper = SmartScraper(
                    prompt=prompt,
                    source=mock_url,
                    config=self.config
                )
                
                result = scraper.run()
                processed_data = self.process_for_manufacturing(result, site)
                all_trends['all_products'].extend(processed_data['products'])
                
                # Aggregate insights
                self.aggregate_insights(all_trends, processed_data, site)
                
            except Exception as e:
                st.error(f"Error analyzing {site}: {str(e)}")
                continue
        
        # Generate manufacturing recommendations
        all_trends['manufacturing_recommendations'] = self.generate_manufacturing_recommendations(all_trends)
        
        return all_trends
    
    def process_for_manufacturing(self, data, site):
        """Process scraped data for manufacturing insights"""
        
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                data = {"products": [], "trends": []}
        
        # Enhanced processing for manufacturing
        processed_products = []
        for product in data.get('products', []):
            manufacturing_insights = {
                'production_complexity': self.assess_production_complexity(product),
                'material_cost_estimate': self.estimate_material_cost(product),
                'recommended_suppliers': self.suggest_suppliers(product),
                'production_time_estimate': self.estimate_production_time(product)
            }
            
            product['manufacturing_insights'] = manufacturing_insights
            processed_products.append(product)
        
        return {
            'products': processed_products,
            'site_trends': data.get('trends', []),
            'design_elements': data.get('design_elements', {})
        }
    
    def assess_production_complexity(self, product):
        """Assess how complex it would be to manufacture this product"""
        complexity_score = 1  # Simple baseline
        
        # Analyze product description for complexity indicators
        description = product.get('description', '').lower()
        
        if any(word in description for word in ['embroidery', 'printing', 'detailed', 'complex']):
            complexity_score += 2
        if any(word in description for word in ['simple', 'basic', 'plain']):
            complexity_score -= 1
        
        return min(max(complexity_score, 1), 5)  # Scale 1-5
    
    def estimate_material_cost(self, product):
        """Rough estimate of material costs"""
        price = product.get('price', 0)
        # Simple heuristic: material cost ~30-50% of retail price
        return price * 0.4 if price > 0 else "Unknown"
    
    def suggest_suppliers(self, product):
        """Suggest supplier types based on product characteristics"""
        materials = product.get('materials', [])
        suppliers = []
        
        if any('cotton' in mat.lower() for mat in materials):
            suppliers.append("Cotton fabric suppliers")
        if any('synthetic' in mat.lower() for mat in materials):
            suppliers.append("Synthetic material vendors")
        
        return suppliers if suppliers else ["General apparel suppliers"]
    
    def estimate_production_time(self, product):
        """Estimate production timeline"""
        complexity = self.assess_production_complexity(product)
        # Simple to complex: 2-6 weeks
        return f"{complexity + 1} - {complexity + 3} weeks"
    
    def aggregate_insights(self, all_trends, processed_data, site):
        """Aggregate insights from all sites"""
        # Color analysis
        colors = processed_data.get('design_elements', {}).get('colors', [])
        for color in colors:
            all_trends['color_analysis'].append(color)
        
        # Price analysis
        prices = [p.get('price', 0) for p in processed_data['products'] if p.get('price', 0) > 0]
        if prices:
            all_trends['competitor_pricing'][site] = {
                'min': min(prices),
                'max': max(prices),
                'average': sum(prices) / len(prices)
            }
    
    def generate_manufacturing_recommendations(self, all_trends):
        """Generate actionable manufacturing recommendations"""
        
        products = all_trends['all_products']
        
        # Sort by potential profitability (simplified)
        scored_products = []
        for product in products:
            score = 0
            price = product.get('price', 0)
            rating = product.get('rating', 0)
            complexity = product.get('manufacturing_insights', {}).get('production_complexity', 3)
            
            # Simple scoring algorithm
            if price > 0:
                score += (price / 1000) * 2  # Higher price better
            score += rating  # Higher rating better
            score -= complexity  # Lower complexity better
            
            scored_products.append((product, score))
        
        # Get top recommendations
        scored_products.sort(key=lambda x: x[1], reverse=True)
        top_products = [p[0] for p in scored_products[:5]]
        
        return {
            'recommended_products': [p.get('name', 'Unknown') for p in top_products],
            'recommended_materials': self.get_top_materials(products),
            'production_timeline': {
                'Design & Sampling': '2-3 weeks',
                'Material Sourcing': '1-2 weeks',
                'Production': '3-4 weeks',
                'Quality Check': '1 week'
            },
            'estimated_costs': self.estimate_costs(top_products)
        }
    
    def get_top_materials(self, products):
        """Extract most common materials"""
        material_count = {}
        for product in products:
            materials = product.get('materials', [])
            for material in materials:
                material_count[material] = material_count.get(material, 0) + 1
        
        return [mat for mat, count in sorted(material_count.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    def estimate_costs(self, products):
        """Estimate manufacturing costs"""
        avg_material_cost = sum(
            p.get('manufacturing_insights', {}).get('material_cost_estimate', 0) 
            for p in products if isinstance(p.get('manufacturing_insights', {}).get('material_cost_estimate'), (int, float))
        ) / len(products) if products else 0
        
        return {
            'average_material_cost_per_unit': avg_material_cost,
            'estimated_setup_cost': '₹50,000 - ₹1,00,000',
            'minimum_order_quantity': '100-500 units'
        }