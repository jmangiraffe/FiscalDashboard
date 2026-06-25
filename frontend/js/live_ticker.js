// Point this to your Render URL later (e.g., https://your-backend.onrender.com)
const API_BASE_URL = "http://127.0.0.1:8000";

async function initLiveTicker() {
    const clockElement = document.getElementById('debt-clock');
    const velocityElement = document.getElementById('velocity-rate');
    
    try {
        // 1. Fetch the data once
        const response = await fetch(`${API_BASE_URL}/api/v1/metrics/current`);
        const result = await response.json();
        
        let currentDebt = result.snapshot.total_debt_raw;
        const velocityPerSecond = result.velocity_per_second;
        
        velocityElement.textContent = velocityPerSecond.toLocaleString();
        
        // 2. Set up the Live Clock Math (Updates every 100 milliseconds)
        const ticksPerSecond = 10;
        const incrementPerTick = velocityPerSecond / ticksPerSecond;
        
        setInterval(() => {
            currentDebt += incrementPerTick; [cite: 150]
            
            // Format to USD currency
            clockElement.textContent = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                maximumFractionDigits: 0
            }).format(currentDebt); [cite: 151, 152, 153, 154, 155, 156]
            
        }, 1000 / ticksPerSecond); [cite: 157]
        
    } catch (error) {
        console.error("Failed to load metrics:", error); [cite: 158, 159]
        clockElement.textContent = "Data Sync Error"; [cite: 160]
    }
}

// Start the engine when the script loads
initLiveTicker(); [cite: 164]
