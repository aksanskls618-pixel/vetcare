package com.vetcare;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Pruebas Unitarias de compatibilidad: Veterinaria")
class VeterinariaTest {

    private Veterinaria veterinaria;

    @BeforeEach
    void setUp() {
        veterinaria = new Veterinaria();
    }

    @Test
    @DisplayName("Debe registrar mascota y devolverla en la lista")
    void testRegistrarMascotaYListar() {
        Mascota m = veterinaria.registrarMascota("Bobby", "Perro", 5);

        assertNotNull(m);
        assertEquals("Bobby", m.getNombre());
        List<Mascota> lista = veterinaria.getMascotas();
        assertEquals(1, lista.size());
        assertEquals("Bobby", lista.get(0).getNombre());
    }

    @Test
    @DisplayName("Debe lanzar excepción al ingresar datos inválidos a través de Veterinaria")
    void testRegistrarMascotaInvalidaLanzaExcepcion() {
        assertThrows(IllegalArgumentException.class, () -> veterinaria.registrarMascota("", "Perro", 2));
        assertThrows(IllegalArgumentException.class, () -> veterinaria.registrarMascota("Bobby", "", 2));
        assertThrows(IllegalArgumentException.class, () -> veterinaria.registrarMascota("Bobby", "Perro", -1));
    }
}
