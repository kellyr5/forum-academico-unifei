const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const db = require('../config/database');

// LOGIN
router.post('/login', async (req, res) => {
    try {
        const { email, senha } = req.body;

        if (!email || !senha) {
            return res.status(400).json({ 
                success: false, 
                message: 'E-mail e senha são obrigatórios' 
            });
        }

        // Buscar usuário
        const [usuarios] = await db.query(`
            SELECT u.*, un.nome as universidade, c.nome as curso
            FROM usuarios u
            JOIN universidades un ON u.universidade_id = un.id
            JOIN cursos c ON u.curso_id = c.id
            WHERE u.email = ? AND u.excluido = FALSE
        `, [email]);

        if (usuarios.length === 0) {
            return res.status(401).json({ 
                success: false, 
                message: 'E-mail ou senha incorretos' 
            });
        }

        const usuario = usuarios[0];

        // Verificar senha
        const senhaValida = await bcrypt.compare(senha, usuario.senha_hash);
        
        if (!senhaValida) {
            return res.status(401).json({ 
                success: false, 
                message: 'E-mail ou senha incorretos' 
            });
        }

        // Log de auditoria
        await db.query(
            'INSERT INTO logs_auditoria (usuario_id, acao, tabela, registro_id) VALUES (?, ?, ?, ?)',
            [usuario.id, 'LOGIN', 'usuarios', usuario.id]
        );

        // Retornar dados do usuário (sem senha)
        delete usuario.senha_hash;

        res.json({ 
            success: true, 
            message: 'Login realizado com sucesso',
            usuario: usuario
        });

    } catch (error) {
        console.error('Erro no login:', error);
        res.status(500).json({ success: false, message: 'Erro ao realizar login' });
    }
});

// VERIFICAR SESSÃO
router.get('/me/:id', async (req, res) => {
    try {
        const [usuarios] = await db.query(`
            SELECT u.id, u.nome_completo, u.email, u.tipo_usuario, u.periodo,
                   un.nome as universidade, c.nome as curso
            FROM usuarios u
            JOIN universidades un ON u.universidade_id = un.id
            JOIN cursos c ON u.curso_id = c.id
            WHERE u.id = ? AND u.excluido = FALSE
        `, [req.params.id]);

        if (usuarios.length === 0) {
            return res.status(404).json({ success: false, message: 'Usuário não encontrado' });
        }

        res.json({ success: true, usuario: usuarios[0] });

    } catch (error) {
        console.error('Erro ao verificar sessão:', error);
        res.status(500).json({ success: false, message: 'Erro ao verificar sessão' });
    }
});

module.exports = router;
