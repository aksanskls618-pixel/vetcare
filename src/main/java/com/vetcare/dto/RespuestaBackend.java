package com.vetcare.dto;

public class RespuestaBackend<T> {
    private int estadoHttp;
    private String mensaje;
    private T datos;

    public RespuestaBackend() {
    }

    public RespuestaBackend(int estadoHttp, String mensaje, T datos) {
        this.estadoHttp = estadoHttp;
        this.mensaje = mensaje;
        this.datos = datos;
    }

    public static <T> RespuestaBackend<T> creada(String mensaje, T datos) {
        return new RespuestaBackend<>(201, mensaje, datos);
    }

    public static <T> RespuestaBackend<T> ok(String mensaje, T datos) {
        return new RespuestaBackend<>(200, mensaje, datos);
    }

    public static <T> RespuestaBackend<T> error(int estadoHttp, String mensaje) {
        return new RespuestaBackend<>(estadoHttp, mensaje, null);
    }

    public int getEstadoHttp() {
        return estadoHttp;
    }

    public void setEstadoHttp(int estadoHttp) {
        this.estadoHttp = estadoHttp;
    }

    public String getMensaje() {
        return mensaje;
    }

    public void setMensaje(String mensaje) {
        this.mensaje = mensaje;
    }

    public T getDatos() {
        return datos;
    }

    public void setDatos(T datos) {
        this.datos = datos;
    }

    public boolean esExitosa() {
        return estadoHttp >= 200 && estadoHttp < 300;
    }

    @Override
    public String toString() {
        return "RespuestaBackend{" +
                "estadoHttp=" + estadoHttp +
                ", mensaje='" + mensaje + '\'' +
                ", datos=" + datos +
                '}';
    }
}
