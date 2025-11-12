const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Rotas
app.use('/api/health', require('./routes/health'));
app.use('/api/usuarios', require('./routes/usuarios'));
app.use('/api/disciplinas', require('./routes/disciplinas'));
app.use('/api/topicos', require('./routes/topicos'));
app.use('/api/respostas', require('./routes/respostas'));
app.use('/api/recados', require('./routes/recados'));

app.use((err, req, res, next) => {
    console.error('❌ Erro:', err.stack);
    res.status(500).json({ 
        success: false, 
        message: 'Erro interno do servidor'
    });
});

app.listen(PORT, () => {
    console.log('');
    console.log('╔════════════════════════════════════════════════════════════════╗');
    console.log('║           FÓRUM ACADÊMICO - API INICIADA                       ║');
    console.log('╚════════════════════════════════════════════════════════════════╝');
    console.log('');
    console.log(`🚀 Servidor: http://localhost:${PORT}`);
    console.log(`📊 Health: http://localhost:${PORT}/api/health`);
    console.log('');
});

module.exports = app;
