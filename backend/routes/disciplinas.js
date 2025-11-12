const express = require('express');
const router = express.Router();
const db = require('../config/database');

router.post('/', async (req, res) => {
    try {
        const { nome, codigo, curso_id, professor_id, periodo_letivo, descricao } = req.body;

        console.log('Recebido:', req.body);

        if (!nome || !codigo) {
            return res.status(400).json({ success: false, message: 'Preencha nome e código' });
        }

        const [result] = await db.query(
            'INSERT INTO disciplinas (nome, codigo, universidade_id, curso_id, professor_id, periodo_letivo, descricao) VALUES (?, ?, 1, ?, ?, ?, ?)',
            [nome, codigo, curso_id || 1, professor_id || 1, periodo_letivo || '2024.2', descricao]
        );

        res.status(201).json({ success: true, message: 'Disciplina cadastrada!', disciplina_id: result.insertId });
    } catch (error) {
        console.error('Erro:', error);
        res.status(500).json({ success: false, message: error.message });
    }
});

router.get('/', async (req, res) => {
    try {
        const [disciplinas] = await db.query(`
            SELECT d.*, c.nome as curso, u.nome_completo as professor, un.nome as universidade
            FROM disciplinas d
            JOIN cursos c ON d.curso_id = c.id
            JOIN usuarios u ON d.professor_id = u.id
            JOIN universidades un ON d.universidade_id = un.id
            ORDER BY d.nome ASC
        `);
        res.json({ success: true, data: disciplinas, total: disciplinas.length });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        await db.query('DELETE FROM disciplinas WHERE id = ?', [req.params.id]);
        res.json({ success: true, message: 'Disciplina excluída' });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

module.exports = router;
