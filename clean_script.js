    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const userLocationData = {{ user_location | tojson }};
            const nearestLocation = {{ nearest_location | tojson }};

            // 1. Initialize the map
            let map = L.map('map').setView([userLocationData.Latitude, userLocationData.Longitude], 12);
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            let geoJsonLayer;

            // 2. Animation Functions
            function createWaterParticles() {
                const mapContainer = document.getElementById('map');
                for (let i = 0; i < 10; i++) {
                    const particle = document.createElement('div');
                    particle.className = 'water-particle';
                    particle.style.left = Math.random() * 100 + '%';
                    particle.style.top = Math.random() * 100 + '%';
                    particle.style.animationDelay = Math.random() * 3 + 's';
                    mapContainer.appendChild(particle);
                }
            }

            function createFlowArrows() {
                const mapContainer = document.getElementById('map');
                setInterval(() => {
                    const arrow = document.createElement('div');
                    arrow.className = 'flow-arrow';
                    arrow.innerHTML = '→';
                    arrow.style.left = Math.random() * 80 + 10 + '%';
                    arrow.style.top = Math.random() * 80 + 10 + '%';
                    mapContainer.appendChild(arrow);
                    
                    setTimeout(() => {
                        if (arrow.parentNode) arrow.parentNode.removeChild(arrow);
                    }, 2000);
                }, 3000);
            }

            function createRippleEffect(x, y) {
                const ripple = document.createElement('div');
                ripple.className = 'ripple-effect';
                ripple.style.left = (x - 25) + 'px';
                ripple.style.top = (y - 25) + 'px';
                ripple.style.width = '50px';
                ripple.style.height = '50px';
                document.getElementById('map').appendChild(ripple);
                
                setTimeout(() => {
                    if (ripple.parentNode) ripple.parentNode.removeChild(ripple);
                }, 1000);
            }

            // 3. Define color schemes and categories
            const layers = {
                rainfall: {
                    name: 'Rainfall Level',
                    property: 'Rainfall_mm',
                    categories: [
                        { range: [0, 500], color: '#ffffcc', label: 'Very Low (<500mm)' },
                        { range: [500, 750], color: '#a1dab4', label: 'Low (500-750mm)' },
                        { range: [750, 1000], color: '#41b6c4', label: 'Moderate (750-1000mm)' },
                        { range: [1000, 2000], color: '#2c7fb8', label: 'High (1000-2000mm)' },
                        { range: [2000, Infinity], color: '#253494', label: 'Very High (>2000mm)' }
                    ],
                    getColor: (value) => {
                        const category = layers.rainfall.categories.find(c => value >= c.range[0] && value < c.range[1]);
                        return category ? category.color : '#808080';
                    }
                },
                aquifer: {
                    name: 'Aquifer Type',
                    property: 'Aquifer_Type',
                    categories: [
                        { value: 'Confined', color: '#fe9929', label: 'Confined' },
                        { value: 'Unconfined', color: '#43a2ca', label: 'Unconfined' },
                        { value: 'Other', color: '#bdbdbd', label: 'Other' }
                    ],
                    getColor: (value) => {
                        const category = layers.aquifer.categories.find(c => c.value.toLowerCase() === value.toLowerCase());
                        return category ? category.color : layers.aquifer.categories.find(c => c.value === 'Other').color;
                    }
                },
                soil: {
                    name: 'Soil Type',
                    property: 'Soil_Type',
                    categories: [
                        { value: 'Sandy', color: '#fed976', label: 'Sandy' },
                        { value: 'Loamy', color: '#ae017e', label: 'Loamy' },
                        { value: 'Clayey', color: '#cc4c02', label: 'Clayey' },
                        { value: 'Other', color: '#bdbdbd', label: 'Other' }
                    ],
                    getColor: (value) => {
                        const category = layers.soil.categories.find(c => c.value.toLowerCase() === value.toLowerCase());
                        return category ? category.color : layers.soil.categories.find(c => c.value === 'Other').color;
                    }
                },
                infiltration: {
                    name: 'Infiltration Rate',
                    property: 'Infiltration_Rate_mm_per_hr',
                    categories: [
                        { range: [0, 10], color: '#fa9fb5', label: 'Low (<10 mm/hr)' },
                        { range: [10, 15], color: '#7bccc4', label: 'Moderate (10-15 mm/hr)' },
                        { range: [15, Infinity], color: '#2b8cbe', label: 'High (>15 mm/hr)' }
                    ],
                    getColor: (value) => {
                        const category = layers.infiltration.categories.find(c => value >= c.range[0] && value < c.range[1]);
                        return category ? category.color : '#808080';
                    }
                }
            };

            // 4. Create GeoJSON features for both locations
            let features = [];
            if (userLocationData) {
                userLocationData.isUser = true;
                features.push({
                    type: 'Feature',
                    properties: userLocationData,
                    geometry: {
                        type: 'Point',
                        coordinates: [userLocationData.Longitude, userLocationData.Latitude]
                    }
                });
            }
            if (nearestLocation) {
                features.push({
                    type: 'Feature',
                    properties: nearestLocation,
                    geometry: {
                        type: 'Point',
                        coordinates: [nearestLocation.Longitude, nearestLocation.Latitude]
                    }
                });
            }

            if (features.length > 0) {
                geoJsonLayer = L.geoJSON(features, {
                    pointToLayer: (feature, latlng) => {
                        const isUserBubble = feature.properties.isUser;
                        return L.circleMarker(latlng, {
                            radius: isUserBubble ? 14 : 10,
                            weight: isUserBubble ? 3 : 1,
                            opacity: 1,
                            fillOpacity: 0.85,
                            color: isUserBubble ? '#FFD700' : '#333',
                            className: 'map-marker-bubble'
                        });
                    },
                    onEachFeature: (feature, layer) => {
                        const props = feature.properties;
                        const title = props.isUser ? `<h3>${props.Region_Name} (Estimated Data)</h3>` : `<h3>${props.Region_Name}</h3>`;
                        const popupContent = `
                            ${title}
                            <p><strong>State:</strong> ${props.State}</p>
                            <p><strong>Rainfall:</strong> ${props.Rainfall_mm} mm</p>
                            <p><strong>Soil Type:</strong> ${props.Soil_Type}</p>
                            <p><strong>Aquifer Type:</strong> ${props.Aquifer_Type}</p>
                            <p><strong>Infiltration Rate:</strong> ${props.Infiltration_Rate_mm_per_hr} mm/hr</p>
                        `;
                        layer.bindPopup(popupContent);

                        // Enhanced interactions
                        layer.on('click', function(e) {
                            const containerPoint = map.latLngToContainerPoint(e.latlng);
                            createRippleEffect(containerPoint.x, containerPoint.y);
                        });
                        
                        layer.on('mouseover', function(e) {
                            e.target.setStyle({
                                fillOpacity: 0.95,
                                weight: 4,
                                color: '#FFD700'
                            });
                        });
                        
                        layer.on('mouseout', function(e) {
                            const isUserBubble = e.target.feature.properties.isUser;
                            e.target.setStyle({
                                fillOpacity: 0.85,
                                weight: isUserBubble ? 3 : 1,
                                color: isUserBubble ? '#FFD700' : '#333'
                            });
                        });
                    }
                }).addTo(map);

                // Initialize animations
                createWaterParticles();
                createFlowArrows();

                // Open user's popup by default
                geoJsonLayer.eachLayer(layer => {
                    if (layer.feature.properties.isUser) {
                        layer.openPopup();
                    }
                });

                updateMapLayer('rainfall');
            }

            // 5. Update map layer function
            function updateMapLayer(layerKey) {
                const layerConfig = layers[layerKey];

                geoJsonLayer.eachLayer(layer => {
                    const value = layer.feature.properties[layerConfig.property];
                    layer.setStyle({
                        fillColor: layerConfig.getColor(value),
                        color: layer.feature.properties.isUser ? '#FFD700' : '#333'
                    });
                });

                updateLegend(layerKey);
            }

            // 6. Update legend function
            function updateLegend(layerKey) {
                const legendContainer = document.getElementById('legend');
                const layerConfig = layers[layerKey];
                
                let legendHTML = `<h4>${layerConfig.name}</h4>`;
                layerConfig.categories.forEach(category => {
                    legendHTML += `
                        <div class="legend-item">
                            <div class="legend-color" style="background-color: ${category.color};"></div>
                            <span>${category.label || category.value}</span>
                        </div>
                    `;
                });
                legendContainer.innerHTML = legendHTML;
            }

            // 7. Event listeners for controls
            const controls = document.getElementById('layer-controls');
            controls.addEventListener('change', (event) => {
                if (event.target.name === 'layer') {
                    updateMapLayer(event.target.value);
                }
            });
        });
    </script>