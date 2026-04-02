// Constants
const API_URL = 'https://krushidoc.onrender.com/diagnose';
const WHATSAPP_NUMBER = '14155238886'; // Replace with your Twilio WhatsApp Sandbox number
const WHATSAPP_MSG = 'Hello KrishiDoc! I want to analyze my crop health.';

// Navigation
function openWhatsApp() {
    const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(WHATSAPP_MSG)}`;
    window.open(url, '_blank');
}

function goToWeb() {
    window.location.href = 'analyze.html';
}

// File Upload Logic (only for analyze.html)
if (document.getElementById('file-input')) {
    const fileInput = document.getElementById('file-input');
    const dropZone = document.getElementById('drop-zone');
    const previewContainer = document.getElementById('preview-container');
    const uploadPrompt = document.getElementById('upload-prompt');
    const imagePreview = document.getElementById('image-preview');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultCard = document.getElementById('result-card');
    const loadingState = document.getElementById('loading-state');
    const errorDisplay = document.getElementById('error-display');
    const errorMessage = document.getElementById('error-message');

    // Click to upload
    dropZone.addEventListener('click', () => fileInput.click());

    // Drag and drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#2D5A27';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = '#68A357';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        handleFileSelection(file);
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        handleFileSelection(file);
    });

    function handleFileSelection(file) {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                previewContainer.classList.remove('hidden');
                uploadPrompt.classList.add('hidden');
                analyzeBtn.disabled = false;
                resultCard.classList.add('hidden');
                errorDisplay.classList.add('hidden');
            };
            reader.readAsDataURL(file);
        }
    }

    window.clearImage = function() {
        fileInput.value = '';
        imagePreview.src = '#';
        previewContainer.classList.add('hidden');
        uploadPrompt.classList.remove('hidden');
        analyzeBtn.disabled = true;
        resultCard.classList.add('hidden');
        errorDisplay.classList.add('hidden');
    }

    window.uploadImage = async function() {
        const file = fileInput.files[0];
        if (!file) return;

        // UI States
        loadingState.classList.remove('hidden');
        analyzeBtn.disabled = true;
        resultCard.classList.add('hidden');
        errorDisplay.classList.add('hidden');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Analysis failed');
            }

            const data = await response.json();
            displayResult(data);
        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = error.message;
            errorDisplay.classList.remove('hidden');
        } finally {
            loadingState.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    }

    function displayResult(data) {
        document.getElementById('res-crop').textContent = data.crop || 'Unknown';
        document.getElementById('res-disease').textContent = data.disease_en || data.disease_or_deficiency || 'Unknown';
        document.getElementById('res-confidence').textContent = `${data.confidence || 0}%`;
        document.getElementById('res-scientific').textContent = data.disease_scientific || '';
        document.getElementById('res-type').textContent = data.disease_type || data.issue_type || 'Unknown';
        document.getElementById('res-yield').textContent = data.yield_risk || 'N/A';
        document.getElementById('res-revisit').textContent = data.revisit_days || data.follow_up_days || 'N/A';

        const severityBadge = document.getElementById('res-severity');
        severityBadge.textContent = data.severity || 'Unknown';
        severityBadge.className = 'severity-badge ' + (data.severity || '').toLowerCase();

        // Render bilingual bullet lists
        function renderList(elId, items) {
            const el = document.getElementById(elId);
            el.innerHTML = '';
            if (!Array.isArray(items)) return;
            items.forEach(item => {
                const li = document.createElement('li');
                li.innerHTML = `<span class="en">${item.en}</span><span class="hi">${item.hi}</span>`;
                el.appendChild(li);
            });
        }

        renderList('res-symptoms', data.symptoms);
        renderList('res-organic', data.organic);
        renderList('res-chemical', data.chemical);

        resultCard.classList.remove('hidden');
        resultCard.scrollIntoView({ behavior: 'smooth' });
    }
}
