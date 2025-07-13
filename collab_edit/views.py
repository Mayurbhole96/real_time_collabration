from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import Document
from .forms import DocumentForm
import language_tool_python

# 🏠 Home Page: List all user’s documents
@login_required
def home(request):
    documents = Document.objects.filter(owner=request.user)
    return render(request, 'editor/home.html', {'documents': documents})


# 📄 Document Editor: Show editor page
@login_required
def document_editor(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)

    # Allow only owner to edit for now
    if document.owner != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    return render(request, 'editor/editor.html', {'document': document})


@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.owner = request.user  # Set the current user as owner
            doc.save()
            return redirect('document_editor', doc_id=doc.id)
    else:
        form = DocumentForm()
    
    return render(request, 'editor/create_document.html', {'form': form})

import requests
# 🤖 AI Suggestions API
@login_required
def ai_suggest(request):
    text = request.GET.get('text', '')
    if not text:
        return JsonResponse({'suggestions': []})

    # try:
    #     tool = language_tool_python.LanguageTool('en-US')
    #     matches = tool.check(text)
    #     suggestions = [
    #         {
    #             'message': match.message,
    #             'offset': match.offset,
    #             'length': match.errorLength
    #         } for match in matches
    #     ]
    # except Exception as e:
    #     suggestions = [{'message': f'AI error: {str(e)}'}]
    
    response = requests.post(
        'https://api.languagetool.org/v2/check',
        data={'text': text, 'language': 'en-US'}
    )
    
    if response.status_code == 200:
        data = response.json()
        suggestions = [
            {
                'message': match['message'],
                'offset': match['offset'],
                'length': match['length'],
                'suggestions': match['replacements']
            }
            for match in data.get('matches', [])
        ]
    else:
        suggestions = [{'message': 'Error connecting to grammar API'}]

    return JsonResponse({'suggestions': suggestions})


# 🔑 Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


# 🚪 Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
