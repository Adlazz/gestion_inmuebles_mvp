from .propietario import Propietario
from .inquilino import Inquilino
from .inmueble import Inmueble
from .contrato import Contrato
from .pago import Pago

# Inyectar las clases en el namespace de cada módulo para resolver forward references
import inmobiliaria.models.propietario as propietario_module
import inmobiliaria.models.inmueble as inmueble_module
import inmobiliaria.models.inquilino as inquilino_module
import inmobiliaria.models.contrato as contrato_module
import inmobiliaria.models.pago as pago_module

propietario_module.Inmueble = Inmueble
inmueble_module.Propietario = Propietario
inmueble_module.Contrato = Contrato
inquilino_module.Contrato = Contrato
contrato_module.Inmueble = Inmueble
contrato_module.Inquilino = Inquilino
contrato_module.Pago = Pago
pago_module.Contrato = Contrato

__all__ = ["Propietario", "Inquilino", "Inmueble", "Contrato", "Pago"]