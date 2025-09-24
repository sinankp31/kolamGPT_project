const API_BASE_URL = 'http://127.0.0.1:5001/api';

export const chatAPI = {
  sendMessage: async (message, image = null) => {
    try {
      let response;

      if (image) {
        const formData = new FormData();
        formData.append('image', image.file);
        if (message) {
          formData.append('prompt', message);
        }

        response = await fetch(`${API_BASE_URL}/chat`, {
          method: 'POST',
          body: formData,
        });
      } else {
        response = await fetch(`${API_BASE_URL}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ prompt: message }),
        });
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Chat API error:', error);
      throw error;
    }
  },

  analyzeKolam: async (imageData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/analyze_kolam`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image_data: imageData }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Analysis API error:', error);
      throw error;
    }
  },

  sendContact: async (contactData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(contactData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Contact API error:', error);
      throw error;
    }
  },
};

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