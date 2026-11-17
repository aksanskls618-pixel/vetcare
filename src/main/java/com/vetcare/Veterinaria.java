package com.vetcare;

import com.vetcare.dto.RegistrarMascotaDTO;
import com.vetcare.repository.InMemoryMascotaRepository;
import com.vetcare.repository.MascotaRepository;
import com.vetcare.service.MascotaService;

import java.util.List;

public class Veterinaria {
    private final MascotaService mascotaService;

    public Veterinaria() {
        MascotaRepository repository = new InMemoryMascotaRepository();
        this.mascotaService = new MascotaService(repository);
    }

    public Veterinaria(MascotaService mascotaService) {
        this.mascotaService = mascotaService;
    }

    /**
     * Registra una nueva mascota en el sistema.
     * En esta versión refactorizada, delega la validación y persistencia a MascotaService,
     * manteniendo total compatibilidad con el contrato público existente.
     */
    public Mascota registrarMascota(String nombre, String especie, int edad) {
        return mascotaService.registrarMascota(new RegistrarMascotaDTO(nombre, especie, edad));
    }

    public List<Mascota> getMascotas() {
        return mascotaService.listarMascotas();
    }
}
