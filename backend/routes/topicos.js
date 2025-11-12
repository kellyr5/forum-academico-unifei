const express = require('express');
const router = express.Router();
const db = require('../config/database');

router.get('/', async (req, res) => {
    try {
        const [rows] = await db.query('SELECT * FROM topicos ORDER BY criado_em DESC');
        res.json({ success: true, data: rows, total: rows.length });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

router.post('/', async (req, res) => {
    try {
        const { titulo, conteudo, disciplina_id, usuario_id, categoria, tags } = req.body;
        const [result] = await db.query(
            'INSERT INTO topicos (titulo, conteudo, disciplina_id, usuario_id, categoria, tags) VALUES (?, ?, ?, ?, ?, ?)',
            [titulo, conteudo, disciplina_id, usuario_id, categoria, tags]
        );
        res.status(201).json({ success: true, topico_id: result.insertId });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

module.exports = router;
