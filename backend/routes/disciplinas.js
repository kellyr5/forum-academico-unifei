const express = require('express');
const router = express.Router();
const db = require('../config/database');

router.get('/', async (req, res) => {
    try {
        const [rows] = await db.query('SELECT * FROM disciplinas ORDER BY nome');
        res.json({ success: true, data: rows, total: rows.length });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

router.post('/', async (req, res) => {
    try {
        const { nome, codigo, curso_id, professor_id, periodo_letivo, descricao } = req.body;
        const [result] = await db.query(
            'INSERT INTO disciplinas (nome, codigo, universidade_id, curso_id, professor_id, periodo_letivo, descricao) VALUES (?, ?, 1, ?, ?, ?, ?)',
            [nome, codigo, curso_id, professor_id, periodo_letivo, descricao]
        );
        res.status(201).json({ success: true, disciplina_id: result.insertId });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

module.exports = router;
