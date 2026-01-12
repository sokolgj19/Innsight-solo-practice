/**
 * Map Component - Leaflet map with auto-zoom and filtered listings
 */

let map = null;
let markersLayer = null;

const MapComponent = {
    /**
     * Initialize the map
     */
    init() {
        // Create map centered on London
        map = L.map('map').setView([51.5074, -0.1278], 11);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18
        }).addTo(map);
        
        // Create layer group for markers
        markersLayer = L.layerGroup().addTo(map);
        
        console.log('Map initialized');
    },

    /**
     * Get marker color based on price
     */
    getMarkerColor(price) {
        if (!price || price === null || price === 0) {
            // This shouldn't happen anymore since we fill null prices
            return '#9ca3af'; // gray fallback
        }
        if (price > 300) return '#ef4444'; // red
        if (price > 150) return '#f59e0b'; // orange
        return '#10b981'; // green
    },

    /**
     * Create custom marker icon
     */
    createMarkerIcon(price) {
        const color = this.getMarkerColor(price);
        
        return L.divIcon({
            className: 'custom-marker',
            html: `
                <div style="
                    background-color: ${color};
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    border: 2px solid white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                "></div>
            `,
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });
    },

    /**
     * Add listings to map (no grey dots - all have prices now)
     */
    addListings(listings) {
        // Clear existing markers
        markersLayer.clearLayers();
        
        if (!listings || listings.length === 0) {
            console.log('No listings to display on map');
            return;
        }
        
        // Filter out any listings without coordinates or price
        const validListings = listings.filter(l => 
            l.latitude && 
            l.longitude && 
            l.price !== null && 
            l.price !== undefined &&
            l.price > 0
        );
        
        console.log(`Displaying ${validListings.length} valid listings (filtered out ${listings.length - validListings.length} without price/coords)`);
        
        // Add markers for each listing
        validListings.forEach(listing => {
            const marker = L.marker(
                [listing.latitude, listing.longitude],
                { icon: this.createMarkerIcon(listing.price) }
            );
            
            // Create popup content
            const popupContent = `
                <div style="font-family: sans-serif;">
                    <h3 style="margin: 0 0 8px 0; font-size: 14px; font-weight: bold;">
                        ${listing.name || 'Unnamed Listing'}
                    </h3>
                    <p style="margin: 0 0 4px 0; font-size: 12px; color: #6b7280;">
                        ${listing.neighbourhood_cleansed || 'Unknown area'}
                    </p>
                    <p style="margin: 0 0 4px 0; font-size: 14px; font-weight: bold; color: #2563eb;">
                        £${listing.price ? listing.price.toFixed(0) : 'N/A'}/night
                    </p>
                    <p style="margin: 0 0 4px 0; font-size: 12px; color: #6b7280;">
                        ${listing.room_type || 'Unknown type'}
                    </p>
                    ${listing.review_scores_rating ? `
                        <p style="margin: 0; font-size: 12px;">
                            ⭐ ${listing.review_scores_rating.toFixed(1)} 
                            (${listing.number_of_reviews || 0} reviews)
                        </p>
                    ` : ''}
                </div>
            `;
            
            marker.bindPopup(popupContent);
            marker.addTo(markersLayer);
        });
        
        console.log(`Added ${validListings.length} markers to map`);
    },

    /**
     * Zoom map to fit neighbourhood bounds
     */
    zoomToNeighbourhood(listings) {
        if (!listings || listings.length === 0) {
            console.log('No listings to zoom to');
            return;
        }
        
        // Get valid coordinates
        const coords = listings
            .filter(l => l.latitude && l.longitude)
            .map(l => [l.latitude, l.longitude]);
        
        if (coords.length === 0) {
            console.log('No valid coordinates for zoom');
            return;
        }
        
        // Create bounds from coordinates
        const bounds = L.latLngBounds(coords);
        
        // Fit map to bounds with padding
        map.fitBounds(bounds, {
            padding: [50, 50],
            maxZoom: 14
        });
        
        console.log(`Zoomed to neighbourhood with ${coords.length} listings`);
    },

    /**
     * Clear all markers
     */
    clearMarkers() {
        if (markersLayer) {
            markersLayer.clearLayers();
        }
    },
    
    /**
     * Reset map view to London
     */
    resetView() {
        map.setView([51.5074, -0.1278], 11);
    }
};