const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

const db = new sqlite3.Database('./database.db');

// Criar tabelas
db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        universidade TEXT,
        curso TEXT,
        periodo TEXT,
        tipo TEXT,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    db.run(`CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        codigo TEXT UNIQUE NOT NULL,
        curso TEXT,
        professor_id INTEGER,
        periodo TEXT,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (professor_id) REFERENCES usuarios(id)
    )`);

    db.run(`CREATE TABLE IF NOT EXISTS topicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        conteudo TEXT NOT NULL,
        disciplina_id INTEGER,
        usuario_id INTEGER,
        categoria TEXT,
        status TEXT DEFAULT 'Aberto',
        melhor_resposta_id INTEGER DEFAULT NULL,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (melhor_resposta_id) REFERENCES respostas(id)
    )`);

    db.run(`CREATE TABLE IF NOT EXISTS respostas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topico_id INTEGER NOT NULL,
        usuario_id INTEGER NOT NULL,
        conteudo TEXT NOT NULL,
        e_melhor_resposta INTEGER DEFAULT 0,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (topico_id) REFERENCES topicos(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )`);

    db.run(`CREATE TABLE IF NOT EXISTS recados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        conteudo TEXT NOT NULL,
        categoria TEXT,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
});

// USUARIOS
app.get('/api/usuarios', (req, res) => {
    db.all('SELECT * FROM usuarios ORDER BY nome', [], (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(rows);
    });
});

app.get('/api/usuarios/:id', (req, res) => {
    db.get('SELECT * FROM usuarios WHERE id = ?', [req.params.id], (err, row) => {
        if (err) return res.status(500).json({ error: err.message });
        if (!row) return res.status(404).json({ error: 'Usuario nao encontrado' });
        res.json(row);
    });
});

app.post('/api/usuarios', (req, res) => {
    const { nome, email, senha, universidade, curso, periodo, tipo } = req.body;
    const sql = 'INSERT INTO usuarios (nome, email, senha, universidade, curso, periodo, tipo) VALUES (?, ?, ?, ?, ?, ?, ?)';
    
    db.run(sql, [nome, email, senha, universidade, curso, periodo, tipo], function(err) {
        if (err) return res.status(400).json({ error: err.message });
        res.json({ id: this.lastID, message: 'Usuario criado com sucesso' });
    });
});

app.put('/api/usuarios/:id', (req, res) => {
    const { nome, senha, curso, periodo } = req.body;
    const sql = 'UPDATE usuarios SET nome = ?, senha = ?, curso = ?, periodo = ? WHERE id = ?';
    
    db.run(sql, [nome, senha, curso, periodo, req.params.id], function(err) {
        if (err) return res.status(400).json({ error: err.message });
        if (this.changes === 0) return res.status(404).json({ error: 'Usuario nao encontrado' });
        res.json({ message: 'Usuario atualizado com sucesso' });
    });
});

app.delete('/api/usuarios/:id', (req, res) => {
    db.run('DELETE FROM usuarios WHERE id = ?', [req.params.id], function(err) {
        if (err) return res.status(400).json({ error: err.message });
        if (this.changes === 0) return res.status(404).json({ error: 'Usuario nao encontrado' });
        res.json({ message: 'Usuario excluido com sucesso' });
    });
});

// DISCIPLINAS
app.get('/api/disciplinas', (req, res) => {
    db.all('SELECT * FROM disciplinas ORDER BY nome', [], (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(rows);
    });
});

app.post('/api/disciplinas', (req, res) => {
    const { nome, codigo, curso, professor_id, periodo } = req.body;
    const sql = 'INSERT INTO disciplinas (nome, codigo, curso, professor_id, periodo) VALUES (?, ?, ?, ?, ?)';
    
    db.run(sql, [nome, codigo, curso, professor_id, periodo], function(err) {
        if (err) return res.status(400).json({ error: err.message });
        res.json({ id: this.lastID, message: 'Disciplina criada com sucesso' });
    });
});

// TOPICOS
app.get('/api/topicos', (req, res) => {
    db.all('SELECT * FROM topicos ORDER BY data_criacao DESC', [], (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(rows);
    });
});

app.post('/api/topicos', (req, res) => {
    const { titulo, conteudo, disciplina_id, usuario_id, categoria } = req.body;
    const sql = 'INSERT INTO topicos (titulo, conteudo, disciplina_id, usuario_id, categoria) VALUES (?, ?, ?, ?, ?)';
    
    db.run(sql, [titulo, conteudo, disciplina_id, usuario_id, categoria], function(err) {
        if (err) return res.status(400).json({ error: err.message });
        res.json({ id: this.lastID, message: 'Topico criado com sucesso' });
    });
});

app.put('/api/topicos/:id/melhor-resposta', (req, res) => {
    const { resposta_id } = req.body;
    
    db.serialize(() => {
        db.run('UPDATE respostas SET e_melhor_resposta = 0 WHERE topico_id = (SELECT topico_id FROM respostas WHERE id = ?)', [resposta_id]);
        db.run('UPDATE respostas SET e_melhor_resposta = 1 WHERE id = ?', [resposta_id]);
        db.run('UPDATE topicos SET melhor_resposta_id = ?, status = "Resolvido" WHERE id = ?', [resposta_id, req.params.id], function(err) {
            if (err) return res.status(400).json({ error: err.message });
            res.json({ message: 'Melhor resposta marcada com sucesso' });
        });
    });
});

app.delete('/api/topicos/:id/melhor-resposta', (req, res) => {
    db.serialize(() => {
        db.run('UPDATE respostas SET e_melhor_resposta = 0 WHERE topico_id = ?', [req.params.id]);
        db.run('UPDATE topicos SET melhor_resposta_id = NULL, status = "Aberto" WHERE id = ?', [req.params.id], function(err) {
            if (err) return res.status(400).json({ error: err.message });
            res.json({ message: 'Melhor resposta removida com sucesso' });
        });
    });
});

// RESPOSTAS
app.get('/api/respostas', (req, res) => {
    const { topico_id } = req.query;
    let sql = 'SELECT * FROM respostas ORDER BY data_criacao ASC';
    let params = [];
    
    if (topico_id) {
        sql = 'SELECT * FROM respostas WHERE topico_id = ? ORDER BY e_melhor_resposta DESC, data_criacao ASC';
        params = [topico_id];
    }
    
    db.all(sql, params, (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(rows);
    });
});

app.post('/api/respostas', (req, res) => {
    const { topico_id, usuario_id, conteudo } = req.body;
    const sql = 'INSERT INTO respostas (topico_id, usuario_id, conteudo) VALUES (?, ?, ?)';
    
    db.run(sql, [topico_id, usuario_id, conteudo], function(err) {
        if (err) return res.status(400).json({ error: err.message });
        res.json({ id: this.lastID, message: 'Resposta criada com sucesso' });
    });
});

// RECADOS
app.get('/api/recados', (req, res) => {
    db.all('SELECT * FROM recados ORDER BY data_criacao DESC', [], (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(rows);
    });
});

app.post('/api/recados', (req, res) => {
    const { titulo, autor, conteudo, categoria } = req.body;
    const sql = 'INSERT INTO recados (titulo, autor, conteudo, categoria) VALUES (?, ?, ?, ?)';
    
    db.run(sql, [titulo, autor, conteudo, categoria], function(err) {
        if (err) return res.status(400).json({ error: err.message });
        res.json({ id: this.lastID, message: 'Recado criado com sucesso' });
    });
});

app.delete('/api/recados/:id', (req, res) => {
    db.run('DELETE FROM recados WHERE id = ?', [req.params.id], function(err) {
        if (err) return res.status(400).json({ error: err.message });
        if (this.changes === 0) return res.status(404).json({ error: 'Recado nao encontrado' });
        res.json({ message: 'Recado excluido com sucesso' });
    });
});

app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});
