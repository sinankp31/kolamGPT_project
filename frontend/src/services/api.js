const API_BASE_URL = 'http://127.0.0.1:5001/api';

export const analyzeKolamApi = async (uploadedImage) => {
    const endpoint = `${API_BASE_URL}/analyze_kolam`;

    const payload = {
        image_data: uploadedImage?.data || null,
    };

    const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: 'Backend request failed with no JSON response.' }));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
};

export const contactFormApi = async (formData) => {
    const endpoint = `${API_BASE_URL}/contact`;

    const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: 'Contact form submission failed.' }));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
};