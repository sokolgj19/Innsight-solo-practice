/**
 * Charts Component - Neighbourhood-Specific Visualizations
 */

const Charts = {
    priceChart: null,
    roomTypeChart: null,
    sentimentChart: null,
    occupancyChart: null,

    /**
     * Update all charts for specific neighbourhood or all London
     */
    async updateAll(neighbourhood = null) {
        const title = neighbourhood ? neighbourhood : 'All London';
        console.log(`Updating charts for: ${title}`);
        
        await Promise.all([
            this.createPriceChart(neighbourhood),
            this.createRoomTypeChart(neighbourhood),
            this.createSentimentChart(neighbourhood),
            this.createOccupancyChart(neighbourhood)
        ]);
    },

    /**
     * Create price by neighbourhood chart
     */
    async createPriceChart(selectedNeighbourhood = null) {
        try {
            const data = await API.getPriceStats();
            
            let neighbourhoods;
            if (selectedNeighbourhood) {
                // Show just the selected neighbourhood
                neighbourhoods = data.by_neighbourhood.filter(n => n._id === selectedNeighbourhood);
            } else {
                // Show top 10
                neighbourhoods = data.by_neighbourhood.slice(0, 10);
            }
            
            const ctx = document.getElementById('priceChart').getContext('2d');
            
            if (this.priceChart) {
                this.priceChart.destroy();
            }
            
            const chartTitle = selectedNeighbourhood 
                ? `Average Price: ${selectedNeighbourhood}`
                : 'Top 10 Neighbourhoods by Price';
            
            this.priceChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: neighbourhoods.map(n => n._id),
                    datasets: [{
                        label: 'Average Price (£)',
                        data: neighbourhoods.map(n => n.avg_price.toFixed(2)),
                        backgroundColor: selectedNeighbourhood ? '#10b981' : '#2563eb',
                        borderColor: selectedNeighbourhood ? '#059669' : '#1d4ed8',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: chartTitle
                        },
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Price (£)'
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error creating price chart:', error);
        }
    },

    /**
     * Create room type distribution chart (neighbourhood-specific)
     */
    async createRoomTypeChart(neighbourhood = null) {
        try {
            const data = await API.getRoomTypeDistribution(neighbourhood);
            
            const ctx = document.getElementById('roomTypeChart').getContext('2d');
            
            if (this.roomTypeChart) {
                this.roomTypeChart.destroy();
            }
            
            const chartTitle = neighbourhood 
                ? `Room Types: ${neighbourhood}`
                : 'Room Type Distribution (All London)';
            
            this.roomTypeChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.distribution.map(d => d._id),
                    datasets: [{
                        data: data.distribution.map(d => d.count),
                        backgroundColor: [
                            '#2563eb',
                            '#10b981',
                            '#f59e0b',
                            '#ef4444'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: chartTitle
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error creating room type chart:', error);
        }
    },

    /**
     * Create sentiment chart (neighbourhood-specific)
     */
    async createSentimentChart(neighbourhood = null) {
        try {
            let sentimentData;
            
            if (neighbourhood) {
                const nbData = await API.getSentimentByNeighbourhood(neighbourhood);
                if (nbData.length > 0) {
                    const data = nbData[0];
                    sentimentData = {
                        positive: { count: data.positive },
                        neutral: { count: data.neutral },
                        negative: { count: data.negative }
                    };
                } else {
                    sentimentData = {
                        positive: { count: 0 },
                        neutral: { count: 0 },
                        negative: { count: 0 }
                    };
                }
            } else {
                const data = await API.getSentiment();
                sentimentData = data.sentiment;
            }
            
            const ctx = document.getElementById('sentimentChart').getContext('2d');
            
            if (this.sentimentChart) {
                this.sentimentChart.destroy();
            }
            
            const chartTitle = neighbourhood 
                ? `Sentiment: ${neighbourhood}`
                : 'Sentiment Analysis (All London)';
            
            this.sentimentChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Positive', 'Neutral', 'Negative'],
                    datasets: [{
                        data: [
                            sentimentData.positive.count,
                            sentimentData.neutral.count,
                            sentimentData.negative.count
                        ],
                        backgroundColor: [
                            '#10b981',
                            '#f59e0b',
                            '#ef4444'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: chartTitle
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error creating sentiment chart:', error);
        }
    },

    /**
     * Create monthly occupancy chart (bar chart with 12 months)
     */
    async createOccupancyChart(neighbourhood = null) {
        try {
            const data = await API.getOccupancy(neighbourhood);
            
            const ctx = document.getElementById('occupancyChart').getContext('2d');
            
            if (this.occupancyChart) {
                this.occupancyChart.destroy();
            }
            
            const chartTitle = neighbourhood 
                ? `Occupancy by Month: ${neighbourhood}`
                : 'Occupancy by Month (All London)';
            
            this.occupancyChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.by_month.map(m => m.month || m._id),
                    datasets: [{
                        label: 'Occupancy Rate (%)',
                        data: data.by_month.map(m => m.occupancy_rate.toFixed(1)),
                        backgroundColor: '#10b981',
                        borderColor: '#059669',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: chartTitle
                        },
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            title: {
                                display: true,
                                text: 'Occupancy Rate (%)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Month'
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error creating occupancy chart:', error);
        }
    },

    /**
     * Initialize all charts (first load)
     */
    async initAll() {
        await this.updateAll(null);
    }
};