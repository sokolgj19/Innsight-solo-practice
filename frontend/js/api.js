/**
 * API Service - Neighbourhood-aware API calls
 */

const API_BASE_URL = 'http://localhost:5000/api';
const CITY = 'london';

const API = {
    /**
     * Get listings with filters
     */
    async getListings(filters = {}) {
        try {
            const params = new URLSearchParams();
            
            if (filters.minPrice) params.append('min_price', filters.minPrice);
            if (filters.maxPrice) params.append('max_price', filters.maxPrice);
            if (filters.roomType) params.append('room_type', filters.roomType);
            if (filters.neighbourhood) params.append('neighbourhood', filters.neighbourhood);
            params.append('limit', filters.limit || 5000);
            
            const response = await fetch(`${API_BASE_URL}/listings/${CITY}?${params}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching listings:', error);
            throw error;
        }
    },

    /**
     * Get neighbourhoods list
     */
    async getNeighbourhoods() {
        try {
            const response = await fetch(`${API_BASE_URL}/listings/${CITY}/neighbourhoods`);
            const data = await response.json();
            return data.neighbourhoods || [];
        } catch (error) {
            console.error('Error fetching neighbourhoods:', error);
            return [];
        }
    },

    /**
     * Get price statistics (optionally for specific neighbourhood)
     */
    async getPriceStats(neighbourhood = null) {
        try {
            const response = await fetch(`${API_BASE_URL}/analytics/${CITY}/price-stats`);
            const data = await response.json();
            
            if (neighbourhood) {
                // Filter for specific neighbourhood
                const nbData = data.by_neighbourhood.find(n => n._id === neighbourhood);
                return nbData || { avg_price: 0, count: 0 };
            }
            
            return data;
        } catch (error) {
            console.error('Error fetching price stats:', error);
            throw error;
        }
    },

    /**
     * Get room type distribution (for neighbourhood if specified)
     */
    async getRoomTypeDistribution(neighbourhood = null) {
        try {
            let url = `${API_BASE_URL}/listings/${CITY}`;
            if (neighbourhood) {
                url += `?neighbourhood=${encodeURIComponent(neighbourhood)}&limit=10000`;
            } else {
                url += '?limit=10000';
            }
            
            const response = await fetch(url);
            const data = await response.json();
            const listings = data.listings || [];
            
            // Calculate distribution client-side
            const roomCounts = {};
            listings.forEach(listing => {
                const roomType = listing.room_type || 'Unknown';
                roomCounts[roomType] = (roomCounts[roomType] || 0) + 1;
            });
            
            const total = listings.length;
            const distribution = Object.keys(roomCounts).map(type => ({
                _id: type,
                count: roomCounts[type],
                percentage: total > 0 ? (roomCounts[type] / total * 100).toFixed(1) : 0
            }));
            
            return {
                city: CITY,
                neighbourhood: neighbourhood,
                total_listings: total,
                distribution
            };
        } catch (error) {
            console.error('Error fetching room type distribution:', error);
            throw error;
        }
    },

    /**
     * Get overall sentiment statistics
     */
    async getSentiment() {
        try {
            const response = await fetch(`${API_BASE_URL}/analytics/${CITY}/sentiment`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching sentiment:', error);
            throw error;
        }
    },

    /**
     * Get sentiment by neighbourhood (all or specific one)
     */
    async getSentimentByNeighbourhood(neighbourhood = null) {
        try {
            const response = await fetch(`${API_BASE_URL}/analytics/${CITY}/sentiment/by-neighbourhood`);
            const data = await response.json();
            
            if (neighbourhood) {
                // Return array with just that neighbourhood
                return data.neighbourhoods.filter(n => n.neighbourhood === neighbourhood);
            }
            
            return data.neighbourhoods || [];
        } catch (error) {
            console.error('Error fetching sentiment by neighbourhood:', error);
            return [];
        }
    },

    /**
     * Get occupancy data (mock for now - requires calendar collection)
     */
    async getOccupancy(neighbourhood = null) {
        try {
            const response = await fetch(`${API_BASE_URL}/analytics/${CITY}/occupancy`);
            const data = await response.json();
            
            // If API returns data, use it
            if (data.by_month && data.by_month.length > 0) {
                return data;
            }
            
            // Otherwise return mock data
            return this.getMockOccupancy(neighbourhood);
        } catch (error) {
            console.log('Occupancy endpoint not available, using mock data');
            return this.getMockOccupancy(neighbourhood);
        }
    },
    
    /**
     * Generate mock occupancy data for demonstration
     */
    getMockOccupancy(neighbourhood) {
        const months = [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ];
        
        // Base occupancy rates (higher in summer)
        const baseRates = [45, 48, 55, 62, 70, 78, 85, 82, 68, 58, 50, 52];
        
        // Add some variation for specific neighbourhoods
        const variation = neighbourhood ? Math.random() * 10 - 5 : 0;
        
        return {
            city: CITY,
            neighbourhood: neighbourhood,
            by_month: months.map((month, i) => ({
                _id: `2024-${String(i + 1).padStart(2, '0')}`,
                month: month,
                occupancy_rate: Math.max(0, Math.min(100, baseRates[i] + variation))
            }))
        };
    },

    /**
     * Get top hosts (for neighbourhood if specified)
     */
    async getTopHosts(neighbourhood = null, limit = 10) {
        try {
            let url = `${API_BASE_URL}/listings/${CITY}`;
            if (neighbourhood) {
                url += `?neighbourhood=${encodeURIComponent(neighbourhood)}&limit=10000`;
            } else {
                url += '?limit=10000';
            }
            
            const response = await fetch(url);
            const data = await response.json();
            const listings = data.listings || [];
            
            // Group by host and count
            const hostCounts = {};
            listings.forEach(listing => {
                const hostId = listing.host_id || 'unknown';
                const hostName = listing.host_name || 'Unknown Host';
                
                if (!hostCounts[hostId]) {
                    hostCounts[hostId] = {
                        host_id: hostId,
                        host_name: hostName,
                        listing_count: 0,
                        total_price: 0,
                        count_with_price: 0
                    };
                }
                
                hostCounts[hostId].listing_count++;
                if (listing.price) {
                    hostCounts[hostId].total_price += listing.price;
                    hostCounts[hostId].count_with_price++;
                }
            });
            
            // Convert to array and calculate averages
            const hosts = Object.values(hostCounts).map(host => ({
                _id: host.host_id,
                host_name: host.host_name,
                listing_count: host.listing_count,
                avg_price: host.count_with_price > 0 
                    ? host.total_price / host.count_with_price 
                    : 0
            }));
            
            // Sort by listing count and take top N
            hosts.sort((a, b) => b.listing_count - a.listing_count);
            
            return {
                city: CITY,
                neighbourhood: neighbourhood,
                top_hosts: hosts.slice(0, limit)
            };
        } catch (error) {
            console.error('Error fetching top hosts:', error);
            return { top_hosts: [] };
        }
    }
};