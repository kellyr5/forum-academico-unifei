const API_URL = 'http://localhost:3000/api';
let usuarioEditando = null;

// ==================== NAVEGACAO ====================
document.addEventListener('DOMContentLoaded', () => {
    // Navegacao entre abas
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetTab = link.dataset.tab;
            
            // Atualizar links
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Atualizar panels
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.getElementById(targetTab).classList.add('active');
            
            // Carregar dados
            carregarDados(targetTab);
        });
    });
    
    // Carregar dados iniciais
    carregarRecados();
});

function carregarDados(aba) {
    switch(aba) {
        case 'mural': carregarRecados(); break;
        case 'usuarios': carregarUsuarios(); break;
        case 'disciplinas': carregarDisciplinas(); break;
        case 'topicos': carregarTopicos(); break;
        case 'respostas': carregarRespostas(); break;
    }
}

// ==================== RECADOS ====================
document.getElementById('form-recado').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const dados = {
        titulo: document.getElementById('rec_titulo').value,
        autor: document.getElementById('rec_autor').value,
        conteudo: document.getElementById('rec_conteudo').value,
        categoria: document.getElementById('rec_categoria').value
    };
    
    try {
        const res = await fetch(`${API_URL}/recados`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        
        if (res.ok) {
            alert('Aviso publicado com sucesso!');
            e.target.reset();
            carregarRecados();
        }
    } catch (err) {
        alert('Erro ao publicar aviso');
    }
});

async function carregarRecados() {
    const container = document.getElementById('lista-recados');
    container.innerHTML = '<div class="loading"></div>';
    
    try {
        const res = await fetch(`${API_URL}/recados`);
        const recados = await res.json();
        
        if (recados.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>Nenhum aviso publicado</p></div>';
            return;
        }
        
        container.innerHTML = recados.map(r => `
            <div class="item-card">
                <div class="item-header">
                    <div>
                        <h3 class="item-title">${r.titulo}</h3>
                        <span class="badge badge-${r.categoria.toLowerCase()}">${r.categoria}</span>
                    </div>
                    <button onclick="deleteRecado(${r.id})" class="btn-sm btn-delete">Excluir</button>
                </div>
                <div class="item-body">${r.conteudo}</div>
                <div class="item-footer">
                    <span>Por: ${r.autor}</span>
                    <span>${new Date(r.data_criacao).toLocaleString('pt-BR')}</span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = '<p>Erro ao carregar avisos</p>';
    }
}

async function deleteRecado(id) {
    if (!confirm('Deseja excluir este aviso?')) return;
    
    try {
        await fetch(`${API_URL}/recados/${id}`, { method: 'DELETE' });
        carregarRecados();
    } catch (err) {
        alert('Erro ao excluir');
    }
}

// ==================== USUARIOS ====================
document.getElementById('form-usuario').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const dados = {
        nome: document.getElementById('user_nome').value,
        email: document.getElementById('user_email').value,
        senha: document.getElementById('user_senha').value,
        universidade: document.getElementById('user_universidade').value,
        curso: document.getElementById('user_curso').value,
        periodo: document.getElementById('user_periodo').value,
        tipo: document.getElementById('user_tipo').value
    };
    
    try {
        const url = usuarioEditando 
            ? `${API_URL}/usuarios/${usuarioEditando}`
            : `${API_URL}/usuarios`;
        
        const method = usuarioEditando ? 'PUT' : 'POST';
        
        const res = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        
        if (res.ok) {
            alert(usuarioEditando ? 'Usuario atualizado!' : 'Usuario cadastrado!');
            cancelarEdicaoUsuario();
            e.target.reset();
            carregarUsuarios();
        }
    } catch (err) {
        alert('Erro ao salvar usuario');
    }
});

document.getElementById('btn-cancelar-usuario').addEventListener('click', cancelarEdicaoUsuario);

function cancelarEdicaoUsuario() {
    usuarioEditando = null;
    document.getElementById('form-usuario').reset();
    document.getElementById('btn-salvar-usuario').textContent = 'Cadastrar';
    document.getElementById('btn-cancelar-usuario').style.display = 'none';
    document.getElementById('user_email').readOnly = false;
}

async function carregarUsuarios() {
    const container = document.getElementById('lista-usuarios');
    container.innerHTML = '<div class="loading"></div>';
    
    try {
        const res = await fetch(`${API_URL}/usuarios`);
        const usuarios = await res.json();
        
        if (usuarios.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>Nenhum usuario cadastrado</p></div>';
            return;
        }
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Email</th>
                        <th>Curso</th>
                        <th>Periodo</th>
                        <th>Tipo</th>
                        <th>Acoes</th>
                    </tr>
                </thead>
                <tbody>
                    ${usuarios.map(u => `
                        <tr>
                            <td>${u.id}</td>
                            <td>${u.nome}</td>
                            <td>${u.email}</td>
                            <td>${u.curso}</td>
                            <td>${u.periodo}º</td>
                            <td><span class="badge badge-duvida">${u.tipo}</span></td>
                            <td class="table-actions">
                                <button onclick="editarUsuario(${u.id})" class="btn-sm btn-edit">Editar</button>
                                <button onclick="deleteUsuario(${u.id})" class="btn-sm btn-delete">Excluir</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (err) {
        container.innerHTML = '<p>Erro ao carregar usuarios</p>';
    }
}

async function editarUsuario(id) {
    try {
        const res = await fetch(`${API_URL}/usuarios/${id}`);
        const usuario = await res.json();
        
        usuarioEditando = id;
        document.getElementById('user_nome').value = usuario.nome;
        document.getElementById('user_email').value = usuario.email;
        document.getElementById('user_email').readOnly = true;
        document.getElementById('user_senha').value = usuario.senha;
        document.getElementById('user_universidade').value = usuario.universidade;
        document.getElementById('user_curso').value = usuario.curso;
        document.getElementById('user_periodo').value = usuario.periodo;
        document.getElementById('user_tipo').value = usuario.tipo;
        
        document.getElementById('btn-salvar-usuario').textContent = 'Atualizar';
        document.getElementById('btn-cancelar-usuario').style.display = 'inline-block';
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
        alert('Erro ao carregar usuario');
    }
}

async function deleteUsuario(id) {
    if (!confirm('Deseja excluir este usuario?')) return;
    
    try {
        await fetch(`${API_URL}/usuarios/${id}`, { method: 'DELETE' });
        carregarUsuarios();
    } catch (err) {
        alert('Erro ao excluir');
    }
}

// ==================== DISCIPLINAS ====================
document.getElementById('form-disciplina').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const dados = {
        nome: document.getElementById('disc_nome').value,
        codigo: document.getElementById('disc_codigo').value,
        curso: document.getElementById('disc_curso').value,
        professor_id: document.getElementById('disc_professor').value,
        periodo: document.getElementById('disc_periodo').value
    };
    
    try {
        const res = await fetch(`${API_URL}/disciplinas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        
        if (res.ok) {
            alert('Disciplina cadastrada!');
            e.target.reset();
            carregarDisciplinas();
        }
    } catch (err) {
        alert('Erro ao cadastrar disciplina');
    }
});

async function carregarDisciplinas() {
    const container = document.getElementById('lista-disciplinas');
    container.innerHTML = '<div class="loading"></div>';
    
    try {
        const res = await fetch(`${API_URL}/disciplinas`);
        const disciplinas = await res.json();
        
        if (disciplinas.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>Nenhuma disciplina cadastrada</p></div>';
            return;
        }
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Codigo</th>
                        <th>Curso</th>
                        <th>Professor ID</th>
                        <th>Periodo</th>
                    </tr>
                </thead>
                <tbody>
                    ${disciplinas.map(d => `
                        <tr>
                            <td>${d.id}</td>
                            <td>${d.nome}</td>
                            <td><span class="badge badge-duvida">${d.codigo}</span></td>
                            <td>${d.curso}</td>
                            <td>${d.professor_id}</td>
                            <td>${d.periodo}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (err) {
        container.innerHTML = '<p>Erro ao carregar disciplinas</p>';
    }
}

// ==================== TOPICOS ====================
document.getElementById('form-topico').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const dados = {
        titulo: document.getElementById('top_titulo').value,
        conteudo: document.getElementById('top_conteudo').value,
        disciplina_id: document.getElementById('top_disciplina').value,
        usuario_id: document.getElementById('top_usuario').value,
        categoria: document.getElementById('top_categoria').value
    };
    
    try {
        const res = await fetch(`${API_URL}/topicos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        
        if (res.ok) {
            alert('Topico criado!');
            e.target.reset();
            carregarTopicos();
        }
    } catch (err) {
        alert('Erro ao criar topico');
    }
});

async function carregarTopicos() {
    const container = document.getElementById('lista-topicos');
    container.innerHTML = '<div class="loading"></div>';
    
    try {
        const res = await fetch(`${API_URL}/topicos`);
        const topicos = await res.json();
        
        if (topicos.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>Nenhum topico criado</p></div>';
            return;
        }
        
        container.innerHTML = topicos.map(t => `
            <div class="item-card">
                <div class="item-header">
                    <div>
                        <h3 class="item-title">${t.titulo}</h3>
                        <span class="badge badge-${t.categoria.toLowerCase()}">${t.categoria}</span>
                        <span class="status-badge status-${t.status.toLowerCase()}">${t.status}</span>
                    </div>
                </div>
                <div class="item-body">${t.conteudo.substring(0, 200)}...</div>
                <div class="item-footer">
                    <span>Disciplina: ${t.disciplina_id} | Usuario: ${t.usuario_id}</span>
                    <span>${new Date(t.data_criacao).toLocaleDateString('pt-BR')}</span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = '<p>Erro ao carregar topicos</p>';
    }
}

// ==================== RESPOSTAS ====================
document.getElementById('form-resposta').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const dados = {
        topico_id: document.getElementById('resp_topico').value,
        usuario_id: document.getElementById('resp_usuario').value,
        conteudo: document.getElementById('resp_conteudo').value
    };
    
    try {
        const res = await fetch(`${API_URL}/respostas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        
        if (res.ok) {
            alert('Resposta enviada!');
            e.target.reset();
            carregarRespostas();
        }
    } catch (err) {
        alert('Erro ao enviar resposta');
    }
});

async function carregarRespostas() {
    const container = document.getElementById('lista-respostas');
    container.innerHTML = '<div class="loading"></div>';
    
    try {
        const res = await fetch(`${API_URL}/respostas`);
        const respostas = await res.json();
        
        if (respostas.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>Nenhuma resposta ainda</p></div>';
            return;
        }
        
        container.innerHTML = respostas.map(r => `
            <div class="item-card ${r.e_melhor_resposta ? 'resposta-melhor' : ''}">
                <div class="item-header">
                    <span>Topico: ${r.topico_id} | Usuario: ${r.usuario_id}</span>
                    ${r.e_melhor_resposta ? '<span class="badge badge-melhor">Melhor Resposta</span>' : `<button onclick="marcarMelhorResposta(${r.topico_id}, ${r.id})" class="btn-sm btn-success">Marcar Melhor</button>`}
                </div>
                <div class="item-body">${r.conteudo}</div>
                <div class="item-footer">
                    <span>${new Date(r.data_criacao).toLocaleString('pt-BR')}</span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = '<p>Erro ao carregar respostas</p>';
    }
}

async function buscarRespostasPorTopico() {
    const topicoId = document.getElementById('busca_topico').value;
    
    if (!topicoId) {
        alert('Digite o ID do topico');
        return;
    }
    
    const container = document.getElementById('lista-respostas');
    container.innerHTML = '<div class="loading"></div>';
    
    try {
        const res = await fetch(`${API_URL}/respostas?topico_id=${topicoId}`);
        const respostas = await res.json();
        
        if (respostas.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>Nenhuma resposta para este topico</p></div>';
            return;
        }
        
        container.innerHTML = respostas.map(r => `
            <div class="item-card ${r.e_melhor_resposta ? 'resposta-melhor' : ''}">
                <div class="item-header">
                    <span>Usuario: ${r.usuario_id}</span>
                    ${r.e_melhor_resposta ? '<span class="badge badge-melhor">Melhor Resposta</span>' : `<button onclick="marcarMelhorResposta(${r.topico_id}, ${r.id})" class="btn-sm btn-success">Marcar Melhor</button>`}
                </div>
                <div class="item-body">${r.conteudo}</div>
                <div class="item-footer">
                    <span>${new Date(r.data_criacao).toLocaleString('pt-BR')}</span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = '<p>Erro ao buscar respostas</p>';
    }
}

async function marcarMelhorResposta(topicoId, respostaId) {
    if (!confirm('Marcar como melhor resposta?')) return;
    
    try {
        const res = await fetch(`${API_URL}/topicos/${topicoId}/melhor-resposta`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resposta_id: respostaId })
        });
        
        if (res.ok) {
            alert('Melhor resposta marcada!');
            carregarRespostas();
        }
    } catch (err) {
        alert('Erro ao marcar');
    }
}
