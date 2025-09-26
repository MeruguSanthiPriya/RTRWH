// --- Mock Backend Data Structure ---

// Define national schemes once to avoid repetition
const nationalSchemes = {
  jalShakti: {
    "name": "Jal Shakti Abhiyan: Catch the Rain",
    "scope": "national",
    "description": "This is a nationwide campaign and not a direct financial subsidy for individuals. It promotes rainwater harvesting through convergence with other schemes like MGNREGS. Consult with your local municipal corporation or gram panchayat for details.",
    "eligibility_criteria": {
      "location": ["urban", "rural"],
      "building_types": ["residential", "commercial", "government"]
    },
    "estimated_subsidy": "N/A (varies locally)",
    "application_link": "https://jalshakti-ddws.gov.in/jal-shakti-abhiyan"
  },
  atalBhujal: {
    "name": "Atal Bhujal Yojana (ABY)",
    "scope": "national",
    "description": "This is a central government initiative limited to specific water-stressed states. Check if your state is a participant.",
    "eligibility_criteria": {
      "location": ["urban", "rural"],
      "building_types": ["residential", "commercial", "government"]
    },
    "participating_states": ["Gujarat", "Haryana", "Karnataka", "Madhya Pradesh", "Maharashtra", "Rajasthan", "Uttar Pradesh"]
  }
};

// Expanded data for multiple states
const subsidyData = {
    "National": {
        "schemes": [
            {
                "name": "Jal Shakti Abhiyan – “Catch the Rain” Campaign",
                "scope": "National",
                "description": "A pan-India campaign enabling states and ULBs to utilize Central grants to subsidize RWH infrastructure. Assistance for structure costs can be 50-80% for eligible communities.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential", "commercial", "government", "institutional"],
                    "beneficiary_category": ["general", "community", "institution"]
                },
                "subsidy_details": "Up to 50-80% of structure cost for communities/panchayats via converged schemes.",
                "link": "https://jalshakti-ddws.gov.in/"
            },
            {
                "name": "Mahatma Gandhi National Rural Employment Guarantee Scheme (MGNREGS)",
                "scope": "National",
                "description": "Funding for RWH works (tanks, check dams) on community land, and on private land for specific categories.",
                "eligibility": {
                    "location": ["rural"],
                    "building_type": ["residential", "community"],
                    "beneficiary_category": ["farmer", "bpl", "sc_st", "women_shg"]
                },
                "subsidy_details": "100% wage and material costs for approved RWH works.",
                "link": "https://nrega.nic.in/"
            }
        ]
    },
    "Andhra Pradesh": {
        "rules": { "mandatory": false },
        "schemes": [
            {
                "name": "Neeru-Chettu Program",
                "scope": "State",
                "description": "Merges traditional and modern water conservation, including rooftop RWH.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential", "institutional"],
                    "beneficiary_category": ["general", "bpl", "women_shg"]
                },
                "subsidy_details": "Up to 60% of construction cost, max ₹25,000 per household/institution.",
                "link": "https://apwrd.ap.gov.in/"
            }
        ]
    },
    "Arunachal Pradesh": {
        "rules": { "mandatory": false },
        "schemes": [
            {
                "name": "Subsidized RWH Promotion",
                "scope": "State",
                "description": "Pilot programs under district-level watershed development missions.",
                "eligibility": {
                    "location": ["rural"],
                    "building_type": ["residential", "community"],
                    "beneficiary_category": ["tribal"]
                },
                "subsidy_details": "50-80% of installation cost, capped at ₹40,000 per system.",
                "link": "Contact local District/Block Development Office."
            }
        ]
    },
    "Assam": {
        "rules": { "mandatory": false },
        "schemes": [
            {
                "name": "Rural Water Conservation Drive",
                "scope": "State",
                "description": "RWH support under flagship irrigation and rural housing schemes.",
                "eligibility": {
                    "location": ["rural"],
                    "building_type": ["residential"],
                    "beneficiary_category": ["bpl", "farmer"]
                },
                "subsidy_details": "Up to 70% of tank/rooftop structure cost for marginalized households.",
                "link": "Contact State Water Resources Department."
            }
        ]
    },
    "Bihar": {
        "rules": { "mandatory": true, "plot_size_min": 200, "location": ["urban"] },
        "schemes": [
            {
                "name": "Housing Support Linked RWH Incentives",
                "scope": "State",
                "description": "RWH is a mandatory component for new government-funded housing.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential"],
                    "beneficiary_category": ["bpl"]
                },
                "subsidy_details": "Cost of RWH component is fully covered for all BPL beneficiaries of government housing schemes.",
                "link": "Contact Bihar Urban Development Department."
            }
        ]
    },
    "Chhattisgarh": {
        "rules": { "mandatory": false },
        "schemes": [
            {
                "name": "RWH in Urban & Rural Housing Grants",
                "scope": "State",
                "description": "RWH support through rural housing grant programs and ULB schemes.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential", "institutional"],
                    "beneficiary_category": ["bpl", "community"]
                },
                "subsidy_details": "60-75% of system cost for households and schools, up to ₹20,000 per unit.",
                "link": "Contact local District authorities."
            }
        ]
    },
    "Delhi": {
        "rules": { "mandatory": true, "plot_size_min": 100, "location": ["urban"] },
        "schemes": [
            {
                "name": "Delhi Jal Board RWH Subsidy",
                "scope": "Municipal",
                "description": "Financial reimbursement for installing or retrofitting RWH systems.",
                "eligibility": {
                    "location": ["urban"],
                    "building_type": ["residential", "institutional", "commercial"],
                    "beneficiary_category": ["general"]
                },
                "subsidy_details": "Reimbursement up to ₹50,000 per system after audit and registration.",
                "link": "https://djb.gov.in/RainWaterHarvesting"
            }
        ]
    },
    "Goa": {
        "rules": { "mandatory": true, "plot_size_min": 200, "location": ["urban"] },
        "schemes": [
            {
                "name": "Indirect Support via RWH Mandates",
                "scope": "State",
                "description": "No direct cash incentives; developers get expedited permits for compliance with mandatory RWH.",
                "eligibility": {
                    "location": ["urban"],
                    "building_type": ["residential", "commercial"],
                    "beneficiary_category": ["general"]
                },
                "subsidy_details": "No direct subsidy. Compliance is mandatory for new constructions.",
                "link": "Contact local Planning and Development Authority."
            }
        ]
    },
    "Gujarat": {
        "rules": { "mandatory": true, "plot_size_min": 150, "location": ["urban"] },
        "schemes": [
            {
                "name": "Taluka Panchayat Infrastructure Program",
                "scope": "State",
                "description": "Funding for RWH works in rural and semi-urban settings.",
                "eligibility": {
                    "location": ["rural"],
                    "building_type": ["institutional", "community"],
                    "beneficiary_category": ["community", "institution"]
                },
                "subsidy_details": "60-80% of structure cost covered from state funds; up to 100% for Gram Panchayat-led projects in water-stressed taluks.",
                "link": "Contact local Taluka/District Panchayat."
            }
        ]
    },
    "Haryana": {
        "rules": { "mandatory": true, "plot_size_min": 250, "location": ["urban"] },
        "schemes": [
            {
                "name": "“Jal Hi Jeevan” RWH Grants",
                "scope": "State",
                "description": "Grants for RWH structures with a special focus on schools and large residential colonies.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential", "institutional", "commercial"],
                    "beneficiary_category": ["general", "institution"]
                },
                "subsidy_details": "Flat ₹20,000 per RWH structure or 75% of cost (whichever is lower).",
                "link": "Contact Haryana Water Resources Authority."
            }
        ]
    },
    "Himachal Pradesh": {
        "rules": { "mandatory": false },
        "schemes": [
            {
                "name": "Watershed Development Bundled RWH Incentive",
                "scope": "State",
                "description": "Part of the climate adaptation agenda for mountainous communities.",
                "eligibility": {
                    "location": ["rural"],
                    "building_type": ["residential"],
                    "beneficiary_category": ["farmer", "women_shg", "tribal"]
                },
                "subsidy_details": "60-100% of system cost for marginalized applicants, capped at ₹15,000 per household.",
                "link": "Contact local Block Development Office."
            }
        ]
    },
    "Jharkhand": {
        "rules": { "mandatory": false },
        "schemes": [
            {
                "name": "Bundled RWH With Rural Water Mission",
                "scope": "State",
                "description": "Parallel support for decentralized RWH alongside piped water supply mission.",
                "eligibility": {
                    "location": ["rural"],
                    "building_type": ["residential", "community", "institutional"],
                    "beneficiary_category": ["bpl"]
                },
                "subsidy_details": "Up to ₹10,000 per rooftop system, prioritizing water-scarce blocks.",
                "link": "Contact Jharkhand Drinking Water & Sanitation Dept."
            }
        ]
    },
    "Karnataka": {
        "rules": { "mandatory": true, "plot_size_min": 225, "location": ["urban"] },
        "schemes": [
            {
                "name": "BWSSB Urban RWH Mandate and Incentives (Bengaluru)",
                "scope": "Municipal",
                "description": "The Bangalore Water Supply and Sewerage Board (BWSSB) enforces compulsory RWH and provides financial assistance.",
                "eligibility": {
                    "location": ["urban"],
                    "building_type": ["residential", "institutional"],
                    "beneficiary_category": ["general"]
                },
                "subsidy_details": "Financial assistance of ₹25,000 (single dwelling) and ₹50,000 (apartments/institutions). Non-compliance results in a 50% hike in water bills.",
                "link": "https://bwssb.karnataka.gov.in/"
            }
        ]
    },
    "Kerala": {
        "rules": { "mandatory": true, "plot_size_min": 150, "location": ["urban"] },
        "schemes": [
            {
                "name": "Revised Government Order on RWH Grants",
                "scope": "State",
                "description": "Updated guidelines with priority for BPL families, farmers, and schools.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential", "institutional"],
                    "beneficiary_category": ["bpl", "farmer"]
                },
                "subsidy_details": "65-80% of system cost, maximum ₹30,000 for a single household/institution.",
                "link": "Contact local self-government institutions (LSGIs)."
            }
        ]
    },
    "Madhya Pradesh": {
        "rules": { "mandatory": true, "plot_size_min": 150, "location": ["urban"] },
        "schemes": [
            {
                "name": "Converged Rural Housing & RWH Assistance",
                "scope": "State",
                "description": "All new PMAY (Gramin) beneficiaries must install rooftop RWH.",
                "eligibility": {
                    "location": ["rural"],
                    "building_type": ["residential"],
                    "beneficiary_category": ["bpl"]
                },
                "subsidy_details": "Cost included in housing subsidy, up to ₹20,000 per rooftop system.",
                "link": "Contact local Gram Panchayat."
            },
            {
                "name": "Farmer Incentive for Farm Ponds",
                "scope": "State",
                "description": "Assistance for farmers to harvest rain runoff.",
                "eligibility": {
                    "location": ["rural"],
                    "building_type": [],
                    "beneficiary_category": ["farmer"]
                },
                "subsidy_details": "₹1.35 lakh per unit for eligible cultivators.",
                "link": "Contact Dept. of Farmer Welfare and Agriculture Development."
            }
        ]
    },
    "Maharashtra": {
        "rules": { "mandatory": true, "plot_size_min": 300, "location": ["urban"] },
        "schemes": [
            {
                "name": "Urban Mandate and Property Tax Rebate",
                "scope": "Municipal",
                "description": "Property tax rebate for verified RWH systems in cities like Mumbai, Pune, Nagpur.",
                "eligibility": {
                    "location": ["urban"],
                    "building_type": ["residential", "commercial"],
                    "beneficiary_category": ["general"]
                },
                "subsidy_details": "5-10% rebate on property tax depending on compliance.",
                "link": "Contact your local Municipal Corporation (e.g., BMC, PMC)."
            }
        ]
    },
    "Odisha": {
        "rules": { "mandatory": false },
        "schemes": [
            {
                "name": "“Chhata” Rainwater Harvesting Scheme",
                "scope": "State",
                "description": "A tech-neutral state-led RWH subsidy program for rooftop or surface-level systems.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential", "commercial", "institutional"],
                    "beneficiary_category": ["general", "farmer", "msme"]
                },
                "subsidy_details": "Up to 50% of cost reimbursed, with a maximum cap of ₹50,000 per installation.",
                "link": "https://urban.odisha.gov.in/chhatas/"
            }
        ]
    },
    "Punjab": {
        "rules": { "mandatory": true, "plot_size_min": 200, "location": ["urban", "rural"] },
        "schemes": [
            {
                "name": "Statewide RWH Compulsory Policy",
                "scope": "State",
                "description": "No direct cash incentive; installation is mandatory for new buildings prior to occupancy.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential", "institutional", "commercial"],
                    "beneficiary_category": ["general"]
                },
                "subsidy_details": "No direct subsidy. Compliance is mandatory.",
                "link": "Contact local Urban Local Body (ULB)."
            }
        ]
    },
    "Rajasthan": {
        "rules": { "mandatory": true, "plot_size_min": 300, "location": ["urban"] },
        "schemes": [
            {
                "name": "Mukhya Mantri Jal Swavlamban Abhiyan (MMJSA)",
                "scope": "State",
                "description": "Flagship state program covering RWH with a focus on water-scarce blocks.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential"],
                    "beneficiary_category": ["general", "bpl"]
                },
                "subsidy_details": "Full or part subsidy (up to 100% for vulnerable/poor), typically capped at ₹25,000 per beneficiary.",
                "link": "https://mjsa.water.rajasthan.gov.in/"
            }
        ]
    },
    "Sikkim": {
        "rules": { "mandatory": false },
        "schemes": [
            {
                "name": "State Subsidy for RWH Installations",
                "scope": "State",
                "description": "A straightforward grant for any applicant.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential", "institutional"],
                    "beneficiary_category": ["general"]
                },
                "subsidy_details": "75% of installation cost or ₹15,000 per beneficiary, whichever is lower.",
                "link": "Contact Rural Development Department, Govt. of Sikkim."
            }
        ]
    },
    "Tamil Nadu": {
        "rules": { "mandatory": true, "plot_size_min": 100, "location": ["urban", "rural"] },
        "schemes": [
            {
                "name": "Pioneering Mandatory RWH and Subsidy",
                "scope": "State",
                "description": "The state has the oldest and most robust compulsory system with support for vulnerable groups.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential"],
                    "beneficiary_category": ["bpl"]
                },
                "subsidy_details": "Up to 100% of expenditure reimbursed for approved RWH components for BPL/vulnerable groups, with a ceiling of ₹25,000 per household.",
                "link": "Contact your local ULB or Town Panchayat."
            }
        ]
    },
    "Telangana": {
        "rules": { "mandatory": true, "plot_size_min": 300, "location": ["urban"] },
        "schemes": [
            {
                "name": "Urban RWH Incentives (Limited)",
                "scope": "Municipal",
                "description": "No direct universal subsidy, but rebates on penal charges for early compliance in group housing.",
                "eligibility": {
                    "location": ["urban"],
                    "building_type": ["residential", "community"],
                    "beneficiary_category": ["community"]
                },
                "subsidy_details": "Rebate on penal charges for societies/housing colonies.",
                "link": "Contact Greater Hyderabad Municipal Corporation (GHMC)."
            }
        ]
    },
    "Tripura": {
        "rules": { "mandatory": false },
        "schemes": [
            {
                "name": "Gram Panchayats and Agri Plan Incentives",
                "scope": "State",
                "description": "Part-subsidy on tank construction and rooftop structures in water-stressed hamlets.",
                "eligibility": {
                    "location": ["rural"],
                    "building_type": ["residential"],
                    "beneficiary_category": ["farmer"]
                },
                "subsidy_details": "25-50% subsidy on cost of tank construction and rooftop structure.",
                "link": "Contact local Gram Panchayat."
            }
        ]
    },
    "Uttar Pradesh": {
        "rules": { "mandatory": true, "plot_size_min": 200, "location": ["urban"] },
        "schemes": [
            {
                "name": "ULB Programs and Rural Mandate",
                "scope": "State",
                "description": "Mandatory installation for educational institutions and new buildings. No direct state-wide subsidy, but select ULBs provide in-kind support.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["residential", "institutional"],
                    "beneficiary_category": ["general"]
                },
                "subsidy_details": "No direct subsidy. Some ULBs offer free technical consultancy or discounted permit fees.",
                "link": "Contact your local ULB."
            }
        ]
    },
    "Uttarakhand": {
        "rules": { "mandatory": false },
        "schemes": [
            {
                "name": "Watershed and Rainwater Harvesting Incentives",
                "scope": "State",
                "description": "Convergence approach focusing on mountain communities and schools.",
                "eligibility": {
                    "location": ["rural"],
                    "building_type": ["residential", "institutional"],
                    "beneficiary_category": ["general"]
                },
                "subsidy_details": "Up to 80% of cost for rooftop/surface RWH system in specified water-scarce blocks.",
                "link": "Contact local Block Development Office."
            }
        ]
    },
    "West Bengal": {
        "rules": { "mandatory": true, "plot_size_min": 300, "location": ["urban"] },
        "schemes": [
            {
                "name": "Urban Mandate & Rural Farmer Assistance",
                "scope": "State/Municipal",
                "description": "Urban areas enforce mandatory installation with property tax rebates. Rural areas have seasonal grants for farmers.",
                "eligibility": {
                    "location": ["urban", "rural"],
                    "building_type": ["institutional", "residential"],
                    "beneficiary_category": ["general", "farmer"]
                },
                "subsidy_details": "Urban: Rebate on property tax. Rural: Grant up to ₹10,000 per farm tank or rooftop unit.",
                "link": "Contact local ULB (urban) or Agriculture Dept. (rural)."
            }
        ]
    }
};

function runEligibilityCheck(state, location, plotSize, buildingType, beneficiaryCategory) {
    const stateData = subsidyData[state];
    let complianceStatus = 'Optional';
    let mandatoryRuleMet = false;
    let eligibleSchemes = [];

    // --- 1. Add National Schemes ---
    if (subsidyData.National && subsidyData.National.schemes) {
        subsidyData.National.schemes.forEach(scheme => {
            const ec = scheme.eligibility;
            if (ec.location.includes(location) && 
                (ec.building_type.length === 0 || ec.building_type.includes(buildingType)) &&
                (ec.beneficiary_category.length === 0 || ec.beneficiary_category.includes(beneficiaryCategory))) {
                eligibleSchemes.push(scheme);
            }
        });
    }

    // --- 2. Compliance & State Scheme Check ---
    if (stateData) {
        // Check for mandatory rule
        if (stateData.rules.mandatory && stateData.rules.location.includes(location) && plotSize >= stateData.rules.plot_size_min) {
            complianceStatus = 'Mandatory';
            mandatoryRuleMet = true;
        }

        // Check for state-specific schemes
        if (stateData.schemes) {
            stateData.schemes.forEach(scheme => {
                const ec = scheme.eligibility;
                if (ec.location.includes(location) &&
                    (ec.building_type.length === 0 || ec.building_type.includes(buildingType)) &&
                    (ec.beneficiary_category.length === 0 || ec.beneficiary_category.includes(beneficiaryCategory))) {
                    eligibleSchemes.push(scheme);
                }
            });
        }
    }

    // --- 3. Display Results ---
    const complianceStatusDiv = document.getElementById('complianceStatus');
    const schemesListUl = document.getElementById('schemesList');
    const warningMessageDiv = document.getElementById('warningMessage');
    const resultsSection = document.getElementById('resultsSection');
    const subsidySchemesDiv = document.getElementById('subsidySchemes');

    schemesListUl.innerHTML = '';
    
    if (complianceStatus === 'Mandatory') {
        complianceStatusDiv.innerHTML = `<span class="compliance-status">✅ Compliance Status: Mandatory</span><p>For your selected criteria in ${state}, rainwater harvesting is a mandatory requirement.</p>`;
        complianceStatusDiv.className = 'result-box green';
        warningMessageDiv.classList.remove('hidden');
    } else {
        complianceStatusDiv.innerHTML = `<span class="compliance-status">📝 Compliance Status: Optional</span><p>Rainwater harvesting is encouraged but not mandatory for your property type in ${state}.</p>`;
        complianceStatusDiv.className = 'result-box yellow';
        warningMessageDiv.classList.add('hidden');
    }

    if (eligibleSchemes.length > 0) {
        eligibleSchemes.forEach(scheme => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${scheme.name} (${scheme.scope})</strong>: ${scheme.description} <br><em>Subsidy: ${scheme.subsidy_details}</em>`;
            if (scheme.link && scheme.link.startsWith('http')) {
                li.innerHTML += ` <a href="${scheme.link}" target="_blank" class="text-cyan-400 hover:underline">Learn More</a>`;
            } else if (scheme.link) {
                 li.innerHTML += ` <span class="text-gray-400 text-sm">(${scheme.link})</span>`;
            }
            schemesListUl.appendChild(li);
        });
        subsidySchemesDiv.classList.remove('hidden');
    } else {
         subsidySchemesDiv.classList.add('hidden');
         const li = document.createElement('li');
         li.textContent = "No specific state-level subsidy schemes matched your criteria. However, national campaigns like Jal Shakti Abhiyan may still offer support through local bodies.";
         schemesListUl.appendChild(li);
    }

    resultsSection.classList.remove('hidden');
}

document.addEventListener('DOMContentLoaded', () => {
    const eligibilityForm = document.getElementById('eligibilityForm');
    const stateSelect = document.getElementById('state');

    // Populate states dropdown
    const states = Object.keys(subsidyData).filter(k => k !== "National").sort();
    states.forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.textContent = state;
        stateSelect.appendChild(option);
    });

    eligibilityForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const state = document.getElementById('state').value;
        const location = document.querySelector('input[name="location"]:checked').value;
        const plotSize = parseInt(document.getElementById('plotSize').value);
        const buildingType = document.querySelector('input[name="buildingType"]:checked').value;
        const beneficiaryCategory = document.getElementById('beneficiaryCategory').value;
        
        runEligibilityCheck(state, location, plotSize, buildingType, beneficiaryCategory);
    });
});