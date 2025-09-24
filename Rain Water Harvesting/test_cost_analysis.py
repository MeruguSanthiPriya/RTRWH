#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recommendations import estimate_costs_and_payback

def test_cost_analysis():
    """Test the new cost analysis function with sample data"""
    print("Testing cost analysis function...")

    # Test with different categories and parameters
    test_cases = [
        {"category_id": 1, "location_type": "urban", "soil_type": "clay", "system_size": 1000},
        {"category_id": 2, "location_type": "rural", "soil_type": "sandy", "system_size": 2000},
        {"category_id": 3, "location_type": "semi-urban", "soil_type": "loamy", "system_size": 1500},
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Category: {test_case['category_id']}, Location: {test_case['location_type']}, Soil: {test_case['soil_type']}, Size: {test_case['system_size']}L")

        try:
            result = estimate_costs_and_payback(**test_case)
            print(f"Total Cost: ₹{result['total_cost']:,.0f}")
            print(f"Subsidy: ₹{result['subsidy_amount']:,.0f}")
            print(f"Net Investment: ₹{result['net_investment']:,.0f}")
            print(f"Payback Period: {result['payback_years']:.1f} years")
            print(f"Annual Savings: ₹{result['annual_savings']:,.0f}")
            print(f"Category Multiplier: {result['category_multiplier']:.2f}x")
            print(f"Total Modifier: {result['total_modifier']:.2f}x")
            print("Component Breakdown:")
            for component, cost in result['component_breakdown'].items():
                print(f"  {component}: ₹{cost:,.0f}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_cost_analysis()