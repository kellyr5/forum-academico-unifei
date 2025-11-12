const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const db = require('../config/database');

router.post('/', async (req, res) => {
    try {
        const { nome_completo, email, senha, confirmar_senha, curso_id, periodo, tipo_usuario } = req.body;

        console.log('Recebido:', req.body);

        if (!nome_completo || !email || !senha) {
            return res.status(400).json({ success: false, message: 'Preencha todos os campos obrigatórios' });
        }

        if (senha !== confirmar_senha) {
            return res.status(400).json({ success: false, message: 'As senhas não coincidem' });
        }

        const senha_hash = await bcrypt.hash(senha, 10);

        const [result] = await db.query(
            'INSERT INTO usuarios (nome_completo, email, senha_hash, universidade_id, curso_id, periodo, tipo_usuario) VALUES (?, ?, ?, 1, ?, ?, ?)',
            [nome_completo, email, senha_hash, curso_id || 1, periodo || 1, tipo_usuario || 'Aluno']
        );

        res.status(201).json({ success: true, message: 'Usuário cadastrado!', usuario_id: result.insertId });

    } catch (error) {
        console.error('Erro ao cadastrar usuário:', error);
        res.status(500).json({ success: false, message: error.message });
    }
});

router.get('/', async (req, res) => {
    try {
        const { nome, tipo_usuario } = req.query;
        
        let query = `SELECT u.*, un.nome as universidade, c.nome as curso 
                     FROM usuarios u 
                     JOIN universidades un ON u.universidade_id = un.id 
                     JOIN cursos c ON u.curso_id = c.id 
                     WHERE u.excluido = FALSE`;
        
        const params = [];

        if (nome) {
            query += ' AND LOWER(u.nome_completo) LIKE LOWER(?)';
            params.push(`%${nome}%`);
        }
        if (tipo_usuario) {
            query += ' AND u.tipo_usuario = ?';
            params.push(tipo_usuario);
        }

        query += ' ORDER BY u.nome_completo ASC';

        const [usuarios] = await db.query(query, params);
        res.json({ success: true, data: usuarios, total: usuarios.length });

    } catch (error) {
        console.error('Erro:', error);
        res.status(500).json({ success: false, message: error.message });
    }
});

router.get('/:id', async (req, res) => {
    try {
        const [usuarios] = await db.query(`
            SELECT u.*, un.nome as universidade, c.nome as curso
            FROM usuarios u
            JOIN universidades un ON u.universidade_id = un.id
            JOIN cursos c ON u.curso_id = c.id
            WHERE u.id = ?
        `, [req.params.id]);

        if (usuarios.length === 0) {
            return res.status(404).json({ success: false, message: 'Usuário não encontrado' });
        }

        res.json({ success: true, data: usuarios[0] });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        await db.query('UPDATE usuarios SET excluido = TRUE WHERE id = ?', [req.params.id]);
        res.json({ success: true, message: 'Usuário excluído' });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

router.get('/aux/cursos/:universidade_id', async (req, res) => {
    try {
        const [cursos] = await db.query('SELECT id, nome FROM cursos WHERE universidade_id = ? ORDER BY nome', [req.params.universidade_id]);
        res.json({ success: true, data: cursos });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

module.exports = router;
