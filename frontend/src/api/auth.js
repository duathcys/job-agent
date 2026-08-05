import client from './client';

export const login = (email, password) =>
  client.post('/auth/login', { email, password });

export const register = (data) => client.post('/users/', data);

export const getMe = () => client.get('/users/me');

export const updateMe = (data) => client.patch('/users/me', data);