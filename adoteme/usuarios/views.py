from django.shortcuts           import render
from django.http.response       import HttpResponse
from django.contrib.auth.models import User
from django.contrib             import messages
from django.contrib.messages    import constants
from django.contrib.auth        import authenticate, login, logout
from django.shortcuts           import redirect

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')   # TODO: Criar essa página

    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome            = request.POST.get("nome").strip()              # TODO: Scape SQLInjection
        email           = request.POST.get("email").strip()             # TODO: Scape SQLInjection
        senha           = request.POST.get("senha").strip()             # TODO: Scape SQLInjection
        confirmar_senha = request.POST.get("confirmar_senha").strip()   # TODO: Scape SQLInjection

        # TODO: Validação (real) de dados
        lens = [len(nome), len(email), len(senha), len(confirmar_senha)]

        if not all(lens):   # Se algum campo tem 0 caracteres:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return render(request, 'cadastro.html')
        elif senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senhas diferentes')
            return render(request, 'cadastro.html')

        # TODO: Senha já está sendo salva como hash ?

        try:
            user = User.objects.create_user(
                username = nome,
                email    = email,
                senha    = senha,
            )
        except Exception as e:
            messages.add_message(request, constants.SUCCESS, "Erro interno do sistema")
            return render(request, 'cadastro.html')

        messages.add_message(request, constants.SUCCESS, "Usuário criado com sucesso")
        return render(request, 'cadastro.html')
    else:
        return HttpResponse('Inválido')         # TODO: Método inválido

def entrar(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')   # TODO: Criar essa página

    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        nome    = request.POST.get("nome")
        senha   = request.POST.get("senha")

        user    = authenticate(username=nome, password=senha)
        if user is None:
            messages.add_message(request, constants.ERROR, 'Credenciais inválidas')
            return render(request, 'login.html')

        login(request, user)
        return redirect('/divulgar/novo_pet')   # TODO: Criar essa página

def sair(request):
    logout(request)
    return redirect('/auth/login')
