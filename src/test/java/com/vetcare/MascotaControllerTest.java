package com.vetcare;

import com.vetcare.controller.MascotaController;
import com.vetcare.dto.RegistrarMascotaDTO;
import com.vetcare.dto.RespuestaBackend;
import com.vetcare.repository.InMemoryMascotaRepository;
import com.vetcare.repository.MascotaRepository;
import com.vetcare.service.MascotaService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Pruebas Unitarias del Controlador de Backend: MascotaController")
class MascotaControllerTest {

    private MascotaController controller;

    @BeforeEach
    void setUp() {
        MascotaRepository repository = new InMemoryMascotaRepository();
        MascotaService service = new MascotaService(repository);
        controller = new MascotaController(service);
    }

    @Test
    @DisplayName("Debe responder con HTTP 201 Created al registrar exitosamente una mascota")
    void testRegistrarMascotaRetorna201Created() {
        RegistrarMascotaDTO dto = new RegistrarMascotaDTO("Thor", "Perro", 4);

        RespuestaBackend<Mascota> respuesta = controller.registrarMascota(dto);

        assertNotNull(respuesta);
        assertEquals(201, respuesta.getEstadoHttp());
        assertTrue(respuesta.esExitosa());
        assertNotNull(respuesta.getDatos());
        assertEquals("Thor", respuesta.getDatos().getNombre());
        assertEquals(1, respuesta.getDatos().getId());
        assertEquals("Mascota registrada exitosamente.", respuesta.getMensaje());
    }

    @Test
    @DisplayName("Debe responder con HTTP 400 Bad Request cuando los datos no cumplen las validaciones")
    void testRegistrarMascotaDatosInvalidosRetorna400BadRequest() {
        RegistrarMascotaDTO dtoInvalido = new RegistrarMascotaDTO("", "Gato", -2);

        RespuestaBackend<Mascota> respuesta = controller.registrarMascota(dtoInvalido);

        assertNotNull(respuesta);
        assertEquals(400, respuesta.getEstadoHttp());
        assertFalse(respuesta.esExitosa());
        assertNull(respuesta.getDatos());
        assertTrue(respuesta.getMensaje().contains("Error de validación: El nombre no puede estar vacío."));
    }

    @Test
    @DisplayName("Debe responder con HTTP 200 OK al solicitar el listado de mascotas")
    void testListarMascotasRetorna200Ok() {
        controller.registrarMascota(new RegistrarMascotaDTO("Pelusa", "Gato", 1));

        RespuestaBackend<List<Mascota>> respuesta = controller.listarMascotas();

        assertNotNull(respuesta);
        assertEquals(200, respuesta.getEstadoHttp());
        assertTrue(respuesta.esExitosa());
        assertEquals(1, respuesta.getDatos().size());
        assertEquals("Pelusa", respuesta.getDatos().get(0).getNombre());
    }
}
