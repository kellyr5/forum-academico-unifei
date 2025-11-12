const mysql = require('mysql2/promise');
require('dotenv').config();

const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || 'senha123',
    database: process.env.DB_NAME || 'forum_academico',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

pool.getConnection()
    .then(connection => {
        console.log('Conectado ao MySQL com sucesso!');
        console.log('Database:', process.env.DB_NAME || 'forum_academico');
        connection.release();
    })
    .catch(err => {
        console.error('Erro ao conectar ao MySQL:', err.message);
        process.exit(1);
    });

module.exports = pool;
