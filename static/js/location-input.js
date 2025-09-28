document.addEventListener('DOMContentLoaded', () => {
  let map, marker;
  let formData = {};

  // Create background particles
  function createParticles() {
    const particlesContainer = document.getElementById('particles');
    for (let i = 0; i < 20; i++) {
      const particle = document.createElement('div');
      particle.classList.add('particle');
      particle.style.left = Math.random() * 100 + '%';
      particle.style.top = Math.random() * 100 + '%';
      particle.style.width = Math.random() * 4 + 2 + 'px';
      particle.style.height = particle.style.width;
      particle.style.animationDuration = Math.random() * 3 + 3 + 's';
      particle.style.animationDelay = Math.random() * 2 + 's';
      particlesContainer.appendChild(particle);
    }
  }

  // Initialize particles
  createParticles();

  // Debounce utility to limit API calls and prevent rate-limiting errors.
  function debounce(func, delay) {
    let timeout;
    return function(...args) {
      const context = this;
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(context, args), delay);
    };
  }

  // Initialize MapLibre GL JS
  // Styles declared in outer scope so toggle can access them
  let streetsStyle;
  let satelliteStyle;
  let currentStyle;
  try {
    const MAPTILER_API_KEY = 'mUiASIDIGsImfNM8L0hq';
    streetsStyle = `https://api.maptiler.com/maps/streets-v2/style.json?key=${MAPTILER_API_KEY}`;
    satelliteStyle = `https://api.maptiler.com/maps/hybrid/style.json?key=${MAPTILER_API_KEY}`;
    currentStyle = satelliteStyle; // The initial style

    if (!MAPTILER_API_KEY || MAPTILER_API_KEY === 'YOUR_MAPTILER_API_KEY') {
      const mapContainer = document.getElementById('map');
      mapContainer.innerHTML = '<div class="h-full w-full flex items-center justify-center bg-gray-800 text-gray-400 p-4 text-center rounded-lg">To display the map, please get a free API key from MapTiler.com</div>';
      // Disable map-dependent features if map fails to load
      document.getElementById('geolocation').disabled = true;
      return; // Stop map initialization
    }

    map = new maplibregl.Map({
      container: 'map',
      style: satelliteStyle,
      center: [78.9629, 20.5937], // India center
      zoom: 5,
      pitch: 0 // Start flat
    });

    map.on('load', () => {
      // This event fires on initial load and after every `setStyle` call.
      // We must re-add any custom layers here.

      // Determine building color based on the current style to ensure visibility.
      const isSatellite = currentStyle === satelliteStyle;
      const buildingColor = isSatellite ? '#ffffff' : '#aaaaaa';
      const buildingOpacity = isSatellite ? 0.7 : 0.6;

      // Add 3D buildings layer. We wrap this in a try/catch because on style change,
      // there can be a race condition. `addLayer` is the safest way to proceed.
      try {
        if (!map.getLayer('3d-buildings')) {
          map.addLayer({
            'id': '3d-buildings',
            'source': 'openmaptiles',
            'source-layer': 'building',
            'type': 'fill-extrusion',
            'minzoom': 15,
            'paint': {
              'fill-extrusion-color': buildingColor,
              'fill-extrusion-height': ['get', 'height'],
              'fill-extrusion-base': ['get', 'min_height'],
              'fill-extrusion-opacity': buildingOpacity
            }
          });
        }
      } catch (e) {
        console.error('Could not add 3D building layer:', e);
      }
    });

    map.on('error', (e) => {
      console.error('Map error:', e);
    });
  } catch (error) {
    console.error('Map initialization failed:', error);
  }

  // Add marker
  marker = new maplibregl.Marker({ draggable: true })
    .setLngLat([78.9629, 20.5937])
    .addTo(map);

  // Map click for pinpointing
  map.on('click', (e) => {
    marker.setLngLat(e.lngLat);
    updateTo3DView(e.lngLat);
    updateFromMarker(e.lngLat);
  });

  // Marker dragend
  marker.on('dragend', () => {
    const lngLat = marker.getLngLat();
    updateTo3DView(lngLat);
    updateFromMarker(lngLat);
  });

  // Switch to 3D view
  function updateTo3DView(lngLat) {
    map.flyTo({
      center: [lngLat.lng, lngLat.lat],
      zoom: 18,
      pitch: 60,
      bearing: 90
    });
  }

  // Reverse geocoding for marker using MapTiler API
  async function updateFromMarker(lngLat) {
    const lat = lngLat.lat.toFixed(6);
    const lng = lngLat.lng.toFixed(6);
    document.getElementById('latitude').value = lat;
    document.getElementById('longitude').value = lng;
    document.getElementById('coords').textContent = `Latitude: ${lat}, Longitude: ${lng}`;
    
    try {
      const MAPTILER_API_KEY = 'mUiASIDIGsImfNM8L0hq';
      const response = await fetch(`https://api.maptiler.com/geocoding/${lng},${lat}.json?key=${MAPTILER_API_KEY}`);
      const data = await response.json();
      
      if (data.features && data.features.length > 0) {
        const topResult = data.features[0];
        
        // Use place_name for the main address field for a full, readable address
        if (topResult.place_name) {
          document.getElementById('address').value = topResult.place_name;
        }
        
        // Initialize variables
        let pincode = '';
        let district = '';
        let city = '';
        let state = '';

        // Helper: find a feature by place_type or id prefix
        const features = data.features || [];
        function findFeatureByTypes(types) {
          return features.find(f => {
            if (f.place_type && Array.isArray(f.place_type)) {
              if (f.place_type.some(t => types.includes(t))) return true;
            }
            if (f.id && typeof f.id === 'string') {
              return types.some(t => f.id.startsWith(t));
            }
            return false;
          });
        }

        // Prefer explicit feature types returned by the geocoder
        const postcodeFeature = findFeatureByTypes(['postcode']);
        const regionFeature = findFeatureByTypes(['region']);
        const districtFeature = findFeatureByTypes(['district', 'county']);
        const placeFeature = findFeatureByTypes(['place', 'locality', 'town', 'village', 'city']);

        if (postcodeFeature && postcodeFeature.text) pincode = postcodeFeature.text;
        if (districtFeature && districtFeature.text) district = districtFeature.text;
        if (placeFeature && placeFeature.text) city = placeFeature.text;
        if (regionFeature && regionFeature.text) state = regionFeature.text;

        // If not found in features, fall back to context array (but only accept region for state)
        if ((!pincode || !district || !city || !state) && topResult.context && Array.isArray(topResult.context)) {
          // Context parsing but with strict matching for region/state
          if (!pincode) {
            const pincodeContext = topResult.context.find(c => c.id && (c.id.startsWith('postcode') || c.id.includes('postal')));
            if (pincodeContext && pincodeContext.text) pincode = pincodeContext.text;
          }
          if (!district) {
            const districtContext = topResult.context.find(c => c.id && (c.id.startsWith('district') || c.id.includes('district') || c.id.includes('county')));
            if (districtContext && districtContext.text) district = districtContext.text;
          }
          if (!city) {
            const cityContext = topResult.context.find(c => c.id && (c.id.startsWith('place') || c.id.includes('locality') || c.id.includes('municipality')));
            if (cityContext && cityContext.text) city = cityContext.text;
          }
          if (!state) {
            const stateContext = topResult.context.find(c => c.id && (c.id.startsWith('region') || c.id.includes('region')));
            if (stateContext && stateContext.text) state = stateContext.text;
          }
        }

        // Alternative parsing from properties if still missing
        if (topResult.properties) {
          if (!pincode && topResult.properties.postcode) pincode = topResult.properties.postcode;
          if (!district && topResult.properties.district) district = topResult.properties.district;
          if (!city && topResult.properties.city) city = topResult.properties.city;
          if (!state && topResult.properties.state) state = topResult.properties.state;
        }

        // Final fallback: parse from place_name but ensure we only accept likely state names
        if (!state && topResult.place_name) {
          const addressParts = topResult.place_name.split(',').map(part => part.trim());
          if (addressParts.length >= 2) {
            const lastPart = addressParts[addressParts.length - 1];
            const secondLastPart = addressParts[addressParts.length - 2];
            const knownStates = ['Delhi','Goa','Punjab','Haryana','Kerala','Karnataka','Maharashtra','Gujarat','Rajasthan','Tamil Nadu','Telangana','Andhra Pradesh','West Bengal','Uttar Pradesh','Madhya Pradesh','Bihar','Jharkhand','Odisha','Chhattisgarh','Assam','Sikkim','Arunachal Pradesh','Nagaland','Manipur','Mizoram','Meghalaya','Tripura','Puducherry','Jammu and Kashmir','Ladakh','Andaman and Nicobar Islands','Lakshadweep','Dadra and Nagar Haveli and Daman and Diu','Chandigarh'];
            if (knownStates.some(s => lastPart.toLowerCase().includes(s.toLowerCase()))) {
              state = lastPart;
            } else if (secondLastPart && knownStates.some(s => secondLastPart.toLowerCase().includes(s.toLowerCase()))) {
              state = secondLastPart;
            }
          }
        }

        // Log findings for debugging
        console.log('Parsed features => postcode:', pincode, 'district:', district, 'city:', city, 'state:', state);
        
        // Apply the found values to form fields
        if (pincode) {
          document.getElementById('pincode').value = pincode;
          console.log('Pin Code found:', pincode);
        }
        
        if (district) {
          document.getElementById('district').value = district;
          console.log('District found:', district);
        }
        
        if (city) {
          document.getElementById('town').value = city;
          console.log('Town/City found:', city);
        }
        
        if (state) {
          document.getElementById('state').value = state;
          console.log('State found and filled:', state);
        }
        
        // Show success feedback
        const addressField = document.getElementById('address');
        const originalStyle = addressField.style.borderColor;
        addressField.style.borderColor = '#10b981';
        addressField.style.boxShadow = '0 0 10px rgba(16, 185, 129, 0.3)';
        setTimeout(() => {
          addressField.style.borderColor = originalStyle;
          addressField.style.boxShadow = '';
        }, 2000);
        
        // Log all found information for debugging
        console.log('Location details found:', {
          pincode, district, city, state,
          fullAddress: topResult.place_name
        });
        
      } else {
        console.warn('No geocoding results found for the coordinates');
        // Clear the fields if no results found
        document.getElementById('address').value = `Location: ${lat}, ${lng}`;
      }
    } catch (error) {
      console.error('Reverse geocoding failed:', error);
      // Fallback display
      document.getElementById('address').value = `Location: ${lat}, ${lng}`;
      alert('Unable to fetch location details. Please fill in manually.');
    }
  }

  // Create a debounced version of the reverse geocoding function.
  const debouncedUpdateFromMarker = debounce(updateFromMarker, 500);

  // Update marker from inputs
  document.getElementById('latitude').addEventListener('input', updateMarkerFromInputs);
  document.getElementById('longitude').addEventListener('input', updateMarkerFromInputs);

  function updateMarkerFromInputs() {
    const lat = parseFloat(document.getElementById('latitude').value);
    const lng = parseFloat(document.getElementById('longitude').value);
    if (!isNaN(lat) && !isNaN(lng) && lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
      const lngLat = { lng, lat };
      marker.setLngLat(lngLat);
      document.getElementById('coords').textContent = `Latitude: ${lat.toFixed(5)}, Longitude: ${lng.toFixed(5)}`;
      // Use the debounced function to avoid excessive API calls while typing.
      debouncedUpdateFromMarker(lngLat);
    }
  }

  // Geolocation button
  document.getElementById('geolocation').addEventListener('click', () => {
    const geolocationBtn = document.getElementById('geolocation');
    const originalText = geolocationBtn.innerHTML;
    
    // Show loading state
    geolocationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Getting Location...</span>';
    geolocationBtn.disabled = true;
    
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const lngLat = { lng: position.coords.longitude, lat: position.coords.latitude };
          marker.setLngLat(lngLat);
          updateTo3DView(lngLat);
          await updateFromMarker(lngLat);
          
          // Show success state briefly
          geolocationBtn.innerHTML = '<i class="fas fa-check"></i><span>Location Found!</span>';
          setTimeout(() => {
            geolocationBtn.innerHTML = originalText;
            geolocationBtn.disabled = false;
          }, 2000);
        },
        (error) => {
          // Reset button state on error
          geolocationBtn.innerHTML = originalText;
          geolocationBtn.disabled = false;
          
          let errorMessage = 'Unable to get your location. ';
          switch(error.code) {
            case error.PERMISSION_DENIED:
              errorMessage += 'Please allow location access and try again.';
              break;
            case error.POSITION_UNAVAILABLE:
              errorMessage += 'Location information is unavailable.';
              break;
            case error.TIMEOUT:
              errorMessage += 'Location request timed out.';
              break;
            default:
              errorMessage += 'An unknown error occurred.';
              break;
          }
          alert(errorMessage);
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 60000
        }
      );
    } else {
      geolocationBtn.innerHTML = originalText;
      geolocationBtn.disabled = false;
      alert('Geolocation is not supported by your browser.');
    }
  });

  // Debounced forward geocoding function for address search
  const debouncedAddressSearch = debounce(async (input) => {
    const suggestionsDiv = document.getElementById('suggestions');
    if (input.length < 3) {
      suggestionsDiv.classList.add('hidden');
      return;
    }

    try {
      const MAPTILER_API_KEY = 'mUiASIDIGsImfNM8L0hq';
      const response = await fetch(`https://api.maptiler.com/geocoding/${encodeURIComponent(input)}.json?key=${MAPTILER_API_KEY}&country=IN&types=address,street,place,postcode,region,district&limit=5`);
      const data = await response.json();

      suggestionsDiv.innerHTML = ''; // Clear previous suggestions
      if (data.features && data.features.length > 0) {
        suggestionsDiv.classList.remove('hidden');
        data.features.forEach(place => {
          const div = document.createElement('div');
          div.className = 'suggestion-item';
          div.textContent = place.place_name;
          div.onclick = () => {
            const [lng, lat] = place.center;
            marker.setLngLat({ lng, lat });
            updateTo3DView({ lng, lat });
            updateFromMarker({ lng, lat });
            suggestionsDiv.classList.add('hidden');
          };
          suggestionsDiv.appendChild(div);
        });
      } else {
        suggestionsDiv.classList.add('hidden');
      }
    } catch (error) {
      console.error('Address search failed:', error);
    }
  }, 300);

  // Attach debounced search to the address input
  document.getElementById('address').addEventListener('input', (e) => {
    debouncedAddressSearch(e.target.value);
  });

  // Hide suggestions on click outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.relative')) {
      document.getElementById('suggestions').classList.add('hidden');
    }
  });

  // Map style toggle functionality
  const viewToggle = document.getElementById('view-toggle');
  const streetsLabel = document.querySelector('#map-style-toggle span:first-of-type');
  const satelliteLabel = document.querySelector('#map-style-toggle span:last-of-type');

  if (viewToggle) {
    viewToggle.addEventListener('change', (e) => {
      const isSatelliteView = e.target.checked;
      // Guard: ensure styles and map are available
      if (!streetsStyle || !satelliteStyle || !map) {
        console.warn('Map styles or map not initialized yet');
        return;
      }

      const newStyle = isSatelliteView ? satelliteStyle : streetsStyle;
      if (currentStyle !== newStyle) {
        currentStyle = newStyle;
        try {
          map.setStyle(newStyle);
        } catch (err) {
          console.error('Failed to set map style:', err);
        }
      }

      // Update label styles to indicate the active view
      satelliteLabel?.classList.toggle('text-white', isSatelliteView);
      satelliteLabel?.classList.toggle('font-semibold', isSatelliteView);
      satelliteLabel?.classList.toggle('text-gray-300', !isSatelliteView);
      streetsLabel?.classList.toggle('text-white', !isSatelliteView);
      streetsLabel?.classList.toggle('font-semibold', !isSatelliteView);
      streetsLabel?.classList.toggle('text-gray-300', isSatelliteView);
    });
  } else {
    console.warn('View toggle element not found: #view-toggle');
  }

  // Radio button functionality
  document.querySelectorAll('.radio-option').forEach(option => {
    option.addEventListener('click', () => {
      const input = option.querySelector('input[type="radio"]');
      const name = input.name;
      
      // Clear other selections in the same group
      document.querySelectorAll(`input[name="${name}"]`).forEach(radio => {
        radio.closest('.radio-option').classList.remove('selected');
      });
      
      // Select this option
      option.classList.add('selected');
      input.checked = true;

      // Trigger change event for property type
      if (name === 'propertyType') {
        const event = new Event('change', { bubbles: true });
        input.dispatchEvent(event);
      }
    });
  });

  // Household size increment/decrement handlers
  const hhInput = document.getElementById('householdSize');
  const hhInc = document.getElementById('household-increment');
  const hhDec = document.getElementById('household-decrement');

  function normalizeHouseholdValue() {
    if (!hhInput) return;
    let v = parseInt(hhInput.value, 10);
    if (isNaN(v) || v < 1) v = 1;
    hhInput.value = v;
    return v;
  }

  hhInc?.addEventListener('click', () => {
    const v = normalizeHouseholdValue();
    hhInput.value = v + 1;
  });

  hhDec?.addEventListener('click', () => {
    const v = normalizeHouseholdValue();
    if (v > 1) hhInput.value = v - 1;
  });

  // Ensure input cannot be set below 1 via typing
  hhInput?.addEventListener('input', () => {
    const v = parseInt(hhInput.value, 10);
    if (isNaN(v) || v < 1) {
      hhInput.value = 1;
    }
  });

  // Area calculator
  window.calculateArea = function() {
    const length = parseFloat(document.getElementById('length').value) || 0;
    const width = parseFloat(document.getElementById('width').value) || 0;
    const area = length * width;
    if (area > 0) {
      document.getElementById('rooftopArea').value = area;
    }
  };

  // Section navigation
  window.nextSection = function() {
    const lat = document.getElementById('latitude').value;
    const lng = document.getElementById('longitude').value;
    
    if (!lat || !lng) {
      alert('Please provide valid coordinates before proceeding.');
      return;
    }
    
    document.getElementById('locationSection').classList.remove('active');
    document.getElementById('dataSection').classList.add('active');
  };

  window.previousSection = function() {
    document.getElementById('dataSection').classList.remove('active');
    document.getElementById('locationSection').classList.add('active');
  };

  window.goBack = function() {
    window.location.href = 'index.html';
  };

  // Form validation and submission
  window.submitData = function() { // Expose function to be called by onclick
    const lat = document.getElementById('latitude').value;
    const lon = document.getElementById('longitude').value;
    const address = document.getElementById('address').value;

    if (!lat || !lon || !address) {
      alert('Please select a location on the map before proceeding.');
      return;
    }

    const submitBtn = document.getElementById('submitData');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Processing...';
    submitBtn.disabled = true;

    const locationData = {
      lat: lat,
      lon: lon,
      address: address
    };

    // Use fetch to send data to the new /submit_location endpoint
    fetch('/submit_location', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(locationData),
    })
    .then(response => response.json())
    .then(data => {
      if (data.redirect_url) {
        // Redirect to the assessment type selection page on success
        window.location.href = data.redirect_url;
      } else {
        // Handle errors
        alert(data.error || 'An unknown error occurred.');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
      }
    })
    .catch(error => {
      console.error('Error submitting location:', error);
      alert('Failed to submit location. Please check your connection and try again.');
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    });
  };

  // Language selector
  document.getElementById('languageSelect').addEventListener('change', function() {
    console.log('Language changed to:', this.value);
    // Implement language switching logic here
  });

  // Auto-calculate area when length/width change
  document.getElementById('length').addEventListener('input', () => {
    const length = parseFloat(document.getElementById('length').value) || 0;
    const width = parseFloat(document.getElementById('width').value) || 0;
    if (length > 0 && width > 0) {
      document.getElementById('rooftopArea').value = length * width;
    }
  });

  document.getElementById('width').addEventListener('input', () => {
    const length = parseFloat(document.getElementById('length').value) || 0;
    const width = parseFloat(document.getElementById('width').value) || 0;
    if (length > 0 && width > 0) {
      document.getElementById('rooftopArea').value = length * width;
    }
  });
});

// Toggle occupancy field based on property type
const propertyTypeRadios = document.querySelectorAll('input[name="propertyType"]');
const occupancyField = document.getElementById('occupancy-field');
const buildingAgeField = document.getElementById('buildingAge');

const communityFields = document.getElementById('community-fields');
const totalPeopleField = document.getElementById('total-people-field');
const householdSizeField = document.getElementById('household-size-field');

propertyTypeRadios.forEach(radio => {
  radio.addEventListener('change', () => {
    const isCommercialOrInstitutional = radio.value === 'Commercial' || radio.value === 'Institutional';
    const isCommunity = radio.value === 'Community';

    occupancyField.classList.toggle('hidden', !isCommercialOrInstitutional);
    communityFields.classList.toggle('hidden', !isCommunity);
    totalPeopleField.classList.toggle('hidden', !isCommunity);
    householdSizeField.classList.toggle('hidden', isCommunity);
  });
});

// Initialize map and other components
// initializeMap(); // This function is not defined, so it's commented out.

// function initializeMap() {
//   // ... existing map initialization code ...
// }