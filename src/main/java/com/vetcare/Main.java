package com.vetcare;

import com.vetcare.controller.MascotaController;
import com.vetcare.dto.RegistrarMascotaDTO;
import com.vetcare.dto.RespuestaBackend;
import com.vetcare.repository.InMemoryMascotaRepository;
import com.vetcare.repository.MascotaRepository;
import com.vetcare.service.MascotaService;
import com.vetcare.ui.VetCareGUI;

import java.awt.GraphicsEnvironment;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        // Inicialización de la arquitectura en capas del Backend
        MascotaRepository repository = new InMemoryMascotaRepository();
        MascotaService service = new MascotaService(repository);
        MascotaController controller = new MascotaController(service);

        boolean modoConsola = Arrays.asList(args).contains("--cli") || GraphicsEnvironment.isHeadless();

        if (!modoConsola) {
            System.out.println("Iniciando interfaz gráfica de VetCare (use --cli para modo consola)...");
            VetCareGUI.iniciarInterfaz(controller);
            return;
        }

        iniciarModoConsola(controller);
    }

    public static void iniciarModoConsola(MascotaController controller) {
        Scanner scanner = new Scanner(System.in);
        boolean salir = false;

        System.out.println("==========================================");
        System.out.println("   VetCare - Arquitectura Frontend/Backend");
        System.out.println("==========================================");

        while (!salir) {
            System.out.println("\nSeleccione una opción:");
            System.out.println("1. Registrar mascota (POST /api/mascotas)");
            System.out.println("2. Listar mascotas   (GET  /api/mascotas)");
            System.out.println("3. Salir");
            System.out.print("Opción: ");

            String opcion = scanner.nextLine().trim();

            switch (opcion) {
                case "1":
                    registrarMascotaCLI(controller, scanner);
                    break;
                case "2":
                    listarMascotasCLI(controller);
                    break;
                case "3":
                    salir = true;
                    System.out.println("¡Gracias por utilizar VetCare!");
                    break;
                default:
                    System.out.println("Opción no válida. Por favor, ingrese 1, 2 o 3.");
            }
        }

        scanner.close();
    }

    private static void registrarMascotaCLI(MascotaController controller, Scanner scanner) {
        System.out.println("\n--- [Frontend] Formulario de Registro de Mascota ---");
        System.out.print("Ingrese el nombre de la mascota: ");
        String nombre = scanner.nextLine();

        System.out.print("Ingrese la especie: ");
        String especie = scanner.nextLine();

        System.out.print("Ingrese la edad: ");
        String edadInput = scanner.nextLine();

        int edad;
        try {
            edad = Integer.parseInt(edadInput.trim());
        } catch (NumberFormatException e) {
            System.out.println("[Frontend Error] La edad debe ser un número entero.");
            return;
        }

        // El Frontend empaqueta los datos en un DTO para enviar al Backend
        RegistrarMascotaDTO dto = new RegistrarMascotaDTO(nombre, especie, edad);

        // Envío de la petición al Controller del Backend
        RespuestaBackend<Mascota> respuesta = controller.registrarMascota(dto);

        // El Frontend interpreta la respuesta HTTP devuelta por el Backend
        if (respuesta.esExitosa()) {
            Mascota m = respuesta.getDatos();
            System.out.printf("[Backend HTTP %d CREATED] %s%n", respuesta.getEstadoHttp(), respuesta.getMensaje());
            System.out.printf("   -> ID: #%d | Nombre: %s | Especie: %s | Edad: %d años%n",
                    m.getId(), m.getNombre(), m.getEspecie(), m.getEdad());
        } else {
            System.out.printf("[Backend HTTP %d BAD REQUEST] %s%n", respuesta.getEstadoHttp(), respuesta.getMensaje());
        }
    }

    private static void listarMascotasCLI(MascotaController controller) {
        System.out.println("\n--- [Frontend] Consulta de Mascotas Registradas ---");
        RespuestaBackend<List<Mascota>> respuesta = controller.listarMascotas();

        if (respuesta.esExitosa()) {
            List<Mascota> lista = respuesta.getDatos();
            System.out.printf("[Backend HTTP %d OK] %s%n", respuesta.getEstadoHttp(), respuesta.getMensaje());
            if (lista.isEmpty()) {
                System.out.println("No hay mascotas registradas hasta el momento.");
            } else {
                for (Mascota m : lista) {
                    System.out.printf("   #%d - Nombre: %-10s | Especie: %-10s | Edad: %d años%n",
                            m.getId(), m.getNombre(), m.getEspecie(), m.getEdad());
                }
            }
        } else {
            System.out.printf("[Backend HTTP %d ERROR] %s%n", respuesta.getEstadoHttp(), respuesta.getMensaje());
        }
    }
}
