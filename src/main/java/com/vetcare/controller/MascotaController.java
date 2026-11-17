package com.vetcare.controller;

import com.vetcare.Mascota;
import com.vetcare.dto.RegistrarMascotaDTO;
import com.vetcare.dto.RespuestaBackend;
import com.vetcare.service.MascotaService;
import java.util.List;

public class MascotaController {
    private final MascotaService mascotaService;

    public MascotaController(MascotaService mascotaService) {
        if (mascotaService == null) {
            throw new IllegalArgumentException("El servicio de mascotas no puede ser nulo.");
        }
        this.mascotaService = mascotaService;
    }

    /**
     * Endpoint simulado: POST /api/mascotas
     * Recibe los datos de registro (DTO), procesa a través del Service y retorna una respuesta HTTP estructurada.
     */
    public RespuestaBackend<Mascota> registrarMascota(RegistrarMascotaDTO dto) {
        try {
            Mascota mascotaCreada = mascotaService.registrarMascota(dto);
            return RespuestaBackend.creada("Mascota registrada exitosamente.", mascotaCreada);
        } catch (IllegalArgumentException e) {
            return RespuestaBackend.error(400, "Error de validación: " + e.getMessage());
        } catch (Exception e) {
            return RespuestaBackend.error(500, "Error interno del servidor: " + e.getMessage());
        }
    }

    /**
     * Endpoint simulado: GET /api/mascotas
     * Retorna la lista de todas las mascotas registradas.
     */
    public RespuestaBackend<List<Mascota>> listarMascotas() {
        try {
            List<Mascota> lista = mascotaService.listarMascotas();
            return RespuestaBackend.ok("Lista de mascotas obtenida exitosamente.", lista);
        } catch (Exception e) {
            return RespuestaBackend.error(500, "Error interno del servidor: " + e.getMessage());
        }
    }
}
