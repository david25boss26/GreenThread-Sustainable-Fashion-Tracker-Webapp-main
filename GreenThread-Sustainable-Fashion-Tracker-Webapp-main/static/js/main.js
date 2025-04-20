$(document).ready(function() {
    $('#brandSelect').change(function() {
        const selectedBrand = $(this).val();
        if (selectedBrand) {
            $('#loadingSpinner').show();
            $('#brandDetails').addClass('d-none');
            $('#quickStats').addClass('d-none');

            fetch(`/api/brand/${encodeURIComponent(selectedBrand)}`)
                .then(response => response.json())
                .then(data => {
                    $('#brandName').text(data.brand_name);
                    
                    // Update sustainability score
                    const score = data.sustainability_score;
                    let scoreClass = '';
                    if (score >= 50) scoreClass = 'score-high';
                    else if (score >= 25) scoreClass = 'score-medium';
                    else scoreClass = 'score-low';
                    
                    $('.sustainability-score')
                        .html(`${Number(score).toFixed(2)}`)
                        .removeClass('score-high score-medium score-low')
                        .addClass(scoreClass);
                    
                    // Update badges
                    const trendColor = data.market_trend === 'Growing' ? 'success' : 
                                     data.market_trend === 'Stable' ? 'primary' : 'warning';
                    $('#marketTrendBadge').html(
                        `<span class="badge bg-${trendColor}">${data.market_trend}</span>`
                    );
                    
                    $('#certificationsBadge').html(
                        `<span class="badge bg-info">${data.certifications}</span>`
                    );
                    
                    // Update additional info
                    const additionalInfo = $('#additionalInfo');
                    additionalInfo.empty();
                    
                    const infoItems = [
                        { icon: 'cube', label: 'Material Type', value: data.material_type },
                        { icon: 'industry', label: 'Manufacturing', value: data.eco_friendly_manufacturing },
                        { icon: 'cloud', label: 'Carbon Footprint (MT)', value: Number(data.carbon_footprint_mt).toFixed(2) },
                        { icon: 'tint', label: 'Water Usage (L)', value: Number(data.water_usage_liters).toFixed(2) },
                        { icon: 'recycle', label: 'Recycling Programs', value: data.recycling_programs },
                        { icon: 'tags', label: 'Product Lines', value: data.product_lines },
                        { icon: 'dollar-sign', label: 'Avg. Price (USD)', value: `$${Number(data.average_price_usd).toFixed(2)}` }
                    ];

                    infoItems.forEach(item => {
                        if (item.value !== undefined && item.value !== null) {
                            additionalInfo.append(`
                                <tr>
                                    <td>
                                        <span class="icon-circle">
                                            <i class="fas fa-${item.icon}"></i>
                                        </span>
                                        ${item.label}
                                    </td>
                                    <td>${item.value}</td>
                                </tr>
                            `);
                        }
                    });
                    
                    $('#brandDetails').removeClass('d-none');
                    $('#quickStats').removeClass('d-none');
                    
                    // Load similar brands
                    loadSimilarBrands(selectedBrand);
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error loading brand details');
                })
                .finally(() => {
                    $('#loadingSpinner').hide();
                });
        } else {
            $('#brandDetails').addClass('d-none');
            $('#quickStats').addClass('d-none');
        }
    });
});

function loadSimilarBrands(brandName) {
    fetch(`/api/similar-brands/${encodeURIComponent(brandName)}`)
        .then(response => response.json())
        .then(data => {
            const similarBrandsContainer = $('#similarBrands');
            similarBrandsContainer.empty();
            
            data.similar_brands.forEach(brand => {
                similarBrandsContainer.append(`
                    <div class="col-md-4 mb-3">
                        <div class="similar-brand-card">
                            <div class="brand-similarity-score">
                                ${brand.similarity_score.toFixed(1)}% Match
                            </div>
                            <div class="brand-name">
                                ${brand.name}
                            </div>
                            <div class="brand-category mb-3">
                                ${brand.category}
                            </div>
                            <div class="brand-stats small text-muted mb-3">
                                <div><i class="fas fa-chart-line me-1"></i>${brand.market_trend}</div>
                                <div><i class="fas fa-certificate me-1"></i>${brand.certifications} Certifications</div>
                            </div>
                            <div class="brand-actions">
                                <button class="btn btn-outline-success btn-sm" 
                                        onclick="viewBrandDetails('${brand.name}')">
                                    <i class="fas fa-chart-bar me-1"></i>
                                    View Details
                                </button>
                                <button class="btn btn-success btn-sm" 
                                        onclick="compareBrands('${brandName}', '${brand.name}')">
                                    <i class="fas fa-exchange-alt me-1"></i>
                                    Compare
                                </button>
                            </div>
                        </div>
                    </div>
                `);
            });
        })
        .catch(error => {
            console.error('Error loading similar brands:', error);
        });
}