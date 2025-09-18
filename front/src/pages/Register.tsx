import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { CustomInput } from '@/components/ui/custom-input';
import { useAuth } from '@/contexts/AuthContext';
import pcsLogo from '@/assets/pcs-logo.png';

const registerSchema = z.object({
  username: z.string().min(3, 'Username deve ter pelo menos 3 caracteres'),
  email: z.string().email('Email inválido'),
  password: z.string().min(6, 'Password deve ter pelo menos 6 caracteres'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords não coincidem',
  path: ['confirmPassword'],
});

type RegisterForm = z.infer<typeof registerSchema>;

const Register = () => {
  const { register: registerUser, isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
  });

  // Redirecionar se já estiver autenticado
  if (isAuthenticated && !loading) {
    return <Navigate to="/profile" replace />;
  }

  const onSubmit = async (data: RegisterForm) => {
    try {
      setIsSubmitting(true);
      await registerUser(data.username, data.email, data.password);
      navigate('/login');
    } catch (error) {
      // Erro já é tratado no contexto
    } finally {
      setIsSubmitting(false);
    }
  };

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

        {/* Formulário de Registro */}
        <div className="bg-card p-8 rounded-lg shadow-sm border space-y-6">
          <h3 className="text-2xl font-bold text-center text-foreground">Criar Conta</h3>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <CustomInput
              placeholder="username"
              {...register('username')}
              error={errors.username?.message}
              disabled={isSubmitting}
            />

            <CustomInput
              type="email"
              placeholder="email"
              {...register('email')}
              error={errors.email?.message}
              disabled={isSubmitting}
            />

            <CustomInput
              type="password"
              placeholder="password"
              {...register('password')}
              error={errors.password?.message}
              disabled={isSubmitting}
            />

            <CustomInput
              type="password"
              placeholder="confirmar password"
              {...register('confirmPassword')}
              error={errors.confirmPassword?.message}
              disabled={isSubmitting}
            />

            <div className="space-y-4">
              <Button 
                type="submit" 
                variant="register"
                disabled={isSubmitting}
                className="w-full"
              >
                {isSubmitting ? 'Criando...' : 'Criar Conta'}
              </Button>

              <Button 
                type="button"
                variant="outline"
                asChild
                className="w-full"
              >
                <Link to="/login">Voltar ao Login</Link>
              </Button>
            </div>
          </form>
        </div>

        {/* Footer */}
        <div className="text-center text-sm text-muted-foreground">
          <p>Desenvolvido com 💀 e 😴</p>
        </div>
      </div>
    </div>
  );
};

export default Register;