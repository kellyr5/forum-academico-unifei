require('dotenv').config();
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Log de requisições
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// Importar rotas
const healthRoutes = require('./routes/health');
const authRoutes = require('./routes/auth');
const usuariosRoutes = require('./routes/usuarios');
const disciplinasRoutes = require('./routes/disciplinas');
const topicosRoutes = require('./routes/topicos');
const respostasRoutes = require('./routes/respostas');
const recadosRoutes = require('./routes/recados');

// Usar rotas
app.use('/api/health', healthRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/usuarios', usuariosRoutes);
app.use('/api/disciplinas', disciplinasRoutes);
app.use('/api/topicos', topicosRoutes);
app.use('/api/respostas', respostasRoutes);
app.use('/api/recados', recadosRoutes);

// Rota raiz
app.get('/', (req, res) => {
    res.json({
        message: 'API do Fórum Acadêmico UNIFEI',
        version: '1.0.0',
        endpoints: [
            '/api/health',
            '/api/auth',
            '/api/usuarios',
            '/api/disciplinas',
            '/api/topicos',
            '/api/respostas',
            '/api/recados'
        ]
    });
});

// Tratamento de erros 404
app.use((req, res) => {
    res.status(404).json({
        success: false,
        message: 'Rota não encontrada'
    });
});

// Tratamento de erros gerais
app.use((err, req, res, next) => {
    console.error('Erro:', err.stack);
    res.status(500).json({
        success: false,
        message: 'Erro interno do servidor',
        error: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
});

// Iniciar servidor
const db = require('./config/database');

async function iniciarServidor() {
    try {
        // Testar conexão com banco
        await db.query('SELECT 1');
        console.log('✓ Conectado ao MySQL com sucesso!');
        console.log('  Database: forum_academico');
        
        app.listen(PORT, () => {
            console.log('\n╔════════════════════════════════════════════════════════════════╗');
            console.log('║         FÓRUM ACADÊMICO - API INICIADA                         ║');
            console.log('╚════════════════════════════════════════════════════════════════╝\n');
            console.log(`✓ Servidor: http://localhost:${PORT}`);
            console.log(`✓ Health: http://localhost:${PORT}/api/health\n`);
        });
    } catch (error) {
        console.error('❌ Erro ao conectar com MySQL:', error.message);
        console.error('   Verifique se o MySQL está rodando: sudo service mysql start');
        process.exit(1);
    }
}

iniciarServidor();

module.exports = app;
