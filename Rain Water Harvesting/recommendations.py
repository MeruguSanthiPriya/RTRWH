
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Any, Callable

@dataclass
class RecommendationCategory:
    """A structured representation of a recommendation category."""
    category_id: int
    name: str
    description: str
    recommended_structures: List[str]
    recharge_feasible: bool
    # A dictionary of criteria functions. Each function takes a value and returns True if it matches.
    criteria: Dict[str, Callable[[Any], bool]]

# Define all categories as a list of dataclass instances.
# This now includes the logic for matching each category.
CATEGORIES = [
    RecommendationCategory(
        category_id=1,
        name='Storage Tank Only',
        description='For properties where groundwater recharge is not feasible due to site constraints (e.g., limited open space, low rainfall, or shallow groundwater).',
        recommended_structures=['Above-ground storage tank', 'First flush diverter'],
        recharge_feasible=False,
        criteria={
            'or': [
                ('roof_area', lambda v: v < 50),
                ('open_space', lambda v: v < 10),
                ('rainfall', lambda v: v < 600),
                ('gw_depth', lambda v: v < 3)
            ]
        }
    ),
    RecommendationCategory(
        category_id=2,
        name='Storage + Small Recharge Pit',
        description='Small to medium homes with limited yard space',
        recommended_structures=['Storage tank (3,000–8,000 liters)', '1×1×2 m recharge pit', 'Sand–gravel–boulder filter and silt trap'],
        recharge_feasible=True,
        criteria={
            'roof_area': lambda v: 50 <= v <= 150,
            'open_space': lambda v: 10 <= v <= 25,
            'rainfall': lambda v: 600 <= v <= 1000,
            'gw_depth': lambda v: 3 <= v <= 8,
            'soil_type': lambda v: v.lower() in ['sandy', 'loamy', 'sandy loam']
        }
    ),
    RecommendationCategory(
        category_id=3,
        name='Recharge Pit/Trench + Storage Tank',
        description='Medium-sized houses with adequate open space',
        recommended_structures=['Storage tank (5,000–15,000 liters)', 'Multiple pits (1–2 m deep) or trench (10–20 m)', 'Filtration and desilting mechanisms'],
        recharge_feasible=True,
        criteria={
            'roof_area': lambda v: 150 <= v <= 400,
            'open_space': lambda v: 25 <= v <= 100,
            'rainfall': lambda v: 1000 <= v <= 1400,
            'gw_depth': lambda v: 5 <= v <= 15,
            'soil_type': lambda v: v.lower() in ['sandy', 'loamy']
        }
    ),
    RecommendationCategory(
        category_id=4,
        name='Recharge Shaft / Borewell Recharge',
        description='Large homes, multi-story buildings',
        recommended_structures=['Storage tank (10,000–25,000 liters)', 'Recharge shaft (25–30 m deep)', 'Injection well (5 liters/sec capacity)'],
        recharge_feasible=True,
        criteria={
            'roof_area': lambda v: 400 <= v <= 1000,
            'open_space': lambda v: 50 <= v <= 200,
            'rainfall': lambda v: v > 1000,
            'gw_depth': lambda v: v > 15
        }
    ),
    RecommendationCategory(
        category_id=5,
        name='Recharge Pond / Community Structures',
        description='Institutions, farms, large plots, apartment complexes',
        recommended_structures=['Large storage (25,000–100,000 liters)', 'Percolation pond/tank (10×10×2–3 m)', 'Check dams'],
        recharge_feasible=True,
        criteria={
            'roof_area': lambda v: v > 1000,
            'open_space': lambda v: v > 200,
            'rainfall': lambda v: v > 800,
            'gw_depth': lambda v: 3 <= v <= 20,
            'soil_type': lambda v: v.lower() in ['sandy', 'loamy']
        }
    ),
    RecommendationCategory(
        category_id=6,
        name='Supplementary Only',
        description='For properties with highly restrictive conditions (e.g., very small area, extremely low rainfall, or poor soil infiltration) where a full-scale system is not practical.',
        recommended_structures=['Small storage tank', 'Shared/community rainwater systems', 'Emphasis on water-use efficiency'],
        recharge_feasible=False,
        criteria={
            'or': [
                ('roof_area', lambda v: v < 30),
                ('open_space', lambda v: v < 5),
                ('rainfall', lambda v: v < 500),
                ('infiltration_rate', lambda v: v < 5)
            ]
        }
    )
]

def determine_category(roof_area, open_space, rainfall, soil_type, gw_depth, infiltration_rate):
    """Classify user by iterating through a data-driven set of category rules."""
    inputs = {
        'roof_area': roof_area, 'open_space': open_space, 'rainfall': rainfall,
        'soil_type': soil_type, 'gw_depth': gw_depth, 'infiltration_rate': infiltration_rate
    }

    # Define the order of checking. Restrictive 'OR' categories first.
    category_check_order = [CATEGORIES[5], CATEGORIES[0], CATEGORIES[1], CATEGORIES[2], CATEGORIES[3], CATEGORIES[4]]

    for category in category_check_order:
        # Handle special 'OR' logic
        if 'or' in category.criteria:
            if any(check_func(inputs[key]) for key, check_func in category.criteria['or']):
                matched_category = category
                break
        # Handle standard 'AND' logic
        else:
            if all(check_func(inputs[key]) for key, check_func in category.criteria.items() if key in inputs):
                matched_category = category
                break
    else:
        # Fallback if no category matches, which is unlikely with the current rules.
        matched_category = CATEGORIES[5]

    category = matched_category
    # Return the selected category as a dictionary to maintain compatibility
    return {
        'category': category.category_id,
        'name': category.name,
        'description': category.description,
        'recommended_structures': category.recommended_structures,
        'recharge_feasible': category.recharge_feasible
    }

def calculate_structure_dimensions(runoff_volume, soil_infiltration, available_space, recharge_feasible=True):
    """Suggest structure dimensions based on runoff volume and site conditions."""
    dimensions = {}

    # Only calculate recharge structures if it's feasible for the category
    if recharge_feasible:
        if runoff_volume <= 50000:
            dimensions['pit'] = {
                'length_m': 1.5, 'width_m': 1.5, 'depth_m': 2.5, 'volume_m3': 5.6,
                'material_cost': '₹8,000-15,000'
            }
        elif runoff_volume <= 150000:
            dimensions['pit'] = {
                'length_m': 2.0, 'width_m': 2.0, 'depth_m': 3.0, 'volume_m3': 12.0,
                'material_cost': '₹15,000-25,000'
            }
        if available_space > 50 and runoff_volume > 100000:
            trench_length = min(available_space * 0.3, runoff_volume / 5000)
            dimensions['trench'] = {
                'length_m': trench_length, 'width_m': 1.0, 'depth_m': 2.0, 'volume_m3': trench_length * 2.0,
                'material_cost': f'₹{int(trench_length * 2000)}-{int(trench_length * 3500)}'
            }

    storage_size = min(runoff_volume * 0.3, 25000)
    dimensions['storage'] = {
        'capacity_liters': int(storage_size),
        'diameter_m': round((storage_size / 1000 / 3.14159 * 4 / 3) ** (1/3), 1),
        'material_cost': f'₹{int(storage_size * 12)}-{int(storage_size * 18)}'
    }

    return dimensions

def estimate_costs_and_payback(structure_type, dimensions, annual_runoff, local_water_cost):
    """Calculate construction costs and payback period."""
    cost_structure = {
        'storage_tank': {
            'base_cost': dimensions.get('storage', {}).get('capacity_liters', 5000) * 15,
            'installation': 5000,
            'maintenance_annual': 2000
        },
        'recharge_pit': {
            'base_cost': 15000, 'installation': 8000, 'maintenance_annual': 3000
        },
        'recharge_trench': {
            'base_cost': 25000, 'installation': 12000, 'maintenance_annual': 4000
        }
    }
    
    # Correctly calculate total cost as base + installation
    selected_costs = cost_structure.get(structure_type, cost_structure['storage_tank'])
    total_cost = selected_costs['base_cost'] + selected_costs['installation']
    
    annual_water_value = annual_runoff * local_water_cost
    annual_savings = annual_water_value - selected_costs['maintenance_annual']

    payback_years = total_cost / annual_savings if annual_savings > 0 else float('inf')

    return {
        'total_construction_cost': total_cost,
        'annual_water_value': annual_water_value,
        'annual_net_savings': annual_savings,
        'payback_years': round(payback_years, 1),
        'roi_percentage': round((annual_savings / total_cost) * 100, 1) if total_cost > 0 else 0
    }

def get_purification_recommendations(intended_use, roof_type, location_data):
    """Recommend filtration sequence based on intended use and conditions."""
    base_sequence = [
        "Gutter mesh/screen - Remove leaves, twigs, debris",
        "First-flush diverter - Discard initial dirty runoff (5-10 min)",
        "Silt trap chamber - Allow heavy particles to settle"
    ]

    if intended_use.lower() in ['drinking', 'potable', 'cooking']:
        base_sequence.extend([
            "Multi-layer filter - Sand, gravel, activated charcoal",
            "UV disinfection or chlorination",
            "Optional: RO system for drinking water"
        ])
        maintenance_freq = "Monthly filter cleaning, quarterly media replacement"
        estimated_cost = "₹15,000-30,000 for complete treatment"

    elif intended_use.lower() in ['gardening', 'toilet', 'non-potable']:
        base_sequence.extend([
            "Simple sand-gravel filter",
            "Mesh filter for final screening"
        ])
        maintenance_freq = "Quarterly cleaning, annual media check"
        estimated_cost = "₹5,000-12,000 for basic treatment"

    else:
        base_sequence.append("Sand-gravel-charcoal filter")
        maintenance_freq = "Bi-monthly cleaning"
        estimated_cost = "₹8,000-18,000 for standard treatment"

    return {
        'treatment_sequence': base_sequence,
        'maintenance_schedule': maintenance_freq,
        'estimated_cost': estimated_cost,
        'water_quality_expected': 'Potable' if 'drinking' in intended_use.lower() else 'Non-potable suitable'
    }
