from flask import Response, request, Blueprint
import json
from ..database import db
from ..models.aluno import Aluno

alunos_bp = Blueprint('alunos', __name__)


@alunos_bp.route('/alunos', methods=['GET'])
def selecionar_alunos():
    alunos = Aluno.query.all()
    alunos_json = [aluno.to_json() for aluno in alunos]

    return gerar_response(
        status=200,
        nome_conteudo='Alunos',
        conteudo=alunos_json,
        mensagem='ok'
        )


@alunos_bp.route('/alunos/<id>', methods=['GET'])
def selecionar_aluno(id):
    aluno = Aluno.query.filter_by(id=id).first()
    aluno_json = aluno.to_json()

    return gerar_response(
        status=200,
        nome_conteudo='Aluno',
        conteudo=aluno_json,
        mensagem='ok'
        )


@alunos_bp.route('/alunos', methods=['POST'])
def criar_aluno():
    body = request.get_json()

    try:
        aluno = Aluno(nome=body['nome'], email=body['email'])
        db.session.add(aluno)
        db.session.commit()
        return gerar_response(
            201,
            'Aluno',
            aluno.to_json(),
            'Aluno criado com sucesso')
    except Exception:
        return gerar_response(
            400,
            'Aluno',
            {},
            'Erro ao tentar criar o aluno'
        )


@alunos_bp.route('/alunos/<id>', methods=['PUT'])
def atualizar_aluno(id):
    aluno = Aluno.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if 'nome' in body:
            aluno.nome = body['nome']
        if 'email' in body:
            aluno.email = body['email']

        db.session.add(aluno)
        db.session.commit()
        return gerar_response(
            200,
            'Aluno',
            aluno.to_json(),
            'Aluno atualizado com sucesso'
        )

    except Exception:
        gerar_response(
            400,
            'Aluno',
            {},
            'Erro ao tentar atualizar o aluno'
        )


@alunos_bp.route('/alunos/<id>', methods=['DELETE'])
def deletar_aluno(id):
    aluno = Aluno.query.filter_by(id=id).first()

    try:
        db.session.delete(aluno)
        db.session.commit()
        return gerar_response(
            202,
            'Aluno',
            aluno.to_json(),
            'Aluno deletado com sucesso'
        )
    except Exception:
        return gerar_response(
            400,
            'Aluno',
            {},
            'Erro ao tentar deletar o aluno'
        )


def gerar_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if mensagem:
        body['mensagem'] = mensagem

    return Response(
        json.dumps(body),
        status=status,
        mimetype='application/json'
        )
