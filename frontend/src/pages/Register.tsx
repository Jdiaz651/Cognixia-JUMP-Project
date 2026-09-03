import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/api';
import { Button } from '../components/Button';
import { Input } from '../components/Input';

export const RegisterPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [branchId, setBranchId] = useState(1); // Default branch
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await api.post('/customers', {
        name,
        email,
        password,
        branch_id: Number(branchId)
      });
      navigate('/login');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2>Create Account</h2>
        {error && <div className="error-message">{error}</div>}
        <Input 
          label="Full Name" 
          value={name} 
          onChange={setName} 
          placeholder="John Doe" 
          required 
        />
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
        <div className="input-group">
          <label>Branch ID</label>
          <input 
            type="number" 
            value={branchId} 
            onChange={(e) => setBranchId(Number(e.target.value))} 
          />
        </div>
        <Button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </Button>
        <p className="auth-footer">
          Already have an account? <Link to="/login">Login here</Link>
        </p>
      </form>
    </div>
  );
};
