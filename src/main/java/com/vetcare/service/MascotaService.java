package com.vetcare.service;

import com.vetcare.Mascota;
import com.vetcare.dto.RegistrarMascotaDTO;
import com.vetcare.repository.MascotaRepository;
import java.util.List;

public class MascotaService {
    private final MascotaRepository mascotaRepository;

    public MascotaService(MascotaRepository mascotaRepository) {
        if (mascotaRepository == null) {
            throw new IllegalArgumentException("El repositorio de mascotas no puede ser nulo.");
        }
        this.mascotaRepository = mascotaRepository;
    }

    /**
     * Aplica las reglas de validación de negocio y registra la mascota.
     */
    public Mascota registrarMascota(RegistrarMascotaDTO dto) {
        if (dto == null) {
            throw new IllegalArgumentException("Los datos de la mascota no pueden ser nulos.");
        }

        // Validación de reglas de negocio
        if (dto.getNombre() == null || dto.getNombre().trim().isEmpty()) {
            throw new IllegalArgumentException("El nombre no puede estar vacío.");
        }
        if (dto.getEspecie() == null || dto.getEspecie().trim().isEmpty()) {
            throw new IllegalArgumentException("La especie no puede estar vacía.");
        }
        if (dto.getEdad() < 0) {
            throw new IllegalArgumentException("La edad no puede ser negativa.");
        }

        // Creación del objeto de dominio con datos limpios
        Mascota nuevaMascota = new Mascota(dto.getNombre().trim(), dto.getEspecie().trim(), dto.getEdad());

        // Delegación de la persistencia a la capa Repository
        return mascotaRepository.guardar(nuevaMascota);
    }

    public List<Mascota> listarMascotas() {
        return mascotaRepository.obtenerTodas();
    }
}
