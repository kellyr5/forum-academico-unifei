const mysql = require('mysql2');

const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: 'senha123',
    database: 'forum_academico',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
    connectTimeout: 10000
});

const promisePool = pool.promise();

// Testar conexão ao iniciar
pool.getConnection((err, connection) => {
    if (err) {
        console.error('❌ ERRO ao conectar ao MySQL:');
        console.error('   Mensagem:', err.message);
        console.error('');
        console.error('🔧 SOLUÇÕES:');
        console.error('   1. Verifique se o MySQL está rodando:');
        console.error('      sudo service mysql status');
        console.error('');
        console.error('   2. Se não estiver rodando, inicie:');
        console.error('      sudo service mysql start');
        console.error('');
        console.error('   3. Verifique as credenciais em backend/.env');
        console.error('');
        process.exit(1);
    }
    
    console.log('✅ Conectado ao MySQL com sucesso!');
    console.log(`   Database: forum_academico`);
    connection.release();
});

module.exports = promisePool;
