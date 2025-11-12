const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const db = require('../config/database');
router.post('/', [
    body('titulo').trim().isLength({ min: 3, max: 150 }),
    body('conteudo').trim().isLength({ min: 10, max: 1000 }),
    body('autor').trim().isLength({ min: 3, max: 100 }),
    body('categoria').isIn(['Aviso', 'Evento', 'Oportunidade', 'Outro'])
], async (req, res) => {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ success: false, errors: errors.array() });
        }

        const { titulo, conteudo, autor, categoria, cor, fixado } = req.body;

        const [result] = await db.query(
            'INSERT INTO mural_recados (titulo, conteudo, autor, categoria, cor, fixado) VALUES (?, ?, ?, ?, ?, ?)',
            [titulo, conteudo, autor, categoria, cor || '#003366', fixado || false]
        );

        res.status(201).json({ 
            success: true, 
            message: 'Recado criado com sucesso',
            recado_id: result.insertId 
        });

    } catch (error) {
        console.error('Erro ao criar recado:', error);
        res.status(500).json({ success: false, message: 'Erro ao criar recado' });
    }
});router.get('/', async (req, res) => {
    try {
        const { categoria } = req.query;
        let query = 'SELECT * FROM mural_recados WHERE 1=1';
        const params = [];

        if (categoria) {
            query += ' AND categoria = ?';
            params.push(categoria);
        }

        query += ' ORDER BY fixado DESC, criado_em DESC';
        const [recados] = await db.query(query, params);

        res.json({ success: true, data: recados, total: recados.length });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao listar recados' });
    }
});

// READ - Por ID
router.get('/:id', async (req, res) => {
    try {
        const [recados] = await db.query('SELECT * FROM mural_recados WHERE id = ?', [req.params.id]);
        if (recados.length === 0) {
            return res.status(404).json({ success: false, message: 'Recado não encontrado' });
        }
        res.json({ success: true, data: recados[0] });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao buscar recado' });
    }
});

// UPDATE
router.put('/:id', async (req, res) => {
    try {
        const { titulo, conteudo, categoria, cor } = req.body;
        const updates = [];
        const params = [];

        if (titulo) { updates.push('titulo = ?'); params.push(titulo); }
        if (conteudo) { updates.push('conteudo = ?'); params.push(conteudo); }
        if (categoria) { updates.push('categoria = ?'); params.push(categoria); }
        if (cor) { updates.push('cor = ?'); params.push(cor); }

        if (updates.length === 0) {
            return res.status(400).json({ success: false, message: 'Nenhum campo para atualizar' });
        }

        params.push(req.params.id);
        await db.query(`UPDATE mural_recados SET ${updates.join(', ')} WHERE id = ?`, params);

        res.json({ success: true, message: 'Recado atualizado com sucesso' });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao editar recado' });
    }
});

// DELETE
router.delete('/:id', async (req, res) => {
    try {
        await db.query('DELETE FROM mural_recados WHERE id = ?', [req.params.id]);
        res.json({ success: true, message: 'Recado excluído com sucesso' });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao excluir recado' });
    }
});

module.exports = router;
