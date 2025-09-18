# Urban Octo Engine - React Firebase App

Uma aplicação React completa com autenticação Firebase e 3 páginas distintas: Cadastro, Login e Principal.

## Funcionalidades

### 📝 Página de Cadastro
- Formulário com 5 campos: e-mail, senha, nome, sobrenome e data de nascimento
- Criação de usuário no Firebase Authentication (E-mail/Senha)
- Armazenamento de dados adicionais no Firestore com UID do usuário
- Validação de campos e feedback visual

### 🔐 Página de Login
- Formulário de autenticação com e-mail e senha
- Validação no Firebase Authentication
- Redirecionamento automático para página Principal em caso de sucesso
- Mensagens de erro informativas para usuários não cadastrados

### 🏠 Página Principal
- Exibição dos dados do usuário: nome, sobrenome e data de nascimento
- Carregamento de dados do Firestore usando UID do usuário
- Rota protegida (apenas usuários autenticados)
- Funcionalidade de logout

## Tecnologias Utilizadas

- **React 19** com TypeScript
- **React Router Dom** para navegação
- **Firebase Authentication** para autenticação
- **Firebase Firestore** para banco de dados
- **React Firebase Hooks** para gerenciamento de estado de auth

## Configuração do Projeto

### 1. Instalação das dependências
```bash
npm install
```

### 2. Configuração do Firebase

1. Crie um projeto no [Firebase Console](https://console.firebase.google.com/)
2. Ative Authentication com provedor E-mail/Senha
3. Crie um banco Firestore
4. Copie as configurações do projeto

### 3. Variáveis de ambiente

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env.local
```

2. Substitua os valores no arquivo `.env.local`:
```env
REACT_APP_FIREBASE_API_KEY=sua-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=seu-projeto.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=seu-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=seu-projeto.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=123456789
REACT_APP_FIREBASE_APP_ID=seu-app-id
```

## Scripts Disponíveis

### `npm start`
Inicia o servidor de desenvolvimento na porta 3000.

### `npm run build`
Cria uma versão otimizada para produção na pasta `build/`.

### `npm test`
Executa os testes em modo interativo.

## Estrutura do Projeto

```
src/
├── components/          # Componentes reutilizáveis
│   └── Loading.tsx      # Componente de carregamento
├── firebase/            # Configuração do Firebase
│   └── config.ts        # Configuração e inicialização
├── pages/               # Páginas da aplicação
│   ├── Cadastro.tsx     # Página de cadastro
│   ├── Login.tsx        # Página de login
│   └── Principal.tsx    # Página principal (dashboard)
├── routes/              # Configuração de rotas
│   └── AppRoutes.tsx    # Rotas da aplicação
├── App.tsx              # Componente principal
└── index.tsx            # Ponto de entrada
```

## Fluxo da Aplicação

1. **Cadastro**: Usuário preenche formulário → Firebase Auth cria conta → Dados salvos no Firestore
2. **Login**: Usuário insere credenciais → Firebase Auth valida → Redirecionamento para Principal
3. **Principal**: Carrega dados do Firestore usando UID → Exibe informações do usuário

## Deploy

### Firebase Hosting
```bash
npm run build
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```

### Netlify/Vercel
```bash
npm run build
# Upload da pasta build/ para sua plataforma de deploy
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.