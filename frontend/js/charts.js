/**
 * Charts Component - Chart.js visualizations
 */

const Charts = {
    priceChart: null,
    roomTypeChart: null,
    sentimentChart: null,
    neighbourhoodChart: null,

    /**
     * Create price by neighbourhood chart
     */
    async createPriceChart() {
        try {
            const data = await API.getPriceStats();
            const neighbourhoods = data.by_neighbourhood.slice(0, 10); // Top 10
            
            const ctx = document.getElementById('priceChart').getContext('2d');
            
            if (this.priceChart) {
                this.priceChart.destroy();
            }
            
            this.priceChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: neighbourhoods.map(n => n._id),
                    datasets: [{
                        label: 'Average Price (£)',
                        data: neighbourhoods.map(n => n.avg_price.toFixed(2)),
                        backgroundColor: '#2563eb',
                        borderColor: '#1d4ed8',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
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
     * Create room type distribution chart
     */
    async createRoomTypeChart() {
        try {
            const data = await API.getRoomTypeDistribution();
            
            const ctx = document.getElementById('roomTypeChart').getContext('2d');
            
            if (this.roomTypeChart) {
                this.roomTypeChart.destroy();
            }
            
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
     * Create sentiment chart
     */
    async createSentimentChart() {
        try {
            const data = await API.getSentiment();
            const sentiment = data.sentiment;
            
            const ctx = document.getElementById('sentimentChart').getContext('2d');
            
            if (this.sentimentChart) {
                this.sentimentChart.destroy();
            }
            
            this.sentimentChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Positive', 'Neutral', 'Negative'],
                    datasets: [{
                        data: [
                            sentiment.positive.count,
                            sentiment.neutral.count,
                            sentiment.negative.count
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
     * Create top neighbourhoods by sentiment chart
     */
    async createNeighbourhoodChart() {
        try {
            const data = await API.getSentimentByNeighbourhood();
            const topNeighbourhoods = data.slice(0, 10);
            
            const ctx = document.getElementById('neighbourhoodChart').getContext('2d');
            
            if (this.neighbourhoodChart) {
                this.neighbourhoodChart.destroy();
            }
            
            this.neighbourhoodChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: topNeighbourhoods.map(n => n.neighbourhood),
                    datasets: [{
                        label: 'Positive %',
                        data: topNeighbourhoods.map(n => n.positive_pct),
                        backgroundColor: '#10b981',
                        borderColor: '#059669',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            max: 100,
                            title: {
                                display: true,
                                text: 'Positive Reviews (%)'
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error creating neighbourhood chart:', error);
        }
    },

    /**
     * Create word cloud visualization
     */
    async createWordCloud(sentiment = 'positive') {
        try {
            const words = await API.getWordCloud(sentiment, 30);
            const container = document.getElementById('wordCloud');
            
            // Clear existing content
            container.innerHTML = '';
            
            if (words.length === 0) {
                container.innerHTML = '<p style="color: #6b7280;">No word data available</p>';
                return;
            }
            
            // Find max count for scaling
            const maxCount = Math.max(...words.map(w => w.count));
            
            // Create word elements
            words.forEach(word => {
                const wordEl = document.createElement('div');
                wordEl.className = 'word-item';
                
                // Scale font size based on frequency
                const fontSize = 0.75 + (word.count / maxCount) * 1.5;
                wordEl.style.fontSize = `${fontSize}rem`;
                
                // Color based on sentiment
                let color = '#2563eb';
                if (sentiment === 'positive') color = '#10b981';
                if (sentiment === 'negative') color = '#ef4444';
                wordEl.style.color = color;
                
                wordEl.textContent = word.word;
                wordEl.title = `${word.word}: ${word.count} mentions`;
                
                container.appendChild(wordEl);
            });
        } catch (error) {
            console.error('Error creating word cloud:', error);
        }
    },

    /**
     * Initialize all charts
     */
    async initAll() {
        await Promise.all([
            this.createPriceChart(),
            this.createRoomTypeChart(),
            this.createSentimentChart(),
            this.createNeighbourhoodChart(),
            this.createWordCloud('positive')
        ]);
    }
};