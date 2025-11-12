const express = require('express');
const cors = require('cors');
const db = require('./config/database');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rotas
const authRoutes = require('./routes/auth');
const usuariosRoutes = require('./routes/usuarios');
const disciplinasRoutes = require('./routes/disciplinas');
const topicosRoutes = require('./routes/topicos');
const respostasRoutes = require('./routes/respostas');
const recadosRoutes = require('./routes/recados');

app.use('/api/auth', authRoutes);
app.use('/api/usuarios', usuariosRoutes);
app.use('/api/disciplinas', disciplinasRoutes);
app.use('/api/topicos', topicosRoutes);
app.use('/api/respostas', respostasRoutes);
app.use('/api/recados', recadosRoutes);

// Rota de health check
app.get('/api/health', (req, res) => {
    res.json({ 
        success: true, 
        message: 'API funcionando',
        timestamp: new Date().toISOString()
    });
});

// Rota raiz
app.get('/', (req, res) => {
    res.json({
        message: 'Forum Academico UNIFEI - API',
        version: '1.0.0',
        endpoints: [
            '/api/auth',
            '/api/usuarios',
            '/api/disciplinas',
            '/api/topicos',
            '/api/respostas',
            '/api/recados',
            '/api/health'
        ]
    });
});

// Middleware de erro
app.use((err, req, res, next) => {
    console.error('Erro:', err.message);
    res.status(500).json({
        success: false,
        message: 'Erro interno do servidor'
    });
});

// Rota 404
app.use((req, res) => {
    res.status(404).json({
        success: false,
        message: 'Rota nao encontrada'
    });
});

async function iniciarServidor() {
    try {
        await db.query('SELECT 1');
        console.log('Conectado ao MySQL com sucesso!');
        console.log('Database: forum_academico');
        
        app.listen(PORT, () => {
            console.log('');
            console.log('FORUM ACADEMICO - API INICIADA');
            console.log('');
            console.log('Servidor: http://localhost:' + PORT);
            console.log('Health: http://localhost:' + PORT + '/api/health');
            console.log('');
        });
    } catch (error) {
        console.error('Erro ao conectar ao banco de dados:', error.message);
        process.exit(1);
    }
}

iniciarServidor();

module.exports = app;
