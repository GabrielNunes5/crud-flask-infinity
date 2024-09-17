from flask import Response, request, Blueprint
import json
from ..database import db
from ..models.professor import Professor

professores_bp = Blueprint('professores', __name__)


@professores_bp.route('/professores', methods=['GET'])
def selecionar_professores():
    professores = Professor.query.all()
    professores_json = [professor.to_json() for professor in professores]

    return gerar_response(
        status=200,
        nome_conteudo='Professores',
        conteudo=professores_json,
        mensagem='ok'
    )


@professores_bp.route('/professores/<id>', methods=['GET'])
def selecionar_professor(id):
    professor = Professor.query.filter_by(id=id).first()
    professor_json = professor.to_json()

    return gerar_response(
        status=200,
        nome_conteudo='Professor',
        conteudo=professor_json,
        mensagem='ok'
    )


@professores_bp.route('/professores', methods=['POST'])
def criar_professor():
    body = request.get_json()

    try:
        professor = Professor(nome=body['nome'], email=body['email'])
        db.session.add(professor)
        db.session.commit()
        return gerar_response(
            201,
            'Professor',
            professor.to_json(),
            'Professor criado com sucesso'
        )

    except Exception:
        return gerar_response(
            400,
            'Professor',
            {},
            'Erro ao tentar criar o professor'
        )


@professores_bp.route('/professores/<id>', methods=['PUT'])
def atualizar_professor(id):
    professor = Professor.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if 'nome' in body:
            professor.nome = body['nome']
        if 'email' in body:
            professor.email = body['email']

        db.session.add(professor)
        db.session.commit()
        return gerar_response(
            200,
            'Professor',
            professor.to_json(),
            'Professor atualizado com sucesso'
        )
    except Exception:
        return gerar_response(
            400,
            'Professor',
            {},
            'Erro ao tentar atualizar o professor'
        )


@professores_bp.route('/professores/<id>', methods=['DELETE'])
def deletar_professor(id):
    professor = Professor.query.filter_by(id=id).first()

    try:
        db.session.delete(professor)
        db.session.commit()
        return gerar_response(
            202,
            'Professor',
            professor.to_json(),
            'Professor deletado com sucesso'
        )
    except Exception:
        return gerar_response(
            400,
            'Professor',
            {},
            'Erro ao tentar deletar o professor'
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