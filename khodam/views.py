import base64
import os
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import khodam


# Create your views here.
@ensure_csrf_cookie  # Memastikan CSRF cookie di-set
def index(request):
    khodam_terpilih = None
    nama = request.POST.get('nama')
    if request.method == 'POST':
        semua_khodam = list(khodam.objects.all())
        khodam_terpilih = random.choice(semua_khodam) if semua_khodam else None
        if khodam_terpilih:
            return JsonResponse({'khodam_terpilih': {'namaKhodam': khodam_terpilih.namaKhodam}, 'nama': nama})
        else:
            return JsonResponse({'error': 'Tidak ada khodam yang tersedia'}, status=404)
    return render(request, 'khodam/index.html')


@ensure_csrf_cookie
def adu_khodam(request):
    khodam_kanan = None
    khodam_kiri = None
    nama_kiri = request.POST.get('namaKiri')
    nama_kanan = request.POST.get('namaKanan')
    if request.method == 'POST':
        semua_khodam = list(khodam.objects.all())
        khodam_kiri = random.choice(semua_khodam)
        khodam_kanan = random.choice(semua_khodam)
        k_khodam_kanan = khodam_kanan.kekuatanKhodam
        k_khodam_kiri = khodam_kiri.kekuatanKhodam
        if k_khodam_kanan > k_khodam_kiri:
            return JsonResponse({
                'pemenang_nama': nama_kanan,
                'pemenang_khodam': khodam_kanan.namaKhodam,
                'khodam_kanan': khodam_kanan.namaKhodam,
                'khodam_kiri': khodam_kiri.namaKhodam
            })
        elif k_khodam_kiri > k_khodam_kanan:
            return JsonResponse({
                'pemenang_nama': nama_kiri,
                'pemenang_khodam': khodam_kiri.namaKhodam,
                'khodam_kanan': khodam_kanan.namaKhodam,
                'khodam_kiri': khodam_kiri.namaKhodam
            })
        else:
            return JsonResponse({
                'pemenang': 'Seri',
                'khodam_kanan': khodam_kanan.namaKhodam,
                'khodam_kiri': khodam_kiri.namaKhodam
            })
    return render(request, 'khodam/adu_khodam.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('crud')
        else:
            return HttpResponse("Invalid login details")
    return render(request, 'khodam/login.html')


@login_required(login_url='login')
def crud_view(request):
    all_khodams = khodam.objects.all()
    return render(request, 'khodam/crud.html', {'khodams': all_khodams})

def create_khodam(request):
    if request.method == 'POST':
        nama = request.POST.get('namaKhodam')
        kekuatan = request.POST.get('kekuatanKhodam')
        new_khodam = khodam(namaKhodam=nama, kekuatanKhodam=int(kekuatan))
        new_khodam.save()
        return redirect('crud')
    return render(request, 'khodam/crud.html')

def update_khodam(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    khodam_obj = get_object_or_404(khodam, id=id)
    if request.method == 'POST':
        nama = request.POST.get('namaKhodam')
        kekuatan = request.POST.get('kekuatanKhodam')
        khodam_obj.namaKhodam = nama
        khodam_obj.kekuatanKhodam = int(kekuatan)
        khodam_obj.save()
        return redirect('crud')
    return render(request, 'khodam/crud.html', {'khodam': khodam_obj})

def delete_khodam(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    khodam_obj = get_object_or_404(khodam, id=id)
    if request.method == 'POST':
        khodam_obj.delete()
        return redirect('crud')
    return render(request, 'khodam/crud.html', {'khodam': khodam_obj})

def logout_view(request):
    logout(request)
    return redirect('login')

