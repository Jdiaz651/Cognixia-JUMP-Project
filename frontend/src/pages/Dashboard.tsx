import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/api';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import type { Account, Transaction, User } from '../types';

export const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [accounts, setAccounts] = useState<Account[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(false);

  // Form states
  const [newAccountType, setNewAccountType] = useState<'checking' | 'savings'>('checking');
  const [depositAccNum, setDepositAccNum] = useState('');
  const [depositAmount, setDepositAmount] = useState('');
  const [withdrawAccNum, setWithdrawAccNum] = useState('');
  const [withdrawAmount, setWithdrawAmount] = useState('');
  const [transferFrom, setTransferFrom] = useState('');
  const [transferTo, setTransferTo] = useState('');
  const [transferAmount, setTransferAmount] = useState('');

  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchData();
  }, [user, navigate]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [accRes, txnRes] = await Promise.all([
        api.get('/accounts'),
        api.get('/transactions')
      ]);

      // Filter accounts by current user
      setAccounts(accRes.data.filter((a: Account) => a.owner_id === user?.id));
      // For now, let's show all transactions or maybe just the ones involving user's accounts.
      // This is a bit complex for a simple demo, so let's just show all transactions for now.
      setTransactions(txnRes.data);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/accounts', { account_type: newAccountType });
      setMessage({ type: 'success', text: 'Account created successfully!' });
      fetchData();
    } catch (err: any) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to create account' });
    }
  };

  const handleDeposit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/accounts/deposit', {
        account_number: Number(depositAccNum),
        amount: Number(depositAmount)
      });
      setMessage({ type: 'success', text: 'Deposit successful!' });
      fetchData();
    } catch (err: any) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Deposit failed' });
    }
  };

  const handleWithdraw = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/accounts/withdraw', {
        account_number: Number(withdrawAccNum),
        amount: Number(withdrawAmount)
      });
      setMessage({ type: 'success', text: 'Withdrawal successful!' });
      fetchData();
    } catch (err: any) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Withdrawal failed' });
    }
  };

  const handleTransfer = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/transactions/transfer', {
        from_account: Number(transferFrom),
        to_account: Number(transferTo),
        amount: Number(transferAmount)
      });
      setMessage({ type: 'success', text: 'Transfer successful!' });
      fetchData();
    } catch (err: any) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Transfer failed' });
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <h1>Welcome, {user?.name}</h1>
          <p>{user?.email}</p>
        </div>
        <Button onClick={logout} className="btn-outline">Logout</Button>
      </header>

      {message && (
        <div className={`alert ${message.type}`}>
          {message.text}
          <Button onClick={() => setMessage(null)} className="btn-close">×</Button>
        </div>
      )}

      <div className="dashboard-grid">
        {/* Quick Actions */}
        <section className="actions-section">
          <h3>Quick Actions</h3>

          <div className="action-card">
            <h4>Create New Account</h4>
            <form onSubmit={handleCreateAccount}>
              <select
                value={newAccountType}
                onChange={(e) => setNewAccountType(e.target.value as any)}
              >
                <option value="checking">Checking</option>
                <option value="savings">Savings</option>
              </select>
              <Button type="submit" className="btn-primary">Create</Button>
            </form>
          </div>

          <div className="action-card">
            <h4>Deposit</h4>
            <form onSubmit={handleDeposit}>
              <Input label="Account Number" value={depositAccNum} onChange={setDepositAccNum} required />
              <Input label="Amount" type="number" value={depositAmount} onChange={setDepositAmount} required />
              <Button type="submit" className="btn-primary">Deposit</Button>
            </form>
          </div>

          <div className="action-card">
            <h4>Withdraw</h4>
            <form onSubmit={handleWithdraw}>
              <Input label="Account Number" value={withdrawAccNum} onChange={setWithdrawAccNum} required />
              <Input label="Amount" type="number" value={withdrawAmount} onChange={setWithdrawAmount} required />
              <Button type="submit" className="btn-primary">Withdraw</Button>
            </form>
          </div>

          <div className="action-card">
            <h4>Transfer Funds</h4>
            <form onSubmit={handleTransfer}>
              <Input label="From Account" value={transferFrom} onChange={setTransferFrom} required />
              <Input label="To Account" value={transferTo} onChange={setTransferTo} required />
              <Input label="Amount" type="number" value={transferAmount} onChange={setTransferAmount} required />
              <Button type="submit" className="btn-primary">Transfer</Button>
            </form>
          </div>
        </section>

        {/* My Accounts */}
        <section className="accounts-section">
          <h3>My Accounts</h3>
          {loading ? <p>Loading...</p> : (
            <div className="account-list">
              {accounts.length > 0 ? (
                accounts.map(a => (
                  <div key={a.id} className="account-card">
                    <div className="acc-header">
                      <span className="acc-type">{a.account_type}</span>
                      <span className="acc-num">#{a.account_number}</span>
                    </div>
                    <div className="acc-balance">${a.balance.toFixed(2)}</div>
                  </div>
                ))
              ) : <p>No accounts found.</p>}
            </div>
          )}
        </section>

        {/* Transactions History */}
        <section className="transactions-section">
          <h3>Recent Transactions</h3>
          <div className="transactions-table">
            <table>
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Amount</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {transactions.slice(0, 10).map(t => (
                  <tr key={t.id}>
                    <td className={`txn-type ${t.type}`}>{t.type}</td>
                    <td className={t.type === 'transfer' ? 'text-primary' : ''}>${t.amount.toFixed(2)}</td>
                    <td>{new Date(t.timestamp).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
};
