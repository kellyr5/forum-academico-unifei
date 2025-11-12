const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Rotas
app.use('/api/usuarios', require('./routes/usuarios'));
app.use('/api/disciplinas', require('./routes/disciplinas'));
app.use('/api/topicos', require('./routes/topicos'));
app.use('/api/respostas', require('./routes/respostas'));

// Rota de teste
app.get('/api/health', (req, res) => {
    res.json({ status: 'OK', message: 'Fórum Acadêmico API está funcionando' });
});

// Tratamento de erros
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ 
        success: false, 
        message: 'Erro interno do servidor',
        error: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
});

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
    console.log(`Acesse: http://localhost:${PORT}/api/health`);
});

module.exports = app;
