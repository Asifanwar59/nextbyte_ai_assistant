import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // Points to your FastAPI Docker container
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadPDF = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const sendChatMessage = (message) => {
  return apiClient.post('/chat', { query: message });
};
