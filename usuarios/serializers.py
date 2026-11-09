from rest_framework import serializers

from .forms import RegistroForm
from .models import DireccionEnvio


class RegistroClienteSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField(max_length=254)
    password1 = serializers.CharField(write_only=True, trim_whitespace=False, max_length=128)
    password2 = serializers.CharField(write_only=True, trim_whitespace=False, max_length=128)

    def validate(self, attrs):
        self.form = RegistroForm(attrs)
        if not self.form.is_valid():
            raise serializers.ValidationError(dict(self.form.errors))
        return attrs

    def create(self, validated_data):
        return self.form.guardar_cliente()


class DireccionEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DireccionEnvio
        fields = "__all__"
        read_only_fields = ["usuario"]
