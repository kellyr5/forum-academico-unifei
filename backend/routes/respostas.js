const express = require('express');
const router = express.Router();
const db = require('../config/database');

router.get('/topico/:topico_id', async (req, res) => {
    try {
        const [rows] = await db.query('SELECT * FROM respostas WHERE topico_id = ? ORDER BY criado_em', [req.params.topico_id]);
        res.json({ success: true, data: rows, total: rows.length });
    } catch (error) {
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

module.exports = router;
