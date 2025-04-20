let currentBrandData = null;

function updateBrandInfo(brandName) {
    if (!brandName) {
        resetCalculator();
        return;
    }

    fetch(`/api/brand/${encodeURIComponent(brandName)}`)
        .then(response => response.json())
        .then(data => {
            currentBrandData = data;
            
            // Initialize slider with current price
            const currentPrice = data.average_price_usd;
            const slider = document.getElementById('priceSlider');
            slider.min = Math.max(1, Math.floor(currentPrice * 0.5));  // 50% lower
            slider.max = Math.ceil(currentPrice * 2);  // 100% higher
            slider.value = currentPrice;
            
            // Update displays
            document.getElementById('currentPriceDisplay').textContent = currentPrice.toFixed(2);
            document.getElementById('newPriceDisplay').textContent = currentPrice.toFixed(2);
            document.getElementById('priceChangeDisplay').textContent = '0%';
            
            // Calculate initial impact
            calculateImpact(currentPrice);
        })
        .catch(error => {
            console.error('Error:', error);
            resetCalculator();
        });
}

function resetCalculator() {
    currentBrandData = null;
    document.getElementById('currentPriceDisplay').textContent = '0.00';
    document.getElementById('newPriceDisplay').textContent = '0.00';
    document.getElementById('priceChangeDisplay').textContent = '0%';
    document.getElementById('impactResults').innerHTML = `
        <div class="alert alert-info">
            Please select a brand to calculate impact.
        </div>
    `;
}

// Add event listener to slider
document.getElementById('priceSlider').addEventListener('input', function(e) {
    if (!currentBrandData) return;
    
    const newPrice = parseFloat(e.target.value);
    const currentPrice = currentBrandData.average_price_usd;
    const priceChange = ((newPrice - currentPrice) / currentPrice * 100).toFixed(1);
    
    // Update displays
    document.getElementById('newPriceDisplay').textContent = newPrice.toFixed(2);
    document.getElementById('priceChangeDisplay').textContent = 
        `${priceChange > 0 ? '+' : ''}${priceChange}%`;
    document.getElementById('priceChangeDisplay').className = 
        priceChange > 0 ? 'text-success' : 'text-danger';
    
    // Calculate impact
    calculateImpact(newPrice);
});

function calculateImpact(newPrice) {
    if (!currentBrandData) return;

    const currentPrice = currentBrandData.average_price_usd;
    const priceDifference = ((newPrice - currentPrice) / currentPrice) * 100;
    
    // Calculate impacts
    const carbonImpact = calculateCarbonImpact(priceDifference);
    const waterImpact = calculateWaterImpact(priceDifference);
    const sustainabilityImpact = calculateSustainabilityImpact(priceDifference);

    // Display results
    const resultsHtml = `
        <div class="impact-card">
            <h6 class="mb-3">Real-time Impact Analysis</h6>
            <div class="impact-meter mb-3">
                <div class="progress">
                    <div class="progress-bar bg-success" 
                         role="progressbar" 
                         style="width: ${Math.min(100, Math.max(0, (currentBrandData.sustainability_score + sustainabilityImpact)))}%">
                    </div>
                </div>
                <span class="impact-label">Sustainability Score</span>
                <span class="impact-value">
                    ${(currentBrandData.sustainability_score + sustainabilityImpact).toFixed(1)}
                    <small class="ms-1 ${sustainabilityImpact >= 0 ? 'text-success' : 'text-danger'}">
                        (${sustainabilityImpact >= 0 ? '+' : ''}${sustainabilityImpact.toFixed(1)})
                    </small>
                </span>
            </div>
            
            <div class="impact-meter mb-3">
                <div class="progress">
                    <div class="progress-bar bg-info" 
                         role="progressbar" 
                         style="width: ${Math.min(100, Math.max(0, ((currentBrandData.carbon_footprint_mt + carbonImpact) / currentBrandData.carbon_footprint_mt) * 100))}%">
                    </div>
                </div>
                <span class="impact-label">Carbon Footprint (MT)</span>
                <span class="impact-value">
                    ${(currentBrandData.carbon_footprint_mt + carbonImpact).toFixed(1)}
                    <small class="ms-1 ${carbonImpact <= 0 ? 'text-success' : 'text-danger'}">
                        (${carbonImpact >= 0 ? '+' : ''}${carbonImpact.toFixed(1)})
                    </small>
                </span>
            </div>
            
            <div class="impact-meter">
                <div class="progress">
                    <div class="progress-bar bg-primary" 
                         role="progressbar" 
                         style="width: ${Math.min(100, Math.max(0, ((currentBrandData.water_usage_liters + waterImpact) / currentBrandData.water_usage_liters) * 100))}%">
                    </div>
                </div>
                <span class="impact-label">Water Usage (L)</span>
                <span class="impact-value">
                    ${(currentBrandData.water_usage_liters + waterImpact).toFixed(1)}
                    <small class="ms-1 ${waterImpact <= 0 ? 'text-success' : 'text-danger'}">
                        (${waterImpact >= 0 ? '+' : ''}${waterImpact.toFixed(1)})
                    </small>
                </span>
            </div>
        </div>
    `;

    document.getElementById('impactResults').innerHTML = resultsHtml;
}

function calculateCarbonImpact(priceDifference) {
    return -(currentBrandData.carbon_footprint_mt * (priceDifference * 0.005));
}

function calculateWaterImpact(priceDifference) {
    return -(currentBrandData.water_usage_liters * (priceDifference * 0.003));
}

function calculateSustainabilityImpact(priceDifference) {
    return priceDifference * 0.2;
}

// Initialize calculator on page load
document.addEventListener('DOMContentLoaded', resetCalculator); 