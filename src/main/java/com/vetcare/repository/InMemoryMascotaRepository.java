package com.vetcare.repository;

import com.vetcare.Mascota;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicInteger;

public class InMemoryMascotaRepository implements MascotaRepository {
    private final List<Mascota> baseDeDatos = new ArrayList<>();
    private final AtomicInteger generadorId = new AtomicInteger(1);

    @Override
    public Mascota guardar(Mascota mascota) {
        if (mascota == null) {
            throw new IllegalArgumentException("No se puede guardar una mascota nula.");
        }
        if (mascota.getId() == null) {
            mascota.setId(generadorId.getAndIncrement());
        }
        baseDeDatos.add(mascota);
        return mascota;
    }

    @Override
    public List<Mascota> obtenerTodas() {
        return new ArrayList<>(baseDeDatos);
    }

    @Override
    public Optional<Mascota> buscarPorId(int id) {
        return baseDeDatos.stream()
                .filter(m -> m.getId() != null && m.getId() == id)
                .findFirst();
    }
}
