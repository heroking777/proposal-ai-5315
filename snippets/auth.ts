import { useState, useEffect } from 'react';
import jwtDecode from 'jwt-decode';

interface AuthState {
  isAuthenticated: boolean;
  user: any | null;
  token: string | null;
}

const useAuth = (): [AuthState, (token: string) => void, () => void] => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    token: null,
  });

  useEffect(() => {
    const token = localStorage.getItem('jwtToken');
    if (token) {
      const decodedUser = jwtDecode(token);
      setAuthState({
        isAuthenticated: true,
        user: decodedUser,
        token: token,
      });
    }
  }, []);

  const login = (token: string): void => {
    localStorage.setItem('jwtToken', token);
    const decodedUser = jwtDecode(token);
    setAuthState({
      isAuthenticated: true,
      user: decodedUser,
      token: token,
    });
  };

  const logout = (): void => {
    localStorage.removeItem('jwtToken');
    setAuthState({
      isAuthenticated: false,
      user: null,
      token: null,
    });
  };

  return [authState, login, logout];
};

export default useAuth;