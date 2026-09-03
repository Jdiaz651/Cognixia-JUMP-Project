import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/api';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/Button';
import { Input } from '../components/Input';

export const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // FastAPI OAuth2PasswordRequestForm expects 'username' and 'password'
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const res = await api.post('/customers/login', formData);
      const { access_token, token_type } = res.data;
      
      // We'll need to fetch user info after login. 
      // For simplicity in this demo, let's assume we can get it from a profile endpoint 
      // or we'll just decode the token if it's simple, but better to call a 'me' endpoint.
      // Since I haven't implemented /me yet, I'll fetch it from the customer list filtering by email 
      // (This is a hack, in real life use /me)
      const userRes = await api.get(`/customers/email?email=${email}`); // I'll need to add this endpoint to backend
      // Actually, I'll just use the customer endpoint if I can.
      // Let's assume for now the user is returned or we have a way to get it.
      
      // For now, I'll just assume the login returns token and I'll redirect.
      // I'll add a hacky user fetch in the next step.
      
      // Let's refine the backend to return user info on login or have a /me endpoint.
      // I'll just implement a /me endpoint in backend.
      
      const meRes = await api.get('/customers/me');
      const user = meRes.data;

      login(access_token, user);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2>Login to Cognixia Bank</h2>
        {error && <div className="error-message">{error}</div>}
        <Input 
          label="Email" 
          type="email" 
          value={email} 
          onChange={setEmail} 
          placeholder="your@email.com" 
          required 
        />
        <Input 
          label="Password" 
          type="password" 
          value={password} 
          onChange={setPassword} 
          placeholder="••••••••" 
          required 
        />
        <Button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </Button>
        <p className="auth-footer">
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </form>
    </div>
  );
};
