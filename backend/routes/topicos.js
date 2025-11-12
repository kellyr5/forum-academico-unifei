const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const db = require('../config/database');

const verificarPalavrasOdio = async (texto) => {
    const [palavras] = await db.query('SELECT palavra FROM palavras_bloqueadas WHERE ativo = TRUE');
    const textoLower = texto.toLowerCase();
    for (let palavra of palavras) {
        if (textoLower.includes(palavra.palavra.toLowerCase())) return true;
    }
    return false;
};

router.post('/', async (req, res) => {
    try {
        const { titulo, conteudo, disciplina_id, usuario_id, categoria, tags } = req.body;
        if (await verificarPalavrasOdio(titulo) || await verificarPalavrasOdio(conteudo)) {
            return res.status(400).json({ success: false, message: 'Conteúdo inadequado' });
        }
        const [result] = await db.query(
            'INSERT INTO topicos (titulo, conteudo, disciplina_id, usuario_id, categoria, tags) VALUES (?, ?, ?, ?, ?, ?)',
            [titulo, conteudo, disciplina_id, usuario_id, categoria, tags]
        );
        res.status(201).json({ success: true, message: 'Tópico criado', topico_id: result.insertId });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao criar tópico' });
    }
});

router.get('/', async (req, res) => {
    try {
        const { titulo, categoria, disciplina_id } = req.query;
        let query = 'SELECT t.*, u.nome_completo as autor, d.nome as disciplina FROM topicos t JOIN usuarios u ON t.usuario_id = u.id JOIN disciplinas d ON t.disciplina_id = d.id WHERE 1=1';
        const params = [];
        if (titulo) { query += ' AND t.titulo LIKE ?'; params.push(`%${titulo}%`); }
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
        await db.query('UPDATE topicos SET visualizacoes = visualizacoes + 1 WHERE id = ?', [req.params.id]);
        res.json({ success: true, data: topicos[0] });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao buscar tópico' });
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
        if (updates.length === 0) return res.status(400).json({ success: false, message: 'Nenhum campo para atualizar' });
        params.push(req.params.id);
        await db.query(`UPDATE topicos SET ${updates.join(', ')} WHERE id = ?`, params);
        res.json({ success: true, message: 'Tópico atualizado' });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao editar tópico' });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        await db.query('DELETE FROM topicos WHERE id = ?', [req.params.id]);
        res.json({ success: true, message: 'Tópico excluído' });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao excluir tópico' });
    }
});

module.exports = router;
