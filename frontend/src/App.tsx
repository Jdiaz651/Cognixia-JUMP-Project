import { useEffect, useState } from 'react'
import './App.css'

interface Customer {
  id: string
  name: string
  email: string
  branch_id: number
  is_active: boolean
}

export default function App() {
  const [customers, setCustomers] = useState<Customer[]>([])

  useEffect(() => {
    fetch('/api/v1/customers')
      .then((res) => res.json())
      .then((data: Customer[]) => setCustomers(data))
      .catch((err) => console.error('Error fetching customers:', err))
  }, [])

  return (
    <div className="container">
      <header className="header">
        <h1>Bank Customers</h1>
        <p>Active account directory connected to FastAPI & MongoDB</p>
      </header>

      <main className="card-grid">
        {customers.map((c) => (
          <div key={c.id} className="card">
            <div className="card-header">
              <h2 className="card-title">{c.name}</h2>
              <span className={`badge ${c.is_active ? 'active' : 'inactive'}`}>
                {c.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>

            <div className="card-details">
              <p>
                <span>Email:</span>
                <strong>{c.email}</strong>
              </p>
              <p>
                <span>Branch:</span>
                <strong>#{c.branch_id}</strong>
              </p>
            </div>
          </div>
        ))}
      </main>
    </div>
  )
}