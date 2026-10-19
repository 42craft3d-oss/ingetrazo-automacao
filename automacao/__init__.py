"""Movimentos por componente para IngeTrazo 0.5.7 / API de extensões 2.

As configurações ficam no documento. Os quadros animados são desenhados em
buffers temporários do viewport; nenhum transform do modelo é alterado.
"""

from __future__ import annotations

import math
import time
import uuid
import copy
import traceback
import sys
from pathlib import Path

from PySide6.QtCore import QSize, Qt, QTimer, QEvent, QObject
from PySide6.QtGui import (QAction, QColor, QIcon, QMatrix4x4, QPen,
                           QVector3D, QGuiApplication)
from PySide6.QtWidgets import (
    QComboBox, QDoubleSpinBox, QFormLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QToolBar, QVBoxLayout, QDialog, QCompleter, QWidget,
    QCheckBox, QScrollArea, QAbstractSpinBox, QApplication,
    QLineEdit, QFrame, QToolButton,
)

from core.group import Group
from core.i18n import current_language
from tools.base import Tool


_UI_TEXT = {
    "en": {
        "Automação": "Automation", "Componente": "Component",
        "Configure a automação de cada componente. Play aciona todas as peças salvas.": "Configure the automation of each component. Play runs all saved parts.",
        "Selecione ou pesquise um componente": "Select or search a component",
        "Digite ao menos 2 letras": "Type at least 2 letters",
        "+ Adicionar bloco": "+ Add block", "Rotação": "Rotation",
        "Deslocamento": "Linear motion", "Deslocamento linear": "Linear motion",
        "Movimento": "Motion", "Delay": "Delay", "Referência": "Reference",
        "Definir referência na cena": "Set reference in scene",
        "Definir origem da peça": "Set part origin",
        "Definir eixo do movimento": "Set motion axis",
        "2 pontos": "2 points",
        "Velocidade": "Speed", "Sentido": "Direction", "Horário": "Clockwise",
        "Anti-horário": "Counter-clockwise", "A → B": "A → B", "B → A": "B → A", "Modo": "Mode", "Somar": "Accumulate",
        "Soma": "Accumulate", "Ida": "One way", "Ida + volta": "Back and forth",
        "Ida e volta": "Back and forth", "Ângulo": "Angle", "Distância": "Distance",
        "Repetição": "Repeat", "Infinito": "Infinite", "Remover bloco": "Remove block",
        "Componentes automatizados: {count}": "Automated components: {count}",
        "Parado": "Stopped", "Pausado": "Paused", "Em movimento: {count} peça(s)": "Running: {count} part(s)",
        "Passo ": "Step ", "Passo atrás": "Step backward", "Passo à frente": "Step forward",
        "Play reverso": "Reverse play", "Pausa": "Pause", "Pontos A e B definidos; salvando referência": "Points A and B defined; saving reference",
        "Referência definida e salva.": "Reference defined and saved.",
        "Tempo corrente da prévia": "Current preview time",
        "Tamanho do passo na linha do tempo": "Timeline step size",
        "Componente: nenhum": "Component: none",
        "Componente: selecione apenas um componente": "Component: select exactly one component",
        "Componente: {name}": "Component: {name}",
        "Configuração: nenhuma": "Configuration: none",
        "Configuração: movimento salvo": "Configuration: motion saved",
        "Configuração: sem movimento": "Configuration: no motion",
        "Eixo: não definido": "Axis: not defined",
        "Marque o ponto A": "Pick point A", "Marque o ponto B": "Pick point B",
        "Limpar movimentos": "Clear motions", "Bloco salvo.": "Block saved.",
        "A referência deste bloco está travada.": "This block's reference is locked.",
        "Selecione um componente primeiro.": "Select a component first.",
        "Eixo da automação": "Automation axis",
        "Clique em dois pontos para definir a direção do movimento.": "Click two points to set the motion direction.",
        "Automação: clique no ponto A.": "Automation: click point A.",
        "Automação: marque o ponto B. Setas: direita = X, esquerda = Y, cima = Z.": "Automation: pick point B. Arrow keys: right = X, left = Y, up = Z.",
        "A transformação do componente não é invertível.": "The component transform is not invertible.",
        "O eixo precisa de dois pontos diferentes.": "The axis needs two different points.",
        "Não foi possível encontrar o bloco capturado.": "The captured block could not be found.",
        "Selecione um componente e defina os pontos A e B.": "Select a component and set points A and B.",
        "Configure e salve pelo menos um movimento.": "Configure and save at least one motion.",
        "Início da animação": "Animation start", "Em retrocesso": "Reversing",
        "Automação: erro registrado no log.": "Automation: error recorded in the log.",
        "Automação requer IngeTrazo 0.5.7 / API 2.": "Automation requires IngeTrazo 0.5.7 / API 2.",
        "Definir eixo por 2 pontos": "Set axis by 2 points",
        "Definir trajetória A e B": "Set A and B path",
        "Fixar tempo 🔒": "Lock time 🔒", "Fixar velocidade 🔒": "Lock speed 🔒",
        "Fixar repetição 🔒": "Lock repeat 🔒", "Fixar nome": "Lock name",
        "Fixar delay": "Lock delay", "Fixar movimento": "Lock motion",
        "Fixar referência": "Lock reference", "Fixar velocidade": "Lock speed",
        "Fixar sentido": "Lock direction", "Fixar distância": "Lock distance",
        "Fixar modo": "Lock mode", "Fixar ângulo": "Lock angle",
        "Fixar repetição": "Lock repeat", "Eixo": "Axis", "Trajetória": "Path",
        "{noun}: definido": "{noun}: set", "{noun}: não definido": "{noun}: not set",
        "Movimento salvo para {name}.": "Motion saved for {name}.",
        "Não foi possível iniciar a prévia: {error}": "Could not start preview: {error}",
        "Tempo: {time:.2f} s": "Time: {time:.2f} s",
        "Pause congela a prévia. Stop retorna todas as peças à posição inicial. Os quadros da animação não são gravados no arquivo.": "Pause freezes the preview. Stop returns every part to its initial position. Animation frames are not saved in the file.",
    },
    "es": {
        "Automação": "Automatización", "Componente": "Componente",
        "Configure a automação de cada componente. Play aciona todas as peças salvas.": "Configure la automatización de cada componente. Reproducir activa todas las piezas guardadas.",
        "Selecione ou pesquise um componente": "Seleccione o busque un componente",
        "Digite ao menos 2 letras": "Escriba al menos 2 letras",
        "+ Adicionar bloco": "+ Añadir bloque", "Rotação": "Rotación",
        "Deslocamento": "Desplazamiento", "Deslocamento linear": "Desplazamiento lineal",
        "Movimento": "Movimiento", "Delay": "Retraso", "Referência": "Referencia",
        "Definir referência na cena": "Definir referencia en la escena",
        "Definir origem da peça": "Definir origen de la pieza",
        "Definir eixo do movimento": "Definir eje del movimiento",
        "2 pontos": "2 puntos",
        "Velocidade": "Velocidad", "Sentido": "Sentido", "Horário": "Horario",
        "Anti-horário": "Antihorario", "A → B": "A → B", "B → A": "B → A", "Modo": "Modo", "Somar": "Acumular",
        "Soma": "Acumular", "Ida": "Solo ida", "Ida + volta": "Ida y vuelta",
        "Ida e volta": "Ida y vuelta", "Ângulo": "Ángulo", "Distância": "Distancia",
        "Repetição": "Repetición", "Infinito": "Infinito", "Remover bloco": "Eliminar bloque",
        "Componentes automatizados: {count}": "Componentes automatizados: {count}",
        "Parado": "Detenido", "Pausado": "En pausa", "Em movimento: {count} peça(s)": "En movimiento: {count} pieza(s)",
        "Passo ": "Paso ", "Passo atrás": "Paso atrás", "Passo à frente": "Paso adelante",
        "Play reverso": "Reproducir inverso", "Pausa": "Pausa", "Pontos A e B definidos; salvando referência": "Puntos A y B definidos; guardando referencia",
        "Referência definida e salva.": "Referencia definida y guardada.",
        "Tempo corrente da prévia": "Tiempo actual de la vista previa",
        "Tamanho do passo na linha do tempo": "Tamaño del paso en la línea de tiempo",
        "Componente: nenhum": "Componente: ninguno",
        "Componente: selecione apenas um componente": "Componente: seleccione exactamente un componente",
        "Componente: {name}": "Componente: {name}",
        "Configuração: nenhuma": "Configuración: ninguna",
        "Configuração: movimento salvo": "Configuración: movimiento guardado",
        "Configuração: sem movimento": "Configuración: sin movimiento",
        "Eixo: não definido": "Eje: no definido",
        "Marque o ponto A": "Marque el punto A", "Marque o ponto B": "Marque el punto B",
        "Limpar movimentos": "Limpiar movimientos", "Bloco salvo.": "Bloque guardado.",
        "A referência deste bloco está travada.": "La referencia de este bloque está bloqueada.",
        "Selecione um componente primeiro.": "Seleccione primero un componente.",
        "Eixo da automação": "Eje de automatización",
        "Clique em dois pontos para definir a direção do movimento.": "Haga clic en dos puntos para definir la dirección del movimiento.",
        "Automação: clique no ponto A.": "Automatización: haga clic en el punto A.",
        "Automação: marque o ponto B. Setas: direita = X, esquerda = Y, cima = Z.": "Automatización: marque el punto B. Flechas: derecha = X, izquierda = Y, arriba = Z.",
        "A transformação do componente não é invertível.": "La transformación del componente no es invertible.",
        "O eixo precisa de dois pontos diferentes.": "El eje necesita dos puntos diferentes.",
        "Não foi possível encontrar o bloco capturado.": "No se pudo encontrar el bloque capturado.",
        "Selecione um componente e defina os pontos A e B.": "Seleccione un componente y defina los puntos A y B.",
        "Configure e salve pelo menos um movimento.": "Configure y guarde al menos un movimiento.",
        "Início da animação": "Inicio de la animación", "Em retrocesso": "En reversa",
        "Automação: erro registrado no log.": "Automatización: error registrado en el registro.",
        "Automação requer IngeTrazo 0.5.7 / API 2.": "Automatización requiere IngeTrazo 0.5.7 / API 2.",
        "Definir eixo por 2 pontos": "Definir eje mediante 2 puntos",
        "Definir trajetória A e B": "Definir trayectoria A y B",
        "Fixar tempo 🔒": "Bloquear tiempo 🔒", "Fixar velocidade 🔒": "Bloquear velocidad 🔒",
        "Fixar repetição 🔒": "Bloquear repetición 🔒", "Fixar nome": "Bloquear nombre",
        "Fixar delay": "Bloquear retraso", "Fixar movimento": "Bloquear movimiento",
        "Fixar referência": "Bloquear referencia", "Fixar velocidade": "Bloquear velocidad",
        "Fixar sentido": "Bloquear sentido", "Fixar distância": "Bloquear distancia",
        "Fixar modo": "Bloquear modo", "Fixar ângulo": "Bloquear ángulo",
        "Fixar repetição": "Bloquear repetición", "Eixo": "Eje", "Trajetória": "Trayectoria",
        "{noun}: definido": "{noun}: definido", "{noun}: não definido": "{noun}: no definido",
        "Movimento salvo para {name}.": "Movimiento guardado para {name}.",
        "Não foi possível iniciar a prévia: {error}": "No se pudo iniciar la vista previa: {error}",
        "Tempo: {time:.2f} s": "Tiempo: {time:.2f} s",
        "Pause congela a prévia. Stop retorna todas as peças à posição inicial. Os quadros da animação não são gravados no arquivo.": "Pausa congela la vista previa. Detener devuelve todas las piezas a la posición inicial. Los fotogramas no se guardan en el archivo.",
    },
}


def _t(text, /, **kwargs):
    """Tradução própria da extensão, orientada pelo idioma do host."""
    translated = _UI_TEXT.get(current_language(), {}).get(text, text)
    return translated.format(**kwargs) if kwargs else translated


def _install_plugin_exception_log(app):
    """Registra erros de callbacks Qt desta extensão sem abrir diálogo vazio."""
    if getattr(app.window, "_automation_exception_hook_installed", False):
        return
    previous = sys.excepthook
    log_path = Path(__file__).parent / "automacao-debug.log"

    def plugin_excepthook(exc_type, value, trace):
        details = "".join(traceback.format_exception(exc_type, value, trace))
        if "motor_continuo.py" in details:
            try:
                stamp = time.strftime("%Y-%m-%d %H:%M:%S")
                with log_path.open("a", encoding="utf-8") as log:
                    log.write(f"[{stamp}] ERRO GLOBAL DO PLUGIN:\n{details}\n")
            except Exception:
                pass
            return
        previous(exc_type, value, trace)

    sys.excepthook = plugin_excepthook
    app.window._automation_exception_hook_installed = True


def _vec(value):
    return [float(value.x()), float(value.y()), float(value.z())]


def _point(value):
    return QVector3D(*value)


def _rotation(a, b, degrees):
    matrix = QMatrix4x4()
    matrix.translate(a)
    matrix.rotate(degrees, (b - a).normalized())
    matrix.translate(-a)
    return matrix


class _FocusedSpinBoxWheelGuard(QObject):
    """Ignora a roda sobre campos numéricos que ainda não foram clicados."""
    def eventFilter(self, watched, event):
        if (event.type() == QEvent.Type.Wheel and
                isinstance(watched, QAbstractSpinBox) and
                not watched.hasFocus()):
            return True
        return False


class _BlankHostDialogGuard(QObject):
    """Oculta o diálogo vazio transitório emitido pelo host.

    Só alcança uma janela de topo intitulada exatamente "IngeTrazo" que não
    contém nenhum texto. Diálogos legítimos têm título diferente ou conteúdo.
    """
    def __init__(self, controller):
        super().__init__(controller.app.window)
        self.controller = controller
        self._scan_timer = QTimer(self)
        self._scan_timer.setInterval(16)
        self._scan_timer.timeout.connect(self._scan_native_windows)
        self._scan_timer.start()

    def _is_empty_host_window(self, window):
        title_getter = getattr(window, "windowTitle", None)
        title = title_getter() if callable(title_getter) else window.title()
        if window is self.controller.panel or title != "IngeTrazo":
            return False
        if isinstance(window, QWidget):
            texts = [label.text().strip() for label in window.findChildren(QLabel)]
            return not any(texts)
        return True

    def _hide_blank_window(self, window):
        if not self._is_empty_host_window(window):
            return
        self.controller._debug(
            f"janela vazia do host suprimida: {type(window).__name__}")
        try:
            window.hide()
        except Exception:
            pass

    def _scan_native_windows(self):
        # O diálogo fugaz do host pode ser criado como QWindow nativa, que
        # não passa pelo filtro de QWidget. Uma varredura curta o alcança.
        for window in QApplication.topLevelWidgets():
            self._hide_blank_window(window)
        for window in QGuiApplication.allWindows():
            self._hide_blank_window(window)

    def eventFilter(self, watched, event):
        if event.type() != QEvent.Type.Show or not isinstance(watched, QWidget):
            return False
        if not watched.isWindow():
            return False
        if not self._is_empty_host_window(watched):
            return False
        QTimer.singleShot(0, lambda: self._hide_blank_window(watched))
        return False


class _TopLevelWindowTrace(QObject):
    """Diagnóstico passivo de janelas mostradas após o plugin carregar."""
    def __init__(self, controller):
        super().__init__(controller.app.window)
        self.controller = controller

    @staticmethod
    def _title(obj):
        getter = getattr(obj, "windowTitle", None)
        if callable(getter):
            return getter()
        getter = getattr(obj, "title", None)
        return getter() if callable(getter) else ""

    def eventFilter(self, watched, event):
        if event.type() != QEvent.Type.Show:
            return False
        is_top = getattr(watched, "isWindow", None)
        is_native_window = type(watched).__name__ == "QWindow"
        if (not is_native_window and
                (not callable(is_top) or not is_top())):
            return False
        title = self._title(watched)
        name_getter = getattr(watched, "objectName", None)
        name = name_getter() if callable(name_getter) else ""
        size = getattr(watched, "size", lambda: None)()
        parent_getter = getattr(watched, "parentWidget", None)
        parent = parent_getter() if callable(parent_getter) else None
        parent_desc = (f"{type(parent).__name__}:{parent.objectName()!r}"
                       if parent is not None else "nenhum")
        children = []
        find_children = getattr(watched, "findChildren", None)
        if callable(find_children):
            try:
                children = [f"{type(child).__name__}:{child.objectName()!r}"
                            for child in find_children(QWidget)[:12]]
            except Exception:
                children = ["indisponível"]
        self.controller._debug(
            f"janela exibida: {type(watched).__name__}; título={title!r}; "
            f"objeto={name!r}; tamanho={size}; pai={parent_desc}; "
            f"filhos={children}")
        return False


class MotorController:
    def __init__(self, app):
        self.app = app
        self.viewport = app.viewport
        self._selected = None
        self._axis_a = None       # local coordinates of the selected component
        self._axis_b = None
        self._picking = None
        self._previous_tool = None
        self._playing = False
        self._play_direction = 1
        self._timeline_s = 0.0
        self._preview = False
        self._scene = None
        self._version = None
        self._motors = []         # runtime entries with independent buffers/angle
        self._last_tick = None
        self._original_draw = None
        self._updating = False
        self._selection_token = None
        self._loaded_config = None
        self._writing_automation = False
        self._automation_document_pending = False
        self._automation_document_seen = False
        self._active_block_id = None
        self._building_cards = False
        self._expanded_block_ids = set()
        self._capture_target = None
        self._wheel_guard = _FocusedSpinBoxWheelGuard(app.window)
        self._pending_save_data = None
        self._debug_path = Path(__file__).parent / "automacao-debug.log"
        self._save_timer = QTimer(app.window)
        self._save_timer.setSingleShot(True)
        self._save_timer.timeout.connect(self._flush_document_save)

        self.timer = QTimer(app.window)
        self.timer.setInterval(33)
        self.timer.timeout.connect(
            lambda: self._run_guard("atualizar prévia", self._tick, False))

        # Janela flutuante única, paiada à janela principal — o padrão dos
        # diálogos do IngeTrazo. Só é mostrada quando o usuário pede pelo
        # ícone/menu; não roubamos foco ao selecionar ou animar uma peça.
        self.dialog = QDialog(app.window)
        self.dialog.setObjectName("automacao_dialog")
        self.dialog.setWindowTitle(_t("Automação"))
        self.dialog.setWindowIcon(QIcon(str(Path(__file__).parent / "icone_motor.svg")))
        self.dialog.resize(470, 690)
        self.dialog.setMinimumWidth(380)
        self.panel = self.dialog  # compatibilidade com os controles existentes
        self._blank_dialog_guard = None
        self._window_trace = _TopLevelWindowTrace(self)
        QApplication.instance().installEventFilter(self._window_trace)
        self._debug("rastreador passivo de janelas ativado")
        root = QVBoxLayout(self.dialog)
        root.setContentsMargins(0, 0, 0, 0)
        self.window_scroll = QScrollArea(self.dialog)
        self.window_scroll.setWidgetResizable(True)
        root.addWidget(self.window_scroll)
        content = QWidget()
        self.window_scroll.setWidget(content)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(10, 12, 10, 10)
        layout.setSpacing(9)
        transport = QHBoxLayout()
        transport.setContentsMargins(0, 0, 0, 0)
        transport.setSpacing(5)
        def transport_button(icon_name, tip, callback):
            button = QToolButton()
            button.setIcon(QIcon(str(Path(__file__).parent / icon_name)))
            button.setIconSize(QSize(26, 26))
            button.setFixedSize(36, 34)
            button.setToolTip(tip)
            button.setAutoRaise(False)
            button.setStyleSheet(
                "QToolButton {"
                " background: #2a3038;"
                " border: 1px solid #56616d; border-radius: 5px;"
                " padding: 2px; }"
                "QToolButton:hover {"
                " border-color: #90a4b8; background: #36414c; }"
                "QToolButton:pressed {"
                " background: #1c2229; border-color: #708397;"
                " padding-top: 3px; padding-left: 3px; }")
            button.clicked.connect(
                lambda _=False, name=tip, fn=callback:
                self._run_guard(name, fn))
            transport.addWidget(button)
            return button
        self.step_back_button = transport_button("icone_passo_atras.svg", _t("Passo atrás"), self.step_back)
        self.reverse_button = transport_button("icone_play_reverso.svg", _t("Play reverso"), self.play_reverse)
        self.stop_button = transport_button("icone_stop.svg", "Stop", self.stop)
        self.pause_button = transport_button("icone_pause.svg", _t("Pausa"), self.pause)
        self.play_button = transport_button("icone_play.svg", "Play", self.play_forward)
        self.step_forward_button = transport_button("icone_passo_frente.svg", _t("Passo à frente"), self.step_forward)
        # Relógio global da prévia: abaixo do transporte, pois todos os
        # cartões compartilham a mesma cronologia.
        self.timeline_label = QLabel("⏱ 00:00,00")
        self.timeline_label.setToolTip(_t("Tempo corrente da prévia"))
        self.timeline_label.setAlignment(Qt.AlignCenter)
        self.timeline_label.setMinimumWidth(122)
        self.timeline_label.setMinimumHeight(32)
        self.timeline_label.setStyleSheet(
            "QLabel { background: #11161d; color: #d8efff;"
            " border: 1px solid #586878; border-radius: 5px;"
            " font-family: Consolas, monospace; font-size: 14px;"
            " font-weight: 600; padding: 0 8px; }")
        self.step_size = QDoubleSpinBox()
        self.step_size.setRange(0.01, 3600.0)
        self.step_size.setDecimals(2)
        # 1 s é um valor inicial visualmente verificável para os padrões
        # (30 rpm e 100 mm/s). O usuário continua podendo informar qualquer
        # intervalo, por exemplo 10 s, quando quiser navegar a cronologia.
        self.step_size.setValue(1.0)
        self.step_size.setPrefix(_t("Passo "))
        self.step_size.setSuffix(" s")
        self.step_size.setToolTip(_t("Tamanho do passo na linha do tempo"))
        self.step_size.setMinimumHeight(32)
        self.step_size.setMinimumWidth(132)
        self.step_size.installEventFilter(self._wheel_filter())
        # Primeira linha: controles. Segunda linha: leitura e passo.
        transport.addStretch(1)
        layout.addLayout(transport)
        timeline_row = QHBoxLayout()
        timeline_row.setContentsMargins(0, 0, 0, 0)
        timeline_row.setSpacing(6)
        timeline_row.addWidget(self.timeline_label)
        timeline_row.addWidget(self.step_size)
        timeline_row.addStretch(1)
        layout.addLayout(timeline_row)
        intro = QLabel(_t("Configure a automação de cada componente. Play aciona todas as peças salvas."))
        intro.setWordWrap(True)
        self.component_combo = QComboBox()
        self.component_combo.setEditable(True)
        self.component_combo.setInsertPolicy(QComboBox.NoInsert)
        self.component_combo.setPlaceholderText(_t("Digite ao menos 2 letras"))
        self.component_completer = QCompleter(self.component_combo.model(), self.panel)
        self.component_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.component_completer.setFilterMode(Qt.MatchContains)
        self.component_completer.setCompletionMode(QCompleter.PopupCompletion)
        self.component_combo.setCompleter(self.component_completer)
        self.component_combo.activated.connect(
            lambda index: self._run_guard("selecionar componente",
                                          lambda: self._component_chosen(index)))
        self.component_completer.activated.connect(
            lambda text: self._run_guard("concluir busca de componente",
                                         lambda: self._completion_chosen(text)))
        self.component_combo.lineEdit().textEdited.connect(
            lambda text: self._run_guard("buscar componente",
                                         lambda: self._component_typed(text)))
        layout.addWidget(self.component_combo)
        self.selection_label = QLabel(_t("Componente: nenhum"))
        self.selection_label.setWordWrap(True)
        self.cards_host = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_host)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(6)
        layout.addWidget(self.cards_host)
        self.add_block_button = QPushButton(_t("+ Adicionar bloco"))
        # Em um QDialog, QPushButton pode tornar-se o botão padrão e receber
        # Enter de um campo numérico. Adicionar bloco deve exigir clique.
        self.add_block_button.setAutoDefault(False)
        self.add_block_button.setDefault(False)
        self.add_block_button.clicked.connect(
            lambda: self._run_guard("adicionar bloco", self.add_block))
        layout.addWidget(self.add_block_button)
        # A instrução fica após a configuração dos blocos, perto do resumo.
        layout.addWidget(intro)
        block_order = QHBoxLayout()
        self.block_up = QPushButton("↑")
        self.block_down = QPushButton("↓")
        for button in (self.block_up, self.block_down):
            button.setAutoDefault(False)
            button.setDefault(False)
        self.block_up.clicked.connect(
            lambda: self._run_guard("mover bloco acima",
                                    lambda: self._move_block(-1)))
        self.block_down.clicked.connect(
            lambda: self._run_guard("mover bloco abaixo",
                                    lambda: self._move_block(1)))
        self.block_up.hide()
        self.block_down.hide()
        block_order.addWidget(self.block_up)
        block_order.addWidget(self.block_down)
        layout.addLayout(block_order)
        self.config_label = QLabel(_t("Configuração: nenhuma"))
        self.config_label.setWordWrap(True)
        layout.addWidget(self.config_label)
        self.axis_label = QLabel(_t("Eixo: não definido"))
        self.axis_label.setWordWrap(True)
        layout.addWidget(self.axis_label)

        self.pick_button = QPushButton(_t("Definir eixo por 2 pontos"))
        self.pick_button.setAutoDefault(False)
        self.pick_button.setDefault(False)
        self.pick_button.clicked.connect(self.pick_axis)
        layout.addWidget(self.pick_button)
        form = QFormLayout()
        self.kind = QComboBox()
        self.kind.addItem("Rotação contínua")
        self.kind.addItem("Deslocamento linear")
        self.kind.currentIndexChanged.connect(self._type_changed)
        form.addRow("Movimento", self.kind)
        self.delay = QDoubleSpinBox()
        self.delay.setRange(0.0, 3600.0)
        self.delay.setDecimals(2)
        self.delay.setSuffix(" s")
        form.addRow("Delay", self.delay)
        self.lock_delay = QCheckBox(_t("Fixar tempo 🔒"))
        form.addRow("", self.lock_delay)
        axes_row = QHBoxLayout()
        self.axis_x = QCheckBox("X")
        self.axis_y = QCheckBox("Y")
        self.axis_z = QCheckBox("Z")
        self.axis_z.setChecked(True)
        self.lock_reference = QCheckBox("🔒")
        for axis in (self.axis_x, self.axis_y, self.axis_z):
            axes_row.addWidget(axis)
            axis.toggled.connect(self._axes_changed)
        axes_row.addWidget(self.lock_reference)
        form.addRow("Referência", axes_row)
        self.rpm = QDoubleSpinBox()
        self.rpm.setRange(0.1, 10000.0)
        self.rpm.setDecimals(1)
        self.rpm.setValue(30.0)
        self.rpm.setSuffix(" rpm")
        form.addRow("Velocidade", self.rpm)
        self.rpm_label = form.labelForField(self.rpm)
        self.speed = QDoubleSpinBox()
        self.speed.setRange(0.1, 1000000.0)
        self.speed.setDecimals(1)
        self.speed.setValue(100.0)
        self.speed.setSuffix(" mm/s")
        form.addRow("Velocidade", self.speed)
        self.speed_label = form.labelForField(self.speed)
        self.repetitions = QSpinBox()
        self.repetitions.setRange(0, 1000000)
        self.repetitions.setSpecialValueText("Contínuo")
        self.repetitions.setValue(1)
        form.addRow("Repetições", self.repetitions)
        self.repetitions_label = form.labelForField(self.repetitions)
        self.lock_speed = QCheckBox(_t("Fixar velocidade 🔒"))
        self.lock_repetitions = QCheckBox(_t("Fixar repetição 🔒"))
        form.addRow("", self.lock_speed)
        form.addRow("", self.lock_repetitions)
        self.direction = QComboBox()
        self.direction.addItems(["A → B", "B → A"])
        form.addRow("Sentido", self.direction)
        self.direction_label = form.labelForField(self.direction)
        layout.addLayout(form)
        self._type_changed()
        # O editor anterior era de um único movimento. Os cartões criados em
        # _refresh_blocks possuem seus próprios controles e substituem-no.
        for widget in (self.config_label, self.axis_label, self.pick_button,
                       self.kind, self.delay, self.axis_x, self.axis_y,
                       self.axis_z, self.lock_reference, self.rpm, self.speed,
                       self.repetitions, self.direction, self.lock_delay,
                       self.lock_speed, self.lock_repetitions):
            widget.hide()
        for field in (self.kind, self.delay, self.rpm, self.speed,
                      self.repetitions, self.direction, self.lock_delay,
                      self.lock_speed, self.lock_repetitions):
            label = form.labelForField(field)
            if label is not None:
                label.hide()
        for row in range(form.rowCount()):
            form.setRowVisible(row, False)
        self._legacy_hidden = True
        self.remove_button = QPushButton(_t("Limpar movimentos"), content)
        self.remove_button.setAutoDefault(False)
        self.remove_button.setDefault(False)
        self.remove_button.setToolTip(
            "Remove a configuração de movimento do componente selecionado.")
        self.remove_button.setStyleSheet(
            "QPushButton { background: #9D3232; color: white; font-weight: 600; }"
            "QPushButton:hover { background: #BD3E3E; }"
            "QPushButton:disabled { background: #5A3737; color: #B9A0A0; }")
        self.remove_button.clicked.connect(self.remove_motor)
        # A remoção global era redundante e não participava do novo modelo
        # por blocos. Cada cartão mantém apenas o próprio "Remover bloco".
        self.remove_button.hide()
        # Mantidos somente como estado interno: a interface não exibe mais
        # contador, status textual nem nota de uso abaixo dos blocos.
        self.count_label = QLabel(_t("Componentes automatizados: {count}", count=0))
        self.status_label = QLabel(_t("Parado"))
        # Enter em um campo numérico só confirma o valor. Nenhum botão da
        # janela pode virar ação-padrão e iniciar a captura do eixo.
        for button in (self.pick_button, self.remove_button):
            button.setAutoDefault(False)
            button.setDefault(False)
        layout.addStretch(1)

        # Com eixo válido, cada alteração destes campos é persistida na hora.
        self.rpm.valueChanged.connect(self._auto_save)
        self.direction.currentIndexChanged.connect(self._auto_save)
        self.speed.valueChanged.connect(self._auto_save)
        self.repetitions.valueChanged.connect(self._auto_save)
        self.delay.valueChanged.connect(self._auto_save)
        self.lock_reference.toggled.connect(self._lock_changed)
        self.lock_delay.toggled.connect(lambda locked: self.delay.setEnabled(not locked))
        self.lock_speed.toggled.connect(self._speed_lock_changed)
        self.lock_repetitions.toggled.connect(
            lambda locked: self.repetitions.setEnabled(not locked))

        app.add_menu_action(_t("Automação") + "…", self.show,
                            tip="Configurar automações de componentes.")
        self._add_toolbar()
        # Estes dois callbacks são chamados diretamente pelo host, fora dos
        # slots Qt já protegidos. Nunca podem deixar uma exceção subir até a
        # janela genérica e vazia do IngeTrazo.
        app.add_overlay(self._safe_draw_axis)
        app.on_document_changed(self._safe_document_changed)
        # The extension API has no selection-changed signal. Poll only the
        # identity of the single selected item; no document or mesh walks.
        self.selection_timer = QTimer(app.window)
        self.selection_timer.setInterval(120)
        self.selection_timer.timeout.connect(
            lambda: self._run_guard("seleção", self._selection_changed, False))
        self.selection_timer.start()
        self._debug("plugin iniciado")
        self._refresh_count()

    def _refresh_component_list(self):
        """Atualiza a caixa de pesquisa sem reagir como uma seleção do usuário."""
        selected_uid = self._selected.uid if self._selected is not None else None
        self.component_combo.blockSignals(True)
        try:
            self.component_combo.clear()
            self.component_combo.addItem(_t("Selecione ou pesquise um componente"), None)
            for group in self.app.scene.groups:
                if group.is_component():
                    self.component_combo.addItem(group.name, group.uid)
            index = self.component_combo.findData(selected_uid)
            self.component_combo.setCurrentIndex(index if index >= 0 else 0)
        finally:
            self.component_combo.blockSignals(False)

    def _component_typed(self, text):
        # A lista só abre a partir de duas letras; a busca encontra o texto em
        # qualquer posição do nome, não apenas no início.
        if len(text.strip()) < 2:
            self.component_completer.popup().hide()
            return
        self.component_completer.setCompletionPrefix(text)
        self.component_completer.complete()

    def _component_chosen(self, index):
        uid = self.component_combo.itemData(index)
        self._select_component_uid(uid)

    def _completion_chosen(self, index):
        self._select_component_uid(index.data(Qt.UserRole))

    def _select_component_uid(self, uid):
        if not uid:
            return
        group = next((item for item in self.app.scene.groups
                      if item.is_component() and item.uid == uid), None)
        if group is None:
            return
        self.app.scene.selection.clear()
        self.app.scene.selection.add(group)
        self._selection_token = None
        self._read_selection()
        self.viewport.update()

    def _add_toolbar(self):
        # Uma barra dedicada mantém a engrenagem visível mesmo quando a
        # barra Principal estiver escondida ou cheia de ferramentas.
        bar = QToolBar("Automação", self.app.window)
        bar.setObjectName("automacao_toolbar")
        bar.setMovable(True)
        bar.setFloatable(True)
        bar.setAllowedAreas(Qt.AllToolBarAreas)
        try:
            from views.icons import toolbar_icon_px
            px = toolbar_icon_px()
        except ImportError:
            px = 32
        bar.setIconSize(QSize(px, px))
        bar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        root = Path(__file__).parent
        gear = QAction(QIcon(str(root / "icone_motor.svg")), "Configurar automação", bar)
        gear.setObjectName("automacao_toolbar_action")
        gear.triggered.connect(self.show)
        gear.setStatusTip("Abrir Automação")
        bar.addAction(gear)
        self.app.window.addToolBar(Qt.TopToolBarArea, bar)
        bar.show()
        self.toolbar = bar
        self._toolbar_action = gear

    def _saved(self):
        # Durante uma interação, a versão pendente é a fonte de verdade para
        # os cartões. Assim uma nova alteração não apaga a anterior enquanto
        # o documento ainda aguarda a gravação agrupada.
        raw = getattr(self, "_pending_save_data", None)
        if raw is None:
            raw = self.app.document_data({"version": 3, "motors": {}})
        return copy.deepcopy(raw) if (isinstance(raw, dict) and
                                      isinstance(raw.get("motors"), dict)) \
            else {"version": 3, "motors": {}}

    def _debug(self, message):
        try:
            stamp = time.strftime("%Y-%m-%d %H:%M:%S")
            path = getattr(self, "_debug_path",
                           Path(__file__).parent / "automacao-debug.log")
            with path.open("a", encoding="utf-8") as log:
                log.write(f"[{stamp}] {message}\n")
        except Exception:
            pass

    def _run_guard(self, action, callback, trace=True):
        try:
            if trace:
                self._debug(f"ação: {action}")
            return callback()
        except Exception:
            detail = traceback.format_exc()
            self._debug(f"ERRO em {action}:\n{detail}")
            try:
                self.viewport.flash_status(_t("Automação: erro registrado no log."))
            except Exception:
                pass
            return None

    def _wheel_filter(self):
        """Cria o filtro também para uma instância antiga após recarregamento."""
        if not hasattr(self, "_wheel_guard"):
            self._wheel_guard = _FocusedSpinBoxWheelGuard(self.app.window)
        return self._wheel_guard

    def _ensure_save_timer(self):
        """Compatibilidade: a janela pode manter o controlador da versão anterior."""
        if not hasattr(self, "_save_timer"):
            self._pending_save_data = None
            self._save_timer = QTimer(self.app.window)
            self._save_timer.setSingleShot(True)
            self._save_timer.timeout.connect(self._flush_document_save)
        return self._save_timer

    def _queue_document_save(self, data):
        """Persiste após a interação, sem reentrar no evento do widget."""
        self._pending_save_data = copy.deepcopy(data)
        self._ensure_save_timer().start(250)

    def _flush_document_save(self):
        data = getattr(self, "_pending_save_data", None)
        if data is None:
            return
        self._pending_save_data = None
        self._automation_document_pending = True
        self._automation_document_seen = False
        self._writing_automation = True
        try:
            self.app.set_document_data(data)
        finally:
            self._writing_automation = False
            # Quando o host emite o sinal de forma síncrona, já o tratamos
            # como alteração interna. Em hosts assíncronos a marca fica até
            # a próxima notificação do documento.
            if self._automation_document_seen:
                self._automation_document_pending = False

    def _refresh_count(self):
        self.count_label.setText(
            _t("Componentes automatizados: {count}",
               count=len(self._saved()["motors"])))

    def _expanded_blocks(self):
        """Compatibilidade com controladores já abertos ao recarregar o plugin."""
        if not hasattr(self, "_expanded_block_ids"):
            self._expanded_block_ids = set()
        return self._expanded_block_ids

    def _refresh_blocks(self):
        """Reconstrói os cartões recolhíveis do componente selecionado."""
        self._building_cards = True
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()
        try:
            if self._selected is None:
                self.add_block_button.setEnabled(False)
                return
            self.add_block_button.setEnabled(True)
            blocks = self._blocks_entry(self._saved()["motors"].get(self._selected.uid))
            active = next((i for i, block in enumerate(blocks)
                           if block.get("id") == self._active_block_id), 0)
            if blocks:
                if not self._expanded_blocks():
                    self._expanded_blocks().add(blocks[active].get("id"))
            for number, block in enumerate(blocks, 1):
                self.cards_layout.addWidget(self._make_block_card(number, block))
        finally:
            self._building_cards = False

    def _make_block_card(self, number, block):
        """Cartão independente, inspirado nos modificadores expansíveis."""
        # QFrame e palette() usam o tema nativo do IngeTrazo, em vez de
        # cores fixas que deixam os blocos visualmente desconectados do app.
        card = QFrame()
        card.setObjectName("automationBlock")
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(
            "QFrame#automationBlock { background: palette(base); "
            "border: 1px solid palette(mid); border-radius: 4px; }")
        outer = QVBoxLayout(card)
        outer.setContentsMargins(6, 5, 6, 6)
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)
        expander = QToolButton()
        expander.setCheckable(True)
        expander.setChecked(block.get("id") in self._expanded_blocks())
        kind_name = _t("Deslocamento") if block.get("kind") == "linear" else _t("Rotação")
        block_name = QLineEdit(block.get("name", f"Bloco {number}"))
        block_name.setPlaceholderText(f"Bloco {number}")
        block_name.setFrame(False)
        block_name.setMinimumWidth(80)
        block_name.setMaximumWidth(190)
        block_name.setStyleSheet("font-weight: 600;")
        kind_label = QLabel(f"— {kind_name}")
        kind_label.setStyleSheet("font-weight: 600; color: palette(mid);")
        header_layout.addWidget(expander)
        header_layout.addWidget(block_name)
        header_layout.addWidget(kind_label)
        outer.addWidget(header)
        body = QWidget()
        form = QFormLayout(body)
        form.setContentsMargins(4, 2, 4, 2)
        kind = QComboBox(); kind.addItems([_t("Rotação"), _t("Deslocamento linear")])
        kind.setCurrentIndex(1 if block.get("kind") == "linear" else 0)
        delay = QDoubleSpinBox(); delay.setRange(0, 3600); delay.setDecimals(2); delay.setSuffix(" s")
        delay.setValue(float(block.get("delay_s", 0)))
        axes = QWidget(); axes_row = QHBoxLayout(axes); axes_row.setContentsMargins(0, 0, 0, 0)
        xyz = block.get("axis", [0, 0, 1])
        locks = block.get("locks", {})
        checks = []
        for text, value in zip(("X", "Y", "Z"), xyz):
            check = QCheckBox(text); check.setChecked(bool(value)); axes_row.addWidget(check); checks.append(check)
        # O quarto eixo fica disponível somente depois de uma captura A/B.
        # Ele permite voltar ao eixo livre de dois pontos sem recapturá-lo.
        points_available = block.get("reference_mode") == "points"
        point_axis = QCheckBox(_t("2 pontos"))
        point_axis.setChecked(points_available)
        point_axis.setEnabled(points_available and not locks.get("reference", False))
        axes_row.addWidget(point_axis)
        capture = QPushButton()
        capture.setAutoDefault(False)
        capture.setDefault(False)
        rpm = QDoubleSpinBox(); rpm.setRange(0.1, 10000); rpm.setSuffix(" rpm"); rpm.setValue(float(block.get("rpm", 30)))
        direction = QComboBox(); direction.addItems([_t("Horário"), _t("Anti-horário")])
        direction.setCurrentIndex(0 if int(block.get("direction", 1)) == 1 else 1)
        linear_direction = QComboBox(); linear_direction.addItems([_t("A → B"), _t("B → A")])
        linear_direction.setCurrentIndex(0 if int(block.get("linear_direction", 1)) == 1 else 1)
        mode = QComboBox(); mode.addItems([_t("Somar"), _t("Ida e volta")])
        mode.setCurrentIndex(1 if block.get("rotation_mode") == "ping_pong" else 0)
        linear_mode = QComboBox(); linear_mode.addItems([_t("Soma"), _t("Ida"), _t("Ida + volta")])
        linear_mode.setCurrentIndex({"accumulate": 0, "one_way": 1, "ping_pong": 2}.get(
            block.get("linear_mode", "ping_pong"), 2))
        angle = QDoubleSpinBox(); angle.setRange(0.1, 36000.0); angle.setDecimals(1); angle.setSuffix(" °")
        angle.setValue(float(block.get("angle_degrees", 360.0)))
        speed = QDoubleSpinBox(); speed.setRange(0.1, 1000000); speed.setSuffix(" mm/s"); speed.setValue(float(block.get("speed_mm_s", 100)))
        distance = QDoubleSpinBox(); distance.setRange(0.1, 1000000); distance.setSuffix(" mm"); distance.setValue(float(block.get("distance_mm", 100)))
        reps = QSpinBox(); reps.setRange(0, 1000000); reps.setSpecialValueText(_t("Infinito")); reps.setValue(int(block.get("repetitions", 0)))
        for spinbox in (delay, rpm, speed, distance, angle, reps):
            spinbox.installEventFilter(self._wheel_filter())
        def lock_button(tip, checked):
            # Ícone de linha no padrão do navegador: aberto/cinza para
            # editar, fechado/dourado quando o parâmetro está fixado.
            lock = QToolButton()
            lock.setCheckable(True)
            lock.setChecked(bool(checked))
            lock.setToolTip(tip)
            lock.setAutoRaise(True)
            lock.setIconSize(QSize(18, 18))
            root = Path(__file__).parent
            opened = QIcon(str(root / "icone_cadeado_aberto.svg"))
            closed = QIcon(str(root / "icone_cadeado_fechado.svg"))
            def sync_icon(is_locked):
                lock.setIcon(closed if is_locked else opened)
            sync_icon(lock.isChecked())
            lock.toggled.connect(sync_icon)
            return lock
        lock_name = lock_button(_t("Fixar nome"), locks.get("name", False))
        lock_delay = lock_button(_t("Fixar delay"), locks.get("delay", False))
        lock_kind = lock_button(_t("Fixar movimento"), locks.get("kind", False))
        lock_ref = lock_button(_t("Fixar referência"), locks.get("reference", False))
        lock_speed = lock_button(_t("Fixar velocidade"), locks.get("speed", False))
        lock_direction = lock_button(_t("Fixar sentido"), locks.get("direction", False))
        linear_lock_direction = lock_button(_t("Fixar sentido"), locks.get("direction", False))
        lock_distance = lock_button(_t("Fixar distância"), locks.get("distance", False))
        lock_mode = lock_button(_t("Fixar modo"), locks.get("mode", False))
        linear_lock_mode = lock_button(_t("Fixar modo"), locks.get("mode", False))
        lock_angle = lock_button(_t("Fixar ângulo"), locks.get("angle", False))
        lock_reps = lock_button(_t("Fixar repetição"), locks.get("repetitions", False))
        header_layout.insertWidget(2, lock_name)
        def with_lock(widget, lock):
            row = QWidget(); row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0); row_layout.setSpacing(2)
            row_layout.addWidget(widget, 1); row_layout.addWidget(lock)
            return row
        speed_row = QWidget(); speed_layout = QHBoxLayout(speed_row)
        speed_layout.setContentsMargins(0, 0, 0, 0); speed_layout.setSpacing(2)
        speed_layout.addWidget(rpm, 1); speed_layout.addWidget(speed, 1); speed_layout.addWidget(lock_speed)
        kind_row = with_lock(kind, lock_kind)
        form.addRow(_t("Movimento"), kind_row); form.addRow(_t("Delay"), with_lock(delay, lock_delay)); form.addRow(_t("Referência"), with_lock(axes, lock_ref))
        angle_row = with_lock(angle, lock_angle)
        distance_row = with_lock(distance, lock_distance)
        direction_row = with_lock(direction, lock_direction)
        linear_direction_row = with_lock(linear_direction, linear_lock_direction)
        mode_row = with_lock(mode, lock_mode)
        linear_mode_row = with_lock(linear_mode, linear_lock_mode)
        form.addRow("", capture); form.addRow(_t("Velocidade"), speed_row); form.addRow(_t("Sentido"), direction_row); form.addRow(_t("Sentido"), linear_direction_row); form.addRow(_t("Modo"), mode_row); form.addRow(_t("Modo"), linear_mode_row); form.addRow(_t("Ângulo"), angle_row); form.addRow(_t("Distância"), distance_row); form.addRow(_t("Repetição"), with_lock(reps, lock_reps))
        remove = QPushButton(_t("Remover bloco"))
        remove.setAutoDefault(False)
        remove.setDefault(False)
        remove.setStyleSheet("QPushButton { background: #9D3232; color: white; }")
        form.addRow("", remove)
        def update_header(opened=None):
            if opened is None:
                opened = expander.isChecked()
            expander.setText("▼" if opened else "▶")
            kind_label.setText("— " +
                               (_t("Deslocamento") if kind.currentIndex() else _t("Rotação")))
        def toggle(opened):
            body.setVisible(opened)
            if opened:
                self._expanded_blocks().add(block.get("id"))
            else:
                self._expanded_blocks().discard(block.get("id"))
            update_header(opened)
        expander.toggled.connect(toggle)
        card._pending_reference = None
        card._reference_changed_by_axes = False
        card._point_axis = point_axis
        card._points_available = points_available

        def commit(*_):
            return self._run_guard(
                f"salvar bloco {block.get('id')}",
                lambda: self._commit_card(block.get("id"), block_name, kind,
                                          delay, checks, point_axis, rpm, direction, linear_direction, mode, linear_mode,
                                          angle, speed, distance, reps,
                                          (lock_name, lock_kind, lock_delay,
                                           lock_ref, lock_speed, lock_direction,
                                           lock_distance, lock_mode, lock_angle,
                                           lock_reps),
                                          reference_changed=card._reference_changed_by_axes,
                                          reference_override=card._pending_reference,
                                          deferred=True))
        def reference_commit(*_):
            return self._run_guard(
                f"referência do bloco {block.get('id')}",
                lambda: self._commit_card(block.get("id"), block_name, kind,
                                          delay, checks, point_axis, rpm, direction, linear_direction, mode, linear_mode,
                                          angle, speed, distance, reps,
                                          (lock_name, lock_kind, lock_delay,
                                           lock_ref, lock_speed, lock_direction,
                                           lock_distance, lock_mode, lock_angle,
                                           lock_reps), reference_changed=True,
                                          deferred=True))
        def refresh_kind(index):
            linear = index == 1
            capture.setText(_t("Definir origem da peça") if linear
                            else _t("Definir eixo do movimento"))
            rpm.setVisible(not linear)
            speed.setVisible(linear)
            distance_row.setVisible(linear); form.labelForField(distance_row).setVisible(linear)
            direction_row.setVisible(not linear); form.labelForField(direction_row).setVisible(not linear)
            linear_direction_row.setVisible(linear); form.labelForField(linear_direction_row).setVisible(linear)
            mode_row.setVisible(not linear); form.labelForField(mode_row).setVisible(not linear)
            linear_mode_row.setVisible(linear); form.labelForField(linear_mode_row).setVisible(linear)
            angle_row.setVisible(not linear); form.labelForField(angle_row).setVisible(not linear)
            update_header()
        kind.currentIndexChanged.connect(refresh_kind)
        kind.currentIndexChanged.connect(commit)
        refresh_kind(kind.currentIndex())
        direction_row.setVisible(kind.currentIndex() == 0); form.labelForField(direction_row).setVisible(kind.currentIndex() == 0)
        linear_direction_row.setVisible(kind.currentIndex() == 1); form.labelForField(linear_direction_row).setVisible(kind.currentIndex() == 1)
        mode_row.setVisible(kind.currentIndex() == 0); form.labelForField(mode_row).setVisible(kind.currentIndex() == 0)
        linear_mode_row.setVisible(kind.currentIndex() == 1); form.labelForField(linear_mode_row).setVisible(kind.currentIndex() == 1)
        angle_row.setVisible(kind.currentIndex() == 0); form.labelForField(angle_row).setVisible(kind.currentIndex() == 0)
        # Valores são salvos automaticamente após uma breve pausa na edição.
        block_name.textChanged.connect(lambda *_: update_header())
        block_name.editingFinished.connect(commit)
        for _widget, signal in ((delay, delay.valueChanged),
                                (rpm, rpm.valueChanged),
                                (direction, direction.currentIndexChanged),
                                (linear_direction, linear_direction.currentIndexChanged),
                                (mode, mode.currentIndexChanged),
                                (linear_mode, linear_mode.currentIndexChanged),
                                (angle, angle.valueChanged),
                                (speed, speed.valueChanged),
                                (distance, distance.valueChanged),
                                (reps, reps.valueChanged)):
            signal.connect(commit)
        def axes_changed(*_):
            point_axis.blockSignals(True)
            point_axis.setChecked(False)
            point_axis.blockSignals(False)
            card._pending_reference = None
            card._reference_changed_by_axes = True
        for check in checks:
            check.toggled.connect(axes_changed)
        for check in checks:
            check.toggled.connect(reference_commit)
        def point_axis_changed(checked):
            if checked:
                card._reference_changed_by_axes = False
            else:
                card._pending_reference = None
                card._reference_changed_by_axes = True
            commit()
        point_axis.toggled.connect(point_axis_changed)
        lock_name.toggled.connect(lambda locked: (block_name.setEnabled(not locked), commit()))
        lock_kind.toggled.connect(lambda locked: (kind.setEnabled(not locked), commit()))
        lock_delay.toggled.connect(lambda locked: (delay.setEnabled(not locked), commit()))
        lock_speed.toggled.connect(lambda locked: (rpm.setEnabled(not locked), speed.setEnabled(not locked), commit()))
        def set_direction_locked(locked):
            for lock in (lock_direction, linear_lock_direction):
                if lock.isChecked() != locked:
                    lock.blockSignals(True)
                    lock.setChecked(locked)
                    lock.blockSignals(False)
            direction.setEnabled(not locked)
            linear_direction.setEnabled(not locked)
            commit()
        lock_direction.toggled.connect(set_direction_locked)
        linear_lock_direction.toggled.connect(set_direction_locked)
        lock_distance.toggled.connect(lambda locked: (distance.setEnabled(not locked), commit()))
        def set_mode_locked(locked):
            for lock in (lock_mode, linear_lock_mode):
                if lock.isChecked() != locked:
                    lock.blockSignals(True)
                    lock.setChecked(locked)
                    lock.blockSignals(False)
            mode.setEnabled(not locked)
            linear_mode.setEnabled(not locked)
            commit()
        lock_mode.toggled.connect(set_mode_locked)
        linear_lock_mode.toggled.connect(set_mode_locked)
        lock_angle.toggled.connect(lambda locked: (angle.setEnabled(not locked), commit()))
        lock_reps.toggled.connect(lambda locked: (reps.setEnabled(not locked), commit()))
        lock_ref.toggled.connect(lambda locked: ([check.setEnabled(not locked) for check in checks], capture.setEnabled(not locked), point_axis.setEnabled(card._points_available and not locked), commit()))
        block_name.setEnabled(not lock_name.isChecked()); kind.setEnabled(not lock_kind.isChecked()); delay.setEnabled(not lock_delay.isChecked()); rpm.setEnabled(not lock_speed.isChecked()); speed.setEnabled(not lock_speed.isChecked()); direction.setEnabled(not lock_direction.isChecked()); linear_direction.setEnabled(not lock_direction.isChecked()); distance.setEnabled(not lock_distance.isChecked()); mode.setEnabled(not lock_mode.isChecked()); linear_mode.setEnabled(not lock_mode.isChecked()); angle.setEnabled(not lock_angle.isChecked()); reps.setEnabled(not lock_reps.isChecked())
        for check in checks: check.setEnabled(not lock_ref.isChecked())
        point_axis.setEnabled(card._points_available and not lock_ref.isChecked())
        capture.setEnabled(not lock_ref.isChecked())
        capture.clicked.connect(
            lambda: self._run_guard("definir referência na cena",
                                    lambda: self._capture_block(block.get("id"), card, commit)))
        remove.clicked.connect(
            lambda: self._run_guard("remover bloco",
                                    lambda: self._remove_block(block.get("id"))))
        update_header(expander.isChecked())
        # Primeiro adote o corpo no cartão. Torná-lo visível antes de
        # adicioná-lo ao layout o faz nascer por um instante como uma janela
        # de topo sem título — o "IngeTrazo" vazio que piscava na tela.
        outer.addWidget(body)
        body.setVisible(expander.isChecked())
        return card

    def _block_selected(self, index):
        if self._updating or self._selected is None or index < 0:
            return
        blocks = self._blocks_entry(self._saved()["motors"].get(self._selected.uid))
        if index < len(blocks):
            self._active_block_id = blocks[index].get("id")
            self._load_current_motion()

    def _commit_card(self, block_id, name_widget, kind_widget, delay, checks, point_axis, rpm, direction, linear_direction, mode, linear_mode, angle, speed, distance, reps, locks,
                     reference_changed=False, reference_override=None,
                     deferred=False):
        if self._selected is None or self._updating or self._building_cards:
            return
        data = self._saved()
        blocks = self._blocks_entry(data["motors"].get(self._selected.uid))
        block = next((item for item in blocks if item.get("id") == block_id), None)
        if block is None:
            return
        axis_direction = [float(check.isChecked()) for check in checks]
        if not any(axis_direction):
            axis_direction[2] = 1.0
        # Alterar os eixos é uma nova referência e portanto prevalece sobre
        # qualquer captura anterior de dois pontos.
        block.update(name=name_widget.text().strip() or f"Bloco {self._blocks_entry(data['motors'].get(self._selected.uid)).index(block) + 1}",
                     kind="linear" if kind_widget.currentIndex() else "rotation",
                     delay_s=float(delay.value()), rpm=float(rpm.value()),
                     direction=1 if direction.currentIndex() == 0 else -1,
                     linear_direction=1 if linear_direction.currentIndex() == 0 else -1,
                     rotation_mode="ping_pong" if mode.currentIndex() else "accumulate",
                     linear_mode=("accumulate", "one_way", "ping_pong")[linear_mode.currentIndex()],
                     angle_degrees=float(angle.value()),
                     speed_mm_s=float(speed.value()), distance_mm=float(distance.value()), repetitions=int(reps.value()),
                     locks={"name": locks[0].isChecked(), "kind": locks[1].isChecked(),
                            "delay": locks[2].isChecked(), "reference": locks[3].isChecked(),
                            "speed": locks[4].isChecked(), "direction": locks[5].isChecked(),
                            "distance": locks[6].isChecked(), "mode": locks[7].isChecked(),
                            "angle": locks[8].isChecked(), "repetitions": locks[9].isChecked()})
        if reference_override is not None:
            point_a, point_b = reference_override
            direction_vector = [point_b[i] - point_a[i] for i in range(3)]
            length = math.sqrt(sum(value * value for value in direction_vector))
            if length > 1e-9:
                axis_direction = [value / length for value in direction_vector]
            block.update(axis=axis_direction, axis_a=point_a, axis_b=point_b,
                         reference_mode="points")
        elif point_axis.isChecked() and block.get("reference_mode") == "points":
            # Reativa o eixo A/B já capturado, sem alterar seus pontos.
            block["reference_mode"] = "points"
        elif reference_changed:
            block.update(axis=axis_direction, axis_a=[0.0, 0.0, 0.0], axis_b=axis_direction,
                         reference_mode="axes")
        data["version"] = 3
        data["motors"][self._selected.uid] = {"blocks": blocks}
        if deferred:
            self._queue_document_save(data)
        else:
            self._writing_automation = True
            try:
                self.app.set_document_data(data)
            finally:
                self._writing_automation = False
        self._loaded_config = copy.deepcopy(block)
        for motor in self._motors:
            if motor["group"] is self._selected:
                self._apply_runtime_motion(motor, self._selected,
                                           block["kind"], block)
        if self._preview:
            self._version = self.app.scene.version
        self._refresh_count()
        if not deferred:
            self.viewport.flash_status(_t("Bloco salvo."))

    def _capture_block(self, block_id, card, on_ready=None):
        # A leitura da seleção no início da captura reconstrói os cartões.
        # Portanto não guarde widgets aqui: após o segundo clique eles já
        # podem ter sido destruídos. O ID do bloco permanece estável.
        self._active_block_id = block_id
        self._flush_document_save()
        self._capture_target = block_id
        self._load_current_motion()
        self.pick_axis()

    def _remove_block(self, block_id):
        self._active_block_id = block_id
        self.remove_motor()

    def add_block(self):
        group = self._read_selection()
        if group is None:
            return
        self._flush_document_save()
        data = self._saved()
        blocks = self._blocks_entry(data["motors"].get(group.uid))
        block = self._new_block()
        blocks.append(block)
        data["version"] = 3
        data["motors"][group.uid] = {"blocks": blocks}
        self._active_block_id = block["id"]
        # O cartão novo abre sem alterar os cartões já recolhidos.
        self._expanded_blocks().add(block["id"])
        self._writing_automation = True
        try:
            self.app.set_document_data(data)
        finally:
            self._writing_automation = False
        self._refresh_blocks()
        self._load_current_motion()

    def _move_block(self, offset):
        if self._selected is None:
            return
        self._flush_document_save()
        data = self._saved()
        blocks = self._blocks_entry(data["motors"].get(self._selected.uid))
        index = next((i for i, block in enumerate(blocks)
                      if block.get("id") == self._active_block_id), -1)
        target = index + offset
        if index < 0 or target < 0 or target >= len(blocks):
            return
        blocks[index], blocks[target] = blocks[target], blocks[index]
        data["motors"][self._selected.uid] = {"blocks": blocks}
        self.app.set_document_data(data)
        self._refresh_blocks()

    def _kind_name(self):
        return "linear" if self.kind.currentIndex() == 1 else "rotation"

    def _axes_changed(self, *_):
        if self._updating or self.lock_reference.isChecked():
            return
        direction = QVector3D(float(self.axis_x.isChecked()),
                              float(self.axis_y.isChecked()),
                              float(self.axis_z.isChecked()))
        if direction.length() < 1e-6:
            self.axis_z.setChecked(True)
            return
        self._axis_a = QVector3D(0, 0, 0)
        self._axis_b = direction.normalized()
        self._auto_save()

    def _lock_changed(self, locked):
        for axis in (self.axis_x, self.axis_y, self.axis_z):
            axis.setEnabled(not locked)
        self.pick_button.setEnabled(not locked)

    def _speed_lock_changed(self, locked):
        self.rpm.setEnabled(not locked)
        self.speed.setEnabled(not locked)

    @staticmethod
    def _new_block(kind="rotation"):
        return {"id": uuid.uuid4().hex, "kind": kind,
                "axis_a": [0.0, 0.0, 0.0], "axis_b": [0.0, 0.0, 1.0],
                "reference_mode": "axes", "axis": [0.0, 0.0, 1.0],
                "delay_s": 0.0, "rpm": 30.0, "direction": 1, "linear_direction": 1,
                "rotation_mode": "accumulate",
                "linear_mode": "ping_pong",
                "angle_degrees": 360.0,
                "speed_mm_s": 100.0, "distance_mm": 100.0, "repetitions": 0,
                "locks": {"name": False, "kind": False, "delay": False, "reference": False,
                          "speed": False, "direction": False, "distance": False,
                          "mode": False, "angle": False,
                          "repetitions": False}}

    @classmethod
    def _blocks_entry(cls, entry):
        """Lê V1/V2 e devolve a lista ordenada usada pela versão de blocos."""
        if not isinstance(entry, dict):
            return []
        if isinstance(entry.get("blocks"), list):
            return [block for block in entry["blocks"] if isinstance(block, dict)]
        blocks = []
        for kind in ("rotation", "linear"):
            spec = cls._motion_spec(entry, kind)
            if isinstance(spec, dict):
                block = cls._new_block(kind)
                block.update(spec)
                block["id"] = uuid.uuid4().hex
                block["kind"] = kind
                blocks.append(block)
        return blocks

    @staticmethod
    def _motion_spec(entry, kind):
        """Lê o formato atual e também os documentos da primeira versão."""
        if not isinstance(entry, dict):
            return None
        if kind in entry and isinstance(entry[kind], dict):
            return entry[kind]
        # V1: cada componente tinha diretamente uma única configuração kind.
        if entry.get("kind", "rotation") == kind and "axis_a" in entry:
            return entry
        return None

    @staticmethod
    def _motions_entry(entry):
        """Converte uma entrada V1 em recipiente de rotação/linear ao salvar."""
        if not isinstance(entry, dict):
            return {}
        if "rotation" in entry or "linear" in entry:
            return {key: value for key, value in entry.items()
                    if key in ("rotation", "linear") and isinstance(value, dict)}
        kind = entry.get("kind", "rotation")
        return {kind: entry} if kind in ("rotation", "linear") else {}

    def _type_changed(self):
        if getattr(self, "_legacy_hidden", False):
            return
        linear = self.kind.currentIndex() == 1
        for widget in (self.rpm, self.rpm_label, self.direction,
                       self.direction_label):
            widget.setVisible(not linear)
        for widget in (self.speed, self.speed_label, self.repetitions,
                       self.repetitions_label):
            widget.setVisible(linear)
        self.pick_button.setText(_t("Definir trajetória A e B") if linear
                                 else _t("Definir eixo por 2 pontos"))
        if not self._updating and self._selected is not None:
            self._load_current_motion()

    def _load_current_motion(self):
        """Mostra somente o tipo de movimento escolhido para a peça atual."""
        group = self._selected
        if group is None:
            return
        blocks = self._blocks_entry(self._saved()["motors"].get(group.uid))
        block = next((item for item in blocks
                      if item.get("id") == self._active_block_id), None)
        if block is None and blocks:
            block = blocks[0]
            self._active_block_id = block.get("id")
        kind = block.get("kind", "rotation") if block else self._kind_name()
        spec = block
        self._loaded_config = spec
        self._updating = True
        try:
            if spec:
                self.kind.setCurrentIndex(1 if kind == "linear" else 0)
                self.delay.setValue(float(spec.get("delay_s", 0.0)))
                axis = spec.get("axis", [0.0, 0.0, 1.0])
                self.axis_x.setChecked(bool(axis[0]))
                self.axis_y.setChecked(bool(axis[1]))
                self.axis_z.setChecked(bool(axis[2]))
                self.lock_reference.setChecked(
                    bool(spec.get("locks", {}).get("reference", False)))
                self.lock_delay.setChecked(bool(spec.get("locks", {}).get("delay", False)))
                self.lock_speed.setChecked(bool(spec.get("locks", {}).get("speed", False)))
                self.lock_repetitions.setChecked(
                    bool(spec.get("locks", {}).get("repetitions", False)))
                self._axis_a = _point(spec["axis_a"])
                self._axis_b = _point(spec["axis_b"])
                if kind == "rotation":
                    self.rpm.setValue(float(spec.get("rpm", 30)))
                    self.direction.setCurrentIndex(
                        0 if spec.get("direction", 1) == 1 else 1)
                else:
                    self.speed.setValue(float(spec.get("speed_mm_s", 100)))
                    self.repetitions.setValue(int(spec.get("repetitions", 0)))
            else:
                self._axis_a = self._axis_b = None
                self.delay.setValue(0.0)
                self.axis_x.setChecked(False)
                self.axis_y.setChecked(False)
                self.axis_z.setChecked(True)
                self.lock_reference.setChecked(False)
                self.lock_delay.setChecked(False)
                self.lock_speed.setChecked(False)
                self.lock_repetitions.setChecked(False)
                if kind == "rotation":
                    self.rpm.setValue(30.0)
                    self.direction.setCurrentIndex(0)
                else:
                    self.speed.setValue(100.0)
                    self.repetitions.setValue(0)
        finally:
            self._updating = False
        noun = _t("Trajetória") if kind == "linear" else _t("Eixo")
        self.axis_label.setText(_t("{noun}: definido", noun=noun)
                                if self._axis_b is not None
                                else _t("{noun}: não definido", noun=noun))
        self.config_label.setText(
            "Configuração: movimento salvo" if spec else "Configuração: sem movimento")

    def show(self):
        self._read_selection()
        self.dialog.show()

    def dispose(self):
        """Desliga uma instância anterior ao recarregar a extensão.

        O host pode executar setup() novamente sem destruir automaticamente
        os QTimers da versão anterior. Dois controladores disputando a mesma
        seleção levam a reconstruções e a avisos vazios transitórios.
        """
        for name in ("timer", "selection_timer", "_save_timer"):
            timer = getattr(self, name, None)
            if timer is not None:
                try:
                    timer.stop()
                except Exception:
                    pass
        dialog = getattr(self, "dialog", None)
        if dialog is not None:
            try:
                dialog.hide()
            except Exception:
                pass
        guard = getattr(self, "_blank_dialog_guard", None)
        if guard is not None:
            try:
                QApplication.instance().removeEventFilter(guard)
                guard._scan_timer.stop()
                guard.deleteLater()
            except Exception:
                pass
        trace = getattr(self, "_window_trace", None)
        if trace is not None:
            try:
                QApplication.instance().removeEventFilter(trace)
                trace.deleteLater()
            except Exception:
                pass
        self._debug("controlador descartado após recarregamento")

    def _selection_changed(self):
        if self._picking is not None:
            return
        selection = self.app.scene.selection
        item = next(iter(selection)) if len(selection) == 1 else None
        # A API pode devolver um novo wrapper Python para o mesmo componente
        # em cada consulta. id(item) então muda a cada poll e reconstrói os
        # cartões continuamente, interrompendo cliques/campos e podendo
        # acionar a janela de erro vazia do host. uid é estável no documento.
        token = (id(self.app.scene), len(selection),
                 getattr(item, "uid", None) if item is not None else None)
        if token != self._selection_token:
            self._selection_token = token
            self._debug(f"seleção mudou: {token[2] or 'nenhuma'}")
            self._read_selection()

    def _read_selection(self):
        selection = list(self.app.scene.selection)
        group = selection[0] if len(selection) == 1 else None
        if not (isinstance(group, Group) and group in self.app.scene.groups
                and group.is_component()):
            self._selected = None
            self._loaded_config = None
            self._axis_a = self._axis_b = None
            self.selection_label.setText(_t("Componente: selecione apenas um componente"))
            self.config_label.setText(_t("Configuração: nenhuma"))
            self.axis_label.setText(_t("Eixo: não definido"))
            self.remove_button.setEnabled(False)
            self._refresh_component_list()
            return None
        selected_uid = getattr(self._selected, "uid", None)
        if group.uid != selected_uid:
            self._active_block_id = None
            self._selected = group
            self._load_current_motion()
        else:
            # Mantém o wrapper atual do host, sem tratar o mesmo componente
            # como uma nova seleção e sem recriar os cartões.
            self._selected = group
        entry = self._saved()["motors"].get(group.uid)
        self.remove_button.setEnabled(bool(self._blocks_entry(entry)))
        self._refresh_component_list()
        self._refresh_blocks()
        self.selection_label.setText(_t("Componente: {name}", name=group.name))
        return group

    def pick_axis(self):
        if self.lock_reference.isChecked():
            self.viewport.flash_status(_t("A referência deste bloco está travada."))
            return
        group = self._read_selection()
        if group is None:
            self.viewport.flash_status(_t("Selecione um componente primeiro."))
            return
        self.stop()
        controller = self

        class AxisPickTool(Tool):
            name = _t("Eixo da automação")
            description = _t("Clique em dois pontos para definir a direção do movimento.")

            def __init__(self):
                # World-space start point used by IngeTrazo's native snap,
                # free-point raycast, rubber band and X/Y/Z arrow locks.
                self.start_point = None
                self.hover_point = None

            def on_activate(self, viewport):
                viewport.flash_status(_t("Automação: clique no ponto A."))

            def on_deactivate(self, viewport):
                controller._picking = None
                self.hover_point = None

            def on_hover(self, ctx):
                self.hover_point = QVector3D(ctx.world)
                ctx.viewport.update()

            def on_click(self, ctx):
                world = QVector3D(ctx.world)
                inverse, invertible = group.xform.inverted()
                if not invertible:
                    ctx.viewport.flash_status(_t("A transformação do componente não é invertível."))
                    return
                local = inverse.map(world)
                if controller._axis_a is None:
                    controller._axis_a = local
                    self.start_point = QVector3D(world)
                    controller.axis_label.setText(_t("Marque o ponto B"))
                    ctx.viewport.flash_status(_t("Automação: marque o ponto B. Setas: direita = X, esquerda = Y, cima = Z."))
                    ctx.viewport.update()
                    return
                if (local - controller._axis_a).length() < 1e-6:
                    ctx.viewport.flash_status(_t("O eixo precisa de dois pontos diferentes."))
                    return
                controller._axis_b = local
                controller.axis_label.setText(
                    _t("Pontos A e B definidos; salvando referência"))
                controller._finish_picking()
                controller._store_captured_reference()

            def on_cancel(self, viewport):
                controller._capture_target = None
                controller._finish_picking()

            def rubber_band_lines(self):
                if self.start_point is None or self.hover_point is None:
                    return []
                return [(self.start_point, self.hover_point)]

        self._axis_a = self._axis_b = None
        self.axis_label.setText(_t("Marque o ponto A"))
        self._previous_tool = self.viewport.active_tool
        self._picking = AxisPickTool()
        self.viewport.set_active_tool(self._picking)
        self.viewport.setFocus(Qt.OtherFocusReason)

    def _store_captured_reference(self):
        """Mantém A/B no cartão até o usuário confirmar Salvar bloco."""
        target = getattr(self, "_capture_target", None)
        self._capture_target = None
        if target is None or self._axis_a is None or self._axis_b is None:
            return
        block_id = target[0] if isinstance(target, tuple) else target
        data = self._saved()
        blocks = self._blocks_entry(data["motors"].get(self._selected.uid))
        block = next((item for item in blocks if item.get("id") == block_id), None)
        if block is None:
            self.viewport.flash_status(_t("Não foi possível encontrar o bloco capturado."))
            return
        point_a, point_b = _vec(self._axis_a), _vec(self._axis_b)
        direction = [point_b[i] - point_a[i] for i in range(3)]
        length = math.sqrt(sum(value * value for value in direction))
        if length <= 1e-9:
            self.viewport.flash_status(_t("O eixo precisa de dois pontos diferentes."))
            return
        block.update(axis=[value / length for value in direction],
                     axis_a=point_a, axis_b=point_b,
                     reference_mode="points")
        data["version"] = 3
        data["motors"][self._selected.uid] = {"blocks": blocks}
        self._writing_automation = True
        try:
            self.app.set_document_data(data)
        finally:
            self._writing_automation = False
        # O cartão reconstruído lê reference_mode=points e já nasce com o
        # quarto eixo habilitado e marcado.
        self._refresh_blocks()
        self.viewport.flash_status(_t("Referência definida e salva."))

    def _finish_picking(self):
        prior = self._previous_tool
        self._previous_tool = None
        self._picking = None
        if prior is not None:
            self.viewport.set_active_tool(prior)
        else:
            # Sem uma ferramenta anterior, retorne explicitamente ao seletor.
            # Deixar AxisPickTool ativa faria cliques/teclas futuros parecerem
            # uma nova definição de eixo.
            activate = getattr(self.app.window, "_activate_tool", None)
            if callable(activate):
                activate("select")
        self.viewport.update()

    def _auto_save(self, *_):
        if not self._updating:
            self.save_motor(silent=True)

    def save_motor(self, silent=False):
        group = self._read_selection()
        if group is None or self._axis_a is None or self._axis_b is None:
            if not silent:
                self.viewport.flash_status(_t("Selecione um componente e defina os pontos A e B."))
            return
        self._flush_document_save()
        data = self._saved()
        spec = {
            "axis_a": _vec(self._axis_a), "axis_b": _vec(self._axis_b),
            "delay_s": float(self.delay.value()),
            "axis": [float(self.axis_x.isChecked()), float(self.axis_y.isChecked()),
                     float(self.axis_z.isChecked())],
            "locks": {"reference": self.lock_reference.isChecked(),
                      "delay": self.lock_delay.isChecked(),
                      "speed": self.lock_speed.isChecked(),
                      "repetitions": self.lock_repetitions.isChecked()},
        }
        if self.kind.currentIndex() == 1:
            spec.update(kind="linear", speed_mm_s=float(self.speed.value()),
                        repetitions=int(self.repetitions.value()))
        else:
            spec.update(kind="rotation", rpm=float(self.rpm.value()),
                        direction=1 if self.direction.currentIndex() == 0 else -1)
        kind = self._kind_name()
        blocks = self._blocks_entry(data["motors"].get(group.uid))
        block = next((item for item in blocks
                      if item.get("id") == self._active_block_id), None)
        if block is None:
            block = self._new_block(kind)
            blocks.append(block)
            self._active_block_id = block["id"]
        spec["locks"]["name"] = bool(block.get("locks", {}).get("name", False))
        spec["locks"]["kind"] = bool(block.get("locks", {}).get("kind", False))
        spec["locks"]["distance"] = bool(block.get("locks", {}).get("distance", False))
        spec["locks"]["direction"] = bool(block.get("locks", {}).get("direction", False))
        if kind == "rotation":
            # A captura de referência usa o editor legado, que não exibe
            # modo/ângulo. Preserve os valores definidos no cartão.
            spec["rotation_mode"] = block.get("rotation_mode", "accumulate")
            spec["angle_degrees"] = float(block.get("angle_degrees", 360.0))
            spec["locks"]["mode"] = bool(block.get("locks", {}).get("mode", False))
            spec["locks"]["angle"] = bool(block.get("locks", {}).get("angle", False))
        block.update(spec)
        block["kind"] = kind
        data["version"] = 3
        data["motors"][group.uid] = {"blocks": blocks}
        self._loaded_config = block
        # Salvar um ajuste não encerra a prévia. Enquanto ela está ativa,
        # os parâmetros do motor em execução recebem o valor imediatamente.
        for motor in self._motors:
            if motor["group"] is group:
                self._apply_runtime_motion(motor, group, kind, block)
        self._writing_automation = True
        try:
            self.app.set_document_data(data)
        finally:
            self._writing_automation = False
        if self._preview:
            self._version = self.app.scene.version
        self._refresh_count()
        self._refresh_blocks()
        self.config_label.setText(_t("Configuração: movimento salvo"))
        self.remove_button.setEnabled(True)
        if not silent:
            self.viewport.flash_status(_t("Movimento salvo para {name}.", name=group.name))

    def remove_motor(self):
        group = self._read_selection()
        if group is None:
            return
        self.stop()
        self._flush_document_save()
        data = self._saved()
        blocks = self._blocks_entry(data["motors"].get(group.uid))
        blocks = [block for block in blocks
                  if block.get("id") != self._active_block_id]
        if blocks:
            data["motors"][group.uid] = {"blocks": blocks}
            self._active_block_id = blocks[0].get("id")
        elif group.uid in data["motors"]:
            del data["motors"][group.uid]
            self._active_block_id = None
        self.app.set_document_data(data)
        self._axis_a = self._axis_b = None
        self._loaded_config = None
        self.axis_label.setText(_t("Eixo: não definido"))
        self.config_label.setText(_t("Configuração: sem movimento"))
        self.remove_button.setEnabled(False)
        self._refresh_blocks()
        if self._active_block_id is not None:
            self._load_current_motion()
        self._refresh_count()

    def _configured(self):
        config = self._saved()["motors"]
        output = []
        for group in self.app.scene.groups:
            if not group.is_component() or group.uid not in config:
                continue
            motor = {"group": group, "blocks": []}
            for block in self._blocks_entry(config[group.uid]):
                runtime = self._runtime_motion(group, block.get("kind"), block)
                if runtime is not None:
                    runtime["kind"] = block.get("kind")
                    runtime["id"] = block.get("id")
                    runtime["delay_s"] = float(block.get("delay_s", 0.0))
                    runtime["pause_s"] = runtime["delay_s"]
                    motor["blocks"].append(runtime)
            if motor["blocks"]:
                output.append(motor)
        return output

    def _runtime_motion(self, group, kind, spec):
        """Transforma uma configuração salva em estado de execução no mundo."""
        if not isinstance(spec, dict):
            return None
        try:
            a = group.xform.map(_point(spec["axis_a"]))
            b = group.xform.map(_point(spec["axis_b"]))
            if (b - a).length() < 1e-6:
                return None
            if kind == "rotation":
                rpm = float(spec["rpm"])
                angle_degrees = float(spec.get("angle_degrees", 360.0))
                if (not math.isfinite(rpm) or rpm <= 0 or
                        not math.isfinite(angle_degrees) or angle_degrees <= 0):
                    return None
                return {"a": a, "b": b, "rpm": rpm,
                        "sign": 1 if int(spec.get("direction", 1)) == 1 else -1,
                        "cycle_degrees": angle_degrees,
                        "rotation_mode": spec.get("rotation_mode", "accumulate"),
                        "leg": 0,
                        "angle": 0.0, "turn_progress": 0.0,
                        "repetitions": int(spec.get("repetitions", 0)),
                        "cycles_done": 0, "done": False}
            speed = float(spec["speed_mm_s"])
            if not math.isfinite(speed) or speed <= 0:
                return None
            distance_mm = float(spec.get("distance_mm", (b - a).length() * 1000.0))
            if not math.isfinite(distance_mm) or distance_mm <= 0:
                return None
            b = a + (b - a).normalized() * (distance_mm / 1000.0)
            if int(spec.get("linear_direction", 1)) != 1:
                a, b = b, a
            return {"a": a, "b": b, "speed_mm_s": speed,
                    # Documentos antigos sempre executavam ida e volta.
                    "linear_mode": spec.get("linear_mode", "ping_pong"),
                    "repetitions": int(spec.get("repetitions", 0)),
                    "distance_mm": 0.0, "phase": 0.0,
                    "cycles_done": 0, "done": False, "reset_next": False}
        except (KeyError, TypeError, ValueError):
            return None

    def _apply_runtime_motion(self, motor, group, kind, spec):
        """Aplica um ajuste salvo à prévia ativa, sem reiniciar o Play."""
        runtime = self._runtime_motion(group, kind, spec)
        if runtime is not None:
            runtime["kind"] = kind
            runtime["id"] = spec.get("id")
            runtime["delay_s"] = float(spec.get("delay_s", 0.0))
            runtime["pause_s"] = runtime["delay_s"]
            old = next((item for item in motor.get("blocks", [])
                        if item.get("id") == runtime["id"]), None)
            if old is not None:
                # Mantém a fase atual ao ajustar apenas velocidade ou sentido.
                for field in ("angle", "distance_mm", "phase", "done", "reset_next",
                              "turn_progress", "cycles_done", "leg"):
                    if field in old:
                        runtime[field] = old[field]
                runtime["pause_s"] = old.get("pause_s", 0.0)
            if old is None:
                motor.setdefault("blocks", []).append(runtime)
            else:
                motor["blocks"][motor["blocks"].index(old)] = runtime

    def play_pause(self):
        if self._playing:
            self.pause()
            return
        self.play_forward()

    def _ensure_preview(self):
        if not self._preview:
            motors = self._configured()
            if not motors:
                self.viewport.flash_status(_t("Configure e salve pelo menos um movimento."))
                return False
            try:
                self._begin_preview(motors)
            except Exception as exc:
                self.stop()
                self.viewport.flash_status(_t("Não foi possível iniciar a prévia: {error}", error=exc))
                return False
        return True

    def play_forward(self):
        if not self._ensure_preview():
            return
        self._play_direction = 1
        self._playing = True
        self._last_tick = time.monotonic()
        self.status_label.setText(
            _t("Em movimento: {count} peça(s)", count=len(self._motors)))
        self.timer.start()

    def play_reverse(self):
        if not self._ensure_preview():
            return
        if self._timeline_s <= 0.0:
            self.status_label.setText(_t("Início da animação"))
            return
        self._play_direction = -1
        self._playing = True
        self._last_tick = time.monotonic()
        self.status_label.setText(_t("Em retrocesso"))
        self.timer.start()

    def pause(self):
        if not self._preview:
            return
        self._playing = False
        self.timer.stop()
        self.status_label.setText(_t("Pausado"))

    def step_forward(self):
        if self._ensure_preview():
            self.pause()
            duration = float(self.step_size.value())
            target = self._timeline_s + duration
            self._debug(f"passo frente: {self._timeline_s:.3f}s + {duration:.3f}s -> {target:.3f}s")
            self._seek(target)

    def step_back(self):
        if self._ensure_preview():
            self.pause()
            target = max(0.0, self._timeline_s - self.step_size.value())
            self._debug(f"passo atrás: {self._timeline_s:.3f}s -> {target:.3f}s")
            self._seek(target)

    def _begin_preview(self, motors):
        vp = self.viewport
        self._scene = self.app.scene
        self._version = self.app.scene.version
        self._motors = motors
        self._preview = True
        self._timeline_s = 0.0
        self._debug(f"prévia iniciada: {len(motors)} componente(s)")
        vp.begin_groups_preview([motor["group"] for motor in motors])
        self._original_draw = vp._draw_groups_preview
        vp.makeCurrent()
        try:
            for motor in motors:
                movers = []
                vp._expand_placements(motor["group"], movers)
                edges, colors, textures = [], [], {}
                for placement in movers:
                    if getattr(placement, "billboard", False):
                        continue
                    chunk = vp._group_chunk(placement)
                    if chunk["edges"]:
                        edges.append(chunk["edges"])
                    if chunk["vcol"]:
                        colors.append(chunk["vcol"])
                    for key, raw in chunk["by_texture"].items():
                        textures.setdefault(key, []).append(raw)
                scratch = {}
                for name, parts, create, divisor in (
                    ("edges", edges, vp._create_dynamic, 12),
                    ("vcol", colors, vp._create_dynamic_vcol, 24),
                ):
                    vao, vbo = create()
                    raw = b"".join(parts)
                    vbo.bind()
                    vbo.allocate(raw or b"\0" * 24, max(len(raw), 24))
                    vbo.release()
                    scratch[name] = (vao, vbo, len(raw) // divisor)
                vao, vbo = vp._create_dynamic_uv()
                runs, parts, offset = [], [], 0
                for key, blobs in textures.items():
                    raw = b"".join(blobs)
                    runs.append((key, offset // 20, len(raw) // 20))
                    parts.append(raw)
                    offset += len(raw)
                raw = b"".join(parts)
                vbo.bind()
                vbo.allocate(raw or b"\0" * 24, max(len(raw), 24))
                vbo.release()
                scratch["tex"] = (vao, vbo, runs)
                motor["scratch"] = scratch
        finally:
            vp.doneCurrent()
        vp._draw_groups_preview = self._draw_motors
        vp.update()

    def _draw_motors(self, mvp):
        vp = self.viewport
        try:
            for motor in self._motors:
                scratch = motor["scratch"]
                matrix = QMatrix4x4()
                for block in motor["blocks"]:
                    if block["kind"] == "linear":
                        matrix.translate((block["b"] - block["a"]) * block["phase"])
                    else:
                        matrix = matrix * _rotation(
                            block["a"], block["b"], block["angle"])
                vp._program.setUniformValue(vp._loc_mvp, mvp * matrix)
                vao, _, count = scratch["vcol"]
                if count:
                    vp._program.setUniformValue(vp._loc_use_vcolor, 1)
                    vao.bind()
                    vp._gl.glDrawArrays(0x0004, 0, count)  # GL_TRIANGLES
                    vao.release()
                    vp._program.setUniformValue(vp._loc_use_vcolor, 0)
                vao, _, runs = scratch["tex"]
                if runs:
                    vp._program.setUniformValue(vp._loc_use_tex, 1)
                    vao.bind()
                    for key, start, count in runs:
                        path, shade = key if isinstance(key, tuple) else (key, 1.0)
                        tex = vp._get_texture(path)
                        if tex is None:
                            continue
                        vp._program.setUniformValue1f(vp._loc_shade, float(shade))
                        vp._program.setUniformValue(
                            vp._loc_hard_cutout, 1 if getattr(tex, "_cutout", False) else 0)
                        tex.bind(0)
                        vp._gl.glDrawArrays(0x0004, start, count)
                        tex.release(0)
                    vao.release()
                    vp._program.setUniformValue1f(vp._loc_shade, 1.0)
                    vp._program.setUniformValue(vp._loc_hard_cutout, 0)
                    vp._program.setUniformValue(vp._loc_use_tex, 0)
                vao, _, count = scratch["edges"]
                if count:
                    vp._set_color(1.0, 0.45, 0.0, 1.0)
                    vao.bind()
                    vp._gl.glDrawArrays(0x0001, 0, count)  # GL_LINES
                    vao.release()
        finally:
            vp._program.setUniformValue(vp._loc_mvp, mvp)

    def _tick(self):
        if not self._preview or not self._playing:
            return
        if (self.app.scene is not self._scene or
                self.app.scene.version != self._version or
                any(m["group"] not in self.app.scene.groups for m in self._motors)):
            self._debug("prévia interrompida: cena, versão ou componente mudou")
            self.stop()
            return
        now = time.monotonic()
        dt = min(max(now - self._last_tick, 0.0), 0.25)
        self._last_tick = now
        if self._play_direction < 0:
            target = max(0.0, self._timeline_s - dt)
            self._seek(target)
            if target <= 0.0:
                self.pause()
            return
        self._timeline_s += dt
        # No Play normal o tempo avança aqui (sem passar por _seek), então o
        # relógio precisa ser atualizado a cada tick sem trocar o status de
        # execução exibido na barra inferior.
        self._update_timeline_clock()
        if not self._advance(dt):
            self._debug("prévia concluída: todos os blocos chegaram ao fim")
            self.pause()

    def _advance(self, dt, redraw=True):
        """Avança o estado temporário dos blocos sem gravar o documento."""
        any_active = False
        for motor in self._motors:
            for block in motor["blocks"]:
                if block.get("done"):
                    continue

                # Tempo é a pausa ANTES de cada ciclo, inclusive antes do
                # primeiro. Ao terminar um ciclo, a pausa é rearmada.
                pause = block.get("pause_s", 0.0)
                if pause > 0.0:
                    block["pause_s"] = max(0.0, pause - dt)
                    any_active = True
                    continue

                cycles = block.get("repetitions", 0)
                if block["kind"] == "rotation":
                    # Cada repetição avança o ângulo escolhido e mantém o
                    # resultado acumulado na peça.
                    increment = min(dt * block["rpm"] * 6.0,
                                    block["cycle_degrees"] - block["turn_progress"])
                    block["turn_progress"] += increment
                    direction = block["sign"]
                    if (block.get("rotation_mode") == "ping_pong" and
                            block.get("leg", 0) == 1):
                        direction = -direction
                    block["angle"] += direction * increment
                    if block["turn_progress"] >= block["cycle_degrees"]:
                        block["turn_progress"] = 0.0
                        if (block.get("rotation_mode") == "ping_pong" and
                                block.get("leg", 0) == 0):
                            # A ida foi concluída. A volta é a segunda perna
                            # do mesmo ciclo, portanto ainda não conta a
                            # repetição.
                            block["leg"] = 1
                            block["pause_s"] = block.get("delay_s", 0.0)
                        else:
                            block["leg"] = 0
                            block["cycles_done"] += 1
                            if cycles and block["cycles_done"] >= cycles:
                                block["done"] = True
                            else:
                                block["pause_s"] = block.get("delay_s", 0.0)
                    if not block["done"]:
                        any_active = True
                    continue

                # Soma mantém o deslocamento acumulado; Ida volta ao início
                # entre ciclos; Ida + volta preserva o comportamento legado.
                length = (block["b"] - block["a"]).length() * 1000.0
                linear_mode = block.get("linear_mode", "ping_pong")
                if block.pop("reset_next", False):
                    block["distance_mm"] = 0.0
                    block["phase"] = 0.0
                block["distance_mm"] += dt * block["speed_mm_s"]
                if linear_mode == "accumulate":
                    block["phase"] = block["distance_mm"] / length
                    completed = int(block["distance_mm"] // length)
                    if cycles and completed >= cycles:
                        block["distance_mm"] = cycles * length
                        block["phase"] = float(cycles)
                        block["cycles_done"] = cycles
                        block["done"] = True
                    elif completed > block["cycles_done"]:
                        block["cycles_done"] = completed
                        block["pause_s"] = block.get("delay_s", 0.0)
                else:
                    travel = length if linear_mode == "one_way" else 2.0 * length
                    if block["distance_mm"] >= travel:
                        block["cycles_done"] += 1
                        if linear_mode == "one_way":
                            block["phase"] = 1.0
                        else:
                            block["phase"] = 0.0
                        if cycles and block["cycles_done"] >= cycles:
                            block["done"] = True
                        else:
                            block["pause_s"] = block.get("delay_s", 0.0)
                            block["reset_next"] = linear_mode == "one_way"
                            if linear_mode != "one_way":
                                block["distance_mm"] = 0.0
                    else:
                        block["phase"] = (block["distance_mm"] / length
                                          if block["distance_mm"] <= length else
                                          (travel - block["distance_mm"]) / length)
                if not block["done"]:
                    any_active = True
        if redraw:
            self.viewport.update()
        return any_active

    def _seek(self, target_s):
        """Calcula a prévia exatamente no instante global solicitado.

        Passo, retrocesso e play reverso usam esta mesma função. Ela sempre
        reinicia apenas o estado temporário dos blocos e reproduz a cronologia
        até ``target_s``; não altera o modelo, nem exige Play/Pause.
        """
        if not self._preview:
            return
        states = {id(motor["group"]): motor for motor in self._configured()}
        for motor in self._motors:
            fresh = states.get(id(motor["group"]))
            if fresh is not None:
                motor["blocks"] = fresh["blocks"]
            else:
                # Um componente removido da configuração não pode manter
                # estado residual de uma busca anterior.
                motor["blocks"] = []
        remaining = max(0.0, float(target_s))
        # Subpassos preservam delays, repetições e ida/volta sem modificar a
        # geometria nem o documento. Eles tornam o resultado independente da
        # quantidade de cliques que levou até este instante.
        while remaining > 1e-9:
            chunk = min(remaining, 0.02)
            self._advance(chunk, redraw=False)
            remaining -= chunk
        self._timeline_s = max(0.0, float(target_s))
        self._debug(f"cronologia aplicada: {self._timeline_s:.3f}s")
        self.viewport.update()
        self._show_timeline()

    def _show_timeline(self):
        """Mostra o tempo aplicado para tornar cada passo verificável."""
        self._update_timeline_clock()
        self.status_label.setText(_t("Tempo: {time:.2f} s", time=self._timeline_s))

    def _update_timeline_clock(self):
        """Atualiza o relógio global no formato minutos:segundos,centésimos."""
        total = max(0.0, float(self._timeline_s))
        minutes = int(total // 60.0)
        seconds = total - minutes * 60.0
        self.timeline_label.setText(
            f"⏱ {minutes:02d}:{seconds:05.2f}".replace(".", ","))

    def stop(self):
        self.timer.stop()
        self._playing = False
        self._last_tick = None
        self.status_label.setText(_t("Parado"))
        if self._preview:
            vp = self.viewport
            if self._original_draw is not None:
                vp._draw_groups_preview = self._original_draw
            # Restore the host's own preview before freeing the per-motor GPU buffers.
            vp.end_groups_preview()
            vp.makeCurrent()
            try:
                for motor in self._motors:
                    for vao, vbo, _ in motor.get("scratch", {}).values():
                        vao.destroy()
                        vbo.destroy()
            finally:
                vp.doneCurrent()
            vp.update()
        self._preview = False
        self._original_draw = None
        self._motors = []
        self._scene = self._version = None
        self._timeline_s = 0.0
        self._update_timeline_clock()
        self._play_direction = 1
        self._debug("prévia parada e tempo resetado")

    def _document_changed(self):
        own_change = (self._writing_automation or
                      getattr(self, "_automation_document_pending", False))
        if own_change:
            self._automation_document_seen = True
            if self._preview and self.app.scene is self._scene:
                self._version = self.app.scene.version
            if not self._writing_automation:
                self._automation_document_pending = False
        if (self._preview and not own_change and
                (self.app.scene is not self._scene or
                 self.app.scene.version != self._version)):
            self._debug("prévia interrompida por alteração externa do documento")
            self.stop()
        selected_still_exists = self._selected is not None and any(
            getattr(group, "uid", None) == getattr(self._selected, "uid", None)
            for group in self.app.scene.groups)
        if self._selected is not None and not selected_still_exists:
            self._selected = None
            self._loaded_config = None
            self._axis_a = self._axis_b = None
            self.selection_label.setText(_t("Componente: nenhum"))
            self.config_label.setText(_t("Configuração: nenhuma"))
            self.axis_label.setText(_t("Eixo: não definido"))
            self.remove_button.setEnabled(False)
        elif self._selected is not None and not own_change:
            current = next((block for block in self._blocks_entry(
                self._saved()["motors"].get(self._selected.uid))
                if block.get("id") == self._active_block_id), None)
            if current != self._loaded_config:
                self._selected = None
                self._read_selection()
        if not own_change:
            self._refresh_component_list()
            self._refresh_blocks()
        self._refresh_count()

    def _draw_axis(self, viewport, painter):
        group = self._selected
        # Os marcadores são exclusivos da captura de um novo eixo. Um eixo
        # salvo nunca reaparece apenas porque o componente foi selecionado.
        if (
            self._picking is None
            or group is None
            or self._axis_a is None
            or group not in self.app.scene.groups
            or group not in self.app.scene.selection
        ):
            return
        points = [group.xform.map(self._axis_a)]
        if self._axis_b is not None:
            points.append(group.xform.map(self._axis_b))
        xs, ys, visible = self.app.world_to_pixels([_vec(p) for p in points])
        if not visible[0]:
            return
        painter.setPen(QPen(QColor("#50CF82"), 2))
        painter.setBrush(QColor("#50CF82"))
        painter.drawEllipse(int(xs[0]) - 4, int(ys[0]) - 4, 8, 8)
        if len(points) == 2 and visible[1]:
            painter.drawLine(int(xs[0]), int(ys[0]), int(xs[1]), int(ys[1]))
            painter.drawEllipse(int(xs[1]) - 4, int(ys[1]) - 4, 8, 8)

    def _safe_draw_axis(self, viewport, painter):
        return self._run_guard(
            "desenhar referência", lambda: self._draw_axis(viewport, painter),
            False)

    def _safe_document_changed(self):
        return self._run_guard(
            "atualizar documento", self._document_changed, False)


def setup(app):
    if app.api_version < 2:
        raise RuntimeError(_t("Automação requer IngeTrazo 0.5.7 / API 2."))
    _install_plugin_exception_log(app)
    old_controller = getattr(app.window, "_motor_controller", None)
    if old_controller is not None:
        try:
            old_controller.dispose()
        except Exception:
            pass
    app.window._motor_controller = MotorController(app)
