package com.vetcare.ui;

import com.vetcare.Mascota;
import com.vetcare.controller.MascotaController;
import com.vetcare.dto.RegistrarMascotaDTO;
import com.vetcare.dto.RespuestaBackend;
import com.vetcare.repository.InMemoryMascotaRepository;
import com.vetcare.repository.MascotaRepository;
import com.vetcare.service.MascotaService;

import javax.swing.*;
import javax.swing.border.CompoundBorder;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.JTableHeader;
import java.awt.*;
import java.util.List;

/**
 * Interfaz gráfica de usuario (Swing) para VetCare.
 * Se comunica exclusivamente con MascotaController respetando la arquitectura en capas.
 */
public class VetCareGUI extends JFrame {

    private final MascotaController controller;

    // Paleta de colores estilo clínica veterinaria moderna
    private static final Color COLOR_PRIMARIO = new Color(15, 118, 110);     // Teal oscuro
    private static final Color COLOR_PRIMARIO_HOVER = new Color(13, 148, 136); // Teal medio
    private static final Color COLOR_FONDO = new Color(241, 245, 249);        // Gris azulado muy claro
    private static final Color COLOR_TARJETA = Color.WHITE;
    private static final Color COLOR_TEXTO = new Color(30, 41, 59);
    private static final Color COLOR_TEXTO_SEC = new Color(100, 116, 139);
    private static final Color COLOR_BORDE = new Color(203, 213, 225);

    // Colores para barra de estado HTTP
    private static final Color BG_EXITO = new Color(220, 252, 231);
    private static final Color TXT_EXITO = new Color(22, 101, 52);
    private static final Color BG_ERROR = new Color(254, 226, 226);
    private static final Color TXT_ERROR = new Color(153, 27, 27);
    private static final Color BG_INFO = new Color(224, 242, 254);
    private static final Color TXT_INFO = new Color(7, 89, 133);

    private JTextField txtNombre;
    private JTextField txtEspecie;
    private JTextField txtEdad;
    private JLabel lblEstadoBackend;
    private JPanel panelEstadoBackend;
    private JLabel lblContador;
    private DefaultTableModel modeloTabla;

    public VetCareGUI(MascotaController controller) {
        if (controller == null) {
            throw new IllegalArgumentException("El controlador no puede ser nulo.");
        }
        this.controller = controller;
        configurarVentana();
        inicializarComponentes();
        actualizarTablaMascotas(false);
    }

    private void configurarVentana() {
        setTitle("VetCare - Gestión de Clínica Veterinaria");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(880, 560);
        setMinimumSize(new Dimension(780, 480));
        setLocationRelativeTo(null);
        getContentPane().setBackground(COLOR_FONDO);
        setLayout(new BorderLayout(0, 0));
    }

    private void inicializarComponentes() {
        // 1. Encabezado superior
        add(crearEncabezado(), BorderLayout.NORTH);

        // 2. Contenedor central (Formulario a la izquierda + Tabla a la derecha)
        JPanel panelCentral = new JPanel(new BorderLayout(20, 0));
        panelCentral.setBackground(COLOR_FONDO);
        panelCentral.setBorder(new EmptyBorder(20, 24, 16, 24));

        panelCentral.add(crearPanelFormulario(), BorderLayout.WEST);
        panelCentral.add(crearPanelTabla(), BorderLayout.CENTER);

        add(panelCentral, BorderLayout.CENTER);

        // 3. Barra inferior de respuesta del Backend (simulando estado HTTP)
        add(crearBarraEstado(), BorderLayout.SOUTH);
    }

    private JPanel crearEncabezado() {
        JPanel header = new JPanel(new BorderLayout());
        header.setBackground(COLOR_PRIMARIO);
        header.setBorder(new EmptyBorder(16, 24, 16, 24));

        JPanel panelTitulos = new JPanel();
        panelTitulos.setLayout(new BoxLayout(panelTitulos, BoxLayout.Y_AXIS));
        panelTitulos.setOpaque(false);

        JLabel lblTitulo = new JLabel("\uD83D\uDC3E VetCare");
        lblTitulo.setFont(new Font("Segoe UI", Font.BOLD, 24));
        lblTitulo.setForeground(Color.WHITE);

        JLabel lblSubtitulo = new JLabel("Sistema de Registro y Consulta de Pacientes Veterinarios");
        lblSubtitulo.setFont(new Font("Segoe UI", Font.PLAIN, 13));
        lblSubtitulo.setForeground(new Color(204, 251, 241));

        panelTitulos.add(lblTitulo);
        panelTitulos.add(Box.createVerticalStrut(3));
        panelTitulos.add(lblSubtitulo);

        lblContador = new JLabel("0 mascotas registradas");
        lblContador.setFont(new Font("Segoe UI", Font.BOLD, 13));
        lblContador.setForeground(COLOR_PRIMARIO);
        lblContador.setOpaque(true);
        lblContador.setBackground(new Color(204, 251, 241));
        lblContador.setBorder(new EmptyBorder(6, 14, 6, 14));

        JPanel panelDerecho = new JPanel(new GridBagLayout());
        panelDerecho.setOpaque(false);
        panelDerecho.add(lblContador);

        header.add(panelTitulos, BorderLayout.WEST);
        header.add(panelDerecho, BorderLayout.EAST);

        return header;
    }

    private JPanel crearPanelFormulario() {
        JPanel tarjeta = new JPanel(new BorderLayout());
        tarjeta.setBackground(COLOR_TARJETA);
        tarjeta.setPreferredSize(new Dimension(310, 0));
        tarjeta.setBorder(new CompoundBorder(
                new LineBorder(COLOR_BORDE, 1, true),
                new EmptyBorder(20, 20, 20, 20)
        ));

        JPanel contenido = new JPanel();
        contenido.setLayout(new BoxLayout(contenido, BoxLayout.Y_AXIS));
        contenido.setBackground(COLOR_TARJETA);

        JLabel lblTituloForm = new JLabel("Registrar Nueva Mascota");
        lblTituloForm.setFont(new Font("Segoe UI", Font.BOLD, 16));
        lblTituloForm.setForeground(COLOR_TEXTO);
        lblTituloForm.setAlignmentX(Component.LEFT_ALIGNMENT);

        JLabel lblDescForm = new JLabel("Complete los datos para dar de alta al paciente.");
        lblDescForm.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        lblDescForm.setForeground(COLOR_TEXTO_SEC);
        lblDescForm.setAlignmentX(Component.LEFT_ALIGNMENT);

        contenido.add(lblTituloForm);
        contenido.add(Box.createVerticalStrut(4));
        contenido.add(lblDescForm);
        contenido.add(Box.createVerticalStrut(18));

        // Campo Nombre
        contenido.add(crearEtiquetaCampo("Nombre de la mascota *"));
        contenido.add(Box.createVerticalStrut(5));
        txtNombre = crearCampoTexto("Ej: Firulais, Michi...");
        contenido.add(txtNombre);
        contenido.add(Box.createVerticalStrut(14));

        // Campo Especie
        contenido.add(crearEtiquetaCampo("Especie *"));
        contenido.add(Box.createVerticalStrut(5));
        txtEspecie = crearCampoTexto("Ej: Perro, Gato, Conejo...");
        contenido.add(txtEspecie);

        // Botones rápidos de especie para facilitar la carga
        JPanel panelSugerencias = new JPanel(new FlowLayout(FlowLayout.LEFT, 6, 4));
        panelSugerencias.setBackground(COLOR_TARJETA);
        panelSugerencias.setAlignmentX(Component.LEFT_ALIGNMENT);
        for (String esp : new String[]{"Perro", "Gato", "Ave", "Conejo"}) {
            JButton btnChip = new JButton(esp);
            btnChip.setFont(new Font("Segoe UI", Font.PLAIN, 11));
            btnChip.setFocusPainted(false);
            btnChip.setBackground(new Color(241, 245, 249));
            btnChip.setForeground(COLOR_TEXTO);
            btnChip.setBorder(new CompoundBorder(
                    new LineBorder(COLOR_BORDE, 1, true),
                    new EmptyBorder(2, 8, 2, 8)
            ));
            btnChip.setCursor(new Cursor(Cursor.HAND_CURSOR));
            btnChip.addActionListener(e -> txtEspecie.setText(esp));
            panelSugerencias.add(btnChip);
        }
        contenido.add(panelSugerencias);
        contenido.add(Box.createVerticalStrut(10));

        // Campo Edad
        contenido.add(crearEtiquetaCampo("Edad (en años, 0 para cachorros) *"));
        contenido.add(Box.createVerticalStrut(5));
        txtEdad = crearCampoTexto("Ej: 0, 2, 5...");
        contenido.add(txtEdad);
        contenido.add(Box.createVerticalStrut(22));

        // Botón Principal: Registrar
        JButton btnRegistrar = new JButton("Registrar Mascota");
        btnRegistrar.setFont(new Font("Segoe UI", Font.BOLD, 14));
        btnRegistrar.setBackground(COLOR_PRIMARIO);
        btnRegistrar.setForeground(Color.WHITE);
        btnRegistrar.setFocusPainted(false);
        btnRegistrar.setBorder(new EmptyBorder(10, 16, 10, 16));
        btnRegistrar.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnRegistrar.setAlignmentX(Component.LEFT_ALIGNMENT);
        btnRegistrar.setMaximumSize(new Dimension(Integer.MAX_VALUE, 40));

        btnRegistrar.addMouseListener(new java.awt.event.MouseAdapter() {
            @Override
            public void mouseEntered(java.awt.event.MouseEvent e) {
                btnRegistrar.setBackground(COLOR_PRIMARIO_HOVER);
            }

            @Override
            public void mouseExited(java.awt.event.MouseEvent e) {
                btnRegistrar.setBackground(COLOR_PRIMARIO);
            }
        });
        btnRegistrar.addActionListener(e -> accionRegistrarMascota());

        // Botón Secundario: Limpiar
        JButton btnLimpiar = new JButton("Limpiar formulario");
        btnLimpiar.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        btnLimpiar.setBackground( new Color(248, 250, 252));
        btnLimpiar.setForeground(COLOR_TEXTO_SEC);
        btnLimpiar.setFocusPainted(false);
        btnLimpiar.setBorder(new CompoundBorder(
                new LineBorder(COLOR_BORDE, 1, true),
                new EmptyBorder(7, 16, 7, 16)
        ));
        btnLimpiar.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnLimpiar.setAlignmentX(Component.LEFT_ALIGNMENT);
        btnLimpiar.setMaximumSize(new Dimension(Integer.MAX_VALUE, 34));
        btnLimpiar.addActionListener(e -> limpiarFormulario());

        contenido.add(btnRegistrar);
        contenido.add(Box.createVerticalStrut(8));
        contenido.add(btnLimpiar);

        // Permitir enviar con Enter desde el campo edad
        txtEdad.addActionListener(e -> accionRegistrarMascota());

        tarjeta.add(contenido, BorderLayout.NORTH);
        return tarjeta;
    }

    private JPanel crearPanelTabla() {
        JPanel tarjetaTabla = new JPanel(new BorderLayout(0, 12));
        tarjetaTabla.setBackground(COLOR_TARJETA);
        tarjetaTabla.setBorder(new CompoundBorder(
                new LineBorder(COLOR_BORDE, 1, true),
                new EmptyBorder(20, 20, 20, 20)
        ));

        // Encabezado de la tabla
        JPanel headerTabla = new JPanel(new BorderLayout());
        headerTabla.setBackground(COLOR_TARJETA);

        JLabel lblTituloTabla = new JLabel("Listado de Mascotas Registradas");
        lblTituloTabla.setFont(new Font("Segoe UI", Font.BOLD, 16));
        lblTituloTabla.setForeground(COLOR_TEXTO);

        JButton btnRefrescar = new JButton("Actualizar listado");
        btnRefrescar.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        btnRefrescar.setBackground(new Color(241, 245, 249));
        btnRefrescar.setForeground(COLOR_TEXTO);
        btnRefrescar.setFocusPainted(false);
        btnRefrescar.setBorder(new CompoundBorder(
                new LineBorder(COLOR_BORDE, 1, true),
                new EmptyBorder(5, 12, 5, 12)
        ));
        btnRefrescar.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnRefrescar.addActionListener(e -> actualizarTablaMascotas(true));

        headerTabla.add(lblTituloTabla, BorderLayout.WEST);
        headerTabla.add(btnRefrescar, BorderLayout.EAST);

        // Modelo y JTable
        String[] columnas = {"ID", "Nombre", "Especie", "Edad"};
        modeloTabla = new DefaultTableModel(columnas, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };

        JTable tabla = new JTable(modeloTabla);
        tabla.setFont(new Font("Segoe UI", Font.PLAIN, 13));
        tabla.setRowHeight(32);
        tabla.setGridColor(new Color(226, 232, 240));
        tabla.setSelectionBackground(new Color(204, 251, 241));
        tabla.setSelectionForeground(COLOR_TEXTO);
        tabla.setShowVerticalLines(false);
        tabla.setFillsViewportHeight(true);

        JTableHeader tableHeader = tabla.getTableHeader();
        tableHeader.setFont(new Font("Segoe UI", Font.BOLD, 13));
        tableHeader.setBackground(new Color(241, 245, 249));
        tableHeader.setForeground(COLOR_TEXTO);
        tableHeader.setPreferredSize(new Dimension(0, 36));
        tableHeader.setReorderingAllowed(false);

        // Centrar columna ID y Edad
        DefaultTableCellRenderer centrado = new DefaultTableCellRenderer();
        centrado.setHorizontalAlignment(SwingConstants.CENTER);
        tabla.getColumnModel().getColumn(0).setCellRenderer(centrado);
        tabla.getColumnModel().getColumn(0).setMaxWidth(70);
        tabla.getColumnModel().getColumn(3).setCellRenderer(centrado);
        tabla.getColumnModel().getColumn(3).setMaxWidth(120);

        JScrollPane scrollPane = new JScrollPane(tabla);
        scrollPane.setBorder(new LineBorder(COLOR_BORDE, 1));
        scrollPane.getViewport().setBackground(Color.WHITE);

        tarjetaTabla.add(headerTabla, BorderLayout.NORTH);
        tarjetaTabla.add(scrollPane, BorderLayout.CENTER);

        return tarjetaTabla;
    }

    private JPanel crearBarraEstado() {
        panelEstadoBackend = new JPanel(new BorderLayout());
        panelEstadoBackend.setBackground(BG_INFO);
        panelEstadoBackend.setBorder(new CompoundBorder(
                new LineBorder(COLOR_BORDE, 1),
                new EmptyBorder(10, 24, 10, 24)
        ));

        lblEstadoBackend = new JLabel("[Backend Listo] Complete el formulario para enviar una petición POST /api/mascotas.");
        lblEstadoBackend.setFont(new Font("Segoe UI", Font.BOLD, 12));
        lblEstadoBackend.setForeground(TXT_INFO);

        panelEstadoBackend.add(lblEstadoBackend, BorderLayout.WEST);
        return panelEstadoBackend;
    }

    private JLabel crearEtiquetaCampo(String texto) {
        JLabel label = new JLabel(texto);
        label.setFont(new Font("Segoe UI", Font.BOLD, 12));
        label.setForeground(COLOR_TEXTO);
        label.setAlignmentX(Component.LEFT_ALIGNMENT);
        return label;
    }

    private JTextField crearCampoTexto(String tooltip) {
        JTextField campo = new JTextField();
        campo.setFont(new Font("Segoe UI", Font.PLAIN, 13));
        campo.setToolTipText(tooltip);
        campo.setBorder(new CompoundBorder(
                new LineBorder(COLOR_BORDE, 1, true),
                new EmptyBorder(7, 10, 7, 10)
        ));
        campo.setAlignmentX(Component.LEFT_ALIGNMENT);
        campo.setMaximumSize(new Dimension(Integer.MAX_VALUE, 36));
        return campo;
    }

    private void accionRegistrarMascota() {
        String nombre = txtNombre.getText();
        String especie = txtEspecie.getText();
        String edadTexto = txtEdad.getText().trim();

        int edad;
        try {
            edad = Integer.parseInt(edadTexto);
        } catch (NumberFormatException ex) {
            mostrarEstadoBackend(400, "Error de formato: La edad debe ser un número entero válido (ej: 0, 1, 5).", false);
            JOptionPane.showMessageDialog(
                    this,
                    "Por favor, ingrese un número entero válido para la edad.",
                    "Edad inválida",
                    JOptionPane.WARNING_MESSAGE
            );
            txtEdad.requestFocus();
            return;
        }

        RegistrarMascotaDTO dto = new RegistrarMascotaDTO(nombre, especie, edad);
        RespuestaBackend<Mascota> respuesta = controller.registrarMascota(dto);

        if (respuesta.esExitosa()) {
            Mascota m = respuesta.getDatos();
            mostrarEstadoBackend(
                    respuesta.getEstadoHttp(),
                    String.format("%s -> Registrada: #%d %s (%s, %d años)",
                            respuesta.getMensaje(), m.getId(), m.getNombre(), m.getEspecie(), m.getEdad()),
                    true
            );
            limpiarFormulario();
            actualizarTablaMascotas(false);
        } else {
            mostrarEstadoBackend(respuesta.getEstadoHttp(), respuesta.getMensaje(), false);
            JOptionPane.showMessageDialog(
                    this,
                    respuesta.getMensaje(),
                    "No se pudo registrar la mascota (HTTP " + respuesta.getEstadoHttp() + ")",
                    JOptionPane.ERROR_MESSAGE
            );
        }
    }

    private void actualizarTablaMascotas(boolean mostrarMensajeEstado) {
        RespuestaBackend<List<Mascota>> respuesta = controller.listarMascotas();
        if (respuesta.esExitosa()) {
            List<Mascota> mascotas = respuesta.getDatos();
            modeloTabla.setRowCount(0);
            for (Mascota m : mascotas) {
                String textoEdad = (m.getEdad() == 0)
                        ? "0 años (Cachorro)"
                        : m.getEdad() + (m.getEdad() == 1 ? " año" : " años");
                modeloTabla.addRow(new Object[]{
                        "#" + m.getId(),
                        m.getNombre(),
                        m.getEspecie(),
                        textoEdad
                });
            }
            int total = mascotas.size();
            lblContador.setText(total + (total == 1 ? " mascota registrada" : " mascotas registradas"));

            if (mostrarMensajeEstado) {
                mostrarEstadoBackend(respuesta.getEstadoHttp(),
                        respuesta.getMensaje() + " (Total: " + total + ")", true);
            }
        } else {
            mostrarEstadoBackend(respuesta.getEstadoHttp(), respuesta.getMensaje(), false);
        }
    }

    private void limpiarFormulario() {
        txtNombre.setText("");
        txtEspecie.setText("");
        txtEdad.setText("");
        txtNombre.requestFocus();
    }

    private void mostrarEstadoBackend(int codigoHttp, String mensaje, boolean exito) {
        panelEstadoBackend.setBackground(exito ? BG_EXITO : BG_ERROR);
        lblEstadoBackend.setForeground(exito ? TXT_EXITO : TXT_ERROR);
        lblEstadoBackend.setText(String.format("[Backend HTTP %d] %s", codigoHttp, mensaje));
    }

    public static void iniciarInterfaz(MascotaController controller) {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ignored) {
        }
        SwingUtilities.invokeLater(() -> {
            VetCareGUI gui = new VetCareGUI(controller);
            gui.setVisible(true);
        });
    }

    public static void main(String[] args) {
        MascotaRepository repository = new InMemoryMascotaRepository();
        MascotaService service = new MascotaService(repository);
        MascotaController controller = new MascotaController(service);
        iniciarInterfaz(controller);
    }
}
