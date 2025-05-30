import datetime
import hashlib

"""
Implementación básica de una blockchain (cadena de bloques)
Esta clase crea una cadena de bloques simple con las siguientes características:
- Inicializa una cadena con un bloque génesis
- Genera bloques adicionales mediante prueba de trabajo (PoW)
- Utiliza SHA-256 para el hash de los bloques
- Define una dificultad de minado con un prefijo de '000'
Atributos:
    DIFFICULTY_PREFIX (str): Prefijo de dificultad para el minado ('000')
    chain (list): Lista de bloques que forman la cadena
El proceso de minado:
1. Toma el bloque anterior y su prueba
2. Busca una nueva prueba que genere un hash con el prefijo requerido
3. Crea un nuevo bloque con:
- Índice incremental
- Marca de tiempo actual
- Nueva prueba calculada
- Hash del bloque anterior
La cadena se inicializa con 3 bloques 
por defecto, incluyendo el bloque génesis.

"""
class blockchain:
    
    def __init__(self):
        self.DIFFICULTY_PREFIX = '000'
        self.chain = []
        
        # Initialize first block
        self.chain.append({
            'index': 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': 1,
            'previous_hash': '0'
        })
        
        # Mine subsequent blocks
        while len(self.chain) < 3:  # Example: Create 3 blocks
            prev_block = self.chain[-1]
            prev_proof = prev_block['proof']
            
            new_proof = 1
            # Mine new block
            while hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()[:4] != self.DIFFICULTY_PREFIX:
                new_proof += 1
            
            new_hash = hashlib.sha256(str(prev_block).encode()).hexdigest()
            
            # Add new block
            self.chain.append({
                'index': len(self.chain) + 1,
                'timestamp': str(datetime.datetime.now()),
                'proof': new_proof,
                'previous_hash': new_hash
            })
