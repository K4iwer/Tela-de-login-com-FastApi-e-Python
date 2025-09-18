import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import pcsLogo from '@/assets/pcs-logo.png';

const Index = () => {
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

        {/* Navegação */}
        <div className="bg-card p-8 rounded-lg shadow-sm border space-y-6">
          <h3 className="text-2xl font-bold text-center text-foreground">Bem-vindo!</h3>
          
          <div className="space-y-4">
            <Button 
              variant="login"
              asChild
              className="w-full"
            >
              <Link to="/login">Fazer Login</Link>
            </Button>

            <Button 
              variant="register"
              asChild
              className="w-full"
            >
              <Link to="/register">Criar Conta</Link>
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

export default Index;
