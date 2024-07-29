from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentForm

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.profile = request.user.profile
            document.save()
            return redirect('documents')
    else:
        form = DocumentForm()
    return render(request, 'documents.html', {'form': form})
