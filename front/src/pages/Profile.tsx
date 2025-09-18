import { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';
import pcsLogo from '@/assets/pcs-logo.png';

const Profile = () => {
  const { user, logout, isAuthenticated, loading } = useAuth();
  const [tokenId, setTokenId] = useState<string>('');

  useEffect(() => {
    // Simular obtenção do token ID (normalmente viria do JWT decodificado)
    const generateTokenId = () => {
      const chars = '0123456789abcdef';
      let result = '';
      for (let i = 0; i < 32; i++) {
        if (i > 0 && i % 4 === 0) result += '-';
        result += chars[Math.floor(Math.random() * chars.length)];
      }
      return result;
    };

    if (user) {
      setTokenId(generateTokenId());
    }
  }, [user]);

  // Redirecionar se não estiver autenticado
  if (!isAuthenticated && !loading) {
    return <Navigate to="/login" replace />;
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
          <p className="mt-2 text-muted-foreground">Carregando...</p>
        </div>
      </div>
    );
  }

  const handleLogout = async () => {
    await logout();
  };

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8">
        {/* Logo e Header */}
        <div className="text-center space-y-4">
          <img 
            src={pcsLogo} 
            alt="PCS Logo" 
            className="h-32 mx-auto object-contain"
          />
          <div className="space-y-2">
            <h1 className="text-2xl font-bold text-foreground">
              Exemplo exemplo exemplo
            </h1>
            <h2 className="text-xl font-semibold text-foreground">PCS3443</h2>
            <p className="text-sm text-muted-foreground">
              Exemplo de Login com autenticação usando JWT
            </p>
          </div>
        </div>

        {/* Dados do Perfil */}
        <div className="bg-card p-8 rounded-lg shadow-sm border space-y-6">
          <h3 className="text-2xl font-bold text-center text-foreground">Perfil</h3>
          
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-primary text-center">
              Dados do seu perfil
            </h4>
            
            <div className="space-y-2">
              <p className="text-sm">
                <span className="font-semibold text-foreground">Username:</span>
                <span className="text-muted-foreground ml-1">{user?.username}</span>
              </p>
              
              <p className="text-sm">
                <span className="font-semibold text-foreground">Email:</span>
                <span className="text-muted-foreground ml-1">{user?.email}</span>
              </p>
              
              <p className="text-sm">
                <span className="font-semibold text-foreground">Id do Token:</span>
                <span className="text-muted-foreground ml-1 font-mono text-xs break-all">
                  {tokenId}
                </span>
              </p>
            </div>

            <Button 
              onClick={handleLogout}
              variant="register"
              className="w-full mt-6"
            >
              Deslogar
            </Button>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-sm text-muted-foreground">
          <p>Desenvolvido com 💀 e 😴</p>
        </div>
      </div>
    </div>
  );
};

export default Profile;