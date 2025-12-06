from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=255)  
    es_admin = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True) 
    fecha_actualizacion = models.DateTimeField(auto_now=True)  

    def save(self, *args, **kwargs):

        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Company(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Companies"


class Customer(models.Model):
    nombre = models.CharField(max_length=255)  
    fecha_nacimiento = models.DateField()
    
    empresa = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='clientes')
    representante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clientes')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Interaction(models.Model):
    TIPOS = [
        ('Call', 'Llamada'),
        ('Email', 'Correo'),
        ('SMS', 'SMS'),
        ('Facebook', 'Facebook'),
        ('WhatsApp', 'WhatsApp'),
        ('LinkedIn', 'LinkedIn'),
        ('Meeting', 'Reunión'),
        ('Video Call', 'Videollamada'),
    ]
    
    cliente = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interacciones')
    tipo = models.CharField(max_length=50, choices=TIPOS)
    fecha = models.DateTimeField()

    def __str__(self):
        return f"{self.tipo} con {self.cliente.nombre}"

    class Meta:
        ordering = ['-fecha']  
