const API_URL = 'http://localhost:3000/api';

function mostrarMensagem(texto, tipo = 'sucesso') {
    const mensagem = document.getElementById('mensagem');
    mensagem.textContent = texto;
    mensagem.className = `mensagem show ${tipo}`;
    setTimeout(() => mensagem.classList.remove('show'), 5000);
}

function formatarData(data) {
    return new Date(data).toLocaleString('pt-BR');
}

// Sistema de Abas
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const tabId = this.dataset.tab;
        
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        this.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    });
});

async function carregarCursos() {
    try {
        const response = await fetch(`${API_URL}/usuarios/aux/cursos/1`);
        const resultado = await response.json();
        
        if (resultado.success) {
            ['curso_id', 'disc_curso'].forEach(id => {
                const select = document.getElementById(id);
                if (select) {
                    select.innerHTML = '<option value="">Selecione o Curso</option>';
                    resultado.data.forEach(c => {
                        select.innerHTML += `<option value="${c.id}">${c.nome}</option>`;
                    });
                }
            });
        }
    } catch (error) {
        console.error('Erro ao carregar cursos:', error);
    }
}

// RECADOS
document.getElementById('form-recado')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        titulo: document.getElementById('rec_titulo').value,
        conteudo: document.getElementById('rec_conteudo').value,
        autor: document.getElementById('rec_autor').value,
        categoria: document.getElementById('rec_categoria').value,
        cor: '#003366'
    };
    
    try {
        const response = await fetch(`${API_URL}/recados`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem('Recado criado com sucesso!', 'sucesso');
            this.reset();
            buscarRecados();
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao conectar com servidor', 'erro');
    }
});

async function buscarRecados() {
    try {
        const response = await fetch(`${API_URL}/recados`);
        const resultado = await response.json();
        
        const lista = document.getElementById('lista-recados');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = '';
            resultado.data.forEach(rec => {
                lista.innerHTML += `
                    <div class="resultado-item" style="border-left: 5px solid ${rec.cor}">
                        <p><strong>${rec.titulo}</strong> - ${rec.categoria}</p>
                        <p>${rec.conteudo}</p>
                        <p><small>Por: ${rec.autor} em ${formatarData(rec.criado_em)}</small></p>
                        <button class="btn btn-danger" onclick="excluirRecado(${rec.id})">
                            <i class="material-icons">delete</i> Excluir
                        </button>
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p>Nenhum recado publicado ainda.</p>';
        }
    } catch (error) {
        mostrarMensagem('Erro ao buscar recados', 'erro');
    }
}

async function excluirRecado(id) {
    if (!confirm('Deseja realmente excluir este recado?')) return;
    try {
        const response = await fetch(`${API_URL}/recados/${id}`, { method: 'DELETE' });
        const resultado = await response.json();
        if (resultado.success) {
            mostrarMensagem('Recado excluído!', 'sucesso');
            buscarRecados();
        }
    } catch (error) {
        mostrarMensagem('Erro ao excluir recado', 'erro');
    }
}

// USUÁRIOS
document.getElementById('form-usuario')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        nome_completo: document.getElementById('nome_completo').value,
        email: document.getElementById('email').value,
        senha: document.getElementById('senha').value,
        confirmar_senha: document.getElementById('confirmar_senha').value,
        universidade_id: 1,
        curso_id: parseInt(document.getElementById('curso_id').value),
        periodo: parseInt(document.getElementById('periodo').value),
        tipo_usuario: document.getElementById('tipo_usuario').value
    };
    
    try {
        const response = await fetch(`${API_URL}/usuarios`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(`Usuário cadastrado! ID: ${resultado.usuario_id}`, 'sucesso');
            this.reset();
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao conectar com servidor', 'erro');
    }
});

document.getElementById('form-buscar-usuario')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const nome = document.getElementById('buscar_nome').value;
    const tipo = document.getElementById('buscar_tipo').value;
    
    let url = `${API_URL}/usuarios?`;
    if (nome) url += `nome=${encodeURIComponent(nome)}&`;
    if (tipo) url += `tipo_usuario=${encodeURIComponent(tipo)}`;
    
    try {
        const response = await fetch(url);
        const resultado = await response.json();
        
        const lista = document.getElementById('lista-usuarios');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total encontrado:</strong> ${resultado.total}</p>`;
            resultado.data.forEach(u => {
                lista.innerHTML += `
                    <div class="resultado-item">
                        <p><strong>ID:</strong> ${u.id} | <strong>Nome:</strong> ${u.nome_completo}</p>
                        <p><strong>Email:</strong> ${u.email}</p>
                        <p><strong>Tipo:</strong> ${u.tipo_usuario} | <strong>Período:</strong> ${u.periodo}º</p>
                        <p><strong>Curso:</strong> ${u.curso}</p>
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p>Nenhum usuário encontrado.</p>';
        }
    } catch (error) {
        mostrarMensagem('Erro ao buscar usuários', 'erro');
    }
});

// DISCIPLINAS
document.getElementById('form-disciplina')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        nome: document.getElementById('disc_nome').value,
        codigo: document.getElementById('disc_codigo').value,
        universidade_id: 1,
        curso_id: parseInt(document.getElementById('disc_curso').value),
        professor_id: parseInt(document.getElementById('disc_professor').value),
        periodo_letivo: document.getElementById('disc_periodo').value,
        descricao: document.getElementById('disc_descricao').value
    };
    
    try {
        const response = await fetch(`${API_URL}/disciplinas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(`Disciplina cadastrada! ID: ${resultado.disciplina_id}`, 'sucesso');
            this.reset();
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao conectar com servidor', 'erro');
    }
});

document.getElementById('form-buscar-disciplina')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const nome = document.getElementById('buscar_disc_nome').value;
    let url = `${API_URL}/disciplinas?`;
    if (nome) url += `nome=${encodeURIComponent(nome)}`;
    
    try {
        const response = await fetch(url);
        const resultado = await response.json();
        
        const lista = document.getElementById('lista-disciplinas');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total:</strong> ${resultado.total}</p>`;
            resultado.data.forEach(d => {
                lista.innerHTML += `
                    <div class="resultado-item">
                        <p><strong>ID:</strong> ${d.id} | <strong>Nome:</strong> ${d.nome}</p>
                        <p><strong>Código:</strong> ${d.codigo} | <strong>Período:</strong> ${d.periodo_letivo}</p>
                        <p><strong>Professor:</strong> ${d.professor} | <strong>Curso:</strong> ${d.curso}</p>
                        ${d.descricao ? `<p><strong>Descrição:</strong> ${d.descricao}</p>` : ''}
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p>Nenhuma disciplina encontrada.</p>';
        }
    } catch (error) {
        mostrarMensagem('Erro ao buscar disciplinas', 'erro');
    }
});

// TÓPICOS
document.getElementById('form-topico')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        titulo: document.getElementById('top_titulo').value,
        conteudo: document.getElementById('top_conteudo').value,
        disciplina_id: parseInt(document.getElementById('top_disciplina').value),
        usuario_id: parseInt(document.getElementById('top_usuario').value),
        categoria: document.getElementById('top_categoria').value,
        tags: document.getElementById('top_tags').value
    };
    
    try {
        const response = await fetch(`${API_URL}/topicos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(`Tópico criado! ID: ${resultado.topico_id}`, 'sucesso');
            this.reset();
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao conectar com servidor', 'erro');
    }
});

document.getElementById('form-buscar-topico')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const titulo = document.getElementById('buscar_top_titulo').value;
    let url = `${API_URL}/topicos?`;
    if (titulo) url += `titulo=${encodeURIComponent(titulo)}`;
    
    try {
        const response = await fetch(url);
        const resultado = await response.json();
        
        const lista = document.getElementById('lista-topicos');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total:</strong> ${resultado.total}</p>`;
            resultado.data.forEach(t => {
                lista.innerHTML += `
                    <div class="resultado-item">
                        <p><strong>ID:</strong> ${t.id} | <strong>Título:</strong> ${t.titulo}</p>
                        <p>${t.conteudo}</p>
                        <p><strong>Categoria:</strong> ${t.categoria} | <strong>Status:</strong> ${t.status}</p>
                        <p><strong>Autor:</strong> ${t.autor} | <strong>Disciplina:</strong> ${t.disciplina}</p>
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p>Nenhum tópico encontrado.</p>';
        }
    } catch (error) {
        mostrarMensagem('Erro ao buscar tópicos', 'erro');
    }
});

// RESPOSTAS
document.getElementById('form-resposta')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        conteudo: document.getElementById('resp_conteudo').value,
        topico_id: parseInt(document.getElementById('resp_topico').value),
        usuario_id: parseInt(document.getElementById('resp_usuario').value),
    };
    
    const pai = document.getElementById('resp_pai').value;
    if (pai) formData.resposta_pai_id = parseInt(pai);
    
    try {
        const response = await fetch(`${API_URL}/respostas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(`Resposta criada! ID: ${resultado.resposta_id}`, 'sucesso');
            this.reset();
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao conectar com servidor', 'erro');
    }
});

document.getElementById('form-buscar-resposta')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const topico = document.getElementById('buscar_resp_topico').value;
    
    try {
        const response = await fetch(`${API_URL}/respostas/topico/${topico}`);
        const resultado = await response.json();
        
        const lista = document.getElementById('lista-respostas');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total:</strong> ${resultado.total}</p>`;
            resultado.data.forEach(r => {
                lista.innerHTML += `
                    <div class="resultado-item">
                        <p><strong>ID:</strong> ${r.id} | <strong>Autor:</strong> ${r.autor} (${r.tipo_usuario})</p>
                        <p>${r.conteudo}</p>
                        <p><strong>Votos:</strong> ${r.votos} | <strong>Data:</strong> ${formatarData(r.criado_em)}</p>
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p>Nenhuma resposta encontrada.</p>';
        }
    } catch (error) {
        mostrarMensagem('Erro ao buscar respostas', 'erro');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    carregarCursos();
    buscarRecados();
    mostrarMensagem('Sistema carregado com sucesso!', 'info');
});
