const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const { body, validationResult } = require('express-validator');
const db = require('../config/database');

// Validação de palavras de ódio
const verificarPalavrasOdio = async (texto) => {
    const [palavras] = await db.query('SELECT palavra FROM palavras_bloqueadas WHERE ativo = TRUE');
    const textoLower = texto.toLowerCase();
    
    for (let palavra of palavras) {
        if (textoLower.includes(palavra.palavra.toLowerCase())) {
            return true;
        }
    }
    return false;
};

// CREATE - Cadastrar usuário (RFS01)
router.post('/', [
    body('nome_completo').trim().isLength({ min: 3, max: 100 }),
    body('email').isEmail().normalizeEmail(),
    body('senha').isLength({ min: 8 }).matches(/^(?=.*[A-Za-z])(?=.*\d)/),
    body('universidade_id').isInt(),
    body('curso_id').isInt(),
    body('periodo').isInt({ min: 1, max: 10 }),
    body('tipo_usuario').isIn(['Aluno', 'Professor', 'Monitor'])
], async (req, res) => {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ success: false, errors: errors.array() });
        }

        const { nome_completo, email, senha, confirmar_senha, universidade_id, curso_id, periodo, tipo_usuario } = req.body;

        // RN04: Verificar palavras de ódio no nome
        if (await verificarPalavrasOdio(nome_completo)) {
            return res.status(400).json({ 
                success: false, 
                message: 'Nome contém palavras inadequadas' 
            });
        }

        // Verificar se as senhas coincidem
        if (senha !== confirmar_senha) {
            return res.status(400).json({ 
                success: false, 
                message: 'As senhas não coincidem' 
            });
        }

        // RN01: Verificar e-mail único
        const [existente] = await db.query('SELECT id FROM usuarios WHERE email = ?', [email]);
        if (existente.length > 0) {
            return res.status(400).json({ 
                success: false, 
                message: 'E-mail já cadastrado' 
            });
        }

        // RN02: Validar formato de e-mail institucional
        if (!email.endsWith('@unifei.edu.br')) {
            return res.status(400).json({ 
                success: false, 
                message: 'E-mail deve ser institucional (@unifei.edu.br)' 
            });
        }

        // RN05: Criptografar senha
        const senha_hash = await bcrypt.hash(senha, 10);

        // Inserir usuário
        const [result] = await db.query(
            'INSERT INTO usuarios (nome_completo, email, senha_hash, universidade_id, curso_id, periodo, tipo_usuario) VALUES (?, ?, ?, ?, ?, ?, ?)',
            [nome_completo, email, senha_hash, universidade_id, curso_id, periodo, tipo_usuario]
        );

        // Log de auditoria
        await db.query(
            'INSERT INTO logs_auditoria (usuario_id, acao, tabela, registro_id, dados_novos) VALUES (?, ?, ?, ?, ?)',
            [result.insertId, 'CREATE', 'usuarios', result.insertId, JSON.stringify({ email, tipo_usuario })]
        );

        res.status(201).json({ 
            success: true, 
            message: 'Usuário cadastrado com sucesso',
            usuario_id: result.insertId 
        });

    } catch (error) {
        console.error('Erro ao cadastrar usuário:', error);
        res.status(500).json({ success: false, message: 'Erro ao cadastrar usuário' });
    }
});

// READ - Consultar usuários (RFS02)
router.get('/', async (req, res) => {
    try {
        const { nome, universidade_id, curso_id, tipo_usuario } = req.query;
        
        let query = `
            SELECT u.id, u.nome_completo, u.email, u.tipo_usuario, u.periodo,
                   un.nome as universidade, c.nome as curso
            FROM usuarios u
            JOIN universidades un ON u.universidade_id = un.id
            JOIN cursos c ON u.curso_id = c.id
            WHERE u.excluido = FALSE
        `;
        
        const params = [];

        if (nome) {
            query += ' AND u.nome_completo LIKE ?';
            params.push(`%${nome}%`);
        }
        if (universidade_id) {
            query += ' AND u.universidade_id = ?';
            params.push(universidade_id);
        }
        if (curso_id) {
            query += ' AND u.curso_id = ?';
            params.push(curso_id);
        }
        if (tipo_usuario) {
            query += ' AND u.tipo_usuario = ?';
            params.push(tipo_usuario);
        }

        query += ' ORDER BY u.nome_completo ASC';

        const [usuarios] = await db.query(query, params);

        res.json({ 
            success: true, 
            data: usuarios,
            total: usuarios.length 
        });

    } catch (error) {
        console.error('Erro ao consultar usuários:', error);
        res.status(500).json({ success: false, message: 'Erro ao consultar usuários' });
    }
});

// READ - Buscar usuário por ID
router.get('/:id', async (req, res) => {
    try {
        const [usuarios] = await db.query(`
            SELECT u.id, u.nome_completo, u.email, u.tipo_usuario, u.periodo, u.criado_em,
                   un.nome as universidade, c.nome as curso
            FROM usuarios u
            JOIN universidades un ON u.universidade_id = un.id
            JOIN cursos c ON u.curso_id = c.id
            WHERE u.id = ? AND u.excluido = FALSE
        `, [req.params.id]);

        if (usuarios.length === 0) {
            return res.status(404).json({ success: false, message: 'Usuário não encontrado' });
        }

        res.json({ success: true, data: usuarios[0] });

    } catch (error) {
        console.error('Erro ao buscar usuário:', error);
        res.status(500).json({ success: false, message: 'Erro ao buscar usuário' });
    }
});

// UPDATE - Editar usuário (RFS03)
router.put('/:id', [
    body('nome_completo').optional().trim().isLength({ min: 3, max: 100 }),
    body('senha').optional().isLength({ min: 8 }).matches(/^(?=.*[A-Za-z])(?=.*\d)/),
    body('curso_id').optional().isInt(),
    body('periodo').optional().isInt({ min: 1, max: 10 })
], async (req, res) => {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ success: false, errors: errors.array() });
        }

        const { nome_completo, senha, senha_atual, curso_id, periodo } = req.body;
        const usuario_id = req.params.id;

        // Buscar dados anteriores
        const [usuarioAtual] = await db.query('SELECT * FROM usuarios WHERE id = ? AND excluido = FALSE', [usuario_id]);
        if (usuarioAtual.length === 0) {
            return res.status(404).json({ success: false, message: 'Usuário não encontrado' });
        }

        // RN10: Verificar palavras de ódio
        if (nome_completo && await verificarPalavrasOdio(nome_completo)) {
            return res.status(400).json({ 
                success: false, 
                message: 'Nome contém palavras inadequadas' 
            });
        }

        const updates = [];
        const params = [];

        if (nome_completo) {
            updates.push('nome_completo = ?');
            params.push(nome_completo);
        }

        // RN09: Alterar senha requer confirmação da senha atual
        if (senha) {
            if (!senha_atual) {
                return res.status(400).json({ 
                    success: false, 
                    message: 'Senha atual é obrigatória para alterar a senha' 
                });
            }

            const senhaValida = await bcrypt.compare(senha_atual, usuarioAtual[0].senha_hash);
            if (!senhaValida) {
                return res.status(400).json({ 
                    success: false, 
                    message: 'Senha atual incorreta' 
                });
            }

            const senha_hash = await bcrypt.hash(senha, 10);
            updates.push('senha_hash = ?');
            params.push(senha_hash);
        }

        if (curso_id) {
            updates.push('curso_id = ?');
            params.push(curso_id);
        }

        if (periodo) {
            updates.push('periodo = ?');
            params.push(periodo);
        }

        if (updates.length === 0) {
            return res.status(400).json({ 
                success: false, 
                message: 'Nenhum campo para atualizar' 
            });
        }

        params.push(usuario_id);

        await db.query(
            `UPDATE usuarios SET ${updates.join(', ')} WHERE id = ?`,
            params
        );

        // RN11: Log de auditoria
        await db.query(
            'INSERT INTO logs_auditoria (usuario_id, acao, tabela, registro_id, dados_anteriores, dados_novos) VALUES (?, ?, ?, ?, ?, ?)',
            [usuario_id, 'UPDATE', 'usuarios', usuario_id, JSON.stringify(usuarioAtual[0]), JSON.stringify(req.body)]
        );

        res.json({ 
            success: true, 
            message: 'Usuário atualizado com sucesso' 
        });

    } catch (error) {
        console.error('Erro ao editar usuário:', error);
        res.status(500).json({ success: false, message: 'Erro ao editar usuário' });
    }
});

// DELETE - Excluir usuário (RFS04)
router.delete('/:id', async (req, res) => {
    try {
        const usuario_id = req.params.id;

        // RN12: Verificar se é criador de tópicos ativos
        const [topicosAtivos] = await db.query(
            'SELECT COUNT(*) as total FROM topicos WHERE usuario_id = ? AND status != "Fechado"',
            [usuario_id]
        );

        if (topicosAtivos[0].total > 0) {
            return res.status(400).json({ 
                success: false, 
                message: 'Usuário possui tópicos ativos. Feche-os antes de excluir a conta.' 
            });
        }

        // RN13: Anonimizar posts anteriores
        await db.query(
            'UPDATE topicos SET conteudo = "Conteúdo removido pelo usuário" WHERE usuario_id = ?',
            [usuario_id]
        );
        await db.query(
            'UPDATE respostas SET conteudo = "Conteúdo removido pelo usuário" WHERE usuario_id = ?',
            [usuario_id]
        );

        // RN14 e RN15: Marcar para exclusão (período de carência)
        await db.query(
            'UPDATE usuarios SET excluido = TRUE, data_exclusao = DATE_ADD(NOW(), INTERVAL 30 DAY) WHERE id = ?',
            [usuario_id]
        );

        // Log de auditoria
        await db.query(
            'INSERT INTO logs_auditoria (usuario_id, acao, tabela, registro_id) VALUES (?, ?, ?, ?)',
            [usuario_id, 'DELETE', 'usuarios', usuario_id]
        );

        res.json({ 
            success: true, 
            message: 'Conta marcada para exclusão em 30 dias' 
        });

    } catch (error) {
        console.error('Erro ao excluir usuário:', error);
        res.status(500).json({ success: false, message: 'Erro ao excluir usuário' });
    }
});

// Rota auxiliar - Listar universidades
router.get('/aux/universidades', async (req, res) => {
    try {
        const [universidades] = await db.query('SELECT id, nome, sigla FROM universidades ORDER BY nome');
        res.json({ success: true, data: universidades });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao buscar universidades' });
    }
});

// Rota auxiliar - Listar cursos por universidade
router.get('/aux/cursos/:universidade_id', async (req, res) => {
    try {
        const [cursos] = await db.query(
            'SELECT id, nome FROM cursos WHERE universidade_id = ? ORDER BY nome',
            [req.params.universidade_id]
        );
        res.json({ success: true, data: cursos });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao buscar cursos' });
    }
});

module.exports = router;
