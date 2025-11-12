const express = require('express');
const router = express.Router();
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

// CREATE - Cadastrar disciplina (RFS05)
router.post('/', [
    body('nome').trim().isLength({ min: 3, max: 100 }),
    body('codigo').trim().isLength({ min: 1, max: 15 }),
    body('universidade_id').isInt(),
    body('curso_id').isInt(),
    body('professor_id').isInt(),
    body('periodo_letivo').matches(/^\d{4}\.[12]$/),
    body('descricao').optional().trim().isLength({ max: 500 })
], async (req, res) => {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ success: false, errors: errors.array() });
        }

        const { nome, codigo, universidade_id, curso_id, professor_id, periodo_letivo, descricao } = req.body;

        // RN18: Verificar palavras de ódio
        if (await verificarPalavrasOdio(nome) || (descricao && await verificarPalavrasOdio(descricao))) {
            return res.status(400).json({ 
                success: false, 
                message: 'Conteúdo contém palavras inadequadas' 
            });
        }

        // RN17: Verificar se usuário é professor
        const [professor] = await db.query(
            'SELECT tipo_usuario FROM usuarios WHERE id = ?',
            [professor_id]
        );

        if (professor.length === 0 || professor[0].tipo_usuario !== 'Professor') {
            return res.status(403).json({ 
                success: false, 
                message: 'Apenas professores podem cadastrar disciplinas' 
            });
        }

        // RN16: Código único por universidade
        const [existente] = await db.query(
            'SELECT id FROM disciplinas WHERE codigo = ? AND universidade_id = ?',
            [codigo, universidade_id]
        );

        if (existente.length > 0) {
            return res.status(400).json({ 
                success: false, 
                message: 'Código de disciplina já existe nesta universidade' 
            });
        }

        // Inserir disciplina
        const [result] = await db.query(
            'INSERT INTO disciplinas (nome, codigo, universidade_id, curso_id, professor_id, periodo_letivo, descricao) VALUES (?, ?, ?, ?, ?, ?, ?)',
            [nome, codigo, universidade_id, curso_id, professor_id, periodo_letivo, descricao]
        );

        // Log de auditoria
        await db.query(
            'INSERT INTO logs_auditoria (usuario_id, acao, tabela, registro_id, dados_novos) VALUES (?, ?, ?, ?, ?)',
            [professor_id, 'CREATE', 'disciplinas', result.insertId, JSON.stringify(req.body)]
        );

        res.status(201).json({ 
            success: true, 
            message: 'Disciplina cadastrada com sucesso',
            disciplina_id: result.insertId 
        });

    } catch (error) {
        console.error('Erro ao cadastrar disciplina:', error);
        res.status(500).json({ success: false, message: 'Erro ao cadastrar disciplina' });
    }
});

// READ - Consultar disciplinas (RFS06)
router.get('/', async (req, res) => {
    try {
        const { nome, curso_id, professor, periodo_letivo, universidade_id } = req.query;
        
        let query = `
            SELECT d.id, d.nome, d.codigo, d.periodo_letivo, d.descricao, d.criado_em,
                   c.nome as curso,
                   u.nome_completo as professor,
                   un.nome as universidade
            FROM disciplinas d
            JOIN cursos c ON d.curso_id = c.id
            JOIN usuarios u ON d.professor_id = u.id
            JOIN universidades un ON d.universidade_id = un.id
            WHERE 1=1
        `;
        
        const params = [];

        // RN19: Filtrar por universidade se fornecido
        if (universidade_id) {
            query += ' AND d.universidade_id = ?';
            params.push(universidade_id);
        }

        if (nome) {
            query += ' AND d.nome LIKE ?';
            params.push(`%${nome}%`);
        }

        if (curso_id) {
            query += ' AND d.curso_id = ?';
            params.push(curso_id);
        }

        if (professor) {
            query += ' AND u.nome_completo LIKE ?';
            params.push(`%${professor}%`);
        }

        if (periodo_letivo) {
            query += ' AND d.periodo_letivo = ?';
            params.push(periodo_letivo);
        }

        // RN20: Ordenação padrão por nome
        query += ' ORDER BY d.nome ASC';

        const [disciplinas] = await db.query(query, params);

        res.json({ 
            success: true, 
            data: disciplinas,
            total: disciplinas.length 
        });

    } catch (error) {
        console.error('Erro ao consultar disciplinas:', error);
        res.status(500).json({ success: false, message: 'Erro ao consultar disciplinas' });
    }
});

// READ - Buscar disciplina por ID
router.get('/:id', async (req, res) => {
    try {
        const [disciplinas] = await db.query(`
            SELECT d.*, 
                   c.nome as curso,
                   u.nome_completo as professor,
                   un.nome as universidade
            FROM disciplinas d
            JOIN cursos c ON d.curso_id = c.id
            JOIN usuarios u ON d.professor_id = u.id
            JOIN universidades un ON d.universidade_id = un.id
            WHERE d.id = ?
        `, [req.params.id]);

        if (disciplinas.length === 0) {
            return res.status(404).json({ success: false, message: 'Disciplina não encontrada' });
        }

        res.json({ success: true, data: disciplinas[0] });

    } catch (error) {
        console.error('Erro ao buscar disciplina:', error);
        res.status(500).json({ success: false, message: 'Erro ao buscar disciplina' });
    }
});

// UPDATE - Editar disciplina
router.put('/:id', [
    body('nome').optional().trim().isLength({ min: 3, max: 100 }),
    body('periodo_letivo').optional().matches(/^\d{4}\.[12]$/),
    body('descricao').optional().trim().isLength({ max: 500 })
], async (req, res) => {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ success: false, errors: errors.array() });
        }

        const { nome, periodo_letivo, descricao } = req.body;
        const disciplina_id = req.params.id;

        // Buscar dados anteriores
        const [disciplinaAtual] = await db.query('SELECT * FROM disciplinas WHERE id = ?', [disciplina_id]);
        if (disciplinaAtual.length === 0) {
            return res.status(404).json({ success: false, message: 'Disciplina não encontrada' });
        }

        // Verificar palavras de ódio
        if (nome && await verificarPalavrasOdio(nome)) {
            return res.status(400).json({ 
                success: false, 
                message: 'Nome contém palavras inadequadas' 
            });
        }

        if (descricao && await verificarPalavrasOdio(descricao)) {
            return res.status(400).json({ 
                success: false, 
                message: 'Descrição contém palavras inadequadas' 
            });
        }

        const updates = [];
        const params = [];

        if (nome) {
            updates.push('nome = ?');
            params.push(nome);
        }

        if (periodo_letivo) {
            updates.push('periodo_letivo = ?');
            params.push(periodo_letivo);
        }

        if (descricao !== undefined) {
            updates.push('descricao = ?');
            params.push(descricao);
        }

        if (updates.length === 0) {
            return res.status(400).json({ 
                success: false, 
                message: 'Nenhum campo para atualizar' 
            });
        }

        params.push(disciplina_id);

        await db.query(
            `UPDATE disciplinas SET ${updates.join(', ')} WHERE id = ?`,
            params
        );

        // Log de auditoria
        await db.query(
            'INSERT INTO logs_auditoria (usuario_id, acao, tabela, registro_id, dados_anteriores, dados_novos) VALUES (?, ?, ?, ?, ?, ?)',
            [disciplinaAtual[0].professor_id, 'UPDATE', 'disciplinas', disciplina_id, JSON.stringify(disciplinaAtual[0]), JSON.stringify(req.body)]
        );

        res.json({ 
            success: true, 
            message: 'Disciplina atualizada com sucesso' 
        });

    } catch (error) {
        console.error('Erro ao editar disciplina:', error);
        res.status(500).json({ success: false, message: 'Erro ao editar disciplina' });
    }
});

// DELETE - Excluir disciplina
router.delete('/:id', async (req, res) => {
    try {
        const disciplina_id = req.params.id;

        // Verificar se disciplina existe
        const [disciplina] = await db.query('SELECT professor_id FROM disciplinas WHERE id = ?', [disciplina_id]);
        if (disciplina.length === 0) {
            return res.status(404).json({ success: false, message: 'Disciplina não encontrada' });
        }

        // Excluir disciplina (CASCADE irá remover tópicos relacionados)
        await db.query('DELETE FROM disciplinas WHERE id = ?', [disciplina_id]);

        // Log de auditoria
        await db.query(
            'INSERT INTO logs_auditoria (usuario_id, acao, tabela, registro_id) VALUES (?, ?, ?, ?)',
            [disciplina[0].professor_id, 'DELETE', 'disciplinas', disciplina_id]
        );

        res.json({ 
            success: true, 
            message: 'Disciplina excluída com sucesso' 
        });

    } catch (error) {
        console.error('Erro ao excluir disciplina:', error);
        res.status(500).json({ success: false, message: 'Erro ao excluir disciplina' });
    }
});

module.exports = router;
