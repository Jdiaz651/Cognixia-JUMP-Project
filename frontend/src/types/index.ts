export interface Customer {
  id: string;
  name: string;
  email: string;
  branch_id: number;
  is_active: boolean;
}

export interface Account {
  id: string;
  account_number: number;
  owner_id: string;
  account_type: 'checking' | 'savings';
  balance: number;
  minimum_balance?: number;
  overdraft_limit?: number;
}

export interface Transaction {
  id: string;
  from_account: number | null;
  to_account: number | null;
  amount: number;
  type: 'deposit' | 'withdraw' | 'transfer';
  timestamp: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
  is_admin: boolean
}
