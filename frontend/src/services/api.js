import axios from 'axios';

const apiClient = axios.create({
  // Use /api prefix to match the FastAPI mount point
  baseURL: '/api',
});

// CRITICAL: Ensure 'export' is present here
export const uploadPDF = (file) => {
  const formData = new FormData();
  // Ensure the key 'file' matches what FastAPI expects: UploadFile = File(...)
  formData.append('file', file);
  return apiClient.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const sendChatMessage = (message) => {
  // Sending as a query parameter to match your FastAPI chat endpoint
  return apiClient.post(`/chat?query=${encodeURIComponent(message)}`);
};





// import axios from 'axios';
//
// const apiClient = axios.create({
//   // In a unified build, the base URL is the same as the window location
//   baseURL: '/api',
// });
//
// export const sendChatMessage = (message) => {
//   return apiClient.post('/chat?query=' + encodeURIComponent(message));
// };
