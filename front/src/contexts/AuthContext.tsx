import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '@/services/api';
import { User } from '@/types/api';
import { toast } from '@/hooks/use-toast';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar se há um usuário logado ao carregar a aplicação
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      await authApi.getStatus();
      // Chegando  aqui, o usuário tá autenticado
      // Buscar dados do usuário se houver um ID salvo
      const savedUserId = localStorage.getItem('userId');
      if (savedUserId) {
        const userData = await authApi.getUser(parseInt(savedUserId));
        setUser(userData);
      }
    } catch (error) {
      // Usuário não tá autenticado
      setUser(null);
      localStorage.removeItem('userId');
    } finally {
      setLoading(false);
    }
  };

  const login = async (username: string, password: string) => {
    try {
      setLoading(true);
      // Fazer login
      const response = await authApi.login({ username, password });
      
      try {
        // Decodificar o token JWT para pegar o user_id
        const token = response.access_token;
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));
        const userId = tokenPayload.sub; // 'sub' é onde o JWT guarda o user_id
        
        // Buscar dados do usuário pelo ID
        const userData = await authApi.getUser(userId);
        setUser(userData);
        localStorage.setItem('userId', userId.toString());
        
        toast({
          title: "Login realizado com sucesso!",
          description: `Bem-vindo, ${userData.username}!`,
        });
      } catch (error) {
        console.error('Erro ao buscar dados do usuário:', error);
        throw error;
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Erro ao fazer login';
      toast({
        title: "Erro no login",
        description: typeof errorMessage === 'string' ? errorMessage : errorMessage.error || 'Credenciais inválidas',
        variant: "destructive",
      });
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (username: string, email: string, password: string) => {
    try {
      setLoading(true);
      await authApi.register({ username, email, password });
      toast({
        title: "Conta criada com sucesso!",
        description: "Agora você pode fazer login com suas credenciais.",
      });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Erro ao criar conta';
      toast({
        title: "Erro ao criar conta",
        description: typeof errorMessage === 'string' ? errorMessage : errorMessage.error || 'Erro interno do servidor',
        variant: "destructive",
      });
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
      setUser(null);
      localStorage.removeItem('userId');
      toast({
        title: "Logout realizado com sucesso!",
        description: "Você foi desconectado da aplicação.",
      });
    } catch (error) {
      // Mesmo se houver erro no logout, limpar o estado local
      setUser(null);
      localStorage.removeItem('userId');
      toast({
        title: "Logout realizado",
        description: "Você foi desconectado da aplicação.",
      });
    }
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};