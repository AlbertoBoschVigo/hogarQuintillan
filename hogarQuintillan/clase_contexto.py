class contextoBase():
    def __init__(self, **kwargs):
        topHeader = [
            ('calendarioGlobal', 'Calendario'),
            ('chat_index', 'Chat'),
            ('recetas_index', 'Recetas'),
            ('memos:list', 'Memos'),
            ('vera_tareas', 'TareasV')
        ]
        rutaInicio = ('index', 'Inicio')
        self.contextoBase = {
            'topHeader': topHeader,
            'inicio': rutaInicio,
            'pageTitle':'Hogar Quintillan'
        }
        self.add(**kwargs)
    
    def add(self, **kwargs):
        for k,v in kwargs.items():
            self.contextoBase[k] = v
    
    def get(self):
        return self.contextoBase