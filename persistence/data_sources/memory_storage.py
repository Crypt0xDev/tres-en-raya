"""
Memory Storage - Almacenamiento en memoria para el juego.

Implementa un almacenamiento en memoria simple para datos del juego.
Este es un adaptador de infraestructura que implementa persistencia temporal.
"""

from typing import Dict, Optional, Any, List
import threading


class MemoryStorage:
    """
    Almacenamiento en memoria thread-safe.
    
    Proporciona operaciones básicas de almacenamiento usando
    diccionarios Python en memoria con protección de hilos.
    
    Principios aplicados:
    - Es INFRAESTRUCTURA, no dominio
    - Implementa persistencia temporal
    - Thread-safe para aplicaciones web
    """
    
    def __init__(self):
        """Inicializa el almacenamiento en memoria."""
        self._data: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
    
    def save(self, collection: str, key: str, data: Dict[str, Any]) -> bool:
        """
        Guarda datos en la colección especificada.
        
        Args:
            collection: Nombre de la colección
            key: Clave única del elemento
            data: Datos a guardar
            
        Returns:
            True si se guardó exitosamente
        """
        with self._lock:
            if collection not in self._data:
                self._data[collection] = {}
            
            self._data[collection][key] = data.copy()
            return True
    
    def get(self, collection: str, key: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene datos por clave de una colección.
        
        Args:
            collection: Nombre de la colección
            key: Clave del elemento
            
        Returns:
            Datos encontrados o None si no existe
        """
        with self._lock:
            if collection not in self._data:
                return None
            
            data = self._data[collection].get(key)
            return data.copy() if data else None
    
    def get_all(self, collection: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los elementos de una colección.
        
        Args:
            collection: Nombre de la colección
            
        Returns:
            Lista de todos los elementos
        """
        with self._lock:
            if collection not in self._data:
                return []
            
            return [data.copy() for data in self._data[collection].values()]
    
    def exists(self, collection: str, key: str) -> bool:
        """
        Verifica si existe un elemento.
        
        Args:
            collection: Nombre de la colección
            key: Clave del elemento
            
        Returns:
            True si el elemento existe
        """
        with self._lock:
            return (
                collection in self._data and 
                key in self._data[collection]
            )
    
    def delete(self, collection: str, key: str) -> bool:
        """
        Elimina un elemento.
        
        Args:
            collection: Nombre de la colección
            key: Clave del elemento
            
        Returns:
            True si se eliminó (existía)
        """
        with self._lock:
            if collection not in self._data:
                return False
            
            if key in self._data[collection]:
                del self._data[collection][key]
                return True
            
            return False
    
    def clear(self, collection: Optional[str] = None) -> None:
        """
        Limpia una colección o todo el almacenamiento.
        
        Args:
            collection: Colección a limpiar (None para limpiar todo)
        """
        with self._lock:
            if collection is None:
                self._data.clear()
            elif collection in self._data:
                self._data[collection].clear()
    
    def count(self, collection: str) -> int:
        """
        Cuenta elementos en una colección.
        
        Args:
            collection: Nombre de la colección
            
        Returns:
            Número de elementos
        """
        with self._lock:
            if collection not in self._data:
                return 0
            
            return len(self._data[collection])
    
    def get_collections(self) -> List[str]:
        """
        Obtiene lista de colecciones existentes.
        
        Returns:
            Lista de nombres de colecciones
        """
        with self._lock:
            return list(self._data.keys())
    
    def find_by(self, collection: str, **criteria) -> List[Dict[str, Any]]:
        """
        Busca elementos que cumplan criterios.
        
        Args:
            collection: Nombre de la colección
            **criteria: Criterios de búsqueda (clave=valor)
            
        Returns:
            Lista de elementos que cumplen los criterios
        """
        with self._lock:
            if collection not in self._data:
                return []
            
            results = []
            for data in self._data[collection].values():
                match = True
                for key, value in criteria.items():
                    if data.get(key) != value:
                        match = False
                        break
                
                if match:
                    results.append(data.copy())
            
            return results