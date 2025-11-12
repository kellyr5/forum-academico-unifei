const express = require('express');
const router = express.Router();
const db = require('../config/database');

router.post('/', async (req, res) => {
    try {
        const { titulo, conteudo, disciplina_id, usuario_id, categoria, tags } = req.body;
        
        if (!titulo || !conteudo || !disciplina_id || !usuario_id || !categoria) {
            return res.status(400).json({ success: false, message: 'Campos obrigatórios faltando' });
        }

        const [result] = await db.query(
            'INSERT INTO topicos (titulo, conteudo, disciplina_id, usuario_id, categoria, tags) VALUES (?, ?, ?, ?, ?, ?)',
            [titulo, conteudo, disciplina_id, usuario_id, categoria, tags]
        );
        res.status(201).json({ success: true, message: 'Tópico criado', topico_id: result.insertId });
    } catch (error) {
        console.error('Erro:', error);
        res.status(500).json({ success: false, message: 'Erro: ' + error.message });
    }
});

router.get('/', async (req, res) => {
    try {
        const { titulo, categoria, disciplina_id } = req.query;
        let query = 'SELECT t.*, u.nome_completo as autor, d.nome as disciplina FROM topicos t JOIN usuarios u ON t.usuario_id = u.id JOIN disciplinas d ON t.disciplina_id = d.id WHERE 1=1';
        const params = [];
        
        if (titulo) { 
            query += ' AND (LOWER(t.titulo) LIKE LOWER(?) OR remover_acentos(t.titulo) LIKE remover_acentos(?))'; 
            params.push(`%${titulo}%`, `%${titulo}%`); 
        }
        if (categoria) { query += ' AND t.categoria = ?'; params.push(categoria); }
        if (disciplina_id) { query += ' AND t.disciplina_id = ?'; params.push(disciplina_id); }
        
        query += ' ORDER BY t.fixo DESC, t.criado_em DESC';
        const [topicos] = await db.query(query, params);
        res.json({ success: true, data: topicos, total: topicos.length });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao consultar tópicos' });
    }
});

router.get('/:id', async (req, res) => {
    try {
        const [topicos] = await db.query('SELECT t.*, u.nome_completo as autor, d.nome as disciplina FROM topicos t JOIN usuarios u ON t.usuario_id = u.id JOIN disciplinas d ON t.disciplina_id = d.id WHERE t.id = ?', [req.params.id]);
        if (topicos.length === 0) return res.status(404).json({ success: false, message: 'Tópico não encontrado' });
        res.json({ success: true, data: topicos[0] });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro' });
    }
});

router.put('/:id', async (req, res) => {
    try {
        const { titulo, conteudo, status } = req.body;
        const updates = [];
        const params = [];
        if (titulo) { updates.push('titulo = ?'); params.push(titulo); }
        if (conteudo) { updates.push('conteudo = ?'); params.push(conteudo); }
        if (status) { updates.push('status = ?'); params.push(status); }
        if (updates.length === 0) return res.status(400).json({ success: false, message: 'Nada para atualizar' });
        params.push(req.params.id);
        await db.query(`UPDATE topicos SET ${updates.join(', ')} WHERE id = ?`, params);
        res.json({ success: true, message: 'Tópico atualizado' });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro' });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        await db.query('DELETE FROM topicos WHERE id = ?', [req.params.id]);
        res.json({ success: true, message: 'Tópico excluído' });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro' });
    }
});

module.exports = router;
