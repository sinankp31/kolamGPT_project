// API service functions for frontend

const API_BASE_URL = '';

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

        response = await fetch(`${API_BASE_URL}/api/chat`, {
          method: 'POST',
          body: formData,
        });
      } else {
        response = await fetch(`${API_BASE_URL}/api/chat`, {
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
      const response = await fetch(`${API_BASE_URL}/api/analyze_kolam`, {
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
      const response = await fetch(`${API_BASE_URL}/api/contact`, {
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