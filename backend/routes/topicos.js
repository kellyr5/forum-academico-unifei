const express = require('express');
const router = express.Router();
const db = require('../config/database');

router.get('/', async (req, res) => {
    try {
        const [rows] = await db.query(`
            SELECT 
                t.id,
                t.titulo,
                t.conteudo,
                t.categoria,
                t.status,
                t.tags,
                t.criado_em,
                u.nome_completo as autor,
                d.nome as disciplina
            FROM topicos t
            LEFT JOIN usuarios u ON t.usuario_id = u.id
            LEFT JOIN disciplinas d ON t.disciplina_id = d.id
            ORDER BY t.criado_em DESC
        `);
        res.json({ success: true, data: rows, total: rows.length });
    } catch (error) {
        console.error('Erro topicos:', error);
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

router.delete('/:id', async (req, res) => {
    try {
        await db.query('DELETE FROM topicos WHERE id = ?', [req.params.id]);
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

module.exports = router;
