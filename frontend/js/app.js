/**
 * Main Application - Orchestrates everything
 * Uses ES6 features: async/await, arrow functions, template literals
 */

const App = {
    currentFilters: {},
    
    /**
     * Initialize the application
     */
    async init() {
        console.log('InnSight Application Starting...');
        
        try {
            // Show loading
            this.showLoading();
            
            // Initialize map
            MapComponent.init();
            
            // Load neighbourhoods into dropdown
            await this.loadNeighbourhoods();
            
            // Load initial data
            await this.loadData();
            
            // Initialize charts
            await Charts.initAll();
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Hide loading
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
     * Load listings data
     */
    async loadData(filters = {}) {
        try {
            this.showLoading();
            
            // Fetch listings
            const listingsData = await API.getListings(filters);
            const listings = listingsData.listings || [];
            
            // Update listing count
            document.getElementById('listingCount').textContent = listings.length.toLocaleString();
            
            // Add to map
            MapComponent.addListings(listings);
            
            // Update stats
            await this.updateStats();
            
            this.hideLoading();
        } catch (error) {
            console.error('Error loading data:', error);
            this.hideLoading();
        }
    },

    /**
     * Update quick stats
     */
    async updateStats() {
        try {
            // Get price stats
            const priceData = await API.getPriceStats();
            const avgPrice = priceData.overall.avg_price;
            document.getElementById('avgPrice').textContent = `£${Math.round(avgPrice)}`;
            
            // Get sentiment stats
            const sentimentData = await API.getSentiment();
            const positivePct = sentimentData.sentiment.positive.percentage;
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
        
        // Word cloud filter buttons
        document.querySelectorAll('.wordcloud-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Remove active class from all buttons
                document.querySelectorAll('.wordcloud-btn').forEach(b => {
                    b.classList.remove('active');
                });
                
                // Add active class to clicked button
                e.target.classList.add('active');
                
                // Get sentiment
                const sentiment = e.target.dataset.sentiment;
                
                // Update word cloud
                Charts.createWordCloud(sentiment || null);
            });
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
     * Apply filters
     */
    async applyFilters() {
        const filters = {
            minPrice: document.getElementById('minPrice').value,
            maxPrice: document.getElementById('maxPrice').value,
            roomType: document.getElementById('roomType').value,
            neighbourhood: document.getElementById('neighbourhood').value,
            limit: 1000
        };
        
        // Remove empty filters
        Object.keys(filters).forEach(key => {
            if (!filters[key]) delete filters[key];
        });
        
        this.currentFilters = filters;
        await this.loadData(filters);
    },

    /**
     * Reset filters
     */
    async resetFilters() {
        document.getElementById('minPrice').value = '';
        document.getElementById('maxPrice').value = '';
        document.getElementById('roomType').value = '';
        document.getElementById('neighbourhood').value = '';
        
        this.currentFilters = {};
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