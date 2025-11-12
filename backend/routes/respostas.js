const express = require('express');
const router = express.Router();
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
        const { conteudo, topico_id, usuario_id, resposta_pai_id } = req.body;
        if (await verificarPalavrasOdio(conteudo)) {
            return res.status(400).json({ success: false, message: 'Conteúdo inadequado' });
        }
        const [result] = await db.query(
            'INSERT INTO respostas (conteudo, topico_id, usuario_id, resposta_pai_id) VALUES (?, ?, ?, ?)',
            [conteudo, topico_id, usuario_id, resposta_pai_id || null]
        );
        await db.query('UPDATE topicos SET atualizado_em = NOW() WHERE id = ?', [topico_id]);
        res.status(201).json({ success: true, message: 'Resposta criada', resposta_id: result.insertId });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao criar resposta' });
    }
});

router.get('/topico/:topico_id', async (req, res) => {
    try {
        const [respostas] = await db.query(
            'SELECT r.*, u.nome_completo as autor, u.tipo_usuario FROM respostas r JOIN usuarios u ON r.usuario_id = u.id WHERE r.topico_id = ? ORDER BY r.criado_em ASC',
            [req.params.topico_id]
        );
        const respostasMap = {};
        const respostasPrincipais = [];
        respostas.forEach(r => { r.respostas_filhas = []; respostasMap[r.id] = r; });
        respostas.forEach(r => {
            if (r.resposta_pai_id && respostasMap[r.resposta_pai_id]) {
                respostasMap[r.resposta_pai_id].respostas_filhas.push(r);
            } else if (!r.resposta_pai_id) {
                respostasPrincipais.push(r);
            }
        });
        res.json({ success: true, data: respostasPrincipais, total: respostas.length });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao consultar respostas' });
    }
});

router.get('/:id', async (req, res) => {
    try {
        const [respostas] = await db.query('SELECT r.*, u.nome_completo as autor FROM respostas r JOIN usuarios u ON r.usuario_id = u.id WHERE r.id = ?', [req.params.id]);
        if (respostas.length === 0) return res.status(404).json({ success: false, message: 'Resposta não encontrada' });
        res.json({ success: true, data: respostas[0] });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao buscar resposta' });
    }
});

router.put('/:id', async (req, res) => {
    try {
        const { conteudo } = req.body;
        if (await verificarPalavrasOdio(conteudo)) {
            return res.status(400).json({ success: false, message: 'Conteúdo inadequado' });
        }
        await db.query('UPDATE respostas SET conteudo = ? WHERE id = ?', [conteudo, req.params.id]);
        res.json({ success: true, message: 'Resposta atualizada' });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao editar resposta' });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        await db.query('DELETE FROM respostas WHERE id = ?', [req.params.id]);
        res.json({ success: true, message: 'Resposta excluída' });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao excluir resposta' });
    }
});

router.post('/:id/votar', async (req, res) => {
    try {
        const { usuario_id } = req.body;
        const [voto] = await db.query('SELECT id FROM votos WHERE resposta_id = ? AND usuario_id = ?', [req.params.id, usuario_id]);
        if (voto.length > 0) {
            await db.query('DELETE FROM votos WHERE id = ?', [voto[0].id]);
            await db.query('UPDATE respostas SET votos = votos - 1 WHERE id = ?', [req.params.id]);
            res.json({ success: true, message: 'Voto removido', acao: 'removido' });
        } else {
            await db.query('INSERT INTO votos (resposta_id, usuario_id) VALUES (?, ?)', [req.params.id, usuario_id]);
            await db.query('UPDATE respostas SET votos = votos + 1 WHERE id = ?', [req.params.id]);
            res.json({ success: true, message: 'Voto registrado', acao: 'adicionado' });
        }
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao votar' });
    }
});

router.post('/:id/melhor-resposta', async (req, res) => {
    try {
        const [resposta] = await db.query('SELECT topico_id FROM respostas WHERE id = ?', [req.params.id]);
        if (resposta.length === 0) return res.status(404).json({ success: false, message: 'Resposta não encontrada' });
        await db.query('UPDATE respostas SET melhor_resposta = FALSE WHERE topico_id = ?', [resposta[0].topico_id]);
        await db.query('UPDATE respostas SET melhor_resposta = TRUE WHERE id = ?', [req.params.id]);
        await db.query('UPDATE topicos SET status = "Resolvido" WHERE id = ?', [resposta[0].topico_id]);
        res.json({ success: true, message: 'Melhor resposta marcada' });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Erro ao marcar melhor resposta' });
    }
});

module.exports = router;
