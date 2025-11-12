const express = require('express');
const router = express.Router();
const db = require('../config/database');

router.post('/', async (req, res) => {
    try {
        const { titulo, conteudo, autor, categoria, cor } = req.body;

        console.log('Recebido recado:', req.body);

        if (!titulo || !conteudo || !autor) {
            return res.status(400).json({ success: false, message: 'Preencha título, conteúdo e autor' });
        }

        const [result] = await db.query(
            'INSERT INTO mural_recados (titulo, conteudo, autor, categoria, cor) VALUES (?, ?, ?, ?, ?)',
            [titulo, conteudo, autor, categoria || 'Aviso', cor || '#003366']
        );

        res.status(201).json({ success: true, message: 'Recado criado!', recado_id: result.insertId });

    } catch (error) {
        console.error('Erro:', error);
        res.status(500).json({ success: false, message: error.message });
    }
});

router.get('/', async (req, res) => {
    try {
        const [recados] = await db.query('SELECT * FROM mural_recados ORDER BY fixado DESC, criado_em DESC');
        res.json({ success: true, data: recados, total: recados.length });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        await db.query('DELETE FROM mural_recados WHERE id = ?', [req.params.id]);
        res.json({ success: true, message: 'Recado excluído' });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

module.exports = router;
