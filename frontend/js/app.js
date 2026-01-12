/**
 * Main Application - Neighbourhood-Specific Analytics
 */

const App = {
    currentFilters: {},
    currentNeighbourhood: null,
    allListings: [],
    
    /**
     * Initialize the application
     */
    async init() {
        console.log('InnSight Application Starting...');
        
        try {
            this.showLoading();
            
            // Initialize map
            MapComponent.init();
            
            // Load neighbourhoods into dropdown
            await this.loadNeighbourhoods();
            
            // Load initial data (all London)
            await this.loadData();
            
            // Initialize charts with all London data
            await Charts.initAll();
            
            // Set up event listeners
            this.setupEventListeners();
            
            this.hideLoading();
            
            console.log('Application initialized successfully!');
        } catch (error) {
            console.error('Error initializing app:', error);
            this.hideLoading();
            alert('Error loading data. Please make sure the API server is running on http://localhost:5000');
        }
    },

    /**
     * Load neighbourhoods into dropdown
     */
    async loadNeighbourhoods() {
        try {
            const neighbourhoods = await API.getNeighbourhoods();
            const select = document.getElementById('neighbourhood');
            
            neighbourhoods.forEach(name => {
                const option = document.createElement('option');
                option.value = name;
                option.textContent = name;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading neighbourhoods:', error);
        }
    },

    /**
     * Load and filter listings data
     */
    async loadData(filters = {}) {
        try {
            this.showLoading();
            
            // Fetch listings
            const listingsData = await API.getListings(filters);
            this.allListings = listingsData.listings || [];
            
            // Update listing count
            document.getElementById('listingCount').textContent = this.allListings.length.toLocaleString();
            
            // Add to map
            MapComponent.addListings(this.allListings);
            
            // If neighbourhood is selected, zoom to it
            if (filters.neighbourhood) {
                MapComponent.zoomToNeighbourhood(this.allListings);
            }
            
            // Update stats based on filtered data
            await this.updateStats(this.allListings, filters.neighbourhood);
            
            // Update all charts
            await Charts.updateAll(filters.neighbourhood);
            
            this.hideLoading();
        } catch (error) {
            console.error('Error loading data:', error);
            this.hideLoading();
        }
    },

    /**
     * Update quick stats based on current listings
     */
    async updateStats(listings, neighbourhood = null) {
        try {
            if (listings && listings.length > 0) {
                // Calculate average price from current listings
                const prices = listings.filter(l => l.price).map(l => l.price);
                const avgPrice = prices.reduce((a, b) => a + b, 0) / prices.length;
                document.getElementById('avgPrice').textContent = `£${Math.round(avgPrice)}`;
            } else {
                document.getElementById('avgPrice').textContent = '£--';
            }
            
            // Get sentiment for neighbourhood or all London
            const sentimentData = neighbourhood 
                ? await API.getSentimentByNeighbourhood(neighbourhood)
                : await API.getSentiment();
            
            let positivePct;
            if (neighbourhood && sentimentData.length > 0) {
                // Find specific neighbourhood
                const nbData = sentimentData.find(n => n.neighbourhood === neighbourhood);
                positivePct = nbData ? nbData.positive_pct : 0;
            } else if (!neighbourhood && sentimentData.sentiment) {
                positivePct = sentimentData.sentiment.positive.percentage;
            } else {
                positivePct = 0;
            }
            
            document.getElementById('sentimentScore').textContent = `${positivePct.toFixed(1)}%`;
            
        } catch (error) {
            console.error('Error updating stats:', error);
        }
    },

    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Apply filters button
        document.getElementById('applyFilters').addEventListener('click', () => {
            this.applyFilters();
        });
        
        // Reset filters button
        document.getElementById('resetFilters').addEventListener('click', () => {
            this.resetFilters();
        });
        
        // Neighbourhood dropdown change
        document.getElementById('neighbourhood').addEventListener('change', (e) => {
            const neighbourhood = e.target.value;
            this.currentNeighbourhood = neighbourhood || null;
            
            // Auto-apply when neighbourhood changes
            this.applyFilters();
        });
        
        // Enter key on inputs
        document.querySelectorAll('input, select').forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.applyFilters();
                }
            });
        });
    },

    /**
     * Apply filters and update everything
     */
    async applyFilters() {
        const filters = {
            minPrice: document.getElementById('minPrice').value,
            maxPrice: document.getElementById('maxPrice').value,
            roomType: document.getElementById('roomType').value,
            neighbourhood: document.getElementById('neighbourhood').value,
            limit: 5000
        };
        
        // Remove empty filters
        Object.keys(filters).forEach(key => {
            if (!filters[key]) delete filters[key];
        });
        
        this.currentFilters = filters;
        this.currentNeighbourhood = filters.neighbourhood || null;
        
        await this.loadData(filters);
    },

    /**
     * Reset all filters
     */
    async resetFilters() {
        document.getElementById('minPrice').value = '';
        document.getElementById('maxPrice').value = '';
        document.getElementById('roomType').value = '';
        document.getElementById('neighbourhood').value = '';
        
        this.currentFilters = {};
        this.currentNeighbourhood = null;
        
        await this.loadData();
    },

    /**
     * Show loading overlay
     */
    showLoading() {
        document.getElementById('loadingOverlay').classList.remove('hidden');
    },

    /**
     * Hide loading overlay
     */
    hideLoading() {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});