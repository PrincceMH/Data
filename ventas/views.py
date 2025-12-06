from django.shortcuts import render
from django.db.models import Max, Subquery, OuterRef
from django.utils import timezone
from datetime import timedelta
from .models import Customer, Interaction


def lista_clientes(request):
    
    ultima_interaccion = Interaction.objects.filter(
        cliente=OuterRef('pk')
    ).order_by('-fecha')
    
    clientes = Customer.objects.select_related('empresa', 'representante').annotate(
        ultima_fecha=Subquery(ultima_interaccion.values('fecha')[:1]),
        ultimo_tipo=Subquery(ultima_interaccion.values('tipo')[:1])
    )
    
    # Filtro por nombre
    buscar = request.GET.get('buscar', '').strip()
    if buscar:
        clientes = clientes.filter(nombre__icontains=buscar)
    
    # Filtro por cumpleaños
    cumple_filtro = request.GET.get('cumple', '')
    hoy = timezone.now().date()
    
    if cumple_filtro == 'hoy':
        clientes = clientes.filter(fecha_nacimiento__month=hoy.month, fecha_nacimiento__day=hoy.day)
    elif cumple_filtro == 'semana':
        # Cumpleaños esta semana
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        ids = [c.id for c in clientes if inicio_semana <= c.fecha_nacimiento.replace(year=hoy.year) <= fin_semana]
        clientes = clientes.filter(id__in=ids)
    elif cumple_filtro == 'mes':
        clientes = clientes.filter(fecha_nacimiento__month=hoy.month)
    
    # Ordenamiento
    orden = request.GET.get('orden', 'nombre')
    direccion = request.GET.get('dir', 'asc')
    prefijo = '-' if direccion == 'desc' else ''
    
    if orden == 'nombre':
        clientes = clientes.order_by(f'{prefijo}nombre')
    elif orden == 'empresa':
        clientes = clientes.order_by(f'{prefijo}empresa__nombre')
    elif orden == 'cumple':
        clientes = clientes.order_by(f'{prefijo}fecha_nacimiento__month', f'{prefijo}fecha_nacimiento__day')
    elif orden == 'ultima':
        clientes = clientes.order_by(f'{prefijo}ultima_fecha')
    
    # Paginacion
    pagina = int(request.GET.get('p', 1))
    por_pagina = 50
    total = clientes.count()
    inicio = (pagina - 1) * por_pagina
    clientes = clientes[inicio:inicio + por_pagina]
    
    ahora = timezone.now()
    lista = []
    
    for c in clientes:
        # Calcula tiempo atrás de la última interaccion
        ultima = None
        if c.ultima_fecha:
            delta = ahora - c.ultima_fecha
            if delta.days == 0:
                tiempo = f"{delta.seconds // 3600}h ago" if delta.seconds >= 3600 else f"{delta.seconds // 60}m ago"
            elif delta.days == 1:
                tiempo = "1 day ago"
            elif delta.days < 30:
                tiempo = f"{delta.days} days ago"
            elif delta.days < 365:
                tiempo = f"{delta.days // 30} months ago"
            else:
                tiempo = f"{delta.days // 365} years ago"
            ultima = f"{tiempo} ({c.ultimo_tipo})"
        

        cumple = c.fecha_nacimiento.strftime("%B %d").replace(" 0", " ")
        
        lista.append({
            'nombre': c.nombre,
            'empresa': c.empresa.nombre,
            'cumple': cumple,
            'ultima': ultima,
            'representante': c.representante.nombre
        })
    
    return render(request, 'ventas/clientes.html', {
        'clientes': lista,
        'buscar': buscar,
        'cumple_filtro': cumple_filtro,
        'orden': orden,
        'direccion': direccion,
        'pagina': pagina,
        'total_paginas': (total + por_pagina - 1) // por_pagina,
        'total': total
    })
