const express = require('express');
const router = express.Router();
const db = require('../config/database');

router.get('/', async (req, res) => {
    try {
        // Testar conexão com banco
        const [result] = await db.query('SELECT 1 as test');
        
        // Contar registros importantes
        const [usuarios] = await db.query('SELECT COUNT(*) as total FROM usuarios WHERE excluido = FALSE');
        const [disciplinas] = await db.query('SELECT COUNT(*) as total FROM disciplinas');
        const [topicos] = await db.query('SELECT COUNT(*) as total FROM topicos');
        
        res.json({
            status: 'OK',
            message: 'Fórum Acadêmico API funcionando',
            database: 'Conectado',
            timestamp: new Date().toISOString(),
            stats: {
                usuarios: usuarios[0].total,
                disciplinas: disciplinas[0].total,
                topicos: topicos[0].total
            }
        });
    } catch (error) {
        res.status(500).json({
            status: 'ERROR',
            message: 'Erro ao conectar com banco de dados',
            error: error.message
        });
    }
});

module.exports = router;
