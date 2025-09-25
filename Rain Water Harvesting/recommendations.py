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
        name='Above-Ground Storage Tank System',
        description='For properties where groundwater recharge is not feasible due to site constraints (e.g., limited open space, low rainfall, or shallow groundwater).',
        recommended_structures=['Above-ground storage tank (500–2,000 liters)', 'First flush diverter', 'Basic filtration unit'],
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
        name='Recharge Pit with Storage Tank System',
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
        name='Recharge Trench with Storage Tank System',
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
        name='Recharge Shaft/Borewell System',
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
        name='Recharge Pond/Community System',
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
        name='Supplementary Storage System',
        description='For properties with highly restrictive conditions (e.g., very small area, extremely low rainfall, or poor soil infiltration) where a full-scale system is not practical.',
        recommended_structures=['Small storage tank (200–1,000 liters)', 'Shared/community rainwater systems', 'Water-use efficiency measures'],
        recharge_feasible=False,
        criteria={
            'or': [
                ('roof_area', lambda v: v < 30),
                ('open_space', lambda v: v < 5),
                ('rainfall', lambda v: v < 500),
                ('infiltration_rate', lambda v: v < 5)
            ]
        }
    ),
    RecommendationCategory(
        category_id=7,
        name='Urban High-Rise Rooftop System',
        description='Multi-story buildings, condominiums, and urban residential complexes with limited ground space',
        recommended_structures=['Elevated storage tanks (5,000–20,000 liters)', 'Rooftop recharge systems', 'Modular filtration units', 'Pressure booster systems'],
        recharge_feasible=True,
        criteria={
            'roof_area': lambda v: v > 200,
            'open_space': lambda v: v < 50,  # Limited ground space
            'rainfall': lambda v: v > 600,
            'building_type': lambda v: v.lower() in ['apartment', 'condominium', 'high-rise', 'multi-story']
        }
    ),
    RecommendationCategory(
        category_id=8,
        name='Commercial Underground Tank System',
        description='Office buildings, shopping centers, and commercial establishments with high occupancy',
        recommended_structures=['Large underground tanks (10,000–50,000 liters)', 'Advanced filtration systems', 'Dual plumbing systems', 'Water quality monitoring'],
        recharge_feasible=True,
        criteria={
            'roof_area': lambda v: 500 <= v <= 5000,
            'occupancy': lambda v: v > 50,  # People per day
            'water_demand': lambda v: v.lower() in ['high', 'commercial'],
            'rainfall': lambda v: v > 700
        }
    ),
    RecommendationCategory(
        category_id=9,
        name='Educational Institution System',
        description='Schools, colleges, universities with large catchment areas and educational water use',
        recommended_structures=['Large storage tanks (20,000–100,000 liters)', 'Educational demonstration systems', 'Greywater integration', 'Student participation features'],
        recharge_feasible=True,
        criteria={
            'roof_area': lambda v: 1000 <= v <= 10000,
            'open_space': lambda v: 100 <= v <= 1000,
            'building_type': lambda v: v.lower() in ['school', 'college', 'university', 'educational'],
            'rainfall': lambda v: v > 600
        }
    ),
    RecommendationCategory(
        category_id=10,
        name='Healthcare Sterile Storage System',
        description='Hospitals, clinics, medical centers requiring high water quality standards',
        recommended_structures=['Sterile storage systems (5,000–30,000 liters)', 'Advanced multi-stage filtration', 'UV disinfection', 'Emergency backup systems', 'Water quality testing labs'],
        recharge_feasible=True,
        criteria={
            'roof_area': lambda v: 500 <= v <= 2000,
            'water_quality_required': lambda v: v.lower() in ['drinking', 'medical', 'sterile'],
            'building_type': lambda v: v.lower() in ['hospital', 'clinic', 'medical', 'healthcare'],
            'rainfall': lambda v: v > 800
        }
    ),
    RecommendationCategory(
        category_id=11,
        name='Industrial Process Water System',
        description='Factories, warehouses, manufacturing facilities with process water needs',
        recommended_structures=['Large industrial tanks (50,000–200,000 liters)', 'Pre-treatment systems', 'Process water integration', 'Sludge management systems'],
        recharge_feasible=True,
        criteria={
            'roof_area': lambda v: 2000 <= v <= 50000,
            'water_usage': lambda v: v.lower() in ['industrial', 'process', 'manufacturing'],
            'open_space': lambda v: 200 <= v <= 2000,
            'rainfall': lambda v: v > 600
        }
    ),
    RecommendationCategory(
        category_id=12,
        name='Community Shared Tank System',
        description='Village communities, small settlements with shared water systems',
        recommended_structures=['Community storage tanks (10,000–50,000 liters)', 'Shared recharge structures', 'Village-level distribution', 'Community maintenance programs'],
        recharge_feasible=True,
        criteria={
            'roof_area': lambda v: 200 <= v <= 2000,  # Combined village roofs
            'population': lambda v: 50 <= v <= 1000,
            'location_type': lambda v: v.lower() in ['rural', 'village', 'community'],
            'rainfall': lambda v: v > 500
        }
    ),
    RecommendationCategory(
        category_id=13,
        name='Coastal Elevated Storage System',
        description='Coastal areas and islands with saline groundwater and specific water challenges',
        recommended_structures=['Elevated storage tanks (2,000–10,000 liters)', 'Saltwater intrusion barriers', 'Corrosion-resistant materials', 'Desalination integration'],
        recharge_feasible=False,  # Limited recharge due to saline water
        criteria={
            'location_type': lambda v: v.lower() in ['coastal', 'island', 'beach', 'marine'],
            'gw_quality': lambda v: v.lower() in ['saline', 'brackish', 'coastal'],
            'rainfall': lambda v: v > 800,  # Often high rainfall in coastal areas
            'roof_area': lambda v: 50 <= v <= 500
        }
    ),
    RecommendationCategory(
        category_id=14,
        name='Green Building Integrated System',
        description='Sustainable buildings, green certified structures with integrated environmental systems',
        recommended_structures=['Green roof integration', 'Permeable paving connection', 'Solar-powered pumps', 'Smart monitoring systems', 'Biodiversity features'],
        recharge_feasible=True,
        criteria={
            'building_certification': lambda v: v.lower() in ['green', 'leed', 'eco', 'sustainable'],
            'roof_type': lambda v: v.lower() in ['green', 'vegetated', 'eco-roof'],
            'open_space': lambda v: v > 20,
            'rainfall': lambda v: v > 600
        }
    ),
    RecommendationCategory(
        category_id=15,
        name='Retrofit Compact System',
        description='Modifying existing buildings without RWH systems to add rainwater harvesting',
        recommended_structures=['Compact storage solutions (1,000–5,000 liters)', 'Minimal excavation recharge', 'Integration with existing plumbing', 'Non-invasive installation methods'],
        recharge_feasible=True,
        criteria={
            'building_age': lambda v: (
                (isinstance(v, (int, float)) and v > 10) or
                (isinstance(v, str) and v.lower() in ['old', 'heritage', 'existing'])
            ),  # Existing buildings (numeric years or categorical)
            'modification_type': lambda v: v.lower() in ['retrofit', 'existing', 'modification'],
            'space_constraints': lambda v: v.lower() in ['limited', 'constrained', 'urban'],
            'roof_area': lambda v: 50 <= v <= 1000
        }
    ),
    RecommendationCategory(
        category_id=16,
        name='Emergency Portable System',
        description='Temporary or emergency water systems for disaster-affected areas',
        recommended_structures=['Portable storage tanks (500–5,000 liters)', 'Quick-deploy filtration', 'Mobile recharge systems', 'Temporary distribution networks'],
        recharge_feasible=True,
        criteria={
            'usage_type': lambda v: v.lower() in ['emergency', 'disaster', 'relief', 'temporary'],
            'deployment_time': lambda v: v.lower() in ['urgent', 'emergency', 'quick'],
            'rainfall': lambda v: v > 400,  # Can work with lower rainfall in emergencies
            'population_served': lambda v: v > 20
        }
    )
]

def determine_category(roof_area, open_space, rainfall, soil_type, gw_depth, infiltration_rate,
                      user_preferences=None, building_age=None, occupancy=None, modification_type=None,
                      space_constraints=None, usage_type=None, deployment_time=None, population_served=None,
                      building_certification=None, roof_type=None, location_type=None, gw_quality=None,
                      water_quality_required=None, water_demand=None, building_type=None):
    """
    Enhanced category determination using scoring and multi-criteria analysis.

    Returns primary recommendation + alternatives with confidence scores.
    """
    inputs = {
        'roof_area': roof_area,
        'open_space': open_space,
        'rainfall': rainfall,
        'soil_type': soil_type.lower() if soil_type else 'unknown',
        'gw_depth': gw_depth,
        'infiltration_rate': infiltration_rate,
        'building_age': building_age,
        'occupancy': occupancy,
        'modification_type': modification_type,
        'space_constraints': space_constraints,
        'usage_type': usage_type,
        'deployment_time': deployment_time,
        'population_served': population_served,
        'building_certification': building_certification,
        'roof_type': roof_type.lower() if isinstance(roof_type, str) else roof_type,
        'location_type': location_type,
        'gw_quality': gw_quality,
        'water_quality_required': water_quality_required,
        'water_demand': water_demand,
        'building_type': building_type.lower() if isinstance(building_type, str) else building_type
    }
    # Remove None values to avoid spurious penalties
    inputs = {k: v for k, v in inputs.items() if v is not None}

    # User preferences (optional) - complexity only
    preferences = user_preferences or {}
    complexity_preference = preferences.get('complexity', 'balanced')  # 'simple', 'balanced', 'advanced'

    category_scores = []

    for category in CATEGORIES:
        score = 0
        match_factors = []
        mismatch_factors = []

        # Evaluate each criterion
        if 'or' in category.criteria:
            # OR logic - any matching criterion gives points
            or_matches = []
            for key, check_func in category.criteria['or']:
                if key in inputs and check_func(inputs[key]):
                    or_matches.append(key)
                    score += 30  # Points for OR match

            if or_matches:
                match_factors.extend([f"Critical factor: {factor}" for factor in or_matches])
            else:
                mismatch_factors.append("No critical factors match")
                score -= 50  # Penalty for OR categories that don't match
        else:
            # AND logic - flexible matching with weighted scoring
            total_criteria = len(category.criteria)
            matched_criteria = 0
            partial_matches = 0  # Criteria that are "close" to matching
            failed_criteria = 0

            for key, check_func in category.criteria.items():
                if key in inputs:
                    value = inputs[key]
                    if check_func(value):
                        matched_criteria += 1
                        score += 25  # Full points for matching criterion
                        match_factors.append(f"{key}: {value}")
                    else:
                        # Check for "close" matches (within 20% of boundary)
                        if _is_close_match(key, value, category.category_id):
                            partial_matches += 1
                            score += 10  # Partial points for close matches
                            match_factors.append(f"{key}: {value} (close match)")
                        else:
                            failed_criteria += 1
                            score -= 15  # Reduced penalty for failed criteria
                            mismatch_factors.append(f"{key}: {value} (expected different range)")
                else:
                    score -= 5  # Reduced penalty for missing data

            # Bonus for complete or near-complete matches
            if matched_criteria == total_criteria and failed_criteria == 0:
                score += 25  # Complete match bonus
                match_factors.append("Complete criteria match")
            elif matched_criteria + partial_matches >= total_criteria - 1 and failed_criteria <= 1:
                score += 10  # Near-complete match bonus
                match_factors.append("Near-complete criteria match")

        # Adjust score based on complexity preference only
        if complexity_preference == 'simple' and not category.recharge_feasible:
            score += 10  # Prefer storage-only for simple maintenance
        elif complexity_preference == 'advanced' and category.recharge_feasible:
            score += 10  # Prefer recharge systems for advanced users

        # Calculate confidence percentage
        max_possible_score = 100
        confidence = min(100, max(0, (score / max_possible_score) * 100))

        category_scores.append({
            'category': category,
            'score': score,
            'confidence': round(confidence, 1),
            'match_factors': match_factors,
            'mismatch_factors': mismatch_factors,
            'recommendation_reason': _generate_recommendation_reason(category, match_factors, mismatch_factors)
        })

    # Sort by score (highest first)
    category_scores.sort(key=lambda x: x['score'], reverse=True)

    # Return top recommendation with alternatives
    result = {
        'primary': category_scores[0],
        'alternatives': category_scores[1:3],  # Top 2 alternatives
        'all_scores': category_scores  # For debugging/analysis
    }

    return result

def _is_close_match(key, value, category_id):
    """
    Check if a value is "close" to matching a category's criteria (within 20% of boundary).
    This allows for more flexible category matching.
    """
    # Define acceptable ranges for each category and parameter
    close_ranges = {
        2: {  # Category 2: Storage + Small Recharge Pit
            'roof_area': (40, 180),  # Extended from (50, 150) to allow overlap
            'open_space': (8, 35),   # Extended from (10, 25)
            'rainfall': (480, 1200), # Extended from (600, 1000)
            'gw_depth': (2.4, 9.6),  # Extended from (3, 8)
        },
        3: {  # Category 3: Recharge Pit/Trench + Storage Tank
            'roof_area': (120, 480), # Extended from (150, 400) to allow overlap
            'open_space': (20, 120),  # Extended from (25, 100)
            'rainfall': (800, 1680), # Extended from (1000, 1400)
            'gw_depth': (4, 18),     # Extended from (5, 15)
        },
        4: {  # Category 4: Recharge Shaft / Borewell Recharge
            'roof_area': (320, 1200), # Extended from (400, 1000)
            'open_space': (40, 240),  # Extended from (50, 200)
            'rainfall': (800, float('inf')), # Any high rainfall
            'gw_depth': (12, float('inf')), # Deep groundwater
        },
        5: {  # Category 5: Recharge Pond / Community Structures
            'roof_area': (800, float('inf')), # Very large roofs
            'open_space': (160, float('inf')), # Large open spaces
            'rainfall': (640, float('inf')), # Any rainfall above minimum
            'gw_depth': (2.4, 24),   # Wide range
        },
        6: {  # Category 6: Supplementary Only
            'roof_area': (0, 36),   # Very small roofs
            'open_space': (0, 6),   # Very limited space
            'rainfall': (0, 600),   # Very low rainfall
            'infiltration_rate': (0, 6), # Poor infiltration
        },
        7: {  # Category 7: Urban High-Rise / Apartment Complex
            'roof_area': (160, float('inf')), # Large roof areas
            'open_space': (0, 60),   # Very limited ground space
            'rainfall': (480, float('inf')), # Urban areas often have varied rainfall
        },
        8: {  # Category 8: Commercial / Office Building System
            'roof_area': (400, 6000), # Extended commercial roof ranges
            'rainfall': (560, float('inf')), # Commercial areas
        },
        9: {  # Category 9: Educational Institution System
            'roof_area': (800, 12000), # Large educational buildings
            'open_space': (80, 1200),  # School grounds
            'rainfall': (480, float('inf')), # Educational institutions
        },
        10: {  # Category 10: Healthcare Facility System
            'roof_area': (400, 2400), # Hospital roof ranges
            'rainfall': (640, float('inf')), # Healthcare facilities
        },
        11: {  # Category 11: Industrial / Manufacturing System
            'roof_area': (1600, 60000), # Very large industrial roofs
            'open_space': (160, 2400),  # Industrial complexes
            'rainfall': (480, float('inf')), # Industrial areas
        },
        12: {  # Category 12: Rural Village / Community System
            'roof_area': (160, 2400), # Combined village roofs
            'rainfall': (400, float('inf')), # Rural areas
        },
        13: {  # Category 13: Coastal / Island System
            'roof_area': (40, 600),  # Coastal property ranges
            'rainfall': (640, float('inf')), # Coastal areas often high rainfall
        },
        14: {  # Category 14: Green Building / Eco-Friendly System
            'open_space': (16, float('inf')), # Green buildings have space
            'rainfall': (480, float('inf')), # Eco-friendly buildings
        },
        15: {  # Category 15: Retrofit / Existing Building System
            'roof_area': (40, 1200), # Retrofit ranges
        },
        16: {  # Category 16: Emergency / Disaster Relief System
            'rainfall': (320, float('inf')), # Can work with lower rainfall in emergencies
        }
    }

    if category_id not in close_ranges or key not in close_ranges[category_id]:
        return False

    min_val, max_val = close_ranges[category_id][key]
    return min_val <= value <= max_val
    """
    Enhanced category determination using scoring and multi-criteria analysis.

    Returns primary recommendation + alternatives with confidence scores.
    """
    inputs = {
        'roof_area': roof_area, 'open_space': open_space, 'rainfall': rainfall,
        'soil_type': soil_type.lower() if soil_type else 'unknown',
        'gw_depth': gw_depth, 'infiltration_rate': infiltration_rate
    }

    # User preferences (optional) - complexity only
    preferences = user_preferences or {}
    complexity_preference = preferences.get('complexity', 'balanced')  # 'simple', 'balanced', 'advanced'

    category_scores = []

    for category in CATEGORIES:
        score = 0
        match_factors = []
        mismatch_factors = []

        # Evaluate each criterion
        if 'or' in category.criteria:
            # OR logic - any matching criterion gives points
            or_matches = []
            for key, check_func in category.criteria['or']:
                if key in inputs and check_func(inputs[key]):
                    or_matches.append(key)
                    score += 30  # Points for OR match

            if or_matches:
                match_factors.extend([f"Critical factor: {factor}" for factor in or_matches])
            else:
                mismatch_factors.append("No critical factors match")
                score -= 50  # Penalty for OR categories that don't match
        else:
            # AND logic - flexible matching with weighted scoring
            total_criteria = len(category.criteria)
            matched_criteria = 0
            partial_matches = 0  # Criteria that are "close" to matching
            failed_criteria = 0

            for key, check_func in category.criteria.items():
                if key in inputs:
                    value = inputs[key]
                    if check_func(value):
                        matched_criteria += 1
                        score += 25  # Full points for matching criterion
                        match_factors.append(f"{key}: {value}")
                    else:
                        # Check for "close" matches (within 20% of boundary)
                        if _is_close_match(key, value, category.category_id):
                            partial_matches += 1
                            score += 10  # Partial points for close matches
                            match_factors.append(f"{key}: {value} (close match)")
                        else:
                            failed_criteria += 1
                            score -= 15  # Reduced penalty for failed criteria
                            mismatch_factors.append(f"{key}: {value} (expected different range)")
                else:
                    score -= 5  # Reduced penalty for missing data

            # Bonus for complete or near-complete matches
            if matched_criteria == total_criteria and failed_criteria == 0:
                score += 25  # Complete match bonus
                match_factors.append("Complete criteria match")
            elif matched_criteria + partial_matches >= total_criteria - 1 and failed_criteria <= 1:
                score += 10  # Near-complete match bonus
                match_factors.append("Near-complete criteria match")

        # Adjust score based on complexity preference only
        if complexity_preference == 'simple' and not category.recharge_feasible:
            score += 10  # Prefer storage-only for simple maintenance
        elif complexity_preference == 'advanced' and category.recharge_feasible:
            score += 10  # Prefer recharge systems for advanced users

        # Calculate confidence percentage
        max_possible_score = 100
        confidence = min(100, max(0, (score / max_possible_score) * 100))

        category_scores.append({
            'category': category,
            'score': score,
            'confidence': round(confidence, 1),
            'match_factors': match_factors,
            'mismatch_factors': mismatch_factors,
            'recommendation_reason': _generate_recommendation_reason(category, match_factors, mismatch_factors)
        })

    # Sort by score (highest first)
    category_scores.sort(key=lambda x: x['score'], reverse=True)

    # Return top recommendation with alternatives
    result = {
        'primary': category_scores[0],
        'alternatives': category_scores[1:3],  # Top 2 alternatives
        'all_scores': category_scores  # For debugging/analysis
    }

    return result


def _generate_recommendation_reason(category, match_factors, mismatch_factors):
    """Generate human-readable explanation for the recommendation."""
    reasons = []

    if match_factors:
        reasons.append(f"Matches {len(match_factors)} key criteria: {', '.join(match_factors[:2])}")

    if mismatch_factors and len(mismatch_factors) <= 2:
        reasons.append(f"Some criteria don't match: {', '.join(mismatch_factors[:2])}")

    # Add category-specific insights
    if category.category_id == 1:
        reasons.append("Best for constrained spaces with limited recharge potential")
    elif category.category_id == 2:
        reasons.append("Balances storage with simple recharge for small to medium properties")
    elif category.category_id in [3, 4]:
        reasons.append("Comprehensive system for medium to large properties with good recharge potential")
    elif category.category_id == 5:
        reasons.append("Large-scale solution for institutions or community use")

    return ". ".join(reasons)


    return result

def calculate_harvesting_potential(roof_area_m2, rainfall_mm, roof_type):
    """
    Calculate the annual water harvesting potential.

    Formula: Harvestable Water = Rooftop Area × Annual Rainfall × Runoff Coefficient

    Args:
        roof_area_m2 (float): Rooftop area in square meters
        rainfall_mm (float): Annual rainfall in millimeters
        roof_type (str): Type of roof material

    Returns:
        dict: Contains annual_liters, runoff_coefficient, and formatted message
    """
    # Debug: print input values
    # print(f"DEBUG: roof_area_m2={roof_area_m2}, rainfall_mm={rainfall_mm}, roof_type={roof_type}")

    # Runoff coefficients based on roof type (typical values for different materials)
    runoff_coefficients = {
        'concrete': 0.85,      # Smooth concrete roofs
        'asbestos': 0.80,      # Asbestos/cement sheets
        'metal': 0.90,         # Metal roofs (high runoff)
        'tile': 0.75,          # Clay/concrete tiles
        'shingles': 0.80,      # Asphalt shingles
        'green': 0.60,         # Green/vegetated roofs (lower runoff due to absorption)
        'flat': 0.82,          # General flat roofs
        'pitched': 0.88,       # Pitched roofs
    }

    # Get runoff coefficient, default to 0.85 if roof type not found
    roof_type_lower = str(roof_type).lower() if roof_type else 'concrete'
    runoff_coefficient = runoff_coefficients.get(roof_type_lower, 0.85)

    # Calculate annual harvestable water volume in liters
    # Formula: Area (m²) × Rainfall (mm) × Runoff Coefficient
    annual_liters = roof_area_m2 * rainfall_mm * runoff_coefficient

    # print(f"DEBUG: runoff_coefficient={runoff_coefficient}, annual_liters={annual_liters}")

    return {
        'annual_liters': round(annual_liters, 0),
        'runoff_coefficient': runoff_coefficient,
        'monthly_average': round(annual_liters / 12, 0),
        'daily_average': round(annual_liters / 365, 1),
        'formatted_message': f"You can harvest approximately {round(annual_liters):,} liters/year"
    }

def get_category_recommendations_with_preferences(user_data, location_data, user_preferences=None):
    """
    Enhanced category recommendation that considers user preferences and provides detailed reasoning.

    Parameters:
    - user_data: Dict with roof_area, open_space, household_size, etc.
    - location_data: Dict with rainfall, soil_type, gw_depth, etc.
    - user_preferences: Dict with complexity_preference, etc. (budget removed)
    """
    # Extract parameters
    roof_area = user_data.get('roof_area', 100)
    open_space = user_data.get('open_space', 20)
    rainfall = location_data.get('Rainfall_mm', 1000)
    soil_type = location_data.get('Soil_Type', 'Loamy')
    gw_depth = location_data.get('Groundwater_Depth_m', 10)
    infiltration_rate = location_data.get('Infiltration_Rate_mm_per_hr', 15)

    # Get scored recommendations
    recommendations = determine_category(
        roof_area, open_space, rainfall, soil_type, gw_depth, infiltration_rate,
        user_preferences
    )

    # Format for API response
    primary = recommendations['primary']
    alternatives = recommendations['alternatives']

    return {
        'recommended_category': {
            'id': primary['category'].category_id,
            'name': primary['category'].name,
            'description': primary['category'].description,
            'confidence_score': primary['confidence'],
            'recommendation_reason': primary['recommendation_reason'],
            'structures': primary['category'].recommended_structures,
            'recharge_feasible': primary['category'].recharge_feasible
        },
        'alternative_categories': [
            {
                'id': alt['category'].category_id,
                'name': alt['category'].name,
                'confidence_score': alt['confidence'],
                'reason': alt['recommendation_reason']
            } for alt in alternatives
        ],
        'recommendation_logic': {
            'scoring_factors': ['roof_area', 'open_space', 'rainfall', 'soil_type', 'gw_depth'],
            'user_preferences_considered': bool(user_preferences),
            'total_categories_evaluated': len(CATEGORIES)
        }
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

def estimate_costs_and_payback(category_id: int, location_type: str = 'urban', soil_type: str = 'loamy', system_size: float = 1000, intended_use: str = 'general'):
    """
    Comprehensive cost estimation based on detailed component pricing from cost analysis document.
    Includes cost modifiers for location, soil type, and other factors.
    Uses exact category costs and payback data from the provided analysis.

    Args:
        category_id: Category ID (1-6) determining system complexity
        location_type: 'urban', 'rural', or 'semi-urban'
        soil_type: 'clay', 'sandy', or 'loamy'
        system_size: System capacity in liters (used for subsidy calculation)
        intended_use: Primary intended use of harvested water

    Returns:
        Dictionary with detailed cost breakdown and financial analysis
    """
    # Exact category costs from the document
    category_costs = {
        1: {
            'total_cost': 49000,
            'components': {
                'storage_tank': 20000,
                'filter_unit': 8000,
                'pipes_fittings': 6000,
                'first_flush': 3000,
                'labour': 12000
            }
        },
        2: {
            'total_cost': 70000,
            'components': {
                'storage_tank': 27000,
                'recharge_pit': 4000,
                'filter_unit': 10000,
                'pipes_fittings': 8000,
                'first_flush': 3000,
                'labour': 18000
            }
        },
        3: {
            'total_cost': 93500,
            'components': {
                'storage_tank': 35000,
                'recharge_trench': 7500,
                'filter_unit': 12000,
                'pipes_fittings': 10000,
                'first_flush': 4000,
                'labour': 25000
            }
        },
        4: {
            'total_cost': 222500,
            'components': {
                'storage_tank': 70000,
                'recharge_shaft': 72500,
                'filter_unit': 20000,
                'pipes_fittings': 15000,
                'first_flush': 5000,
                'labour': 40000
            }
        },
        5: {
            'total_cost': 123500,
            'components': {
                'storage_tank': 52500,
                'recharge_structure': 25000,
                'filter_system': 15000,
                'pipes_fittings': 12000,
                'first_flush_system': 4000,
                'installation_misc': 15000
            }
        },
        6: {
            'total_cost': 564500,
            'components': {
                'central_storage': 262500,
                'recharge_structure': 150000,
                'central_filter': 42000,
                'pipe_network': 38000,
                'pumps_controls': 27000,
                'installation_misc': 45000
            }
        }
    }

    # Payback data from the document
    payback_data = {
        1: {'payback_years': 10, 'annual_savings': 10000},
        2: {'payback_years': 8, 'annual_savings': 15000},
        3: {'payback_years': 6, 'annual_savings': 22000},
        4: {'payback_years': 9, 'annual_savings': 45000},
        5: {'payback_years': 14, 'annual_savings': 30000},
        6: {'payback_years': 10, 'annual_savings': 150000}
    }

    # Get base costs for the category
    if category_id not in category_costs:
        category_id = 1  # Default to category 1

    base_cost = category_costs[category_id]['total_cost']
    components = category_costs[category_id]['components']

    # Cost modifiers from the document
    cost_modifiers = {
        'location': {
            'urban': 1.15,      # Urban Premium
            'semi-urban': 1.0,  # Base rate
            'rural': 0.85       # Rural Discount
        },
        'soil': {
            'hard': 1.25,       # Hard Soil
            'soft': 0.90,       # Soft Soil
            'loamy': 1.0,       # Base rate
            'sandy': 0.95,      # Sandy soil
            'clay': 1.1         # Clay soil
        },
        'materials': 1.20,      # Premium Materials
        'contingency': 1.15     # Contingency
    }

    # Intended use cost modifier
    intended_use_modifier = 1.0  # Default
    if intended_use and intended_use.lower() in ['drinking', 'potable', 'cooking']:
        intended_use_modifier = 1.25  # 25% premium for potable water systems
    elif intended_use and intended_use.lower() in ['gardening', 'irrigation', 'landscaping']:
        intended_use_modifier = 0.9   # 10% discount for non-potable uses

    # Apply modifiers
    location_modifier = cost_modifiers['location'].get(location_type.lower(), 1.0)
    soil_modifier = cost_modifiers['soil'].get(soil_type.lower(), 1.0)

    # Calculate final costs with all modifiers
    total_cost = base_cost * location_modifier * soil_modifier * cost_modifiers['materials'] * cost_modifiers['contingency'] * intended_use_modifier

    # Government subsidy (₹10,000 to ₹50,000 based on system size)
    if system_size <= 1000:
        subsidy_amount = 10000
    elif system_size <= 2000:
        subsidy_amount = 20000
    elif system_size <= 5000:
        subsidy_amount = 35000
    else:
        subsidy_amount = 50000

    # Net investment after subsidy
    net_investment = total_cost - subsidy_amount

    # Get payback data for the category
    payback_info = payback_data.get(category_id, payback_data[1])
    payback_years = payback_info['payback_years']
    annual_savings = payback_info['annual_savings']

    # Calculate ROI (20-year period)
    total_20_year_savings = annual_savings * 20
    if net_investment > 0:
        roi_percentage = ((total_20_year_savings - net_investment) / net_investment) * 100
    else:
        roi_percentage = 0

    # Calculate annual water savings (reverse engineered from annual savings)
    # Assuming water cost of ₹0.20 per liter
    annual_water_savings = annual_savings / 0.20

    return {
        'component_breakdown': components,
        'total_base_cost': base_cost,
        'category_multiplier': 1.0,  # Not used since we have exact costs
        'location_modifier': location_modifier,
        'soil_modifier': soil_modifier,
        'intended_use_modifier': intended_use_modifier,
        'total_modifier': location_modifier * soil_modifier * cost_modifiers['materials'] * cost_modifiers['contingency'] * intended_use_modifier,
        'total_cost': total_cost,
        'total_initial_cost': total_cost,  # For backward compatibility
        'subsidy_amount': subsidy_amount,
        'net_investment': net_investment,
        'annual_water_savings': annual_water_savings,
        'annual_savings': annual_savings,
        'annual_net_savings': annual_savings,  # For backward compatibility
        'payback_years': payback_years,
        'roi_percentage': roi_percentage
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
