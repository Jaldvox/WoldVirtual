"""
Sistema de UI para WoldVirtual Crypto 3D
"""

import pygame
import sys
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Importar estilos usando path absoluto
from styles.ui_styles import UI_STYLE, BUTTON_STYLE, COLORS
from core.security_manager import SecurityManager

@dataclass
class UIElement:
    x: int
    y: int
    width: int
    height: int
    color: tuple
    text: str = ""
    font_size: int = 16

class UI:
    """Sistema de interfaz de usuario seguro"""
    
    def __init__(self, scene_3d, security_manager: SecurityManager):
        self.scene_3d = scene_3d
        self.security_manager = security_manager
        self.screen = None
        self.font = None
        self.elements = {}
        self.active_user = None
        
        # Inicializar pygame para UI
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        
        # Elementos de UI
        self._create_ui_elements()
    
    def _create_ui_elements(self):
        """Crear elementos de la interfaz"""
        
        # Panel de login
        self.elements['login_panel'] = {
            'username_input': UIElement(50, 100, 300, 40, COLORS['input_bg']),
            'password_input': UIElement(50, 160, 300, 40, COLORS['input_bg']),
            'login_button': UIElement(50, 220, 150, 40, COLORS['button_primary']),
            'register_button': UIElement(220, 220, 150, 40, COLORS['button_secondary'])
        }
        
        # Panel principal de crypto
        self.elements['main_panel'] = {
            'wallet_balance': UIElement(20, 20, 200, 60, COLORS['panel_bg']),
            'crypto_list': UIElement(20, 100, 300, 400, COLORS['panel_bg']),
            'trading_panel': UIElement(340, 100, 400, 400, COLORS['panel_bg']),
            'settings_button': UIElement(20, 520, 100, 40, COLORS['button_secondary'])
        }
        
        # Panel de configuración 3D
        self.elements['3d_controls'] = {
            'quality_slider': UIElement(760, 20, 200, 30, COLORS['slider_bg']),
            'vr_toggle': UIElement(760, 70, 100, 30, COLORS['toggle_bg']),
            'reset_view': UIElement(760, 120, 100, 40, COLORS['button_primary'])
        }
    
    def render(self, screen: pygame.Surface):
        """Renderizar la interfaz de usuario"""
        self.screen = screen
        
        if not self.active_user:
            self._render_login_screen()
        else:
            self._render_main_interface()
        
        # Renderizar overlay de seguridad si es necesario
        self._render_security_overlay()
    
    def _render_login_screen(self):
        """Renderizar pantalla de login"""
        # Fondo
        self.screen.fill(COLORS['background'])
        
        # Título
        title_text = self.font.render("WoldVirtual Crypto 3D", True, COLORS['text_primary'])
        title_rect = title_text.get_rect(center=(self.screen.get_width()//2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Panel de login
        login_panel = self.elements['login_panel']
        
        # Campo de usuario
        pygame.draw.rect(self.screen, login_panel['username_input'].color, 
                        (login_panel['username_input'].x, login_panel['username_input'].y,
                         login_panel['username_input'].width, login_panel['username_input'].height))
        
        username_text = self.font.render("Username", True, COLORS['text_secondary'])
        self.screen.blit(username_text, (login_panel['username_input'].x + 10, 
                                       login_panel['username_input'].y - 25))
        
        # Campo de contraseña
        pygame.draw.rect(self.screen, login_panel['password_input'].color,
                        (login_panel['password_input'].x, login_panel['password_input'].y,
                         login_panel['password_input'].width, login_panel['password_input'].height))
        
        password_text = self.font.render("Password", True, COLORS['text_secondary'])
        self.screen.blit(password_text, (login_panel['password_input'].x + 10,
                                       login_panel['password_input'].y - 25))
        
        # Botones
        self._render_button(login_panel['login_button'], "Login")
        self._render_button(login_panel['register_button'], "Register")
    
    def _render_main_interface(self):
        """Renderizar interfaz principal"""
        # Fondo semi-transparente para overlay sobre 3D
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(200)
        overlay.fill(COLORS['overlay'])
        self.screen.blit(overlay, (0, 0))
        
        # Panel de balance
        main_panel = self.elements['main_panel']
        self._render_wallet_balance(main_panel['wallet_balance'])
        
        # Lista de criptomonedas
        self._render_crypto_list(main_panel['crypto_list'])
        
        # Panel de trading
        self._render_trading_panel(main_panel['trading_panel'])
        
        # Controles 3D
        controls_3d = self.elements['3d_controls']
        self._render_3d_controls(controls_3d)
    
    def _render_wallet_balance(self, element: UIElement):
        """Renderizar balance del wallet"""
        pygame.draw.rect(self.screen, element.color, 
                        (element.x, element.y, element.width, element.height))
        
        balance_text = self.font.render("Total Balance", True, COLORS['text_primary'])
        self.screen.blit(balance_text, (element.x + 10, element.y + 10))
        
        # Obtener balance del usuario (simulado)
        total_usd = "$12,345.67"
        amount_text = self.font.render(total_usd, True, COLORS['success'])
        self.screen.blit(amount_text, (element.x + 10, element.y + 35))
    
    def _render_crypto_list(self, element: UIElement):
        """Renderizar lista de criptomonedas"""
        pygame.draw.rect(self.screen, element.color,
                        (element.x, element.y, element.width, element.height))
        
        # Título
        title = self.font.render("Your Crypto Assets", True, COLORS['text_primary'])
        self.screen.blit(title, (element.x + 10, element.y + 10))
        
        # Lista de cryptos (simulada)
        cryptos = [
            ("Bitcoin", "1.25 BTC", "$65,000"),
            ("Ethereum", "15.3 ETH", "$24,500"),
            ("Litecoin", "45.7 LTC", "$3,200")
        ]
        
        y_offset = 50
        for crypto, amount, value in cryptos:
            crypto_text = self.font.render(f"{crypto}: {amount}", True, COLORS['text_secondary'])
            value_text = self.font.render(value, True, COLORS['success'])
            
            self.screen.blit(crypto_text, (element.x + 10, element.y + y_offset))
            self.screen.blit(value_text, (element.x + 200, element.y + y_offset))
            
            y_offset += 30
    
    def _render_trading_panel(self, element: UIElement):
        """Renderizar panel de trading"""
        pygame.draw.rect(self.screen, element.color,
                        (element.x, element.y, element.width, element.height))
        
        title = self.font.render("Trading Panel", True, COLORS['text_primary'])
        self.screen.blit(title, (element.x + 10, element.y + 10))
        
        # Botones de trading
        buy_button = UIElement(element.x + 20, element.y + 50, 80, 35, COLORS['success'])
        sell_button = UIElement(element.x + 120, element.y + 50, 80, 35, COLORS['danger'])
        
        self._render_button(buy_button, "BUY")
        self._render_button(sell_button, "SELL")
    
    def _render_3d_controls(self, controls: Dict[str, UIElement]):
        """Renderizar controles 3D"""
        # Panel de fondo
        panel_bg = UIElement(750, 10, 220, 200, COLORS['panel_bg'])
        pygame.draw.rect(self.screen, panel_bg.color,
                        (panel_bg.x, panel_bg.y, panel_bg.width, panel_bg.height))
        
        title = self.font.render("3D Controls", True, COLORS['text_primary'])
        self.screen.blit(title, (760, 20))
        
        # Botón reset
        self._render_button(controls['reset_view'], "Reset View")
    
    def _render_button(self, element: UIElement, text: str):
        """Renderizar botón"""
        pygame.draw.rect(self.screen, element.color,
                        (element.x, element.y, element.width, element.height))
        
        # Borde
        pygame.draw.rect(self.screen, COLORS['border'],
                        (element.x, element.y, element.width, element.height), 2)
        
        # Texto centrado
        button_text = self.font.render(text, True, COLORS['text_primary'])
        text_rect = button_text.get_rect(center=(element.x + element.width//2, 
                                               element.y + element.height//2))
        self.screen.blit(button_text, text_rect)
    
    def _render_security_overlay(self):
        """Renderizar overlay de seguridad si es necesario"""
        # Verificar si hay alertas de seguridad
        if hasattr(self.security_manager, 'has_security_alerts'):
            if self.security_manager.has_security_alerts():
                alert_text = self.font.render("⚠️ Security Alert", True, COLORS['danger'])
                self.screen.blit(alert_text, (self.screen.get_width() - 200, 10))
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Manejar eventos de UI"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            return self._handle_key_press(event)
        
        return False
    
    def _handle_mouse_click(self, pos: tuple) -> bool:
        """Manejar clicks del mouse"""
        x, y = pos
        
        if not self.active_user:
            # Manejar clicks en pantalla de login
            login_panel = self.elements['login_panel']
            
            # Verificar click en botón de login
            login_btn = login_panel['login_button']
            if (login_btn.x <= x <= login_btn.x + login_btn.width and
                login_btn.y <= y <= login_btn.y + login_btn.height):
                self._handle_login()
                return True
        
        else:
            # Manejar clicks en interfaz principal
            controls_3d = self.elements['3d_controls']
            reset_btn = controls_3d['reset_view']
            
            if (reset_btn.x <= x <= reset_btn.x + reset_btn.width and
                reset_btn.y <= y <= reset_btn.y + reset_btn.height):
                self.scene_3d.reset_camera()
                return True
        
        return False
    
    def _handle_key_press(self, event: pygame.event.Event) -> bool:
        """Manejar teclas presionadas"""
        if event.key == pygame.K_ESCAPE:
            if self.active_user:
                self._handle_logout()
            return True
        
        return False
    
    def _handle_login(self):
        """Manejar proceso de login"""
        # Aquí iría la validación real con security_manager
        # Por ahora, login simulado
        self.active_user = {"username": "demo_user", "user_id": 1}
        print("Login successful")
    
    def _handle_logout(self):
        """Manejar logout"""
        self.active_user = None
        print("Logout successful")