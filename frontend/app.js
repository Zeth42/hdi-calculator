document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('hdiForm');
    const sliders = ['elec_access', 'outages', 'losses', 'oil', 'gas', 'renewables'];
    
    // Reference database for auto-fill feature
    const countryData = {
        norway: { gdp: 87500, cons: 23500, access: 100, outages: 0, losses: 5, oil: 0, gas: 1, renewables: 99 },
        mexico: { gdp: 11400, cons: 2600, access: 99, outages: 12, losses: 14, oil: 11, gas: 58, renewables: 31 },
        nigeria: { gdp: 2100, cons: 140, access: 55, outages: 82, losses: 16, oil: 15, gas: 65, renewables: 20 }
    };

    // Update UI text displays when sliders move
    const updateSliderUI = (id, value) => {
        const slider = document.getElementById(id);
        const display = document.getElementById(`${id}_val`);
        
        if (slider) slider.value = value;
        if (display) display.textContent = `${value}%`;

        if (['oil', 'gas', 'renewables'].includes(id)) {
            const oilEl = document.getElementById('oil');
            const gasEl = document.getElementById('gas');
            const renEl = document.getElementById('renewables');
            const totalDisplay = document.getElementById('matrix_total_display');

            if (oilEl && gasEl && renEl && totalDisplay) {
                const total = parseInt(oilEl.value || 0) +
                            parseInt(gasEl.value || 0) +
                            parseInt(renEl.value || 0);
                
                totalDisplay.textContent = `Total Matriz: ${total}%`;
                totalDisplay.style.color = (total !== 100) ? '#ef4444' : '#166534';
            }
        }
    };

    // Attach event listeners to all sliders
    sliders.forEach(id => {
        document.getElementById(id).addEventListener('input', (e) => updateSliderUI(id, e.target.value));
    });

    // Handle "Load" buttons from the Reference Table
    document.querySelectorAll('.btn-load').forEach(btn => {
        btn.addEventListener('click', () => {
            const countryKey = btn.getAttribute('data-country');
            const data = countryData[countryKey];

            // Populate text inputs
            document.getElementById('gdp_capita').value = data.gdp;
            document.getElementById('consumption_capita').value = data.cons;

            // Populate sliders and update UI labels
            sliders.forEach(id => {
                if (data[id] !== undefined) updateSliderUI(id, data[id]);
            });
        });
    });

    // Form Submission to FastAPI Backend
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI Elements
        const resultCard = document.getElementById('resultCard');
        const resultPlaceholder = document.getElementById('resultPlaceholder');
        const resultDisplay = document.getElementById('resultDisplay');
        const hdiValue = document.getElementById('hdiValue');
        const hdiBadge = document.getElementById('hdiBadge');
        const submitBtn = document.getElementById('submitBtn');

        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing Mathematical Simulation...';

        // Pack payload and format percentages into [0, 1] fractions for the ML model
        const payload = {
            gdp_capita: parseFloat(document.getElementById('gdp_capita').value),
            elec_access: parseFloat(document.getElementById('elec_access').value) / 100,
            consumption_capita: parseFloat(document.getElementById('consumption_capita').value),
            outages: parseFloat(document.getElementById('outages').value) / 100,
            losses: parseFloat(document.getElementById('losses').value) / 100,
            oil: parseFloat(document.getElementById('oil').value) / 100,
            gas: parseFloat(document.getElementById('gas').value) / 100,
            renewables: parseFloat(document.getElementById('renewables').value) / 100
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error('Backend Engine Connection Failed.');

            const data = await response.json();

            // Render Results
            resultPlaceholder.style.display = 'none';
            resultDisplay.style.display = 'block';
            resultCard.classList.add('success');
            
            // Format float to 3 decimal places (UN Standard)
            hdiValue.textContent = data.estimated_hdi.toFixed(3);
            
            // Update Human Development Classification Badge
            hdiBadge.className = `badge ${data.interpretation.replace(' ', '')}`;
            
            const transMap = { 'Very High': 'Muy Alto', 'High': 'Alto', 'Medium': 'Medio', 'Low': 'Bajo' };
            hdiBadge.textContent = `Desarrollo ${transMap[data.interpretation]}`;

        } catch (error) {
            alert(`Error: ${error.message}`);
            resultPlaceholder.style.display = 'block';
            resultDisplay.style.display = 'none';
            resultCard.classList.remove('success');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Calcular IDH Predictivo';
        }
    });
});