"""Gêmeo lógico em terminal do MVP Academia Pelé (Sprint 3)."""
from datetime import date, datetime

POSICOES = ["Goleiro", "Zagueiro", "Lateral", "Volante", "Meia", "Ponta", "Atacante"]
PESOS = {
    "Goleiro": {"defesas": 4, "saidas": 2.5, "posicionamento": 2, "passe": 1, "fisico": .5},
    "Zagueiro": {"marcacao": 4, "posicionamento": 3, "fisico": 2, "passe": 1.5, "visao": .5, "tecnica": .5, "finalizacao": .3},
    "Lateral": {"marcacao": 2.5, "fisico": 2.5, "passe": 2, "posicionamento": 2, "tecnica": 1.5, "visao": 1, "finalizacao": .7},
    "Volante": {"marcacao": 2.5, "passe": 2.5, "posicionamento": 2, "fisico": 2, "visao": 2, "tecnica": 1.5, "finalizacao": 1},
    "Meia": {"passe": 2.5, "visao": 2.5, "tecnica": 2.5, "finalizacao": 1.8, "marcacao": 1.8, "fisico": 1.5, "posicionamento": 1.5},
    "Ponta": {"tecnica": 3, "fisico": 2.5, "finalizacao": 2, "passe": 1.5, "visao": 1.5, "posicionamento": 1, "marcacao": .5},
    "Atacante": {"finalizacao": 4, "posicionamento": 2.5, "tecnica": 2, "fisico": 1.5, "passe": 1, "visao": 1, "marcacao": .5},
}
OUTFIELD = {"finalizacao": "Finalização", "passe": "Passe", "tecnica": "Técnica e drible", "visao": "Visão de jogo", "marcacao": "Marcação e desarme", "posicionamento": "Posicionamento", "fisico": "Físico e velocidade"}
GOALKEEPER = {"defesas": "Defesas e reflexos", "saidas": "Jogo aéreo e saídas", "posicionamento": "Posicionamento", "passe": "Passe e reposição", "fisico": "Físico e agilidade"}

contas = [{"id": 1, "nome": "Gabriel Martins", "nascimento": "2008-03-14", "idade": 18, "categoria": "Sub-20", "cpf": "11144477735", "email": "gabriel@academiapele.com", "senha": "Demo123!", "telefone": "(11) 99999-0000", "cep": "01000-000", "cidade": "São Paulo", "estado": "SP", "bairro": "Centro", "endereco": "Rua da Academia", "numero": "100", "posicao": "Atacante", "secundaria": "Ponta", "pe": "Destro", "avaliacoes": [], "role": "player"}]
peneiras = []
avaliacoes = []
conversas = []
favoritos = []
funcionarios = [
    {"nome": "Marina Lopes", "email": "funcionario@academiapele.com", "senha": "Academia123!", "cargo": "Olheira"},
    {"nome": "Bruno Martins", "email": "treinador@academiapele.com", "senha": "Academia123!", "cargo": "Treinador"},
]


def ler_numero(pergunta, minimo=None, maximo=None):
    """Repete a pergunta até receber um número dentro do intervalo permitido."""
    while True:
        valor = input(pergunta).strip()
        if valor.isdigit():
            numero = int(valor)
            if (minimo is None or numero >= minimo) and (maximo is None or numero <= maximo):
                return numero
        print("Informe um número válido" + (f" entre {minimo} e {maximo}" if minimo is not None and maximo is not None else "."))


def idade_de(nascimento):
    partes = nascimento.split("-")
    if len(partes) != 3 or any(not parte.isdigit() for parte in partes):
        return None
    ano, mes, dia = (int(parte) for parte in partes)
    if ano < 1900 or mes < 1 or mes > 12:
        return None
    dias_mes = [31, 29 if ano % 400 == 0 or (ano % 4 == 0 and ano % 100 != 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if dia < 1 or dia > dias_mes[mes - 1]:
        return None
    data_nasc = date(ano, mes, dia)
    if data_nasc > date.today():
        return None
    hoje = date.today()
    return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))


def categoria(idade):
    for limite in (7, 9, 11, 13, 15, 17, 20):
        if idade <= limite:
            return f"Sub-{limite}"
    return "Fora da faixa"


def cadastrar_atleta():
    print("\n=== Cadastro de jogador ===")
    nome = input("Como podemos chamar você? Informe seu nome completo: ").strip()
    nascimento = input("Qual é sua data de nascimento? (AAAA-MM-DD): ").strip()
    idade = idade_de(nascimento)
    if not nome or idade is None or idade < 7 or idade > 20:
        print("Não foi possível concluir o cadastro. Confira seu nome e a data de nascimento; aceitamos atletas de 7 a 20 anos.")
        return
    cpf = "".join(c for c in input("CPF (11 dígitos): ") if c.isdigit())
    if not cpf_valido(cpf) or any(a.get("cpf") == cpf for a in contas):
        print("Esse CPF não parece válido ou já está associado a outra conta. Confira os números e tente novamente.")
        return
    email = input("E-mail: ").strip().lower()
    if "@" not in email or any(a["email"] == email for a in contas):
        print("E-mail inválido ou já cadastrado.")
        return
    senha = input("Senha (mínimo 6 caracteres): ")
    if len(senha) < 6:
        print("Escolha uma senha com pelo menos 6 caracteres para proteger sua conta.")
        return
    print("Posições:", ", ".join(POSICOES))
    posicao = input("Posição principal: ").strip().title()
    secundaria = input("Posição secundária (ou —): ").strip().title()
    if posicao not in POSICOES or (secundaria != "—" and secundaria not in POSICOES) or secundaria == posicao:
        print("Selecione posições válidas; a secundária deve ser diferente da principal.")
        return
    telefone = input("Telefone: ").strip()
    cep = input("CEP: ").strip()
    cidade = input("Cidade: ").strip()
    estado = input("Estado (UF): ").strip().upper()
    bairro = input("Bairro: ").strip()
    endereco = input("Endereço: ").strip()
    numero = input("Número: ").strip()
    if not all((telefone, cep, cidade, estado, bairro, endereco, numero)):
        print("Falta alguma informação de contato ou endereço. Preencha todos os campos para continuar.")
        return
    atleta = {"id": len(contas) + 1, "nome": nome, "nascimento": nascimento, "idade": idade, "categoria": categoria(idade), "cpf": cpf, "email": email, "senha": senha, "telefone": telefone, "cep": cep, "cidade": cidade, "estado": estado, "bairro": bairro, "endereco": endereco, "numero": numero, "posicao": posicao, "secundaria": secundaria, "pe": "Destro", "avaliacoes": [], "role": "player"}
    contas.append(atleta)
    print(f"Pronto, {nome}! Sua conta foi criada na categoria {atleta['categoria']}. Agora você já pode entrar.")


def cpf_valido(cpf):
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito = (soma * 10) % 11
    if digito == 10:
        digito = 0
    if digito != int(cpf[9]):
        return False
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito = (soma * 10) % 11
    if digito == 10:
        digito = 0
    return digito == int(cpf[10])


def listar_atletas():
    print("\n=== Banco de atletas ===")
    nome = input("Filtrar por nome (Enter para todos): ").strip().lower()
    pos = input("Filtrar por posição (Enter para todas): ").strip().title()
    cidade = input("Filtrar por cidade (Enter para todas): ").strip().lower()
    encontrados = [a for a in contas if a.get("posicao") and nome in a["nome"].lower() and (not pos or pos in (a["posicao"], a["secundaria"])) and (not cidade or cidade in a["cidade"].lower())]
    if not encontrados:
        print("Nenhum atleta encontrado.")
    for a in encontrados:
        notas = [r["nota"] for r in avaliacoes if r["atleta_id"] == a["id"]]
        media = sum(notas) / len(notas) if notas else 0
        print(f"{a['id']} | {a['nome']} | {a['idade']} anos | {a['categoria']} | {a['posicao']} / {a['secundaria']} | {a['cidade']}-{a['estado']} | Nota média: {media:.1f} ({len(notas)} avaliações)")


def criar_peneira():
    print("\n=== Criar/agendar peneira ===")
    titulo = input("Nome da peneira: ").strip() or "Nova peneira"
    data = input("Data (AAAA-MM-DD): ").strip() or "2026-09-30"
    horario = input("Horário (HH:MM): ").strip() or "09:00"
    vagas = ler_numero("Quantidade de vagas: ", 1)
    locais = ["Centro de Treinamento Pelé — São Paulo/SP", "Arena Oeste — Osasco/SP", "CT Litoral — Santos/SP"]
    for i, local in enumerate(locais, 1):
        print(f"{i}. {local}")
    escolha = ler_numero("Local: ", 1, len(locais))
    print("Posições:", ", ".join(POSICOES))
    entrada = input("Posições aceitas, separadas por vírgula: ").split(",")
    posicoes = [p.strip().title() for p in entrada if p.strip().title() in POSICOES]
    if not posicoes:
        print("Selecione pelo menos uma posição válida.")
        return
    peneiras.append({"id": len(peneiras) + 1, "titulo": titulo, "data": data, "horario": horario, "local": locais[escolha - 1], "vagas": vagas, "inscritos": [], "posicoes": posicoes})
    print("Peneira publicada! Os jogadores já podem encontrar essa oportunidade.")


def inscrever_peneira(email=None):
    if not peneiras:
        print("Ainda não há peneiras agendadas.")
        return
    atletas = [a for a in contas if a.get("posicao")]
    if not atletas:
        print("Cadastre um atleta antes de se inscrever.")
        return
    if email is None:
        listar_atletas()
        email = input("E-mail do atleta para inscrição: ").strip().lower()
    atleta = next((a for a in atletas if a["email"] == email), None)
    if atleta is None:
        print("Atleta não encontrado.")
        return
    for p in peneiras:
        print(f"{p['id']}. {p['titulo']} | {p['data']} {p['horario']} | {p['local']} | {p['vagas'] - len(p['inscritos'])} vagas | {', '.join(p['posicoes'])}")
    peneira = next((p for p in peneiras if p["id"] == ler_numero("Número da peneira: ", 1, len(peneiras))), None)
    if email in peneira["inscritos"]:
        print("Este atleta já está inscrito.")
    elif atleta["categoria"] == "Fora da faixa":
        print("Atleta fora das categorias aceitas.")
    elif not any(pos in peneira["posicoes"] for pos in (atleta["posicao"], atleta["secundaria"])):
        print("A posição do atleta não está entre as posições aceitas.")
    elif len(peneira["inscritos"]) >= peneira["vagas"]:
        print("Não há mais vagas nesta peneira.")
    else:
        peneira["inscritos"].append(email)
        print("Inscrição confirmada.")


def avaliar_atleta():
    atletas = [a for a in contas if a.get("posicao")]
    if not atletas:
        print("Nenhum atleta cadastrado.")
        return
    listar_atletas()
    atleta = next((a for a in atletas if a["id"] == ler_numero("ID do atleta: ", 1, len(contas))), None)
    if atleta is None:
        print("Atleta não encontrado.")
        return
    campos = GOALKEEPER if atleta["posicao"] == "Goleiro" else OUTFIELD
    notas = {}
    for chave, rotulo in campos.items():
        notas[chave] = ler_numero(f"{rotulo} (0 a 10): ", 0, 10)
    pesos = PESOS[atleta["posicao"]]
    total = sum(pesos[k] for k in campos)
    nota = round(sum(notas[k] * pesos[k] for k in campos) / total, 1)
    comentario = input("Comentário do olheiro: ").strip()
    avaliacoes.append({"atleta_id": atleta["id"], "nota": nota, "notas": notas, "comentario": comentario})
    atleta["avaliacoes"].append(nota)
    print(f"Nota ponderada: {nota:.1f}/10 — {'Aprovado para acompanhamento' if nota >= 6 else 'Não aprovado nesta avaliação'}.")


def dashboard():
    atletas = [a for a in contas if a.get("posicao")]
    notas = [r["nota"] for r in avaliacoes]
    print("\n=== Visão geral / Dashboard ===")
    print(f"Atletas cadastrados: {len(atletas)} | Peneiras: {len(peneiras)} | Inscrições: {sum(len(p['inscritos']) for p in peneiras)}")
    print(f"Avaliações: {len(notas)} | Nota média geral: {sum(notas) / len(notas):.1f}" if notas else "Avaliações: 0 | Nota média geral: ainda sem avaliações")
    for pos in POSICOES:
        qtd = sum(a["posicao"] == pos for a in atletas)
        if qtd:
            print(f"{pos}: {qtd} atleta(s)")


def enviar_mensagem():
    origem = input("Seu nome/e-mail: ").strip()
    destino = input("Destinatário (nome/e-mail): ").strip()
    texto = input("Mensagem: ").strip()
    if origem and destino and texto:
        conversas.append({"de": origem, "para": destino, "mensagem": texto, "data": datetime.now().isoformat(timespec="minutes")})
        print("Mensagem enviada.")
    else:
        print("Preencha remetente, destinatário e mensagem.")


def menu_funcionario(funcionario):
    """Mostra as ferramentas de trabalho disponíveis para funcionários."""
    while True:
        print(f"\n=== Olá, {funcionario['nome']}! | Área de {funcionario['cargo']} ===")
        print("1. Banco de atletas  2. Criar/agendar peneira  3. Avaliar atleta")
        print("4. Dashboard         5. Enviar mensagem       0. Sair da conta")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            listar_atletas()
        elif opcao == "2":
            criar_peneira()
        elif opcao == "3":
            avaliar_atleta()
        elif opcao == "4":
            dashboard()
        elif opcao == "5":
            enviar_mensagem()
        elif opcao == "0":
            print("Você saiu da sua conta. Até a próxima!")
            break
        else:
            print("Não entendi essa opção. Escolha um dos números do menu, por favor.")


def menu_jogador(atleta):
    """Mostra ao jogador seu perfil, oportunidades e avaliações recebidas."""
    while True:
        print(f"\n=== Olá, {atleta['nome']}! Que bom ter você por aqui. ===")
        print("1. Meu perfil  2. Ver peneiras e me inscrever  3. Minhas avaliações")
        print("4. Enviar mensagem  0. Sair da conta")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            print(f"{atleta['nome']} | {atleta['idade']} anos | {atleta['categoria']} | {atleta['posicao']} / {atleta['secundaria']} | {atleta['cidade']}-{atleta['estado']}")
        elif opcao == "2":
            inscrever_peneira(atleta["email"])
        elif opcao == "3":
            minhas_notas = [r for r in avaliacoes if r["atleta_id"] == atleta["id"]]
            if not minhas_notas:
                print("Você ainda não recebeu avaliações.")
            for avaliacao in minhas_notas:
                print(f"Nota: {avaliacao['nota']:.1f}/10 | {avaliacao['comentario']}")
        elif opcao == "4":
            enviar_mensagem()
        elif opcao == "0":
            print("Você saiu da sua conta. Até a próxima!")
            break
        else:
            print("Não entendi essa opção. Escolha um dos números do menu, por favor.")


def autenticar():
    """Apresenta o acesso e encaminha cada pessoa à sua própria área."""
    while True:
        print()
        print("=== Bem-vindo à Academia Pelé ===")
        print("O que você gostaria de fazer?")
        print("1. Entrar na minha conta  2. Criar uma conta de jogador  0. Encerrar")
        print("Acesso de teste funcionário: funcionario@academiapele.com / Academia123!")
        print("Acesso de teste jogador: gabriel@academiapele.com / Demo123!")
        opcao = input("Escolha: ").strip()

        if opcao == "0":
            print("Obrigado por visitar a Academia Pelé. Até logo!")
            return
        elif opcao == "2":
            cadastrar_atleta()
        elif opcao == "1":
            email = input("E-mail: ").strip().lower()
            senha = input("Senha: ")
            funcionario = next((f for f in funcionarios if f["email"] == email and f["senha"] == senha), None)

            if funcionario:
                menu_funcionario(funcionario)
            else:
                atleta = next((a for a in contas if a["email"] == email and a["senha"] == senha), None)
                if atleta:
                    menu_jogador(atleta)
                else:
                    print("Não encontramos uma conta com esses dados. Confira o e-mail e a senha e tente de novo.")
        else:
            print("Não entendi essa opção. Escolha um dos números do menu, por favor.")

if __name__ == "__main__":
    autenticar()
