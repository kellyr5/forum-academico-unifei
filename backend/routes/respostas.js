const express = require('express');
const router = express.Router();
const db = require('../config/database');

router.get('/topico/:topico_id', async (req, res) => {
    try {
        const [rows] = await db.query(`
            SELECT 
                r.id,
                r.conteudo,
                r.votos,
                r.melhor_resposta,
                r.criado_em,
                u.nome_completo as autor,
                u.tipo_usuario
            FROM respostas r
            LEFT JOIN usuarios u ON r.usuario_id = u.id
            WHERE r.topico_id = ?
            ORDER BY r.melhor_resposta DESC, r.votos DESC, r.criado_em ASC
        `, [req.params.topico_id]);
        res.json({ success: true, data: rows, total: rows.length });
    } catch (error) {
        console.error('Erro respostas:', error);
        res.status(500).json({ success: false, message: error.message });
    }
});

router.post('/', async (req, res) => {
    try {
        const { conteudo, topico_id, usuario_id, resposta_pai_id } = req.body;
        const [result] = await db.query(
            'INSERT INTO respostas (conteudo, topico_id, usuario_id, resposta_pai_id) VALUES (?, ?, ?, ?)',
            [conteudo, topico_id, usuario_id, resposta_pai_id || null]
        );
        res.status(201).json({ success: true, resposta_id: result.insertId });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        await db.query('DELETE FROM respostas WHERE id = ?', [req.params.id]);
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

module.exports = router;
