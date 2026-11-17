package com.vetcare.repository;

import com.vetcare.Mascota;
import java.util.List;
import java.util.Optional;

public interface MascotaRepository {
    Mascota guardar(Mascota mascota);
    List<Mascota> obtenerTodas();
    Optional<Mascota> buscarPorId(int id);
}
