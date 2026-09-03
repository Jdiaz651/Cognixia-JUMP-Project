import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/Button';

export const LandingPage = () => {
  return (
    <div className="landing-container">
      <header className="landing-header">
        <div className="logo">
          <span className="logo-icon">🏦</span>
          <h1>Cognixia Bank</h1>
        </div>
      </header>

      <main className="landing-content">
        <section className="hero-section">
          <h1>Secure. Fast. Reliable.</h1>
          <p>
            Experience the next generation of digital banking. 
            Manage your accounts, track transactions, and transfer funds 
            with unparalleled ease and security.
          </p>
          <div className="hero-actions">
            <Link to="/login">
              <Button className="btn-primary">Get Started</Button>
            </Link>
            <Link to="/register">
              <Button className="btn-outline">Open an Account</Button>
            </Link>
          </div>
        </section>

        <section className="features-section">
          <div className="feature-card">
            <div className="feature-icon">🛡️</div>
            <h3>Bank-Grade Security</h3>
            <p>Your assets are protected with industry-leading encryption and monitoring.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Instant Transfers</h3>
            <p>Move money between accounts or to other users in seconds, not days.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Real-time Insights</h3>
            <p>Track every penny with detailed transaction history and account summaries.</p>
          </div>
        </section>
      </main>

      <footer className="landing-footer">
        <p>&copy; {new Date().getFullYear()} Cognixia Bank. All rights reserved.</p>
      </footer>
    </div>
  );
};
