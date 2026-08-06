import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import PortfolioPage from './pages/PortfolioPage';
import ProfilePage from './pages/ProfilePage';
import RegisterPage from './pages/RegisterPage';

function PrivateRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/"
          element={
            <PrivateRoute>
              <HomePage />
            </PrivateRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <PrivateRoute>
              <ProfilePage />
            </PrivateRoute>
          }
        />
        <Route
          path="/portfolio"
          element={
            <PrivateRoute>
              <PortfolioPage />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}