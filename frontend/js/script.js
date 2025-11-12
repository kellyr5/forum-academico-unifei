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

// Sistema de Abas com AUTO-LOAD
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const tabId = this.dataset.tab;
        
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        this.classList.add('active');
        const tabElement = document.getElementById(tabId);
        if (tabElement) {
            tabElement.classList.add('active');
            
            // AUTO-CARREGAR dados ao abrir aba
            setTimeout(() => {
                if (tabId === 'disciplinas') buscarDisciplinas();
                if (tabId === 'topicos') buscarTopicos();
                if (tabId === 'usuarios') buscarUsuarios();
            }, 100);
        }
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

// ===== RECADOS =====
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
            mostrarMensagem('Recado criado!', 'sucesso');
            this.reset();
            buscarRecados();
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro', 'erro');
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
            lista.innerHTML = '<p>Nenhum recado.</p>';
        }
    } catch (error) {
        mostrarMensagem('Erro', 'erro');
    }
}

async function excluirRecado(id) {
    if (!confirm('Excluir?')) return;
    try {
        const response = await fetch(`${API_URL}/recados/${id}`, { method: 'DELETE' });
        const resultado = await response.json();
        if (resultado.success) {
            mostrarMensagem('Excluído!', 'sucesso');
            buscarRecados();
        }
    } catch (error) {
        mostrarMensagem('Erro', 'erro');
    }
}

// ===== USUÁRIOS =====
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
            mostrarMensagem(`Usuário ID: ${resultado.usuario_id}`, 'sucesso');
            this.reset();
            buscarUsuarios();
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro', 'erro');
    }
});

async function buscarUsuarios() {
    try {
        const nome = document.getElementById('buscar_nome')?.value || '';
        const tipo = document.getElementById('buscar_tipo')?.value || '';
        let url = `${API_URL}/usuarios?`;
        if (nome) url += `nome=${encodeURIComponent(nome)}&`;
        if (tipo) url += `tipo_usuario=${encodeURIComponent(tipo)}`;
        
        const response = await fetch(url);
        const resultado = await response.json();
        const lista = document.getElementById('lista-usuarios');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total:</strong> ${resultado.total} usuários</p>`;
            resultado.data.forEach(u => {
                lista.innerHTML += `
                    <div class="resultado-item">
                        <p><strong>ID:</strong> ${u.id} | ${u.nome_completo}</p>
                        <p>${u.email} | ${u.tipo_usuario} | ${u.periodo}º período</p>
                        <p>${u.curso}</p>
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p>Nenhum usuário.</p>';
        }
    } catch (error) {
        mostrarMensagem('Erro', 'erro');
    }
}

document.getElementById('form-buscar-usuario')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    buscarUsuarios();
});

// ===== DISCIPLINAS =====
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
            mostrarMensagem(`Disciplina ID: ${resultado.disciplina_id}`, 'sucesso');
            this.reset();
            buscarDisciplinas();
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro', 'erro');
    }
});

async function buscarDisciplinas() {
    try {
        const nome = document.getElementById('buscar_disc_nome')?.value || '';
        let url = `${API_URL}/disciplinas`;
        if (nome) url += `?nome=${encodeURIComponent(nome)}`;
        
        const response = await fetch(url);
        const resultado = await response.json();
        const lista = document.getElementById('lista-disciplinas');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total:</strong> ${resultado.total} disciplinas</p>`;
            resultado.data.forEach(d => {
                lista.innerHTML += `
                    <div class="resultado-item">
                        <p><strong>ID:</strong> ${d.id} | <strong>${d.nome}</strong></p>
                        <p><strong>Código:</strong> ${d.codigo} | <strong>Período:</strong> ${d.periodo_letivo}</p>
                        <p><strong>Professor:</strong> ${d.professor} | <strong>Curso:</strong> ${d.curso}</p>
                        ${d.descricao ? `<p>${d.descricao}</p>` : ''}
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p>Nenhuma disciplina.</p>';
        }
    } catch (error) {
        console.error(error);
        mostrarMensagem('Erro ao buscar disciplinas', 'erro');
    }
}

document.getElementById('form-buscar-disciplina')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    buscarDisciplinas();
});

// ===== TÓPICOS =====
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
            mostrarMensagem(`Tópico ID: ${resultado.topico_id}`, 'sucesso');
            this.reset();
            buscarTopicos();
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro', 'erro');
    }
});

async function buscarTopicos() {
    try {
        const titulo = document.getElementById('buscar_top_titulo')?.value || '';
        let url = `${API_URL}/topicos`;
        if (titulo) url += `?titulo=${encodeURIComponent(titulo)}`;
        
        const response = await fetch(url);
        const resultado = await response.json();
        const lista = document.getElementById('lista-topicos');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total:</strong> ${resultado.total} tópicos</p>`;
            resultado.data.forEach(t => {
                lista.innerHTML += `
                    <div class="resultado-item topico-card">
                        <h4>${t.titulo}</h4>
                        <p>${t.conteudo}</p>
                        <p><strong>Categoria:</strong> ${t.categoria} | <strong>Status:</strong> ${t.status}</p>
                        <p><strong>Autor:</strong> ${t.autor} | <strong>Disciplina:</strong> ${t.disciplina}</p>
                        ${t.tags ? `<p><strong>Tags:</strong> ${t.tags}</p>` : ''}
                        <button class="btn btn-primary" onclick="verRespostas(${t.id})">
                            <i class="material-icons">question_answer</i> Ver Respostas
                        </button>
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p>Nenhum tópico encontrado.</p>';
        }
    } catch (error) {
        console.error(error);
        mostrarMensagem('Erro ao buscar tópicos', 'erro');
    }
}

document.getElementById('form-buscar-topico')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    buscarTopicos();
});

// ===== RESPOSTAS =====
async function verRespostas(topicoId) {
    try {
        const response = await fetch(`${API_URL}/respostas/topico/${topicoId}`);
        const resultado = await response.json();
        
        document.querySelector('button[data-tab="respostas"]').click();
        const lista = document.getElementById('lista-respostas');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total:</strong> ${resultado.total} respostas</p>`;
            resultado.data.forEach(r => {
                const melhor = r.melhor_resposta ? '<span class="badge-melhor">✓ Melhor Resposta</span>' : '';
                lista.innerHTML += `
                    <div class="resultado-item resposta-card ${r.melhor_resposta ? 'melhor-resposta' : ''}">
                        ${melhor}
                        <p><strong>${r.autor}</strong> <span class="badge">${r.tipo_usuario}</span></p>
                        <p>${r.conteudo}</p>
                        <p><i class="material-icons">thumb_up</i> ${r.votos} votos | ${formatarData(r.criado_em)}</p>
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p>Nenhuma resposta ainda.</p>';
        }
        mostrarMensagem(`${resultado.total || 0} respostas`, 'info');
    } catch (error) {
        mostrarMensagem('Erro', 'erro');
    }
}

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
            mostrarMensagem(`Resposta ID: ${resultado.resposta_id}`, 'sucesso');
            this.reset();
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro', 'erro');
    }
});

document.getElementById('form-buscar-resposta')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    const topico = document.getElementById('buscar_resp_topico').value;
    verRespostas(topico);
});

// INICIALIZAR
document.addEventListener('DOMContentLoaded', function() {
    carregarCursos();
    buscarRecados();
    mostrarMensagem('Sistema carregado! Clique nas abas para ver os dados.', 'info');
});
