from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=20)
    correo = forms.EmailField()
    motivo = forms.CharField(max_length=150)
    comentarios = forms.CharField(widget=forms.Textarea)