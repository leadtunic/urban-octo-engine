import React, { useState, useEffect } from 'react';
import { signOut } from 'firebase/auth';
import { doc, getDoc } from 'firebase/firestore';
import { useAuthState } from 'react-firebase-hooks/auth';
import { useNavigate } from 'react-router-dom';
import { auth, db } from '../firebase/config';
import Loading from '../components/Loading';

interface UserData {
  nome: string;
  sobrenome: string;
  dataNascimento: string;
  email: string;
}

const Principal: React.FC = () => {
  const [user, loading, error] = useAuthState(auth);
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loadingUserData, setLoadingUserData] = useState(true);
  const [dataError, setDataError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      if (user) {
        try {
          const docRef = doc(db, 'users', user.uid);
          const docSnap = await getDoc(docRef);
          
          if (docSnap.exists()) {
            setUserData(docSnap.data() as UserData);
          } else {
            setDataError('Dados do usuário não encontrados');
          }
        } catch (error) {
          setDataError('Erro ao carregar dados do usuário');
          console.error('Erro:', error);
        } finally {
          setLoadingUserData(false);
        }
      }
    };

    fetchUserData();
  }, [user]);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/login');
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
  };

  if (loading || loadingUserData) {
    return <Loading />;
  }

  if (error) {
    return (
      <div style={{ textAlign: 'center', padding: '50px', color: 'red' }}>
        Erro de autenticação: {error.message}
      </div>
    );
  }

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#f5f5f5',
      padding: '20px'
    }}>
      {/* Header */}
      <div style={{
        backgroundColor: 'white',
        padding: '20px',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        marginBottom: '30px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h1 style={{ margin: 0, color: '#333' }}>Página Principal</h1>
        <button
          onClick={handleLogout}
          style={{
            padding: '10px 20px',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '14px'
          }}
        >
          Sair
        </button>
      </div>

      {/* Conteúdo principal */}
      <div style={{
        backgroundColor: 'white',
        padding: '40px',
        borderRadius: '8px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
        maxWidth: '600px',
        margin: '0 auto'
      }}>
        <h2 style={{ textAlign: 'center', marginBottom: '30px', color: '#333' }}>
          Dados do Usuário
        </h2>

        {dataError ? (
          <div style={{
            backgroundColor: '#ffe6e6',
            color: '#d8000c',
            padding: '15px',
            borderRadius: '4px',
            textAlign: 'center',
            marginBottom: '20px'
          }}>
            {dataError}
          </div>
        ) : userData ? (
          <div style={{ fontSize: '16px', lineHeight: '1.6' }}>
            <div style={{
              display: 'grid',
              gap: '20px',
              gridTemplateColumns: 'auto 1fr',
              alignItems: 'center'
            }}>
              <div style={{
                backgroundColor: '#f8f9fa',
                padding: '15px',
                borderRadius: '4px',
                marginBottom: '15px',
                gridColumn: '1 / -1'
              }}>
                <strong style={{ color: '#495057' }}>Nome Completo:</strong>
                <div style={{ fontSize: '18px', color: '#333', marginTop: '5px' }}>
                  {userData.nome} {userData.sobrenome}
                </div>
              </div>

              <div style={{
                backgroundColor: '#f8f9fa',
                padding: '15px',
                borderRadius: '4px',
                marginBottom: '15px',
                gridColumn: '1 / -1'
              }}>
                <strong style={{ color: '#495057' }}>Data de Nascimento:</strong>
                <div style={{ fontSize: '18px', color: '#333', marginTop: '5px' }}>
                  {formatDate(userData.dataNascimento)}
                </div>
              </div>

              <div style={{
                backgroundColor: '#f8f9fa',
                padding: '15px',
                borderRadius: '4px',
                marginBottom: '15px',
                gridColumn: '1 / -1'
              }}>
                <strong style={{ color: '#495057' }}>E-mail:</strong>
                <div style={{ fontSize: '18px', color: '#333', marginTop: '5px' }}>
                  {userData.email}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div style={{ textAlign: 'center', color: '#666' }}>
            Carregando dados do usuário...
          </div>
        )}

        {/* Informação adicional */}
        <div style={{
          marginTop: '30px',
          padding: '20px',
          backgroundColor: '#e7f3ff',
          borderRadius: '4px',
          borderLeft: '4px solid #007bff'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>Bem-vindo!</h3>
          <p style={{ margin: 0, color: '#666' }}>
            Você está logado com sucesso na aplicação. Seus dados foram carregados 
            do Firebase Firestore e sua autenticação é gerenciada pelo Firebase Authentication.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Principal;