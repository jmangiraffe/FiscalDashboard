// Point this to your Render URL later (e.g., https://your-backend.onrender.com)
const API_BASE_URL = "http://127.0.0.1:8000"; [cite: 135]

async function initLiveTicker() {
    const clockElement = document.getElementById('debt-clock'); [cite: 137]
    const velocityElement = document.getElementById('velocity-rate'); [cite: 138]
    
    try {
        // 1. Fetch the data once
        const response = await fetch(`${API_BASE_URL}/api/v1/metrics/current`); [cite: 141]
        const result = await response.json(); [cite: 142]
        
        let currentDebt = result.snapshot.total_debt_raw; [cite: 143]
        const velocityPerSecond = result.velocity_per_second; [cite: 144]
        
        velocityElement.textContent = velocityPerSecond.toLocaleString(); [cite: 145]
        
        // 2. Set up the Live Clock Math (Updates every 100 milliseconds)
        const ticksPerSecond = 10; [cite: 147]
        const incrementPerTick = velocityPerSecond / ticksPerSecond; [cite: 148]
        
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
