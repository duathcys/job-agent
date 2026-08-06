import client from './client';

export const uploadResume = (file, apply = false) => {
  const formData = new FormData();
  formData.append('file', file);
  return client.post(`/resume/upload?apply=${apply}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};