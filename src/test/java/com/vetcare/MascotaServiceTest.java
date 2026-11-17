package com.vetcare;

import com.vetcare.dto.RegistrarMascotaDTO;
import com.vetcare.repository.InMemoryMascotaRepository;
import com.vetcare.repository.MascotaRepository;
import com.vetcare.service.MascotaService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Pruebas Unitarias del Servicio de Backend: MascotaService")
class MascotaServiceTest {

    private MascotaRepository repository;
    private MascotaService service;

    @BeforeEach
    void setUp() {
        repository = new InMemoryMascotaRepository();
        service = new MascotaService(repository);
    }

    @Test
    @DisplayName("Debe registrar exitosamente una mascota con datos válidos")
    void testRegistrarMascotaExitosa() {
        RegistrarMascotaDTO dto = new RegistrarMascotaDTO("Milo", "Perro", 3);

        Mascota resultado = service.registrarMascota(dto);

        assertNotNull(resultado);
        assertNotNull(resultado.getId(), "El ID autoincremental debe ser asignado por el repositorio");
        assertEquals(1, resultado.getId());
        assertEquals("Milo", resultado.getNombre());
        assertEquals("Perro", resultado.getEspecie());
        assertEquals(3, resultado.getEdad());
        assertEquals(1, service.listarMascotas().size());
    }

    @Test
    @DisplayName("Debe registrar válidamente una mascota con edad 0 (cachorro o recién nacido)")
    void testRegistrarMascotaConEdadCeroEsValido() {
        RegistrarMascotaDTO dto = new RegistrarMascotaDTO("Copito", "Gato", 0);

        Mascota resultado = service.registrarMascota(dto);

        assertNotNull(resultado);
        assertEquals(0, resultado.getEdad());
    }

    @Test
    @DisplayName("Debe lanzar excepción cuando el nombre es nulo o está en blanco")
    void testRegistrarMascotaNombreInvalido() {
        RegistrarMascotaDTO dtoNulo = new RegistrarMascotaDTO(null, "Perro", 2);
        RegistrarMascotaDTO dtoVacio = new RegistrarMascotaDTO("   ", "Perro", 2);

        IllegalArgumentException exNulo = assertThrows(IllegalArgumentException.class, () -> service.registrarMascota(dtoNulo));
        assertEquals("El nombre no puede estar vacío.", exNulo.getMessage());

        IllegalArgumentException exVacio = assertThrows(IllegalArgumentException.class, () -> service.registrarMascota(dtoVacio));
        assertEquals("El nombre no puede estar vacío.", exVacio.getMessage());
    }

    @Test
    @DisplayName("Debe lanzar excepción cuando la especie es nula o está en blanco")
    void testRegistrarMascotaEspecieInvalida() {
        RegistrarMascotaDTO dtoNulo = new RegistrarMascotaDTO("Luna", null, 2);
        RegistrarMascotaDTO dtoVacio = new RegistrarMascotaDTO("Luna", "  ", 2);

        IllegalArgumentException exNulo = assertThrows(IllegalArgumentException.class, () -> service.registrarMascota(dtoNulo));
        assertEquals("La especie no puede estar vacía.", exNulo.getMessage());

        IllegalArgumentException exVacio = assertThrows(IllegalArgumentException.class, () -> service.registrarMascota(dtoVacio));
        assertEquals("La especie no puede estar vacía.", exVacio.getMessage());
    }

    @Test
    @DisplayName("Debe lanzar excepción cuando la edad es un número negativo")
    void testRegistrarMascotaEdadNegativaInvalida() {
        RegistrarMascotaDTO dtoNegativo = new RegistrarMascotaDTO("Simba", "Felino", -1);

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> service.registrarMascota(dtoNegativo));
        assertEquals("La edad no puede ser negativa.", ex.getMessage());
    }

    @Test
    @DisplayName("Debe lanzar excepción cuando el DTO de datos es nulo")
    void testRegistrarMascotaDtoNulo() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> service.registrarMascota(null));
        assertEquals("Los datos de la mascota no pueden ser nulos.", ex.getMessage());
    }
}
