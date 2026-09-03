import React from 'react';

interface InputProps {
  label: string;
  type?: string;
  value: string | number;
  onChange: (val: string) => void;
  placeholder?: string;
  required?: boolean;
}

export const Input: React.FC<InputProps> = ({ label, type = 'text', value, onChange, placeholder, required = false }) => (
  <div className="input-group">
    <label>{label}</label>
    <input 
      type={type} 
      value={value} 
      onChange={(e) => onChange(e.target.value)} 
      placeholder={placeholder}
      required={required}
    />
  </div>
);
