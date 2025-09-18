import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from '../firebase/config';

// Importar componentes das páginas
import Cadastro from '../pages/Cadastro';
import Login from '../pages/Login';
import Principal from '../pages/Principal';
import Loading from '../components/Loading';

// Componente para proteger rotas que precisam de autenticação
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, loading] = useAuthState(auth);

  if (loading) return <Loading />;
  
  return user ? <>{children}</> : <Navigate to="/login" replace />;
};

// Componente para rotas públicas (redirecciona se já estiver logado)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, loading] = useAuthState(auth);

  if (loading) return <Loading />;
  
  return !user ? <>{children}</> : <Navigate to="/principal" replace />;
};

const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Rotas públicas */}
        <Route path="/cadastro" element={
          <PublicRoute>
            <Cadastro />
          </PublicRoute>
        } />
        <Route path="/login" element={
          <PublicRoute>
            <Login />
          </PublicRoute>
        } />
        
        {/* Rotas protegidas */}
        <Route path="/principal" element={
          <ProtectedRoute>
            <Principal />
          </ProtectedRoute>
        } />
        
        {/* Rota padrão */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        
        {/* Rota para páginas não encontradas */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;