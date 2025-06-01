class RecursosUsuario:
    
    def __init__(self, porcentaje_cpu, porcentaje_ancho_banda, recursos_comunitarios=None):
        self.porcentaje_cpu = porcentaje_cpu
        self.porcentaje_ancho_banda = porcentaje_ancho_banda
        
        if recursos_comunitarios:
            self.recursos_asignados = {
                'cpu': recursos_comunitarios['cpu'] * (self.porcentaje_cpu / 100),
                'ancho_banda': recursos_comunitarios['ancho_banda'] * (self.porcentaje_ancho_banda / 100),
            }
        else:
            self.recursos_asignados = None

class MonitoreoRecursos:

    
    def __init__(self):
        """Initialize the resource monitoring system"""
        self.recursos_usuarios = {}
        print("Recursos inicializados")
        
    def gestionar_recursos(self, nombre_usuario=None, uso_cpu=None, uso_ancho_banda=None):
        """
        Manage system resources efficiently.
        
        Args:
            nombre_usuario (str, optional): Username to update resources
            uso_cpu (float, optional): CPU usage percentage 
            uso_ancho_banda (float, optional): Bandwidth usage percentage
            
        Returns:
            dict: Current resource usage for all users
        """
        # Update resources if all parameters are provided
        if all([nombre_usuario, uso_cpu, uso_ancho_banda]):
            self.recursos_usuarios[nombre_usuario] = {
                'uso_cpu': uso_cpu,
                'uso_ancho_banda': uso_ancho_banda
            }
            
        return self.recursos_usuarios
        # Assign the inner function to the instance
# This line was removed as it was unreachable code after the return statement
