import { useState } from 'react'
import './App.css'

interface Customer {
  id: string
  name: string
  email: string
  branch_id: number
  is_active: boolean
}

export default function App() {
  // Login form state
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')

  // Current logged in user state
  const [currentUser, setCurrentUser] = useState<Customer | null>(null)

  // Function to submit credentials to FastAPI
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    try {
      const response = await fetch('/api/v1/customers/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email }),
      })

      if (!response.ok) {
        throw new Error('Invalid name or email combination')
      }

      const userData: Customer = await response.json()
      setCurrentUser(userData) // Save user to state upon successful login
    } catch (err: any) {
      setError(err.message || 'Failed to login')
    }
  }

  const handleLogout = () => {
    setCurrentUser(null)
    setName('')
    setEmail('')
  }

  // --- IF NOT LOGGED IN: SHOW LOGIN SCREEN ---
  if (!currentUser) {
    return (
      <div className="container">
        <div className="login-card">
          <header className="header" style={{ border: 'none', padding: 0 }}>
            <h1>Bank Portal Sign In</h1>
            <p>Enter your Name and Email to continue</p>
          </header>

          <form onSubmit={handleLogin} className="login-form">
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                placeholder="e.g. Alice"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>Email Address</label>
              <input
                type="email"
                placeholder="alice@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            {error && <p className="error-message">{error}</p>}

            <button type="submit" className="btn-primary">
              Sign In
            </button>
          </form>
        </div>
      </div>
    )
  }

  // --- IF LOGGED IN: SHOW DASHBOARD ---
  return (
    <div className="container">
      <header className="header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>Welcome, {currentUser.name}!</h1>
          <p>Logged in as {currentUser.email}</p>
        </div>
        <button onClick={handleLogout} className="btn-primary" style={{ backgroundColor: '#64748b' }}>
          Log Out
        </button>
      </header>

      <main className="card-grid">
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Your Profile Details</h2>
            <span className="badge active">Active</span>
          </div>
          <div className="card-details">
            <p><span>Customer ID:</span> <strong>{currentUser.id}</strong></p>
            <p><span>Branch ID:</span> <strong>#{currentUser.branch_id}</strong></p>
            <p><span>Email:</span> <strong>{currentUser.email}</strong></p>
          </div>
        </div>
      </main>
    </div>
  )
}