import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/api';
import { Button } from '../components/Button';
import type { Customer } from '../types';

export const AdminDashboard = () => {
  const navigate = useNavigate();
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    setLoading(true);
    try {
      const res = await api.get('/customers');
      setCustomers(res.data);
    } catch (err) {
      console.error('Error fetching customers:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this customer?')) return;
    try {
      await api.delete(`/customers/${id}`);
      setMessage({ type: 'success', text: 'Customer deleted successfully!' });
      fetchCustomers();
    } catch (err: any) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to delete customer' });
    }
  };

  const handleDeactivate = async (id: string) => {
    try {
      await api.delete(`/customers/${id}`); // The controller uses delete for deactivation (soft delete)
      setMessage({ type: 'success', text: 'Customer status updated!' });
      fetchCustomers();
    } catch (err: any) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to update status' });
    }
  };

  return (
    <div className="admin-dashboard">
      <header className="dashboard-header">
        <h1>Admin Management Console</h1>
        <div className="admin-actions">
          <Button onClick={() => navigate('/dashboard')} className="btn-outline">Go to My Account</Button>
          <Button onClick={() => navigate('/')} className="btn-outline">Home</Button>
        </div>
      </header>

      {message && (
        <div className={`alert ${message.type}`}>
          {message.text}
          <Button onClick={() => setMessage(null)} className="btn-close">×</Button>
        </div>
      )}

      <section className="admin-content">
        <div className="admin-card">
          <h3>All System Customers</h3>
          <p>Manage user access and account statuses across the entire branch network.</p>

          {loading ? (
            <p>Loading customers...</p>
          ) : (
            <div className="admin-table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Branch</th>
                    <th>Status</th>
                    <th>Role</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {customers.map((c) => (
                    <tr key={c.id}>
                      <td>{c.name}</td>
                      <td>{c.email}</td>
                      <td>#{c.branch_id}</td>
                      <td>
                        <span className={`status-dot ${c.is_active ? 'active' : 'inactive'}`}></span>
                        {c.is_active ? 'Active' : 'Inactive'}
                      </td>
                      <td>
                        {c.is_admin ? <span className="badge admin">ADMIN</span> : <span className="badge user">USER</span>}
                      </td>
                      <td>
                        <div className="admin-actions-cell">
                          <Button onClick={() => handleDeactivate(c.id)} className="btn-secondary btn-sm">
                            {c.is_active ? 'Deactivate' : 'Reactivate'}
                          </Button>
                          <Button onClick={() => handleDelete(c.id)} className="btn-error btn-sm">
                            Delete
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </section>
    </div>
  );
};
