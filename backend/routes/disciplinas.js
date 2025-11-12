const express = require('express');
const router = express.Router();
const db = require('../config/database');

router.get('/', async (req, res) => {
    try {
        const [rows] = await db.query(`
            SELECT 
                d.id, 
                d.nome, 
                d.codigo, 
                d.periodo_letivo, 
                d.descricao,
                c.nome as curso,
                u.nome_completo as professor
            FROM disciplinas d
            LEFT JOIN cursos c ON d.curso_id = c.id
            LEFT JOIN usuarios u ON d.professor_id = u.id
            ORDER BY d.nome ASC
        `);
        res.json({ success: true, data: rows, total: rows.length });
    } catch (error) {
        console.error('Erro disciplinas:', error);
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

router.delete('/:id', async (req, res) => {
    try {
        await db.query('DELETE FROM disciplinas WHERE id = ?', [req.params.id]);
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

module.exports = router;
