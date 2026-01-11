/**
 * API Service - Handles all API calls to Flask backend
 * Uses ES6 async/await and Promises
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
            params.append('limit', filters.limit || 1000);
            
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
     * Get price statistics
     */
    async getPriceStats() {
        try {
            const response = await fetch(`${API_BASE_URL}/analytics/${CITY}/price-stats`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching price stats:', error);
            throw error;
        }
    },

    /**
     * Get room type distribution
     */
    async getRoomTypeDistribution() {
        try {
            const response = await fetch(`${API_BASE_URL}/analytics/${CITY}/room-type-distribution`);
            const data = await response.json();
            return data;
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
     * Get sentiment by neighbourhood
     */
    async getSentimentByNeighbourhood() {
        try {
            const response = await fetch(`${API_BASE_URL}/analytics/${CITY}/sentiment/by-neighbourhood`);
            const data = await response.json();
            return data.neighbourhoods || [];
        } catch (error) {
            console.error('Error fetching sentiment by neighbourhood:', error);
            return [];
        }
    },

    /**
     * Get word cloud data
     */
    async getWordCloud(sentiment = null, limit = 30) {
        try {
            const params = new URLSearchParams();
            if (sentiment) params.append('sentiment', sentiment);
            params.append('limit', limit);
            
            const response = await fetch(`${API_BASE_URL}/analytics/${CITY}/wordcloud?${params}`);
            const data = await response.json();
            return data.words || [];
        } catch (error) {
            console.error('Error fetching word cloud:', error);
            return [];
        }
    },

    /**
     * Get top hosts
     */
    async getTopHosts(limit = 10) {
        try {
            const response = await fetch(`${API_BASE_URL}/analytics/${CITY}/top-hosts?limit=${limit}`);
            const data = await response.json();
            return data.top_hosts || [];
        } catch (error) {
            console.error('Error fetching top hosts:', error);
            return [];
        }
    }
};