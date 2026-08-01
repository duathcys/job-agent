import { useState } from 'react';
import { login as loginApi } from '../api/auth';

export function useAuth() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const res = await loginApi(email, password);
      localStorage.setItem('token', res.data.access_token);
      return true;
    } catch (e) {
      setError(e.response?.data?.detail || '로그인 실패');
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  const isLoggedIn = () => !!localStorage.getItem('token');

  return { login, logout, isLoggedIn, loading, error };
}